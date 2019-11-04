__author__ = 'michaelpeck'


from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SelectField, FloatField, DecimalField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from src.users.user import User
from src.common.database import Database


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = Database.find_one(collection='users', query={'username': username.data})
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = Database.find_one(collection='users', query={'email': email.data})
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.objects(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.objects(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')


class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.objects(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')


class StaticRangeForm(FlaskForm):
    ticker = StringField('Ticker', validators=[DataRequired(), Length(min=1, max=6)])
    period = SelectField('Period', choices=[('1d', '1 day'), ('5d', '5 days'),
                                                ('1mo', '1 month'), ('3mo', '3 months'),
                                                ('6mo', '6 months'), ('1y', '1 year')])
    interval = SelectField('Interval', choices=[('1m', '1 minute'), ('2m', '2 minutes'),
                                                ('5m', '5 minutes'), ('15m', '15 minutes'),
                                                ('30m', '30 minutes'), ('60m', '60 minutes'),
                                                ('90m', '90 minutes'), ('1d', '1 day')])
    money = DecimalField('Account balance', places=2, validators=[DataRequired()])
    buy = DecimalField('Buy point', places=4, validators=[DataRequired()])
    sell = DecimalField('Sell point', places=4, validators=[DataRequired()])
    trade_cost = DecimalField('Cost per trade', places=2, validators=[DataRequired()])
    submit = SubmitField('Submit')

    def validate_interval(self, period, interval):
        if period == ('1mo' or '3mo' or '6mo' or '1y') and interval == '1m':
            raise ValidationError('1 minute data is only available up to 5 days.')
        elif period == ('3mo' or '6mo' or '1y') and interval == ('1m' or '2m' or '5m' or '15m' or '30m' or '60m' or '90m'):
            raise ValidationError('Intraday data is only available up to 1 month.')