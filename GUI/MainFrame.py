import tkinter as tk
from tkinter import ttk as ttk

from PIL import Image, ImageTk


class CreateMainFrame(ttk.Frame):

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        # photos
        self.image_smting = Image.open('logo2.png')
        self.image_smting.thumbnail((200, 200))
        self.image_smting = ImageTk.PhotoImage(self.image_smting)

        # frames
        self.top_frame = tk.Frame(self.parent)
        self.left_frame = tk.Frame(self.parent, bg="#d8d8d8", pady=15)
        self.right_frame = tk.Frame(self.parent, bg="white")
        self.message_frame = tk.Frame(self.parent, bg="#e6e6e6")

        # buttons
        self.load_pcap_btn = ttk.Button(master=self.left_frame, text="Load Pcap", width=10, style='Blue.TButton')
        self.stop_decipher_btn = ttk.Button(master=self.left_frame,width=3, style='Stop.TButton')
        self.plots_radio = ttk.Radiobutton(self.left_frame, text='Plots\t', width=10, style='Blue.TRadiobutton')
        self.settings_btn = ttk.Button(self.left_frame, text='Settings', width=10, style="Blue.TButton")

        self.message_label_left = tk.Label(self.message_frame, bg="#e6e6e6", fg="green", text="", padx=10)
        self.message_label_middle = tk.Label(self.message_frame, bg="#e6e6e6", fg="green", text="",
                                             font='Arial 15 bold')
        self.message_label_right = tk.Label(self.message_frame, bg="#e6e6e6", fg="green", text="")

        self.create_main_frame()

    def create_main_frame(self):
        self.parent.grid_columnconfigure(1, weight=1)
        self.parent.grid_rowconfigure(2, weight=10)

        self.top_frame.grid(row=0, column=0, columnspan=3, sticky="nswe")
        self.top_frame.grid_columnconfigure(0, weight=1)
        self.top_frame.grid_rowconfigure(0, weight=1)
        # self.top_frame

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

        tk.Label(self.top_frame, fg="#0061A1", image=self.image_smting).grid(row=0, column=0)

        self.load_pcap_btn.grid(row=0, column=0, padx=5, pady=5)
        self.stop_decipher_btn.grid(row=0, column=1)
        self.plots_radio.grid(row=1, column=0, padx=5, pady=5)
        self.settings_btn.grid(row=3, column=0, padx=5, pady=5)
