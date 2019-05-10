from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class find_form(FlaskForm):
    orig = StringField('Origin',
                       validators=[DataRequired(), Length(3)])
    dest = StringField('Destination',
                       validators=[DataRequired(), Length(3)])
    cri = StringField('By',
                      validators=[DataRequired()])
    submit = SubmitField('Search')


