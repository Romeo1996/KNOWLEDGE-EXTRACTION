import sys

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

from knowledge_base_package.interface import Knowledge_Extraction_GUI_support


def vp_start_gui():
    '''Starting point when module is the main routine.'''
    global val, w, root
    root = tk.Tk()
    Knowledge_Extraction_GUI_support.set_Tk_var()
    top = Toplevel1(root)
    Knowledge_Extraction_GUI_support.init(root, top)
    root.mainloop()


w = None


def create_Toplevel1(rt, *args, **kwargs):
    '''Starting point when module is imported by another module.
       Correct form of call: 'create_Toplevel1(root, *args, **kwargs)' .'''
    global w, w_win, root
    # rt = root
    root = rt
    w = tk.Toplevel(root)
    Knowledge_Extraction_GUI_support.set_Tk_var()
    top = Toplevel1(w)
    Knowledge_Extraction_GUI_support.init(w, top, *args, **kwargs)
    return (w, top)


def destroy_Toplevel1():
    global w
    w.destroy()
    w = None


class Toplevel1:
    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9'  # X11 color: 'gray85'
        _ana1color = '#d9d9d9'  # X11 color: 'gray85'
        _ana2color = '#ececec'  # Closest X11 color: 'gray92'
        self.style = ttk.Style()
        if sys.platform == "win32":
            self.style.theme_use('winnative')
        self.style.configure('.', background=_bgcolor)
        self.style.configure('.', foreground=_fgcolor)
        self.style.configure('.', font="TkDefaultFont")
        self.style.map('.', background=
        [('selected', _compcolor), ('active', _ana2color)])

        top.geometry("919x714+318+114")
        top.minsize(120, 1)
        top.maxsize(1924, 1061)
        top.resizable(1, 1)
        top.title("New Toplevel")
        top.configure(background="#d9d9d9")
        top.protocol("WM_DELETE_WINDOW", lambda: Knowledge_Extraction_GUI_support.destroy_window())

        self.Frame1 = tk.Frame(top)
        self.Frame1.place(relx=0.011, rely=0.165, relheight=0.416
                , relwidth=0.974)
        self.Frame1.configure(relief='groove')
        self.Frame1.configure(borderwidth="2")
        self.Frame1.configure(relief="groove")
        self.Frame1.configure(background="#d9d9d9")

        self.btn_connect = tk.Button(self.Frame1)
        self.btn_connect.place(relx=0.011, rely=0.062, height=34, width=67)
        self.btn_connect.configure(activebackground="#ececec")
        self.btn_connect.configure(activeforeground="#000000")
        self.btn_connect.configure(background="#d9d9d9")
        self.btn_connect.configure(disabledforeground="#a3a3a3")
        self.btn_connect.configure(foreground="#000000")
        self.btn_connect.configure(highlightbackground="#d9d9d9")
        self.btn_connect.configure(highlightcolor="black")
        self.btn_connect.configure(pady="0")
        self.btn_connect.configure(text='''Connect''')
        self.btn_connect.bind('<Button-1>', lambda e: Knowledge_Extraction_GUI_support.p2p_connection(e))

        self.bootstrap_check = tk.Checkbutton(self.Frame1)
        self.bootstrap_check.place(relx=0.089, rely=0.062, relheight=0.105
                , relwidth=0.117)
        self.bootstrap_check.configure(activebackground="#ececec")
        self.bootstrap_check.configure(activeforeground="#000000")
        self.bootstrap_check.configure(background="#d9d9d9")
        self.bootstrap_check.configure(disabledforeground="#a3a3a3")
        self.bootstrap_check.configure(foreground="#000000")
        self.bootstrap_check.configure(highlightbackground="#d9d9d9")
        self.bootstrap_check.configure(highlightcolor="black")
        self.bootstrap_check.configure(justify='left')
        self.bootstrap_check.configure(text='''Give Bootstrap''')
        self.bootstrap_check.configure(variable=Knowledge_Extraction_GUI_support.che48)

        self.boostrap_entry = tk.Entry(self.Frame1)
        self.boostrap_entry.place(relx=0.212, rely=0.062, height=34, relwidth=0.764)
        self.boostrap_entry.configure(background="white")
        self.boostrap_entry.configure(cursor="fleur")
        self.boostrap_entry.configure(disabledforeground="#a3a3a3")
        self.boostrap_entry.configure(font="TkFixedFont")
        self.boostrap_entry.configure(foreground="#000000")
        self.boostrap_entry.configure(insertbackground="black")

        self.my_ip_text = tk.Text(self.Frame1)
        self.my_ip_text.place(relx=0.011, rely=0.308, relheight=0.105, relwidth=0.974)
        self.my_ip_text.configure(background="white")
        self.my_ip_text.configure(font="TkTextFont")
        self.my_ip_text.configure(foreground="black")
        self.my_ip_text.configure(highlightbackground="#d9d9d9")
        self.my_ip_text.configure(highlightcolor="black")
        self.my_ip_text.configure(insertbackground="black")
        self.my_ip_text.configure(selectbackground="blue")
        self.my_ip_text.configure(selectforeground="white")
        self.my_ip_text.configure(wrap="word")
        self.my_ip_text.configure(state="disabled")

        self.all_agent_text = tk.Text(self.Frame1)
        self.all_agent_text.place(relx=0.011, rely=0.523, relheight=0.44, relwidth=0.974)
        self.all_agent_text.configure(background="white")
        self.all_agent_text.configure(font="TkTextFont")
        self.all_agent_text.configure(foreground="black")
        self.all_agent_text.configure(highlightbackground="#d9d9d9")
        self.all_agent_text.configure(highlightcolor="black")
        self.all_agent_text.configure(insertbackground="black")
        self.all_agent_text.configure(selectbackground="blue")
        self.all_agent_text.configure(selectforeground="white")
        self.all_agent_text.configure(wrap="word")
        self.all_agent_text.configure(state="disabled")

        self.Label2 = tk.Label(self.Frame1)
        self.Label2.place(relx=0.011, rely=0.191, height=23, width=94)
        self.Label2.configure(background="#d9d9d9")
        self.Label2.configure(disabledforeground="#a3a3a3")
        self.Label2.configure(foreground="#000000")
        self.Label2.configure(text='''My IP address:''')

        self.Label3 = tk.Label(self.Frame1)
        self.Label3.place(relx=0.011, rely=0.431, height=23, width=107)
        self.Label3.configure(background="#d9d9d9")
        self.Label3.configure(disabledforeground="#a3a3a3")
        self.Label3.configure(foreground="#000000")
        self.Label3.configure(text='''All Online Agents:''')

        self.Frame2 = tk.Frame(top)
        self.Frame2.place(relx=0.011, rely=0.602, relheight=0.384, relwidth=0.974)
        self.Frame2.configure(relief='groove')
        self.Frame2.configure(borderwidth="2")
        self.Frame2.configure(relief="groove")
        self.Frame2.configure(background="#d9d9d9")

        columns = ("Col0", "Col1", "Col2", "Col3")
        self.style.configure('Treeview', font="TkDefaultFont")
        self.Scrolledtreeview1 = ScrolledTreeView(self.Frame2)
        self.Scrolledtreeview1.place(relx=0.011, rely=0.087, relheight=0.89, relwidth=0.981)
        self.Scrolledtreeview1.configure(columns=columns)
        # build_treeview_support starting.
        self.Scrolledtreeview1.heading("#0", text="")
        self.Scrolledtreeview1.heading("#0", anchor="center")
        self.Scrolledtreeview1.column("#0", width="10")
        self.Scrolledtreeview1.column("#0", minwidth="10")
        self.Scrolledtreeview1.column("#0", stretch="1")
        self.Scrolledtreeview1.column("#0", anchor="w")
        self.Scrolledtreeview1.heading("Col0", text="Agents")
        self.Scrolledtreeview1.heading("Col0", anchor="center")
        self.Scrolledtreeview1.column("Col0", width="500")
        self.Scrolledtreeview1.column("Col0", minwidth="30")
        self.Scrolledtreeview1.column("Col0", stretch="1")
        self.Scrolledtreeview1.column("Col0", anchor="w")
        self.Scrolledtreeview1.heading("Col1", text="Visited Pages")
        self.Scrolledtreeview1.heading("Col1", anchor="center")
        self.Scrolledtreeview1.column("Col1", width="120")
        self.Scrolledtreeview1.column("Col1", minwidth="30")
        self.Scrolledtreeview1.column("Col1", stretch="1")
        self.Scrolledtreeview1.column("Col1", anchor="w")
        self.Scrolledtreeview1.heading("Col2", text="Target Pages")
        self.Scrolledtreeview1.heading("Col2", anchor="center")
        self.Scrolledtreeview1.column("Col2", width="120")
        self.Scrolledtreeview1.column("Col2", minwidth="30")
        self.Scrolledtreeview1.column("Col2", stretch="1")
        self.Scrolledtreeview1.column("Col2", anchor="w")
        self.Scrolledtreeview1.heading("Col3", text="Found Nodes")
        self.Scrolledtreeview1.heading("Col3", anchor="center")
        self.Scrolledtreeview1.column("Col3", width="120")
        self.Scrolledtreeview1.column("Col3", minwidth="20")
        self.Scrolledtreeview1.column("Col3", stretch="1")
        self.Scrolledtreeview1.column("Col3", anchor="w")
        self.Scrolledtreeview1['show'] = 'headings'
        for col in columns:
            self.Scrolledtreeview1.heading(col, command=lambda _col=col: Knowledge_Extraction_GUI_support.treeview_sort_column(self.Scrolledtreeview1, _col, False))
        # self.Scrolledtreeview1.pack()

        self.Label1 = tk.Label(top)
        self.Label1.place(relx=0.033, rely=0.153, height=22, width=174)
        self.Label1.configure(background="#d9d9d9")
        self.Label1.configure(disabledforeground="#a3a3a3")
        self.Label1.configure(foreground="#000000")
        self.Label1.configure(text='''Multi-Agent P2P Connection''')

        self.Label4 = tk.Label(top)
        self.Label4.place(relx=0.033, rely=0.588, height=22, width=34)
        self.Label4.configure(background="#d9d9d9")
        self.Label4.configure(disabledforeground="#a3a3a3")
        self.Label4.configure(foreground="#000000")
        self.Label4.configure(text='''Stats''')

        self.Frame3 = tk.Frame(top)
        self.Frame3.place(relx=0.011, rely=0.026, relheight=0.121, relwidth=0.974)
        self.Frame3.configure(relief='groove')
        self.Frame3.configure(borderwidth="2")
        self.Frame3.configure(relief="groove")
        self.Frame3.configure(background="#d9d9d9")

        self.btn_file = tk.Button(self.Frame3)
        self.btn_file.place(relx=0.022, rely=0.316, height=34, width=67)
        self.btn_file.configure(activebackground="#ececec")
        self.btn_file.configure(activeforeground="#000000")
        self.btn_file.configure(background="#d9d9d9")
        self.btn_file.configure(disabledforeground="#a3a3a3")
        self.btn_file.configure(foreground="#000000")
        self.btn_file.configure(highlightbackground="#d9d9d9")
        self.btn_file.configure(highlightcolor="black")
        self.btn_file.configure(pady="0")
        self.btn_file.configure(text='''Browse''')
        self.btn_file.bind('<Button-1>', lambda e: Knowledge_Extraction_GUI_support.load_file_thread(e))

        self.delete_btn = tk.Button(self.Frame3)
        self.delete_btn.place(relx=0.123, rely=0.316, height=34, width=97)
        self.delete_btn.configure(activebackground="#ececec")
        self.delete_btn.configure(activeforeground="#000000")
        self.delete_btn.configure(background="#d9d9d9")
        self.delete_btn.configure(disabledforeground="#a3a3a3")
        self.delete_btn.configure(foreground="#000000")
        self.delete_btn.configure(highlightbackground="#d9d9d9")
        self.delete_btn.configure(highlightcolor="black")
        self.delete_btn.configure(pady="0")
        self.delete_btn.configure(text='''Delete Graph''')
        self.delete_btn.bind('<Button-1>', lambda e: Knowledge_Extraction_GUI_support.delete_graph_thread(e))

        self.start_btn = tk.Button(self.Frame3)
        self.start_btn.place(relx=0.250, rely=0.316, height=34, width=97)
        self.start_btn.configure(activebackground="#ececec")
        self.start_btn.configure(activeforeground="#000000")
        self.start_btn.configure(background="#d9d9d9")
        self.start_btn.configure(disabledforeground="#a3a3a3")
        self.start_btn.configure(foreground="#000000")
        self.start_btn.configure(highlightbackground="#d9d9d9")
        self.start_btn.configure(highlightcolor="black")
        self.start_btn.configure(pady="0")
        self.start_btn.configure(text='''Start Search''')
        self.start_btn.bind('<Button-1>', lambda e: Knowledge_Extraction_GUI_support.start_search(e))

        self.info_text = tk.Text(self.Frame3)
        self.info_text.place(relx=0.492, rely=0.211, relheight=0.568, relwidth=0.488)
        self.info_text.configure(background="white")
        self.info_text.configure(font="TkTextFont")
        self.info_text.configure(foreground="black")
        self.info_text.configure(highlightbackground="#d9d9d9")
        self.info_text.configure(highlightcolor="black")
        self.info_text.configure(insertbackground="black")
        self.info_text.configure(selectbackground="blue")
        self.info_text.configure(selectforeground="white")
        self.info_text.configure(wrap="word")
        self.info_text.configure(state="disabled")


        self.Label5 = tk.Label(top)
        self.Label5.place(relx=0.022, rely=0.013, height=21, width=44)
        self.Label5.configure(background="#d9d9d9")
        self.Label5.configure(disabledforeground="#a3a3a3")
        self.Label5.configure(foreground="#000000")
        self.Label5.configure(text='''Utilities''')

    def get_check_bootstrap(self):
        return self.bootstrap_check

    def get_treeview(self):
        return self.Scrolledtreeview1

    def get_all_agent_text(self):
        return self.all_agent_text

    def get_my_ip_text(self):
        return self.my_ip_text

    def get_bootstrap_entry(self):
        return self.boostrap_entry

    def get_start_btn(self):
        return self.start_btn

    def get_info_text(self):
        return self.info_text

    def get_btn_file(self):
        return self.btn_file

    def get_delete_btn(self):
        return self.delete_btn

    def get_btn_connect(self):
        return self.btn_connect


