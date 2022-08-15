from flask import Flask
from flask import render_template, jsonify, redirect, request

from forms.search_form import SearchForm
from repository.data_regulation_repository import DataRegulationRepository

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

@app.route('/')
def index():
   return render_template('index.html')

@app.route('/search', methods=['GET', 'POST'])
def search_page():
       
    classes = dataRegulation.get_all_classes()

    technological_data = "DataRegulationOntology.Business_Data"

    #instances_criteria = dataRegulation.get_instance_of_regulated_technological_data()
    #instances_criteria = dataRegulation.get_instance_of_regulation()
    #instances_criteria = dataRegulation.get_instance_by_regulated_data("GDPRData")
    #instances_criteria = dataRegulation.get_object_properties_from_class("GDPRArt32")
    instances_criteria = dataRegulation.get_instances_of_class("TOto.Act")

    return render_template('search.html', instances_criteria=instances_criteria)

@app.route('/consult', methods=['GET', 'POST'])
def consult_page():
    # Select 1 : Class
    # Select 2 : Instance
    # Select 3 : Properties
    classes = dataRegulation.get_all_classes()
    instances = dataRegulation.get_instances_of_class(classes[0])
    properties = dataRegulation.get_instance_properties(instances[0])
    relations = []

    if request.method == 'POST':
        classSelected = request.form["select1"]
        instances = dataRegulation.get_instances_of_class(classSelected)
        instanceSelected = request.form["select2"]
        properties = dataRegulation.get_instance_properties(instanceSelected)
        propertiesSelected = request.form["select3"]
        relations = dataRegulation.get_properties_relation(propertiesSelected)

    
    return render_template('consult.html', 
        classes=classes,
        instances=instances,
        properties=properties,
        relations=relations
    )

@app.route('/_get_options/',  methods=['GET', 'POST'])
def _get_options():
    #classes = dataRegulation.get_all_properties()
    #classes = [(str(c), str(c).split('.')[-1]) for c in classes]
    #return jsonify(classes)

    form = SearchForm()

    if form.is_submitted():
        print(form)

    return render_template('search.html', form=form)
