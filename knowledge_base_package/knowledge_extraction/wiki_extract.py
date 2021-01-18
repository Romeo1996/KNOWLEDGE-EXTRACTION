# WIKIPEDIA
import wikipediaapi


class wiki_extract():

    def __init__(self, search, test=False):
        self.search = search
        self.test = test

    def wiki_api_summary(self):
        wiki_wiki = wikipediaapi.Wikipedia(
            language='en',
            extract_format=wikipediaapi.ExtractFormat.WIKI
        )

        p_wiki = wiki_wiki.page(self.search)
        text = p_wiki.summary
        if self.test:
            print(text)
        return text

    def wiki_api_title(self):
        wiki_wiki = wikipediaapi.Wikipedia(
            language='en',
            extract_format=wikipediaapi.ExtractFormat.WIKI
        )

        p_wiki = wiki_wiki.page(self.search)
        text = p_wiki.title
        if self.test:
            print(text)
        return text
