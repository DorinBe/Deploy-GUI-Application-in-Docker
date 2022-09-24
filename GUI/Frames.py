from tkinter import ttk
from tkinter.ttk import Style


class MainFrame(ttk.Frame):

    def __init__(self, container):
        super().__init__(container)
        self.grid(row=0, column=0)
        container.grid_columnconfigure(0, weight=1)

        s = Style()
        s.configure('Custom.TLabel', foreground="green")
        self.label = ttk.Label(self, style='Custom.TLabel', text="PyGames", font=('Arial', 20))
        self.label.grid(row=0, column=0)
