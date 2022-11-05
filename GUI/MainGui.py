import math
import time
import tkinter as tk
from threading import Thread
from tkinter import messagebox, ttk
from tkinter.filedialog import askopenfilename
from tkinter.scrolledtext import ScrolledText
from tkinter.ttk import Entry

import matplotlib.backends.backend_tkagg as tkagg
import pyautogui as pg
from matplotlib import pyplot as plt

from GUI import AppWidgets, FeedbackWidgets, MainFrame
from GUI.AppWidgets import MyFrame
from GUI.Styles import MyStyle
from Logic import AppBoot, PcapLogic

import ctypes
import threading

MAX_X, MAX_Y = 1300, 800

# tabs globals
ad_new_tab_flag = False


class StartGUI(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.window = parent
        MyStyle()
        self.window.title(f"PySurfs")  # title of the GUI window
        self.window.iconbitmap("icon2.ico")
        place_center(self.window, width=MAX_X, height=MAX_Y)

        self.path = ""
        self.main_window = self.window
        self.selected = tk.IntVar()
        self.vars = []
        self.btns = [ttk.Checkbutton()]

        self.main_frame = MainFrame.CreateMainFrame(self.main_window)
        self.ab = AppBoot.AppBoot(self.main_frame.message_label_middle)
        self.initial_program()

        # Notebooks
        self.notebook_plots = AppWidgets.MyNotebook(self.main_frame.right_frame)
        self.notebook_settings = AppWidgets.MyNotebook(self.main_frame.right_frame)

    def initial_program(self):
        # set functionalities to buttons
        self.main_frame.load_pcap_btn.configure(
            command=lambda: self.open_file(".pcapng", self.ab.dest_port))
        self.main_frame.stop_decipher_btn.configure(command=self.stop_threads)
        self.main_frame.plots_radio.configure(value=1, variable=self.selected, command=self.show_selected_size,
                                              state='disabled')
        self.main_frame.settings_btn.configure(command=self.settings_button, state='disabled')

        self.selected.set(-1)

    def stop_threads(self):
        print("thread list: ", thread_list := threading.enumerate())
        for thread in thread_list:
            if thread.name != 'MainThread' and 'pydev' not in thread.name:
                ctypes.pythonapi.PyThreadState_SetAsyncExc(thread.ident, ctypes.py_object(SystemExit))
                thread.join()
        PcapLogic.stop_pcap_bool = True
        self.main_frame.message_label_middle.config(text="")
        print(f"thread list after remove: ", threading.enumerate())
        PcapLogic.stop_pcap_bool = False

    def open_file(self, extension, dest_port):

        def insert_to_gui_thread():
            self.after_idle(self.select_plots)

        def check_pcap(callback):
            while not PcapLogic.stop_pcap_bool:
                time.sleep(3)
            callback()

        self.stop_threads()

        self.selected.set(-1)
        title = "Please choose " + extension + " file to work with"
        self.path = askopenfilename(filetypes=[("Custom Files:", extension)], title=title)
        self.main_frame.path_label_middle.configure(text=self.path)
        if not self.path:
            print(f"Error opening file {self.path}")
            return
        extension = self.path.split('.')[1]

        # clear graphs and notebooks data
        self.notebook_plots = self.notebook_plots.destroy()
        self.notebook_plots = AppWidgets.MyNotebook(self.main_frame.right_frame)

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
                plt.barh((remove.columns.values[20 * i:20 * i + 20]), y[20 * i:20 * i + 20], color="#73B8FA",
                         edgecolor="#73B8FA")
                # plt.xticks(np.arange(min(y[20 * i:20 * i + 20]), max(y[20 * i:20 * i + 20])+1, 1.0))
                # plt.grid(color="#EDF6FF")

                self.notebook_plots.counter += 1

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

        parent.grid_rowconfigure(0, weight=1)
        parent.grid_rowconfigure(1, weight=30)

        pick_sites_text = "Choose sites to present on graph:"
        pick_sites_label = ttk.Label(parent, style="Settings.TLabel", text=pick_sites_text, font = ("Helvetica", 12))
        pick_sites_label.grid(row=0, column=0, sticky="w")

        scrolled_text = ScrolledText(parent, width=20, height=10, relief="flat")
        scrolled_text.grid(row=1, column=0, sticky="nwse")

        search_frame = ttk.Frame(parent, style='Custom.TFrame')
        search_frame.grid(row=2, column=0)
        search_label = ttk.Label(search_frame, style="Settings.TLabel", text='Search')
        search_label.grid(row=0, column=1)
        search_entry = Entry(search_frame)
        search_entry.grid(row=1, column=1)

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

        def get(event):
            to_search = search_entry.get()
            if to_search:
                for check_btn in self.btns:
                    if to_search == check_btn.cget("text"):
                        scrolled_text.tag_add('found', check_btn, check_btn)
                        scrolled_text.see(check_btn)
                        check_btn.configure(style='Selected.TCheckbutton')
                        check_btn.state(['selected'])
                    elif to_search in check_btn.cget("text"):
                        scrolled_text.tag_add('found', check_btn, check_btn)
                        scrolled_text.see(check_btn)
                        check_btn.configure(style='Selected.TCheckbutton')
                    else:
                        check_btn.configure(style='Custom.TCheckbutton')

        search_entry.bind("<Return>", get)
        self.notebook_settings.update()

    def update_select_plots(self, site_name, btn_state):
        AppBoot.add_new_param_to_ini(site_name, btn_state)
        self.notebook_plots = self.notebook_plots.destroy()
        self.notebook_plots = AppWidgets.MyNotebook(self.main_frame.right_frame)

    def create_settings_tab(self):
        self.notebook_settings.tabs.append(frame := tk.Frame(self.notebook_settings, bg='white'))  # tab[1]
        self.notebook_settings.add(frame, text='SETTINGS')
        self.notebook_settings.counter += 1

        font = ("Helvetica", 12)
        ttk.Label(frame, style='Settings.TLabel', text='Destination IP = ', font=font).grid(row=0, column=0,
                                                                                            sticky="e")
        ttk.Label(frame, style='Settings.TLabel', text='Destination Port = ', font=font).grid(row=1, column=0,
                                                                                              sticky="e")
        width = 100
        port_entry = ttk.Entry(frame, width=width)
        port_entry.grid(row=0, column=1)
        port_entry.insert(0, self.ab.dest_port)


def place_center(w1, width, height):  # Placing the window in the center of the screen
    reso = pg.size()
    rx = reso[0]
    ry = reso[1]
    x = int((rx / 2) - (MAX_X / 2))
    y = int((ry / 2) - (MAX_Y / 2))
    width_str = str(width)
    height_str = str(height)
    w1.geometry(width_str + "x" + height_str + "+" + str(x) + "+" + str(y))
