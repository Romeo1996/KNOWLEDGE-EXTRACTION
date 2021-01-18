import sys
from knowledge_base_package.multi_agent.multi_agent import MultiAgent, add_observ, add_lis
from knowledge_base_package.database.database_function import Database
from knowledge_base_package.database.json_function import *
from knowledge_base_package.knowledge_extraction.know_extr import know_extr
from knowledge_base_package.knowledge_extraction.web_crawler import Crawler
import threading
from tkinter.filedialog import askopenfilename
import easygui
from tkinter import messagebox

TIME = 600

try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

try:
    import ttk

    py3 = False
except ImportError:
    import tkinter.ttk as ttk

    py3 = True


def set_Tk_var():
    global che48
    che48 = tk.IntVar()


class Support:
    def __init__(self):
        self.agent = None
        self.db = Database("tizio", "ciao")
        self.all_agents = dict()

    def initialize(self, inp):
        self.agent = MultiAgent(inp)
        self.agent.start()
        add_observ(self)

    def update(self, element, save=True):
        my_ip = w.get_my_ip_text()
        agents = w.get_all_agent_text()

        if len(my_ip.get("1.0", "end-1c")) == 0 and "ip4" in element:
            set_text_in_text(my_ip, element)
            self.all_agents[element] = [0, 0, 0, []]
        elif "delete " in element:
            div = element.split("delete ")
            lis_dim = int(div[0])
            elem = div[1]
            text = agents.get("1.0", "end-1c")
            text = text.replace(elem + "\n", "").replace("\n", "")
            set_text_in_text(agents, text)
            if lis_dim == 1:
                btn = w.get_btn_connect()
                btn.configure(state="active")
                btn.configure(text="Reconnect")
                che48.set(1)
                w.get_bootstrap_entry().configure(state="normal")
                w.get_bootstrap_entry().delete(0, "end")
        elif "search" in element:
            if save:
                file_json_save(element)
            tit, ip, rel, onto_name, labels = json_decode(element)
            if onto_name == "":
                new_nodes, r, t = self.db.update_database(tit, rel, "", labels)
                if ip != "":
                    # Update Target
                    self.all_agents[ip][1] += 1
                    # Update Nodes
                    self.all_agents[ip][2] += new_nodes
                    # Update searches
                    self.all_agents[ip][3] += [tit]
            else:
                self.db.update_database(tit, rel, onto_name)
        elif "visited" in element:
            search, score, links, ip = json_decode_pagerank(element)
            self.all_agents[ip][0] += 1
            buffer.append([search, score, links])
        else:
            add_text_in_text(agents, element + "\n")
            if element not in self.all_agents.keys():
                self.all_agents[element] = [0, 0, 0, []]

        update_treeview(self.all_agents)

    def add_json(self, string):
        if self.agent is not None:
            print("JSON SENT: ", string)
            self.agent.add_json(string)

    def update_agent(self, element):
        self.all_agents[element] = [0, 0, 0, []]

    def add_nodes(self, nodes):
        if get_my_ip() != "":
            self.all_agents[get_my_ip()][2] += nodes
            update_treeview(self.all_agents)

    def add_visited(self):
        if get_my_ip() != "":
            self.all_agents[get_my_ip()][0] += 1
            update_treeview(self.all_agents)

    def add_target(self):
        if get_my_ip() != "":
            self.all_agents[get_my_ip()][1] += 1
            update_treeview(self.all_agents)

    def add_search_title(self, title):
        if get_my_ip() != "":
            self.all_agents[get_my_ip()][3] += [title]
            update_treeview(self.all_agents)

    def save_on_file(self):
        if os.path.isfile("timestamp.txt"):
            f = open("timestamp.txt", "a", encoding="utf-8")
            f.write(str(self.all_agents) + "\n")
            f.close()
        else:
            f = open("timestamp.txt", "w+", encoding="utf-8")
            f.write(str(self.all_agents) + "\n")
            f.close()
        threading.Timer(TIME, agent.save_on_file).start()


