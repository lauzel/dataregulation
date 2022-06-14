from flask import Flask
from flask import render_template, jsonify, redirect

from forms.search_form import SearchForm
from repository.data_regulation_repository import DataRegulationRepository

def init_app():
    app = Flask(__name__)
    app.config.update(dict(
        SECRET_KEY="powerful secretkey",
        WTF_CSRF_SECRET_KEY="a csrf secret key",
        OWL_FILE_PATH="C:/Users/Alexandre/Downloads/DataRegulationOntology.owl"
    ))

    return app

app = init_app()
dataRegulation = DataRegulationRepository(app)

@app.route('/')
def index():
   return render_template('index.html')

@app.route('/search', methods=['GET', 'POST'])
def search_page():
       
    classes = dataRegulation.get_all_classes()

    form = SearchForm()
    form.query1.choices = [(c, str(c).split('.')[-1]) for c in classes]
    form.query2.choices = [(c, str(c).split('.')[-1]) for c in classes]
    form.query3.choices = [(c, str(c).split('.')[-1]) for c in classes]

    if form.is_submitted():
        choices = dataRegulation.get_subclass_of("Documentation")
        #print(choices)
    
    return render_template('search.html', form=form)

@app.route('/consult', methods=['GET', 'POST'])
def consult_page():
       
    classes = dataRegulation.get_all_classes()

    form = SearchForm()
    form.query1.choices = [(c, str(c).split('.')[-1]) for c in classes]
    form.query2.choices = [(c, str(c).split('.')[-1]) for c in classes]
    form.query3.choices = [(c, str(c).split('.')[-1]) for c in classes]

    if form.is_submitted():
        choices = dataRegulation.get_subclass_of("Documentation")
        #print(choices)
    
    return render_template('consult.html', form=form)

@app.route('/_get_options/',  methods=['GET', 'POST'])
def _get_options():
    #classes = dataRegulation.get_all_properties()
    #classes = [(str(c), str(c).split('.')[-1]) for c in classes]
    #return jsonify(classes)

    form = SearchForm()

    if form.is_submitted():
        print(form)

    return render_template('search.html', form=form)
