from tkinter import ttk
from GUI.Styles import my_style


class MainFrame(ttk.Frame):

    def __init__(self, container):
        super().__init__(container)
        self.grid(row=0, column=0)
        container.grid_columnconfigure(0, weight=1)

        self.label = ttk.Label(self, style='GreenForeground.TLabel', text="PyGames", font=('Arial', 20))
        self.label.grid(row=0, column=0)