def get_my_ip():
    """Retrive my ip addr from interface"""
    my_ip = w.get_my_ip_text()
    return my_ip.get("1.0", "end-1c")


def update_treeview(agents):
    tree = w.get_treeview()
    remove_all(tree)
    for agent_name, values in agents.items():
        father = tree.insert("", "end", text=agent_name, values=([agent_name] + values[0:3]))
        for val in values[3]:
            tree.insert(father, "end", text=val, values=(val, "", "", ""))


def remove_all(tree):
    x = tree.get_children()
    print('get_children values: ', x, '\n')
    if x != '()':  # checks if there is something in the first row
        for child in x:
            tree.delete(child)


def treeview_sort_column(tv, col, reverse):
    l = [(tv.set(k, col), k) for k in tv.get_children('')]
    l.sort(reverse=reverse)

    # rearrange items in sorted positions
    for index, (val, k) in enumerate(l):
        tv.move(k, '', index)

    # reverse sort next time
    tv.heading(col, command=lambda _col=col: treeview_sort_column(tv, _col, not reverse))


def init(top, gui, *args, **kwargs):
    global w, top_level, root, agent, search, stop, buffer
    w = gui
    top_level = top
    root = top
    buffer = []
    agent = Support()
    search = None
    stop = False
    threading.Thread(target=lambda: knowledge_extraction()).start()


def p2p_connection(p1):
    chk = w.get_check_bootstrap()
    ip = w.get_bootstrap_entry()
    btn_state = p1.widget.cget('state')
    if btn_state != "disabled":
        if che48.get() == 0:
            inp = 0
            agent.initialize(inp)
        else:
            inp = ip.get()
            agents = w.get_all_agent_text()
            add_text_in_text(agents, inp + "\n")
            agent.update_agent(inp)
            if p1.widget.cget('text') != "Reconnect":
                agent.initialize(inp)
            else:
                add_lis(inp)
        threading.Timer(TIME, agent.save_on_file).start()
        chk.configure(state="disabled")
        p1.widget.configure(state="disabled")
        ip.configure(state="disabled")
    sys.stdout.flush()


def delete_graph_thread(p1):
    btn_state = p1.widget.cget('state')
    if btn_state != "disabled":
        threading.Thread(target=lambda: delete_graph()).start()


def delete_graph():
    disable_buttons()
    info = w.get_info_text()
    set_text_in_text(info, "Deleting...")
    agent.db.delete_all()  # Clear Graph
    messagebox.showinfo("Delete", "Graph Deleted")
    set_text_in_text(info, "Ready to use")
    enable_buttons()


def enable_buttons():
    w.get_start_btn().configure(state="active")
    w.get_btn_file().configure(state="active")
    w.get_delete_btn().configure(state="active")
    w.get_btn_connect().configure(state="active")


def disable_buttons():
    w.get_start_btn().configure(state="disabled")
    w.get_btn_file().configure(state="disabled")
    w.get_delete_btn().configure(state="disabled")
    w.get_btn_connect().configure(state="disabled")


def start_search(p1):
    global search, stop
    btn_state = p1.widget.cget('state')
    if btn_state != "disabled":
        disable_buttons()
        search = easygui.enterbox("Search: ")  # "Pizza Margherita"
        if search is not None and search.lower().islower():
            stop = False
            info = w.get_info_text()
            set_text_in_text(info, "Searching...")
        else:
            enable_buttons()


def load_file_thread(p1):
    btn_state = p1.widget.cget('state')
    if btn_state != "disabled":
        threading.Thread(target=lambda: load_file()).start()


