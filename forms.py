from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Length, NumberRange, Regexp

class ProfileForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(message="Username is required"), 
        Length(min=3, max=30, message="Username must be between 3 and 30 characters"),
        Regexp('^[a-zA-Z0-9_]+$', message="Username can only contain letters, numbers, and underscores")
    ])
    full_name = StringField('Full name', validators=[
        DataRequired(message="Full name is required"), 
        Length(min=2, max=100, message="Full name must be between 2 and 100 characters")
    ])
    email = StringField('Email', validators=[
        DataRequired(message="Email is required"), 
        Email(message="Please enter a valid email address"), 
        Length(max=120, message="Email cannot exceed 120 characters")
    ])
    age = IntegerField('Age', validators=[
        NumberRange(min=0, max=120, message="Age must be between 0 and 120")
    ])
    bio = TextAreaField('Bio', validators=[
        Length(max=500, message="Bio cannot exceed 500 characters")
    ])
    submit = SubmitField('Save')