from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from wtforms import StringField, TextAreaField, SubmitField, SelectField, FieldList
from wtforms.validators import DataRequired, Length
from Myna.models import User
from Myna import photos
from flask_wtf.file import FileField, FileRequired, FileAllowed

class CreateAvatar(FlaskForm):
    username = StringField('UserID', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    STAKEHOLDER_CHOICES=[('Engineer', 'Engineer'), ('Architect', 'Architect'), ('Planner', 'Planner'), ('Contrator', 'Contrator')]
    stakeholder=SelectField(label='Stakeholder',choices=STAKEHOLDER_CHOICES)
    avatar_img=FileField('Profile Picture',validators=[FileAllowed(photos, 'Image only!'), FileRequired('File was empty!')])
    submit = SubmitField('Create Avatar')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class UpdateAvatar(FlaskForm):
    email=StringField('Email', validators=[DataRequired(), Email()])
    password=PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    STAKEHOLDER_CHOICES=[('Engineer', 'Engineer'), ('Architect', 'Architect'), ('Planner', 'Planner'), ('Contrator', 'Contrator')]
    stakeholder=SelectField(label='Stakeholder',choices=STAKEHOLDER_CHOICES)
    avatar_img=FileField('Profile Picture',validators=[FileAllowed(photos, 'Image only!'), FileRequired('File was empty!')])
    submit = SubmitField('Update Avatar')

    def __init__(self, original_email, *args, **kwargs):
        super(UpdateAvatar, self).__init__(*args, **kwargs)
        self.original_email = original_email

    def validate_username(self, email):
        if email.data != self.original_email:
            user = User.query.filter_by(email=self.email.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')


class LoginToAvatar(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Avatar Login')