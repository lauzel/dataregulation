from flask_wtf import FlaskForm
from wtforms import SelectField, TextAreaField
from wtforms.validators import DataRequired

class SearchForm(FlaskForm):
    def __init__(self, *args, **kwargs):
        self.repo = kwargs.get("repo")
        super(SearchForm, self).__init__(*args, **kwargs)

    query1 = SelectField('Select a class', validators=[], validate_choice=False)
    query2 = SelectField('Select a class', validators=[], validate_choice=False, render_kw={'disabled':''})
    query3 = SelectField('Select an instance', validators=[], validate_choice=False, render_kw={'disabled':''})
    result = TextAreaField('result', validators=[], render_kw={'disabled':''})

    def update_data(self):
        form = self

        query1 = form.data["query1"]
        query2 = form.data["query2"]
        query3 = form.data["query3"]

        if query1 is not None:
            form.query2.choices = [""] + self.repo.get_class_data_regulated()
            form.query2.render_kw={}

        if query2 is not None:
            form.query3.choices =  self.repo.get_instances_of_class(query2)
            form.query3.render_kw={}

        if query3 is not None:
            form.result.data = self.repo.get_person_by_data_type(query3)

    
    def default_data(self):
        classes = self.repo.get_class_regulated()
        class_data_regulated = self.repo.get_class_data_regulated()
        properties = []
        form = self

        print(classes)

        form.query1.choices = classes
        form.query2.choices = class_data_regulated
        form.query3.choices = properties
