from flask import Flask, g, render_template, redirect, url_for, request, flash
import sqlite3
from datetime import datetime
from models import get_db, close_connection, init_db, add_sample_data
from forms import ProfileForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key-change-me'

# Register teardown context
app.teardown_appcontext(close_connection)

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

@app.route('/')
def index():
    """Show a simple list of users with links to view or edit each profile."""
    db = get_db()
    users = db.execute('SELECT id, username, full_name, email FROM users ORDER BY id DESC').fetchall()
    return render_template('index.html', users=users)

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Display registration form and store user on valid POST."""
    form = ProfileForm()
    if form.validate_on_submit():
        db = get_db()
        try:
            # Handle age properly
            age_value = None
            if form.age.data is not None and form.age.data != '':
                try:
                    age_value = int(form.age.data)
                except (ValueError, TypeError):
                    age_value = None
            
            bio_value = (form.bio.data or '').strip()
            
            db.execute(
                'INSERT INTO users (username, full_name, email, age, bio) VALUES (?, ?, ?, ?, ?)',
                ( (form.username.data or '').strip(),
                  (form.full_name.data or '').strip(),
                  (form.email.data or '').strip(),
                  age_value,
                  bio_value
                )
            )
            db.commit()
            flash('User registered successfully.', 'success')
            return redirect(url_for('index'))
        except sqlite3.IntegrityError:
            db.rollback()
            flash('Error saving user: username or email might already exist.', 'error')
    return render_template('register.html', form=form)

@app.route('/profile/<int:user_id>')
def profile(user_id):
    """Show stored user data dynamically from the DB."""
    db = get_db()
    user = db.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    if not user:
        flash('User not found', 'error')
        return redirect(url_for('index'))
    return render_template('profile.html', user=user)

@app.route('/update/<int:user_id>', methods=['GET', 'POST'])
def update(user_id):
    """Preload user data into the update form and save changes on POST."""
    db = get_db()
    user = db.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    if not user:
        flash('User not found', 'error')
        return redirect(url_for('index'))

    form = ProfileForm()
    if request.method == 'GET':
        form.username.data = user['username']
        form.full_name.data = user['full_name']
        form.email.data = user['email']
        form.age.data = user['age']
        form.bio.data = user['bio']
    elif form.validate_on_submit():
        try:
            # Handle age properly
            age_value = None
            if form.age.data is not None and form.age.data != '':
                try:
                    age_value = int(form.age.data)
                except (ValueError, TypeError):
                    age_value = None
                    
            bio_value = (form.bio.data or '').strip()
            
            db.execute(
                'UPDATE users SET username = ?, full_name = ?, email = ?, age = ?, bio = ? WHERE id = ?',
                ( (form.username.data or '').strip(),
                  (form.full_name.data or '').strip(),
                  (form.email.data or '').strip(),
                  age_value,
                  bio_value,
                  user_id
                )
            )
            db.commit()
            flash('User updated successfully.', 'success')
            return redirect(url_for('profile', user_id=user_id))
        except sqlite3.IntegrityError:
            db.rollback()
            flash('Error updating user: username or email might conflict with an existing user.', 'error')

    return render_template('update.html', form=form, user=user)

if __name__ == '__main__':
    init_db()
    add_sample_data()
    app.run(debug=True)