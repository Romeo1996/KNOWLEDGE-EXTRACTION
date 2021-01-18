import spacy
from spacy.matcher import Matcher
import re
from knowledge_base_package.knowledge_extraction.nlp_preprocessing import pre_process


class nlp_func():

    def __init__(self, title, search, text, test=False):
        self.nlp = spacy.load('en_core_web_lg')
        self.test = test
        self.nlp_pre_process = pre_process(title, search, text, self.nlp, test)
        self.search, self.title, self.text = self.nlp_pre_process.pre_process_text()
        self.entities = dict()

    def find_words_relations(self):
        """After text preprocessing he find all relation and words by get final"""
        all_words = []
        all_relations = []
        for ph in self.text:
            if ph != "" and ph != " ":
                word, rel = self.get_final_sentences(ph)
                all_words += word
                all_relations += rel
        # Find all labels for the Database update
        labels = self.nlp_ents(all_relations)

        return self.search, self.title, self.text, len(self.text), all_words, all_relations, labels

    def get_final_sentences(self, sent):
        """Used to find the final set of sentences to save on FILEs"""

        entities, sentences, relations = self.extract_sentence(sent)
        print("\nEnt: ", entities)
        print("Rel: ", relations)
        print("Sent: ", sentences)

        # Apply the switching of the first entity
        sw, relations = self.subject_switch(entities, sentences, relations)
        self.remove_and(sw)
        print("\nSwitched: \n", sw, "\n----------------------------------------------------")
        # Update the dictionary
        self.find_entities_in_phrases(relations, sw)

        return sw, relations

    def split_entities(self, ent):

        ent = ent.replace(",", "and")
        ent = re.sub(' +', ' ', ent)
        ent = re.sub("\\b(\\w+)(\\b\\W+\\b\\1\\b)*", '\\1', ent)
        ent = ent.split(" and ")
        print(ent)
        return ent

    def extract_sentence(self, phrase):
        """Used to extract sentence from phrase"""

        sentences = []
        entities = []
        relations = []
        flag = True
        while flag:
            ent, word, flag, old = self.get_entities(phrase)
            ent[0] = self.remove_and([ent[0]])[0]  # remove and and , from ent
            ent[1] = self.remove_and([ent[1]])[0]
            obj = self.split_entities(ent[1])

            for o in obj:
                rel = self.get_relation(old)
                merge = ent[0] + " " + rel + " " + o
                merge = self.remove_blank_and_duplicates(merge)
                # If the sentence is composed with one word we remove it
                if len(merge.split()) > 1:
                    sentences.append(merge)
                    relations.append([ent[0], rel, o])
                    entities.append(ent[0])
            phrase = word
        return entities, sentences, relations

    def remove_blank_and_duplicates(self, string):
        string = re.sub(' +', ' ', string)
        string = re.sub("\\b(\\w+)(\\b\\W+\\b\\1\\b)*", '\\1', string)
        string = re.sub(' +', ' ', string)
        return string

    def remove_and(self, sw):
        """Used to remove 'and' from start/finish phrase"""
        for i in range(len(sw)):
            try:
                w = sw[i].split()
                if w[-1] == "and" or w[-1] == ",":
                    sw[i] = sw[i].rsplit(' ', 1)[0]
                if w[0] == "and" or w[0] == ",":
                    sw[i] = sw[i].split(' ', 1)[1]
            except:
                continue
        return sw

    def subject_switch(self, ent, fr, rel):
        """ Pass all entities and relations to obtain switched subject phrase"""
        subj = self.title
        new_fr = []
        new_rel = rel
        cont = 0
        for i in range(len(fr)):
            newfr = ""
            for n in self.nlp(fr[i]):
                if " " not in n.text:
                    if n.pos_ == "PRON":
                        newfr += subj + " "
                        new_rel[i][0] = new_rel[i][0].replace(n.text, subj)
                    elif n.dep_.find("subj") == True:
                        subj = ent[i]
                        newfr += n.text + " "
                    else:
                        newfr += n.text + " "
            cont += 1
            new_fr.append(newfr.strip())
        return new_fr, new_rel

    def get_entities(self, sent):
        """Used to retrive entities in a passed sentence"""

        ent1 = ""
        ent2 = ""

        cont = 0  # count subject in phrase
        flag_ent1 = False  # Actually we don't have finded ent1
        flag_ent2 = False  # Actually we don't have finded ent2

        mod_ent1 = True  # ent2 is completed
        mod_ent2 = True  # ent2 is completed

        new_sent = False  # False = this is the actual phrase to consider; True = ignore all and create phrase

        old_phrase = ""  # Verified word
        phrase = ""  # Rest of text

        for word in self.nlp(sent):
            if word.text != " ":
                # If is a new phrase we recreate the text without the finded
                if new_sent:
                    phrase = phrase + " " + word.text
                else:
                    if word.dep_.find("subj") == True:
                        cont += 1
                        if cont == 2:
                            new_sent = True  # From now we ignore all and reformat phrase
                            phrase = phrase + " " + word.text
                            mod_ent1 = False
                            mod_ent2 = False

                    # Verify first entity (Subject/s)
                    if mod_ent1:
                        ent1, flag_ent1, mod_ent1 = self.check_dependencies(word, ent1, flag_ent1, mod_ent1, "subj")
                        old_phrase = old_phrase + " " + word.text

                    # Verify first entity (Object/s)
                    elif mod_ent2:
                        ent2, flag_ent2, mod_ent2 = self.check_dependencies(word, ent2, flag_ent2, mod_ent2, "obj")
                        if mod_ent2:
                            old_phrase = old_phrase + " " + word.text

        return [ent1.strip(), ent2.strip()], phrase, new_sent, old_phrase

    def check_dependencies(self, word, ent, flag_ent, mod_ent, mod):
        """Used to set if a word is part of entities"""

        if word.dep_ != "det" and word.dep_ != "prep" and not self.nlp_pre_process.check_verb_pos_dep(
                word):  # Ho tolto true_verb
            ent = ent + " " + word.text
        if word.dep_.find(mod) == True:
            flag_ent = True
        elif word.dep_ != "det" and word.dep_ != "prep" and word.dep_ != "advcl" and word.dep_ != "punct" and \
                word.dep_ != "conj" and word.dep_ != "cc" and word.dep_ != "attr" and word.dep_ != "appos" and \
                word.dep_ != "compound" and word.dep_.endswith("mod") != True:
            if flag_ent:
                mod_ent = False
            else:
                ent = ""
        return ent, flag_ent, mod_ent

    def get_relation(self, sent):
        words = self.nlp(sent)
        # Matcher class object
        matcher = Matcher(self.nlp.vocab)

        # define the pattern
        pattern1 = [{'DEP': 'ROOT'},
                    {'DEP': 'prep', 'OP': "?"},
                    {'DEP': 'agent', 'OP': "?"},
                    {'POS': 'ADJ', 'OP': "?"}]  # questo era quello che già c'era
        pattern2 = [{'POS': 'AUX'},
                    {'DEP': 'prep', 'OP': "?"},
                    {'DEP': 'agent', 'OP': "?"},
                    {'POS': 'ADJ', 'OP': "?"}]
        pattern3 = [{'DEP': 'advcl'},
                    {'DEP': 'prep', 'OP': "?"},
                    {'DEP': 'agent', 'OP': "?"},
                    {'POS': 'ADJ', 'OP': "?"}]
        pattern4 = [{'DEP': 'auxpass'},
                    {'DEP': 'prep', 'OP': "?"},
                    {'DEP': 'agent', 'OP': "?"},
                    {'POS': 'ADJ', 'OP': "?"}]
        pattern5 = [{'DEP': 'ROOT'},
                    {'POS': 'VERB',
                     'OP': "+"}]
        matcher.add("matching_1", None, pattern5, pattern1, pattern2, pattern3,
                    pattern4)

        matches = matcher(words)
        k = len(matches) - 1
        verb = words[matches[k][1]:matches[k][2]]

        return verb.text

    def find_entities_in_phrases(self, ent, phrases):
        """Give a phrase and his ents and add it to a dictionary"""
        count = 0
        for phrase in phrases:
            ents = []
            app = ent[count][0].replace(".", "")
            if not app.isnumeric():
                ents.append(ent[count][0])
            app = ent[count][2].replace(".", "")
            if not app.isnumeric():
                ents.append(ent[count][2])
            self.entities[phrase] = ents
            count += 1

    def nlp_ents(self, rel):
        """Find labels for relations"""
        pl = []
        for r in rel:
            try:
                pl1 = self.nlp(r[0]).ents[0].label_
            except:
                pl1 = "other"
            try:
                pl2 = self.nlp(r[2]).ents[0].label_
            except:
                pl2 = "other"
                if r[2] == "":
                    pl2 = "remove"
            pl.append([pl1, pl2])
        return pl
