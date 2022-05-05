from owlready2 import *

class DataRegulationRepository:
    def __init__(self, app) -> None:
        file_path = app.config.get("OWL_FILE_PATH")
        self.onto = get_ontology(f'file://{file_path}').load()

    def get_all_classes(self):
        classes = self.onto.classes()

        return list(classes)


    def get_subclass_of(self, subclass):
         data = self.onto.search(iri=f"*{subclass}*")
         classes = self.onto.search(subclass_of=data)

         return list(classes)