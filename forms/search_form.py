from flask_wtf import FlaskForm
from wtforms import SelectField
from wtforms.validators import DataRequired

class SearchForm(FlaskForm):
    query1 = SelectField('query1', validators=[DataRequired()])
    query2 = SelectField('query2', validators=[DataRequired()])
    query3 = SelectField('query3', validators=[DataRequired()])