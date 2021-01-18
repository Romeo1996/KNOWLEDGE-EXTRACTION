import glob
import wordninja
import shutil
from owlready2 import *
from knowledge_base_package.knowledge_extraction.model_training import train_model, find_similarity
import tensorflow_hub as hub
import numpy as np


class ontology():
    def __init__(self, text, test=False):
        self.text = text
        self.test = test

    def choose_ontology(self):
        shutil.rmtree('./model', ignore_errors=True)
        f = open("sentences.txt", "w+", encoding="utf-8")
        ontos = glob.glob("./ontologies/*_onto.owl")

        for i in range(len(ontos)):
            ontos[i] = ontos[i].replace("./ontologies\\", "")
            ontos[i] = ontos[i].replace("_onto.owl", "")

            o = wordninja.split(ontos[i])
            ontos[i] = ""
            for q in o:
                ontos[i] += " " + q
            ontos[i] = ontos[i].strip()
            f.write(ontos[i] + "\n")

        f.close()
        train_model()

        simple, detailed = find_similarity(self.text, 1)
        simple = self.sim_reformat(simple)
        detailed = self.det_perc_reformat(detailed)
        best_score = float(detailed[0])
        best = simple[0]

        return best, best_score

    def find_properties(self, path_onto):
        world = World()
        onto = world.get_ontology(path_onto).load()
        onto_classes = list(onto.classes()).__str__()
        onto_classes = onto_classes.replace("[", "")
        onto_classes = onto_classes.replace("]", "")
        onto_classes = onto_classes.split(",")
        if self.test:
            print("CHOOSE ONTOLOGY: ")
            print(onto_classes)

        property = []
        for onto_c in onto_classes:
            onto_c = onto_c.split(".")[1]
            qu = wordninja.split(onto_c)
            prop = ""
            for q in qu:
                prop += " " + q
            property.append(prop.strip().lower())

        return property

    def find_path(self, text):
        return "./ontologies/" + text + "_onto.owl"

    def file_saving(self, words, filename):
        f = open(filename + ".txt", "w+", encoding="utf-8")
        for tr in words:
            f.write(tr + "\n")
        f.close()

    def general_file_saving(self, words, filename):
        f = open(filename + ".txt", "w+", encoding="utf-8")
        for word in words:
            if word != "" and word != " ":
                f.write(word + "\n")
        f.close()

    def sim_reformat(self, sd):
        return re.findall(r'"([^"]*)"', sd)

    def det_perc_reformat(self, ds):
        return re.findall("[0-9]+\\.[0-9]+", ds)

    def onto_choosed(self):
        self.ontology_name, self.score = self.choose_ontology()
        return self.ontology_name, self.score

    def find_ontology_relations(self, all_words, phrase_number, entities):
        path_onto = self.find_path(self.ontology_name)
        onto_classes = self.find_properties(path_onto)
        if self.test:
            print("ONTOLOGY: ", path_onto)

        # FIND MORE SIMILAR WORDS
        similar_word = []
        for quest in onto_classes:
            words = all_words
            simple_dict = self.text_similarity(quest, words)
            print(simple_dict)
            simple = list(simple_dict.keys())
            detailed = list(simple_dict.values())

            # Find all entities in simple phrases
            actual_ents = dict()

            for i in range(len(simple)):
                if float(detailed[i]) > 0.28:
                    for en in entities[simple[i]]:
                        if en != "and":
                            actual_ents[en] = simple[i]

            if actual_ents:

                self.general_file_saving(actual_ents.keys(), "sentences")
                train_model()
                print("FINAL result with quest: ", quest, "\nSimple & Detailed: ")
                simple, detailed = find_similarity(quest, len(actual_ents))

                simple = self.sim_reformat(simple)
                detailed = self.det_perc_reformat(detailed)
                print("\n\n")

                # Add if similar > 70%
                for i in range(min(len(simple), len(detailed))):
                    if float(detailed[i]) >= 0.7:
                        similar_word.append([quest, simple[i], actual_ents[simple[i]]])
                        break
        return similar_word

    def train_defined_model(self, links, onto_name):
        self.file_saving(links, "sentences")
        train_model()
        simple, detailed = find_similarity(onto_name, len(links))
        simple = self.sim_reformat(simple)
        detailed = self.det_perc_reformat(detailed)
        return simple, detailed

    def text_similarity(self, message1, messages):
        embed = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")

        messages = [message1] + messages
        message_embeddings = embed(messages)
        corr = np.inner(message_embeddings, message_embeddings)

        row = corr[0][1:]
        ans = dict()
        for i in range(len(row)):
            ans[messages[i + 1]] = row[i]
        sort = {k: v for k, v in sorted(ans.items(), key=lambda item: item[1], reverse=True)}

        return sort