# The following code is added to facilitate the Scrolled widgets you specified.
class AutoScroll(object):
    '''Configure the scrollbars for a widget.'''

    def __init__(self, master):
        #  Rozen. Added the try-except clauses so that this class
        #  could be used for scrolled entry widget for which vertical
        #  scrolling is not supported. 5/7/14.
        try:
            vsb = ttk.Scrollbar(master, orient='vertical', command=self.yview)
        except:
            pass
        hsb = ttk.Scrollbar(master, orient='horizontal', command=self.xview)
        try:
            self.configure(yscrollcommand=self._autoscroll(vsb))
        except:
            pass
        self.configure(xscrollcommand=self._autoscroll(hsb))
        self.grid(column=0, row=0, sticky='nsew')
        try:
            vsb.grid(column=1, row=0, sticky='ns')
        except:
            pass
        hsb.grid(column=0, row=1, sticky='ew')
        master.grid_columnconfigure(0, weight=1)
        master.grid_rowconfigure(0, weight=1)
        # Copy geometry methods of master  (taken from ScrolledText.py)
        if py3:
            methods = tk.Pack.__dict__.keys() | tk.Grid.__dict__.keys() \
                      | tk.Place.__dict__.keys()
        else:
            methods = tk.Pack.__dict__.keys() + tk.Grid.__dict__.keys() \
                      + tk.Place.__dict__.keys()
        for meth in methods:
            if meth[0] != '_' and meth not in ('config', 'configure'):
                setattr(self, meth, getattr(master, meth))

    @staticmethod
    def _autoscroll(sbar):
        '''Hide and show scrollbar as needed.'''

        def wrapped(first, last):
            first, last = float(first), float(last)
            if first <= 0 and last >= 1:
                sbar.grid_remove()
            else:
                sbar.grid()
            sbar.set(first, last)

        return wrapped

    def __str__(self):
        return str(self.master)


