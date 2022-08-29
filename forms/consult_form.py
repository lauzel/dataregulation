from flask_wtf import FlaskForm
from wtforms import SelectField, TextAreaField
from wtforms.validators import DataRequired

class ConsultForm(FlaskForm):
    def __init__(self, *args, **kwargs):
        self.repo = kwargs.get("repo")
        super(ConsultForm, self).__init__(*args, **kwargs)

    query1 = SelectField('query1', validators=[], validate_choice=False)
    query2 = SelectField('query2', validators=[], validate_choice=False, render_kw={'disabled':''})
    query3 = SelectField('query3', validators=[], validate_choice=False, render_kw={'disabled':''})
    result = TextAreaField('result', validators=[], render_kw={'disabled':''})

    def update_data(self):
        form = self

        query1 = form.data["query1"]
        query2 = form.data["query2"]
        query3 = form.data["query3"]

        if query1 is not None:
            form.query2.choices = self.repo.get_instances_of_class(query1)
            form.query2.render_kw={}

        if query2 is not None:
            form.query3.choices = self.repo.get_instance_properties(query2)
            form.query3.render_kw={}

        if query3 is not None:
            form.result.data = self.repo.get_relations_properties(query3, query2)

    
    def default_data(self):
        classes = self.repo.get_all_classes()
        instances = self.repo.get_instances_of_class(classes[0])
        properties = self.repo.get_instance_properties(instances[0])
        form = self

        form.query1.choices = classes
        form.query2.choices = instances
        form.query3.choices = properties
