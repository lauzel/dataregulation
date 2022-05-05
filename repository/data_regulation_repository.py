from owlready2 import *

class DataRegulationRepository:
    def __init__(self, app) -> None:
        file_path = app.config.get("OWL_FILE_PATH")
        self.onto = get_ontology(f'file://{file_path}').load()

    def get_all_classes(self):
        result = self.onto.search(iri="*")

        return list(result)