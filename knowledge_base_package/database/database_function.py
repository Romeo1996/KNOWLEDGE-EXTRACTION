from owlready2 import *
from py2neo import Graph, Relationship
from py2neo.matching import *


def connect_graph(name, password):
    graph = Graph("bolt://localhost:7687", user=name, password=password)
    return graph


class Database:

    def __init__(self, name, password):
        self.graph = connect_graph(name, password)

    def print_informations(self):
        print("nodes ", len(self.graph.nodes))
        print(self.graph.run("MATCH (n1)-[r]->(n2) RETURN r, n1, n2"))

    def delete_all(self):
        self.graph.run("MATCH (n) DETACH DELETE n")

    def __create_first(self, title, create=False):
        first = Node("title", name=title)
        first.__primarylabel__ = "title"
        first.__primarykey__ = "name"

        if create:
            self.graph.create(first)

        return first

    # def __run_command(self, command):
    #     return self.graph.run(command)

    def update_database(self, title, rel, ontology="", labels=[]):
        """Update the database with all the relations, used for normal phrase, for ontology and for JSONs arrived"""
        init_nodes = len(self.graph.nodes)

        first = self.__create_first(title)

        lab_count = 0

        for r in rel:
            r[0] = re.sub(' +', ' ', r[0].lower())
            r[1] = re.sub(' +', ' ', r[1].lower())
            r[2] = re.sub(' +', ' ', r[2].lower())

            ignore = False

            if ontology == "":
                pl1 = labels[lab_count][0]
                pl2 = labels[lab_count][1]
                if pl2 == "remove":
                    ignore = True
                lab_count += 1
            else:
                pl1 = "ontology"
                pl2 = "ontology"
                if r[2] == "":
                    ignore = True

            if not ignore:
                if ontology == "":
                    if r[0] != title:
                        s = Node(pl1, name=r[0])
                        s.__primarylabel__ = pl1
                        s.__primarykey__ = "name"
                    else:
                        s = first

                    o = Node(pl2, name=r[2])
                    o.__primarylabel__ = pl2
                    o.__primarykey__ = "name"

                else:
                    if r[1] != "answer":
                        if r[0] != title:
                            s = Node(pl1, name=r[0])
                            s.__primarylabel__ = pl1
                            s.__primarykey__ = "name"
                        else:
                            s = first

                        o = Node(pl2, name=r[2])
                        o.__primarylabel__ = pl2
                        o.__primarykey__ = "name"

                    else:
                        s = Node(pl1, name=r[0])
                        s.__primarylabel__ = pl1
                        s.__primarykey__ = "name"

                        o = Node(title.replace(" ", "_"), name=r[2])
                        o.__primarylabel__ = title.replace(" ", "_")
                        o.__primarykey__ = "name"

                REL = Relationship.type(r[1].upper().replace(" ", "_"))
                self.graph.merge(REL(s, o))

                if ontology == "":
                    REL = Relationship.type("SEARCH")
                    self.graph.merge(REL(first, s) | REL(first, o))

        new_nodes = len(self.graph.nodes) - init_nodes

        if ontology == "":
            return new_nodes, rel, title
        else:
            return new_nodes, rel, title, ontology
