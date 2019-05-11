from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length
from .. import Database


class find_form(FlaskForm):
    orig = StringField(u'Origin',
                       validators=[DataRequired(), Length(3)])
    dest = StringField(u'Destination',
                       validators=[DataRequired(), Length(3)])

    options = []
    for option in Database.Criterion:
        name = option.name
        options.append((name, name.capitalize() ))

    cri = SelectField(u'By',
                      validators=[DataRequired()], choices=options)
    submit = SubmitField('Search')


