import math
import time
import tkinter as tk
from threading import Thread
from tkinter import messagebox, ttk
from tkinter.filedialog import askopenfilename
from tkinter.scrolledtext import ScrolledText
from tkinter.ttk import Style

import matplotlib.backends.backend_tkagg as tkagg
from matplotlib import pyplot as plt

from GUI import Notebooks, FeedbackWidgets
from GUI.Notebooks import MyFrame
from Logic import AppBoot, PcapLogic

# tabs globals
ad_new_tab_flag = False

# size globals
MAX_X = 1200
MAX_Y = 700


class GuiLogic(tk.Frame):
    def __init__(self, main_window):
        tk.Frame.__init__(self, width=MAX_X, height=MAX_Y)
        self.path = ""
        self.main_window = main_window
        self.selected = tk.IntVar()
        self.vars = []
        self.btns = []

        self.main_frame = CreateMainFrame(self.main_window)
        self.ab = AppBoot.AppBoot(self.main_frame.message_label_middle)
        self.initial_program()

        # Notebooks
        self.notebook_plots = Notebooks.MyNotebook(self.main_frame.right_frame)
        self.notebook_settings = Notebooks.MyNotebook(self.main_frame.right_frame)

    def initial_program(self):
        # set functionalities to buttons
        self.main_frame.load_pcap_btn.configure(
            command=lambda: self.open_file(".pcapng", self.ab.dest_port))
        self.main_frame.plots_radio.configure(value=1, variable=self.selected, command=self.show_selected_size,
                                              state='disabled')
        self.main_frame.settings_btn.configure(command=self.settings_button, state='disabled')

        self.selected.set(-1)

    def open_file(self, extension, dest_port):

        self.selected.set(-1)
        title = "Please choose " + extension + " file to work with"
        self.path = askopenfilename(filetypes=[("Custom Files:", extension)], title=title)
        if not self.path:
            print(f"Error opening file {self.path}")
            return
        extension = self.path.split('.')[1]

        # clear graphs and notebooks data
        self.notebook_plots = self.notebook_plots.destroy()
        self.notebook_plots = Notebooks.MyNotebook(self.main_frame.right_frame)

        def insert_to_gui_thread():
            self.after_idle(self.select_plots)

        def check_pcap(callback):
            while not PcapLogic.stop_pcap_bool:
                time.sleep(3)
            callback()

        if extension == "pcapng" or extension == "pcap":
            t = PcapLogic.AsyncPcap2Bin(self.path, dest_port, self.main_frame.message_label_middle)
            FeedbackWidgets.AsyncPcap2Bin(self.main_frame.message_label_middle).start()

            thread = Thread(target=check_pcap, args=(insert_to_gui_thread,))
            thread.start()
            t.start()

        else:
            messagebox.showerror(message="Please choode pcap files or bin files")
            return

    def show_selected_size(self):
        if self.selected.get() == 1:
            self.select_plots()

    def select_plots(self):
        global ad_new_tab_flag

        style = Style()
        style.theme_use('clam')

        self.selected.set(1)
        self.notebook_settings.grid_remove()

        if self.notebook_plots.counter == 0:
            data = PcapLogic.deciphered_bin_df
            stay_names = AppBoot.sites_dict.get('sites').split(':')

            # show columns of stay_names
            remove = data.drop(columns=data.columns.difference(other=stay_names), axis=1, inplace=False)
            length = math.ceil(len(stay_names) / 20)  # round up

            for i in range(0, length):
                frame = MyFrame(self.notebook_plots)

                self.notebook_plots.tabs.append(frame)
                self.notebook_plots.add(frame, text=i)

                fig, ax = plt.subplots()
                canvas = tkagg.FigureCanvasTkAgg(fig, master=frame)
                canvas.get_tk_widget().grid(row=0, column=0, sticky="nswe")
                canvas.get_tk_widget().grid_columnconfigure(0, weight=1)
                toolbar = tkagg.NavigationToolbar2Tk(canvas, frame, pack_toolbar=False)
                toolbar.update()
                toolbar.grid(row=1, column=0)
                y = remove.iloc[:1].values[0]
                plt.barh(remove.columns.values[20 * i:20 * i + 20], y[20 * i:20 * i + 20])

                self.notebook_plots.counter += 1

        self.main_frame.create_plot_btn["state"] = "normal"
        self.main_frame.plots_radio['state'] = 'normal'
        self.main_frame.settings_btn['state'] = 'normal'
        self.notebook_plots.grid(row=0, column=0, sticky="nswe")
        ad_new_tab_flag = False

    def settings_button(self):
        self.selected.set(-1)
        self.notebook_plots.grid_remove()

        if self.notebook_settings.counter == 0:
            self.create_sites_tab()  # tab[0]
            self.create_settings_tab()  # tab[1]
        self.notebook_settings.grid(row=0, column=0, sticky="nswe")

    def create_sites_tab(self):
        frame = MyFrame(self.notebook_settings)
        frame.grid(row=0, column=0, sticky="nswe")

        self.notebook_settings.tabs.append(frame)
        self.notebook_settings.add(frame, text='Sites')
        self.notebook_settings.counter += 1

        self.insert_sites_names(frame)

    def insert_sites_names(self, parent):
        for child in parent.winfo_children():
            child.destroy()

        s = Style()
        s.theme_use('clam')
        s.configure('Custom.TCheckbutton', background="white", font=("Helvetica", 15))
        s.configure('Custom.TFrame', background="white")
        s.configure('Yellow.TButton', background="yellow")
        s.configure('Green.TButton', background="green", activebackground="green")

        scrolled_text = ScrolledText(parent, width=20, height=10)
        scrolled_text.grid(row=0, column=0, sticky="nwse")

        sites = AppBoot.sites_dict.get('sites').split(':')

        btn = ttk.Checkbutton
        i = 0
        for site in PcapLogic.deciphered_bin_df.columns:
            # create widgets
            self.btns.append(btn := ttk.Checkbutton(scrolled_text, text=site, style="Custom.TCheckbutton"))
            if site in sites:
                btn.state(['selected'])

            btn.configure(command=lambda b=btn, site_name=site: self.update_select_plots(site_name, b.state()))

            btn.grid(row=i, column=0, sticky="w")
            scrolled_text.window_create('end', window=btn)
            scrolled_text.insert('end', '\n')
            i += 1

        self.notebook_settings.update()

    def update_select_plots(self, site_name, btn_state):
        AppBoot.add_new_param_to_ini(site_name, btn_state)
        self.notebook_plots = self.notebook_plots.destroy()
        self.notebook_plots = Notebooks.MyNotebook(self.main_frame.right_frame)

    def create_settings_tab(self):
        self.notebook_settings.tabs.append(frame := tk.Frame(self.notebook_settings, bg='white'))  # tab[1]
        self.notebook_settings.add(frame, text='SETTINGS')
        self.notebook_settings.counter += 1

        style = ttk.Style()
        style.theme_use("clam")
        style.configure('Settings.TLabel', background='white')
        font = ("Helvetica", 12)
        style.configure("Settings.TLabel", foreground="black", font=('Helvetica normal', 10), background="white")
        ttk.Label(frame, style='Settings.TLabel', text='Destination IP = ', font=font).grid(row=0, column=0,
                                                                                            sticky="e")
        ttk.Label(frame, style='Settings.TLabel', text='Destination Port = ', font=font).grid(row=1, column=0,
                                                                                              sticky="e")
        width = 100
        port_entry = ttk.Entry(frame, width=width)
        port_entry.grid(row=0, column=1)
        port_entry.insert(0, self.ab.dest_port)


