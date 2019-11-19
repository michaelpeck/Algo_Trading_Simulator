__author__ = 'michaelpeck'


from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SelectField, FloatField, DecimalField, IntegerField, PasswordField, SubmitField, FormField

from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange
from flask_login import current_user
from src.users.user import User
from src.common.database import Database


class StaticRangeForm(FlaskForm):
    ticker = StringField('Ticker', validators=[DataRequired(), Length(min=1, max=6)])
    period = SelectField('Period', choices=[('1d', '1 day'), ('5d', '5 days'),
                                                ('1mo', '1 month'), ('3mo', '3 months'),
                                                ('6mo', '6 months'), ('1y', '1 year')], validators=[DataRequired()])
    interval = SelectField('Interval', choices=[('1m', '1 minute'), ('2m', '2 minutes'),
                                                ('5m', '5 minutes'), ('15m', '15 minutes'),
                                                ('30m', '30 minutes'), ('60m', '60 minutes'),
                                                ('90m', '90 minutes'), ('1d', '1 day')], validators=[DataRequired()])
    money = DecimalField('Account balance', places=2,
                         validators=[DataRequired(), NumberRange(min=0, message="Account balance must be positive")])
    buy = DecimalField('Buy point', places=4, validators=[DataRequired(), NumberRange(min=0, message="Buy point must be positive")])
    sell = DecimalField('Sell point', places=4, validators=[DataRequired(), NumberRange(min=0, message="Sell point must be positive")])
    trade_cost = DecimalField('Cost per trade', places=2,
                              validators=[DataRequired(), NumberRange(min=0, max=15, message="Cost per trade cannot exceed $15")])
    submit = SubmitField('Submit')

    def validate(self):
        if not FlaskForm.validate(self):
            return False
        if (self.period.data in ('1mo', '3mo', '6mo', '1y')) and (self.interval.data == '1m'):
            self.interval.errors.append('1 minute data is only available up to 5 days.')
            return False
        elif self.period.data in ('3mo', '6mo', '1y') and self.interval.data in (
                '1m', '2m', '5m', '15m', '30m', '60m', '90m'):
            self.interval.errors.append('Intraday data is only available up to 1 month.')
            return False
        return True

class MovingAverageForm(FlaskForm):
    ticker = StringField('Ticker', validators=[DataRequired(), Length(min=1, max=6)])
    period = SelectField('Period', choices=[('1mo', '1 month'), ('3mo', '3 months'),
                                                ('6mo', '6 months'), ('1y', '1 year')], validators=[DataRequired()])
    length = IntegerField('Length of average', validators=[DataRequired(),
                                                           NumberRange(min=0, message="Length of average must be positive")])
    money = DecimalField('Account balance', places=2, validators=[DataRequired(), NumberRange(min=0, message="Account balance must be positive")])
    buy = DecimalField('Buy point', places=2, validators=[DataRequired(), NumberRange(min=0, message="Buy point must be positive")])
    sell = DecimalField('Sell point', places=2, validators=[DataRequired(), NumberRange(min=0, message="Sell point must be positive")])
    trade_cost = DecimalField('Cost per trade', places=2,
                              validators=[DataRequired(), NumberRange(min=0, max=15, message="Cost per trade cannot exceed $15")])
    submit = SubmitField('Submit')


class WeightedMovingAverageForm(FlaskForm):
    ticker = StringField('Ticker', validators=[DataRequired(), Length(min=1, max=6)])
    period = SelectField('Period', choices=[('1mo', '1 month'), ('3mo', '3 months'),
                                                ('6mo', '6 months'), ('1y', '1 year')], validators=[DataRequired()])
    length = IntegerField('Length of average', validators=[DataRequired(), NumberRange(min=0, message="Length of average must be positive")])
    money = DecimalField('Account balance', places=2, validators=[DataRequired(), NumberRange(min=0, message="Account balance must be positive")])
    buy = DecimalField('Buy point', places=2, validators=[DataRequired(), NumberRange(min=0, message="Buy point must be positive")])
    sell = DecimalField('Sell point', places=2, validators=[DataRequired(), NumberRange(min=0, message="Sell point must be positive")])
    trade_cost = DecimalField('Cost per trade', places=2,
                              validators=[DataRequired(), NumberRange(min=0, max=15, message="Cost per trade cannot exceed $15")])
    submit = SubmitField('Submit')

class TryAgain(FlaskForm):
    submit = SubmitField('Try Again')

class SaveEntry(FlaskForm):
    saveentry = SubmitField('Save Entry')

class SaveModel(FlaskForm):
    name = StringField('Name', validators=[Length(max=20)])
    savemodel = SubmitField('Save Model')

class PickModel(FlaskForm):
    model = SelectField('Model')
    pop_model = SubmitField('Populate')

class StockDataForm(FlaskForm):
    check_ticker = StringField('Ticker', validators=[DataRequired(), Length(min=1, max=6)])
    check = SubmitField('Check')

