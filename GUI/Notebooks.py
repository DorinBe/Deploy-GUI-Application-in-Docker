from tkinter import ttk

from GUI.ScrollableNotebook import ScrollableNotebook


class MyNotebook(ScrollableNotebook):
    def __init__(self, parent):
        super().__init__(parent)
        self.counter = 0
        self.tabs = []
        self.grid_remove()


class MyFrame(ttk.Frame):

    def __init__(self, master):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_propagate(True)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