class CreateMainFrame:
    """
    |---------------------------|
    |           Top Level       |
    |---------------------------|
    |----border--|--------------|
    |----files---|              |
    |            |     Right    |
    |            |              |
    |------------|              |
    |----buttons-|              |
    |            |              |
    |            |              |
    |------------|              |
    |----/border-|--------------|
    """

    def __init__(self, parent):
        self.parent = parent

        # photos
        # self.image_smting = Image.open('smting.png')
        # self.image_smting.thumbnail((150, 150))
        # self.image_smting = ImageTk.PhotoImage(self.image_smting)

        # frames
        self.left_frame = tk.Frame(self.parent, bg="#d8d8d8", pady=15)
        self.right_frame = tk.Frame(self.parent, bg="white")
        self.message_frame = tk.Frame(self.parent, bg="#e6e6e6")

        # buttons
        style = Style()
        style.theme_use('clam')
        style.configure('Custom.TRadiobutton', background="#d8d8d8")
        self.load_pcap_btn = ttk.Button(self.left_frame, text="Load Pcap", width=10)
        self.plots_radio = ttk.Radiobutton(self.left_frame, text='Plots\t', width=10)
        self.settings_btn = ttk.Button(self.left_frame, text='Settings', width=10)
        self.create_plot_btn = ttk.Button(self.left_frame, text='Create Plot', width=10)

        self.message_label_left = tk.Label(self.message_frame, bg="#e6e6e6", fg="green", text="", padx=10)
        self.message_label_middle = tk.Label(self.message_frame, bg="#e6e6e6", fg="green", text="",
                                             font='Arial 15 bold')
        self.message_label_right = tk.Label(self.message_frame, bg="#e6e6e6", fg="green", text="")

        self.create_main_frame()

    def create_main_frame(self):
        self.parent.grid_columnconfigure(0, weight=1)
        self.parent.grid_columnconfigure(1, weight=1)
        self.parent.grid_columnconfigure(2, weight=1)
        self.parent.grid_rowconfigure(2, weight=10)

        self.left_frame.grid(row=2, rowspan=2, column=0, sticky="nsew")
        self.left_frame.columnconfigure(0, weight=1)

        self.right_frame.grid(row=2, column=1, columnspan=2, sticky="nswe")
        self.right_frame.grid_columnconfigure(0, weight=1)
        self.right_frame.grid_rowconfigure(0, weight=1)

        self.message_frame.grid(row=1, column=0, columnspan=3, sticky='ewn')
        self.message_frame.rowconfigure(0, weight=1)
        self.message_frame.columnconfigure(0, weight=1)
        self.message_frame.columnconfigure(1, weight=1)
        self.message_frame.columnconfigure(2, weight=1)

        self.message_label_left.grid(row=0, column=0, sticky='ew')
        self.message_label_middle.grid(row=0, column=1, sticky="ew")
        self.message_label_right.grid(row=0, column=2, sticky='ew')

        tk.Label(self.parent, fg="#0061A1", text="Sites Statistics", font='Arial 20 normal') \
            .grid(row=0, column=1, sticky="nswe", padx=350)

        self.load_pcap_btn.grid(row=0, column=0, padx=5, pady=5)
        self.plots_radio.grid(row=1, column=0, padx=5, pady=5)
        self.settings_btn.grid(row=4, column=0, padx=5, pady=5)
        self.create_plot_btn.grid(row=3, column=0, padx=5, pady=5)
