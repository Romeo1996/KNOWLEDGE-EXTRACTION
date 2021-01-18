from nltk.tokenize import word_tokenize
import re


class pre_process():

    def __init__(self, title, search, text, nlp, test=False):
        self.nlp = nlp
        self.search = self.__clear_search_title(search)
        self.title = self.__clear_search_title(title)
        self.text = self.__clear_search_title(text)
        self.test = test

    def pre_process_text(self):
        """Used to preprocess all the text finded on Wikipedia"""
        # Add subject if it don't exist for a verb
        new_sent = []
        split_sent, conj = self.__remove_char(self.text)
        split_sent = split_sent.split(" and ")
        words = ""
        c = -1

        for sent in split_sent:

            ent, f_subj = self.__insert_verb(sent)

            if f_subj:
                app = sent
            else:
                app = ent

            new_sent.append(app)
            if words == "":
                words += app
            else:
                words += conj[c] + " " + app
            c += 1
        if self.test:
            print("NEW SENTENCE:\n", new_sent)
            print("\nLONG WORDS: \n", words)

        # Apply get_entities
        words = words.split(".")
        words =[i for i in words if i]

        self.__remove_space_duplicate(words)

        return self.search, self.title, words

    def __remove_char(self, text):
        text = re.sub(r"\(.*?\)+", '', text)  # Remove (...)
        text = text.replace("\n", "")  # Remove \n
        text = re.sub('[^A-Za-z0-9.,\']+', ' ', text)  # Remove all symbols, not . and ,
        text = re.sub(' +', ' ', text)
        text = text.replace("'s", "")

        conj = []
        for el in word_tokenize(text):
            if el == "," or el == "and":
                conj.append(el)

        text = text.replace(", ", " and ")
        return text, conj

    def __remove_space_duplicate(self, words):
        for i in range(len(words)):
            words[i] = re.sub(' +', ' ', words[i])
            words[i] = re.sub("\\b(\\w+)(\\b\\W+\\b\\1\\b)*", '\\1', words[i])
            if self.test:
                print(words[i])

    def __insert_verb(self, sent):
        f_subj = False

        new_sent = ""

        for tok in self.nlp(sent):

            if tok.dep_.find("subj") == True:
                f_subj = True

            if not f_subj and self.check_verb_pos_dep(tok):
                new_sent += "he " + tok.text + " "  # Substitution with search
            else:
                new_sent += tok.text + " "

        return new_sent, f_subj

    def __clear_search_title(self, text):
        txt = re.sub(r"\(.*?\)+", '', text)
        txt = re.sub('[^A-Za-z0-9.,\']+', ' ', txt)
        txt = txt.lower().strip()
        return txt

    def check_verb(self, worden):
        """Check verb type given spacy worden"""
        if worden.pos_ == 'VERB':
            indirect_object = False
            direct_object = False
            for item in worden.children:
                if item.dep_ == "iobj" or item.dep_ == "pobj":
                    indirect_object = True
                if item.dep_ == "dobj" or item.dep_ == "dative":
                    direct_object = True
            if indirect_object and direct_object:
                return 'DITRANVERB'
            elif direct_object and not indirect_object:
                return 'TRANVERB'
            elif not direct_object and not indirect_object:
                return 'INTRANVERB'
            else:
                return 'VERB'
        else:
            return worden.pos_

    def true_verb(self, check):
        if self.check_verb(check) == "AUX" or self.check_verb(check) == "VERB" or self.check_verb(
                check) == "DITRANVERB" or self.check_verb(check) == "TRANVERB" or self.check_verb(check) == "INTRANVERB":
            return True

    def check_verb_pos_dep(self, word):
        if word.dep_ == "ccomp" or word.dep_ == "acl" or word.dep_ == "auxpass" or (
                word.dep_ == "ROOT" and self.true_verb(word)):
            return True
