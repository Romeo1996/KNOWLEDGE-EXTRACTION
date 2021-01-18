import requests
from bs4 import BeautifulSoup
import numpy.random as random
import networkx as nx


class Crawler:
    def __init__(self, test=False):
        self.graph = nx.Graph()
        self.test = test
        self.links = []
        self.scores = dict()
        self.pagerank = dict()

    def graph_empty(self):
        """See if the graph is empty"""
        return nx.is_empty(self.graph)

    def all_visited(self):
        """See in all node who are visited"""
        nodes = self.graph.nodes(data=True)
        total = 0
        for node, prop in nodes:
            if prop["visited"]:
                total += 1
        num = len(nodes)
        if num - total == 0:
            return True
        return False

    def add_new_links(self, search, score, links):
        """Update links after JSON received"""
        if not search in self.graph:
            self.graph.add_node(search, visited=False)

        for link in links:
            if link[0] not in self.graph:
                self.graph.add_node(link[0], visited=False)
            self.graph.add_edge(search, link[0], weight=0)
            self.graph[search][link[0]]['weight'] = float(link[1])
            self.links.append([link[0], float(link[1])])
            self.scores[link[0]] = float(link[1])

    def get_all_website_links(self, url, score, target_links=[]):

        source = requests.get(url).content
        extl = "<span class=\"mw-headline\" id=\"External_links\""
        extr = "<span class=\"mw-headline\" id=\"References\""
        pos1 = source.decode().find(extl)
        pos2 = source.decode().find(extr)
        if pos1 < pos2 or pos1 == -1:
            source = source.decode().split(extl)[0]
        else:
            source = source.decode().split(extr)[0]
        soup = BeautifulSoup(source, "html.parser")

        self.links = []
        links = []

        url = url.replace("https://en.wikipedia.org/wiki/", "").replace("_", " ")
        url = ''.join([c if len(c.encode('utf-8')) < 4 else '?' for c in url])
        if url in self.graph:
            self.graph.nodes[url]["visited"] = True
        else:
            self.graph.add_node(url, visited=True)
            self.scores[url] = score

        for a_tag in soup.body.findAll("a"):
            href = a_tag.attrs.get("href")
            if href == "" or href is None or "/wiki/" not in href or "File" in href or "Special" in href or "ISBN" \
                    in href or "Verifiability" in href or "http" in href or "https" in href or "Wikipedia" in href or \
                    "Category" in href or "Talk" in href or "Main Page" in href or "Portal" in href or "Help" \
                    in href or "//" in href or "%" in href or "\\" in href or "Template" in href:
                continue
            else:
                url1 = href.replace("/wiki/", "").replace("_", " ")
                url1 = ''.join([c if len(c.encode('utf-8')) < 4 else '?' for c in url1])
                if url1 not in links and (not target_links or url1 in target_links):
                    if url1 not in self.graph:
                        self.graph.add_node(url1, visited=False)
                    self.graph.add_edge(url, url1, weight=0)
                    links.append(url1)

        return links

    def assign_page_score(self, simple, detailed, url):
        for i in range(len(simple)):
            self.graph[url][simple[i]]['weight'] = float(detailed[i])
            self.links.append([simple[i], float(detailed[i])])
            self.scores[simple[i]] = float(detailed[i])

    def update_score(self, url):

        self.pagerank = nx.pagerank(self.graph, personalization=self.scores)
        for k, v in self.scores.items():
            self.pagerank[k] = (self.pagerank[k] + v) / 2
        print("PAGERANK: ", self.pagerank)

    def calc_probability(self, url):
        """Define probability values of all nodes"""
        vist = dict()
        nodes = self.graph.nodes(data=True)
        names = []
        for node, prop in nodes:
            if not prop["visited"]:
                names.append(node)
                vist[node] = self.pagerank[node]

        sort_pr = {k: v for k, v in sorted(vist.items(), key=lambda item: item[1], reverse=True)}
        weights = []
        print("nomi ", names)
        high = sort_pr[list(sort_pr.keys())[0]]
        high = high - high * 0.25
        pr = dict()
        for key, values in sort_pr.items():
            if values < high:
                break
            pr[key] = values

        names = list(pr.keys())
        total = sum(list(pr.values()))
        print("NOMI ", names)

        for name in names:
            weights.append(pr[name] / total)

        if self.test:
            for i in range(len(names)):
                print(names[i], " ", weights[i])

        if self.test:
            print("WEIGHTS")
            for i in range(len(names)):
                print(names[i], " ", weights[i])

        choice = random.choice(names, 1, p=weights)[0]
        self.graph.nodes[choice]["visited"] = True
        self.graph.nodes[url]["visited"] = True
        return choice
