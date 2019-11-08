__author__ = 'michaelpeck'


from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError


class NewPostForm(FlaskForm):
    title = StringField('Title',
                           validators=[DataRequired(), Length(min=2, max=30)])
    content = StringField('Content',
                        validators=[DataRequired(), Length(min=1, max=1000)])
    submit = SubmitField('Post')