def _create_container(func):
    '''Creates a ttk Frame with a given master, and use this new frame to
    place the scrollbars and the widget.'''

    def wrapped(cls, master, **kw):
        container = ttk.Frame(master)
        container.bind('<Enter>', lambda e: _bound_to_mousewheel(e, container))
        container.bind('<Leave>', lambda e: _unbound_to_mousewheel(e, container))
        return func(cls, container, **kw)

    return wrapped


class ScrolledTreeView(AutoScroll, ttk.Treeview):
    '''A standard ttk Treeview widget with scrollbars that will
    automatically show/hide as needed.'''

    @_create_container
    def __init__(self, master, **kw):
        ttk.Treeview.__init__(self, master, **kw)
        AutoScroll.__init__(self, master)


import platform


def _bound_to_mousewheel(event, widget):
    child = widget.winfo_children()[0]
    if platform.system() == 'Windows' or platform.system() == 'Darwin':
        child.bind_all('<MouseWheel>', lambda e: _on_mousewheel(e, child))
        child.bind_all('<Shift-MouseWheel>', lambda e: _on_shiftmouse(e, child))
    else:
        child.bind_all('<Button-4>', lambda e: _on_mousewheel(e, child))
        child.bind_all('<Button-5>', lambda e: _on_mousewheel(e, child))
        child.bind_all('<Shift-Button-4>', lambda e: _on_shiftmouse(e, child))
        child.bind_all('<Shift-Button-5>', lambda e: _on_shiftmouse(e, child))


