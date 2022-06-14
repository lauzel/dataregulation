from flask_wtf import FlaskForm
from wtforms import SelectField
from wtforms.validators import DataRequired

class SearchForm(FlaskForm):
    query1 = SelectField('query1', validators=[])
    query2 = SelectField('query2', validators=[])
    query3 = SelectField('query3', validators=[])