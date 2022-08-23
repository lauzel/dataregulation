from flask_wtf import FlaskForm
from wtforms import SelectField, TextAreaField
from wtforms.validators import DataRequired

PERSON = "Person"
TECHNOLOGICAL_DATA = "Technological_Data"
IT_SYSTEM = "IT_System"
FUNCTIONAL_PROCESS = "Functional_Process"
ACT= "Act"

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

        query1Sf = self.repo.remove_prefix(query1)
        query2Sf = self.repo.remove_prefix(query2)

        if query1 is not None:
            form.query2.choices = [""] + self.repo.get_class_data_regulated()
            form.query2.render_kw={}

        if query2 is not None:
            form.query3.choices =  self.repo.get_instances_of_class(query2)
            form.query3.render_kw={}

        if query3 is not None:
            path = """"""
            if (query1Sf == PERSON and query2Sf == TECHNOLOGICAL_DATA):
                path = """
                    ?subject dro:isPersonInvolvedIn ?funcprocess.
                    ?itsystem dro:isITSystemInvolvedIn ?funcprocess.
                    ?itsystem dro:performs ?activite.
                    ?activite dro:process ?lastcrit.
                """
    

            if (query1Sf == IT_SYSTEM and query2Sf == TECHNOLOGICAL_DATA):
                path = """
                    ?subject dro:performs ?activite.
                    ?activite dro:process ?lastcrit.
                """

            if (query1Sf == FUNCTIONAL_PROCESS and query2Sf == TECHNOLOGICAL_DATA):
                path = """
                    ?subject dro:involvesITSystem ?itsystem.
                    ?itsystem dro:performs ?activite.
                    ?activite dro:process ?lastcrit.
                """

            if (query1Sf == PERSON and query2Sf == ACT):
                path1 = """
                    ?subject dro:isPersonInvolvedIn ?funcprocess.
                    ?itsystem dro:isITSystemInvolvedIn ?funcprocess.
                    ?itsystem dro:performs ?activite.
                    ?activite dro:process ?dataOne.
                    ?dataOne dro:isBusinessDataGovernedBy ?lastcrit.
                """

                path2 = """
                    ?subject dro:isPersonInvolvedIn ?funcprocess.
                    ?itsystem dro:isITSystemInvolvedIn ?funcprocess.
                    ?itsystem dro:performs ?activite.
                    ?activite dro:process ?dataOne.
                    ?dataOne dro:isPersonalDataGovernedBy ?lastcrit.
                """

                data1 = self.repo.search_request(path1, query3)
                data2 = self.repo.search_request(path2, query3)

                form.result.data = data1 + data2

                return

            if (query1Sf == IT_SYSTEM and query2Sf == ACT):
                path1 = """
                    ?subject dro:performs ?activite.
                    ?activite dro:process ?dataOne
                    ?dataOne dro:isBusinessDataGovernedBy ?lastcrit.
                """

                path2 = """
                    ?subject dro:performs ?activite.
                    ?activite dro:process ?dataOne
                    ?dataOne dro:isPersonalDataGovernedBy ?lastcrit.
                """

                data1 = self.repo.search_request(path1, query3)
                data2 = self.repo.search_request(path2, query3)

                form.result.data = data1 + data2

                return

            if (query1Sf == FUNCTIONAL_PROCESS and query2Sf == ACT):
                path1 = """
                    ?subject dro:involvesITSystem ?itsystem.
                    ?itsystem dro:performs ?activite.
         	        ?activite dro:process ?dataOne.
                    ?dataOne dro:isPersonalDataGovernedBy ?lastcrit.

                """

                path2 = """
                    ?subject dro:involvesITSystem ?itsystem.
                    ?itsystem dro:performs ?activite.
                    ?activite dro:process ?dataOne.
                    ?dataOne dro:isBusinessDataGovernedBy ?lastcrit.
                """

                data1 = self.repo.search_request(path1, query3)
                data2 = self.repo.search_request(path2, query3)

                form.result.data = data1 + data2

                return


            form.result.data = self.repo.search_request(path, query3)           

    
    def default_data(self):
        classes = [""] + self.repo.get_class_regulated()
        class_data_regulated = [""] +  self.repo.get_class_data_regulated()
        properties = []
        form = self

        print(classes)

        form.query1.choices = classes
        form.query2.choices = class_data_regulated
        form.query3.choices = properties