def _unbound_to_mousewheel(event, widget):
    if platform.system() == 'Windows' or platform.system() == 'Darwin':
        widget.unbind_all('<MouseWheel>')
        widget.unbind_all('<Shift-MouseWheel>')
    else:
        widget.unbind_all('<Button-4>')
        widget.unbind_all('<Button-5>')
        widget.unbind_all('<Shift-Button-4>')
        widget.unbind_all('<Shift-Button-5>')


def _on_mousewheel(event, widget):
    if platform.system() == 'Windows':
        widget.yview_scroll(-1 * int(event.delta / 120), 'units')
    elif platform.system() == 'Darwin':
        widget.yview_scroll(-1 * int(event.delta), 'units')
    else:
        if event.num == 4:
            widget.yview_scroll(-1, 'units')
        elif event.num == 5:
            widget.yview_scroll(1, 'units')


def _on_shiftmouse(event, widget):
    if platform.system() == 'Windows':
        widget.xview_scroll(-1 * int(event.delta / 120), 'units')
    elif platform.system() == 'Darwin':
        widget.xview_scroll(-1 * int(event.delta), 'units')
    else:
        if event.num == 4:
            widget.xview_scroll(-1, 'units')
        elif event.num == 5:
            widget.xview_scroll(1, 'units')


if __name__ == '__main__':
    vp_start_gui()
