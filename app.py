from flask import Flask
from flask import render_template, jsonify, redirect, request

from forms.consult_form import ConsultForm
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
    instances_criteria = dataRegulation.get_instances_of_class("DataRegulationOntology.Act")

    return render_template('search.html', instances_criteria=instances_criteria)

@app.route('/consult',  methods=['GET', 'POST'])
def consult_page():
    form = ConsultForm()
    form.default_data(dataRegulation)

    if form.is_submitted():
        form.update_data(dataRegulation)

    return render_template('consult.html', form=form)
