from owlready2 import *

class DataRegulationRepository:
    def __init__(self, app) -> None:
        file_path = app.config.get("OWL_FILE_PATH")
        self.onto = get_ontology(f'file://{file_path}').load()

    def remove_prefix(self, name):
        return ".".join(str(name).split(".")[1:])

    def query(self, query, *params): 
        q = query % (params)
        return list(default_world.sparql(q))

    def get_all_classes(self):
        classes = self.onto.classes()

        return list(classes)

    def get_all_properties(self):
        properties = self.onto.object_properties()

        return list(properties)

    def get_subclass_of(self, subclass):
         data = self.onto.search(iri=f"*{subclass}*")
         print(list(data[0].get_properties()))
         classes = self.onto.search(subclass_of=data)

         return list(classes)

    def get_class_by_name(self, name):
        return     

    def get_instance_from_it(self):
        data = self.query("""
            PREFIX dro: <urn:absolute:DataRegulationOntology#>
            SELECT ?subject
            WHERE { ?subject dro:isITSystemInvolvedIn ?object .
            ?subject dro:performs ?lol.
            ?lol dro:process ?x.
            ?x dro:isPersonalDataGovernedBy ?Z}
        """)
        return data

    def get_instance_of_regulated_technological_data(self):

        data = self.query("""
            PREFIX dro: <urn:absolute:DataRegulationOntology#>
            SELECT ?subject
            WHERE {
            { ?subject dro:isBusinessDataGovernedBy ?b } union
            { ?subject dro:isPersonalDataGovernedBy ?b }
          }
        """)


        return data[0]

    def get_instance_of_regulation(self):
        
        data = self.query("""
            PREFIX dro: <urn:absolute:DataRegulationOntology#>
            SELECT DISTINCT ?subject 
            WHERE
            { ?subject dro:governsLegalEntity ?c. }

        """)

        return data[0]    

    def get_instance_by_regulated_data(self, regulated_data):
        data = self.query("""
            PREFIX dro: <urn:absolute:DataRegulationOntology#>
            SELECT ?subject 
            WHERE { ?subject dro:isITSystemInvolvedIn ?object .
            ?subject dro:performs ?lol.
            ?lol dro:process ?x.
            ?x dro:isPersonalDataGovernedBy ?Z.
            ?x dro:hasName "EARBusiness_Data"^^xsd:string }
        """)

        return data

    def get_object_properties_from_class(self, targetClass):

        data = self.query("""
            PREFIX dro: <urn:absolute:DataRegulationOntology#>
            SELECT ?subject 
            WHERE { ?subject rdfs:domain dro:%s.}
        """, targetClass)

        return data

    def get_instances_of_class(self, targetClass):
        targetClass = self.remove_prefix(targetClass)
        classObj = self.onto[targetClass]
        return list(classObj.instances())     

    def get_instance_properties(self, targetInstance):
        targetInstance = self.remove_prefix(targetInstance)
        instance = self.onto[targetInstance]
        return list(instance.get_properties())