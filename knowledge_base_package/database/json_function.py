import json
import os


def all_search_connection(similar_word, title):
    rel = []

    for sim in similar_word:
        sim[0] = sim[0].upper().replace(" ", "_")  # name of property in lower
        sim[1] = sim[1].lower()
        sim[2] = sim[2].lower()

        rel.append([title, sim[0], sim[1]])
        rel.append([sim[1], "ANSWER", sim[2]])

    return rel


def json_encode(words, title, ip, ontology=None, labels=[]):
    j_base = dict()
    j_base["search"] = title
    j_base["ip"] = ip

    if ontology is not None:
        j_base["ontology"] = ontology

    count = 0

    for word in words:
        j_in = dict()
        j_in["subj"] = word[0]
        j_in["rel"] = word[1]
        j_in["obj"] = word[2]
        if ontology is None:
            j_in["subj_label"] = labels[count][0]
            j_in["obj_label"] = labels[count][1]
        j_base[str(count)] = j_in
        count += 1

    return json.dumps(j_base)


def file_json_save(json_string):
    if file_exist("json_strings"):
        f = open("json_strings.txt", "a")
        f.write(json_string + "\n")
        f.close()
    else:
        f = open("json_strings.txt", "w+")
        f.write(json_string + "\n")
        f.close()


def json_decode(json_string):
    json_dict = json.loads(json_string)

    title = json_dict["search"]
    del json_dict["search"]

    ip = json_dict["ip"]
    del json_dict["ip"]

    ontology = ""
    if "ontology" in json_dict:
        ontology = json_dict["ontology"]
        del json_dict["ontology"]

    rel = []
    labels = []
    for num, dicts in json_dict.items():
        act = []
        lab = []
        for key, item in dicts.items():
            if key != "subj_label" and key != "obj_label":
                act.append(item)
            else:
                lab.append(item)
        rel.append(act)
        labels.append(lab)
    return title, ip, rel, ontology, labels


def file_exist(name):
    return os.path.isfile(name + ".txt")


def json_encode_pagerank(links, search, score, ip):
    j_base = dict()
    j_base["visited"] = search
    j_base["score"] = score
    j_base["ip"] = ip

    count = 0

    for link in links:
        j_in = dict()
        j_in["link"] = link[0]
        j_in["score"] = link[1]
        j_base[str(count)] = j_in
        count += 1

    return json.dumps(j_base)


def json_decode_pagerank(json_string):
    json_dict = json.loads(json_string)

    title = json_dict["visited"]
    del json_dict["visited"]
    score = json_dict["score"]
    del json_dict["score"]
    ip = json_dict["ip"]
    del json_dict["ip"]

    links = []
    for num, dicts in json_dict.items():
        lab = []
        for key, item in dicts.items():
            lab.append(item)
        links.append(lab)

    return title, score, links, ip
