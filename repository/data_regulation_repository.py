from owlready2 import *

class DataRegulationRepository:
    def __init__(self, app) -> None:
        file_path = app.config.get("OWL_FILE_PATH")
        self.onto = get_ontology(f'file://{file_path}').load()

    def remove_prefix(self, name):
        return ".".join(str(name).split(".")[1:])

    def query(self, query, *params): 
        q = query % (params)
        print(q)
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
        return self.onto.search(iri=name)  

    def get_class_regulated(self):
        functional = list(self.get_class_by_name('*Functional_Process'))
        person = [str(self.onto["Person"])]
        it = list(self.get_class_by_name('*IT_System'))

        return functional + person + it

    def get_class_data_regulated(self):
        temp = list(self.get_class_by_name('*Technological_Data'))
        temp2 = [str(self.onto["Act"])]

        return temp + temp2

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

    def get_person_by_technological_data(self, dataType):
        dataType = self.remove_prefix(dataType)

        data = self.query("""
            PREFIX dro: <urn:absolute:DataRegulationOntology#>
            SELECT
            DISTINCT ?subject 
            WHERE { ?subject dro:isPersonInvolvedIn ?funcpro.
            ?itsys dro:isITSystemInvolvedIn ?funcpro.
            ?itsys dro:performs ?acti.
            ?acti dro:process ?fdp.
            ?fdp dro:hasName "%s"^^xsd:string
            }
        """, dataType)

        return data

    def search_request(self, path, dataType):
        print("path : ", path)
        print("dataType : ", dataType)
        dataType = self.remove_prefix(dataType)

        data = self.query("""
            PREFIX dro: <urn:absolute:DataRegulationOntology#>
            SELECT
            DISTINCT ?subject 
            WHERE { 
            %s
            ?lastcrit dro:hasName "%s"^^xsd:string
            }
        """, path, dataType)

        return data    

    def get_it_system_by_technological_data(self, dataType):
        dataType = self.remove_prefix(dataType)

        data = self.query("""
            PREFIX dro: <urn:absolute:DataRegulationOntology#>
            SELECT
            DISTINCT ?subject 
            WHERE { 
            ?subject dro:performs ?activite.
            ?activite dro:process ?dataOne.
            ?dataOne dro:hasName "%s"^^xsd:string
            }
        """, dataType)

        return data

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

    def get_relations_properties(self, targetProperties):
        targetProperties = self.remove_prefix(targetProperties)
        prop = self.onto[targetProperties]
        return list(prop.get_relations())    