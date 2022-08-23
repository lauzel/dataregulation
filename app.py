from flask import Flask
from flask import render_template, jsonify, redirect, request

from forms.consult_form import ConsultForm
from forms.search_form import SearchForm
from repository.data_regulation_repository import DataRegulationRepository

from owlready2 import *
from owlready2.sparql.endpoint import *

def init_app():
    app = Flask(__name__)
    app.config.update(dict(
        SECRET_KEY="powerful secretkey",
        WTF_CSRF_SECRET_KEY="a csrf secret key",
        OWL_FILE_PATH="./onto/DataRegulationOntology.owl"
    ))

    return app

app = init_app()
dataRegulation = DataRegulationRepository(app)
endpoint = EndPoint(default_world)
app.route('/sparql', methods=['GET'])(endpoint)

@app.route('/')
def index():
   return render_template('index.html')

@app.route('/search', methods=['GET', 'POST'])
def search_page():
    form = SearchForm(repo=dataRegulation)
    form.default_data()

    if form.is_submitted():
        form.update_data()

    return render_template('search.html', form=form)

@app.route('/questions', methods=['GET', 'POST'])
def questions_page():
    return render_template('questions.html')    

@app.route('/add', methods=['GET', 'POST'])
def add_page():
    return render_template('add.html')    


@app.route('/consult',  methods=['GET', 'POST'])
def consult_page():
    form = ConsultForm(repo=dataRegulation)
    form.default_data()

    if form.is_submitted():
        form.update_data()

    return render_template('consult.html', form=form)
