from flask import Flask
from flask import render_template, jsonify, request

from forms.search_form import SearchForm
from repository.data_regulation_repository import DataRegulationRepository
app = Flask(__name__)
app.config.update(dict(
    SECRET_KEY="powerful secretkey",
    WTF_CSRF_SECRET_KEY="a csrf secret key",
    OWL_FILE_PATH="C:/Users/Alexandre/Downloads/DataRegulationOntology.owl"
))

dataRegulation = DataRegulationRepository(app)

@app.route('/')
def search_page():
       
    classes = dataRegulation.get_all_classes()
    form = SearchForm()
    form.query1.choices = [(c, c) for c in classes]

    return render_template('search.html', form=form)

@app.route('/_get_options/')
def _get_options():
    classes = dataRegulation.get_all_classes()
    classes = [(str(c), str(c)) for c in classes]
    return jsonify(classes)    