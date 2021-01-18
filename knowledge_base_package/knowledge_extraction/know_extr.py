from knowledge_base_package.knowledge_extraction.wiki_extract import wiki_extract
from knowledge_base_package.knowledge_extraction.nlp_function import nlp_func
from knowledge_base_package.knowledge_extraction.ontologies_function import ontology



class know_extr():

    def __init__(self, search, test=False):
        wiki = wiki_extract(search)
        self.search = search
        self.text = wiki.wiki_api_summary()
        self.title = wiki.wiki_api_title().lower()
        self.test = test
        self.len_pre_proc = 0
        self.entities = dict()
        self.ont = ontology(self.search, self.test)

    def __execute_simple_extraction(self):
        nlp = nlp_func(self.title, self.search, self.text, self.test)
        self.search, self.title, self.text, self.len_pre_proc, all_words, all_relations, labels = nlp.find_words_relations()
        self.entities = nlp.entities
        return all_words, all_relations, labels

    def __execute_ontology_extraction(self, all_words):
        simple = self.ont.find_ontology_relations(all_words, self.len_pre_proc, self.entities)
        return simple

    def execute(self):
        all_words, all_relations, labels = self.__execute_simple_extraction()
        if not self.test:
            simple = self.__execute_ontology_extraction(all_words)
        else:
            simple = []
        return self.title, all_words, all_relations, simple, labels

    def get_onto_score(self):
        return self.ont.onto_choosed()

    def train_defined_model(self, links, onto_name):
        simple, detailed = self.ont.train_defined_model(links, onto_name)
        return simple, detailed