def load_file():
    disable_buttons()
    filename = askopenfilename(filetypes=[("Block Note Files", ".txt")])
    if filename != "":
        info = w.get_info_text()
        set_text_in_text(info, "Loading...")
        f = open(filename, "r")
        db_strings = f.read()
        db_strings = db_strings.split("\n")
        f.close()
        for st in db_strings:
            if st != "":
                agent.update(st, False)
        set_text_in_text(info, "Ready to use")
        messagebox.showinfo("Load", "Graph Loaded")
    enable_buttons()


def knowledge_extraction(test=False):
    global search, stop, buffer
    crawler = Crawler()
    while True:
        if search is not None and search.lower().islower() and not stop:
            stop = True
            count = 0
            no_found = 0
            while search is not None and count < 100 and no_found < 10:
                extractor = know_extr(search, test)
                onto_name, onto_score = extractor.get_onto_score()

                if not test:
                    print("ACTUAL SCORE: ", onto_name, "\t", search, "\t", onto_score)
                if onto_score is not None and onto_score > 0.2:
                    # Update target and title
                    agent.add_target()
                    agent.add_search_title(search)

                    no_found = 0
                    # Find all phrases and relations to use in lists
                    title, all_words, all_relations, similar_word, ent_labels = extractor.execute()
                    # Update DataBase and create JSON string for multiagent
                    new_nodes, relation, title = agent.db.update_database(title, all_relations, "", ent_labels)
                    # Update Nodes
                    agent.add_nodes(new_nodes)
                    json_string = json_encode(relation, title, get_my_ip(), None, ent_labels)
                    file_json_save(json_string)
                    agent.add_json(json_string)
                    agent.db.print_informations()

                    if test:
                        print("\nAll similar words: ", similar_word)

                    all_relations = all_search_connection(similar_word, title)
                    new_nodes, relation, title, onto = agent.db.update_database(title, all_relations, onto_name)
                    json_string = json_encode(relation, title, get_my_ip(), onto)
                    file_json_save(json_string)
                    agent.add_json(json_string)
                    agent.db.print_informations()
                print("END MAIN\n")

                print("START PAGE-RANK")
                temp_buffer = buffer
                if temp_buffer:
                    for se, sc, li in temp_buffer:
                        crawler.add_new_links(se, sc, li)
                        crawler.update_score(se)
                    buffer = [el for el in buffer if el not in temp_buffer]

                if onto_score is not None:
                    url = "https://en.wikipedia.org/wiki/" + search.replace(" ", "_")
                    found_links = crawler.get_all_website_links(url, onto_score)
                    if found_links:
                        simple, detailed = extractor.train_defined_model(found_links, onto_name)
                        crawler.assign_page_score(simple, detailed, search)
                        crawler.update_score(search)
                        pr_links = []
                        for i in range(len(simple)):
                            pr_links.append([simple[i], float(detailed[i])])
                        json_string = json_encode_pagerank(pr_links, search, onto_score, get_my_ip())
                        agent.add_json(json_string)
                if not crawler.graph_empty() and not crawler.all_visited():
                    search = crawler.calc_probability(search)
                    print("NEW SEARCH ", search)
                    count += 1
                    # Update Visited
                    agent.add_visited()
                elif crawler.all_visited():
                    search = None

                no_found += 1
            search = None
            info = w.get_info_text()
            set_text_in_text(info, "SEARCH ENDED")
            enable_buttons()


def set_text_in_text(textForm, text):
    """Set text in a TextForm of Tkinter"""
    textForm.configure(state="normal")
    textForm.delete(1.0, "end")
    textForm.insert(1.0, text)
    textForm.configure(state="disabled")


def add_text_in_text(textForm, text):
    """Add text in a TextForm of Tkinter"""
    textForm.configure(state="normal")
    textForm.insert(1.0, text)
    textForm.configure(state="disabled")


def del_text_in_text(textForm):
    """Clear text in a TextForm of Tkinter"""
    textForm.configure(state="normal")
    textForm.delete(1.0, "end")
    textForm.configure(state="disabled")


def destroy_window():
    import os
    os.kill(os.getpid(), 9)
