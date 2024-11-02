from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Length, ValidationError

class RegistrationForm(FlaskForm):
    email = StringField(validators=[DataRequired()])
    firstname = StringField(validators=[DataRequired()])
    lastname = StringField(validators=[DataRequired()])
    phone = StringField(validators=[DataRequired()])
    password = PasswordField(validators=[
        DataRequired(),
        Length(min=8, max=15, message="Password must be between 8 and 15 characters")
    ])
    confirm_password = PasswordField(validators=[
        DataRequired(),
        EqualTo('password', message='Both password fields must be equal!')
    ])
    submit = SubmitField()

    # Custom validator for password strength without using 're'
    def validate_password(self, field):
        password = field.data

        # Check for at least 1 uppercase letter
        if not any(char.isupper() for char in password):
            raise ValidationError('Password must contain at least 1 uppercase letter.')

        # Check for at least 1 lowercase letter
        if not any(char.islower() for char in password):
            raise ValidationError('Password must contain at least 1 lowercase letter.')

        # Check for at least 1 digit
        if not any(char.isdigit() for char in password):
            raise ValidationError('Password must contain at least 1 digit.')

        # Check for at least 1 special character (non-alphanumeric)
        if not any(not char.isalnum() for char in password):
            raise ValidationError('Password must contain at least 1 special character.')

class LoginForm(FlaskForm):
    email = StringField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired()])
    recaptcha = RecaptchaField()
    submit = SubmitField()
