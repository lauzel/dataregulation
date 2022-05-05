from flask import Flask
from flask import render_template, jsonify, redirect

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
def index():
   return redirect('/search')

@app.route('/search', methods=['GET', 'POST'])
def search_page():
       
    classes = dataRegulation.get_subclass_of("Technological_Data")
    form = SearchForm()
    form.query1.choices = [(c, str(c).split('.')[-1]) for c in classes]
    form.query2.choices = [(c, str(c).split('.')[-1]) for c in classes]
    form.query3.choices = [(c, str(c).split('.')[-1]) for c in classes]

    if form.validate_on_submit():
        print(form.data)
    
    return render_template('search.html', form=form)

@app.route('/_get_options/')
def _get_options():
    classes = dataRegulation.get_all_classes()
    classes = [(str(c), str(c).split('.')[-1]) for c in classes]
    return jsonify(classes)    