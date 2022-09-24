from tkinter.ttk import Style


class MyStyle:

    def __init__(self):
        super().__init__()
        self.my_style = Style()
        self.my_style.theme_use('clam')
        self.my_style.configure('GreenForeground.TLabel', foreground="green")
        self.my_style.configure('Custom.TCheckbutton', background="white", font=("Helvetica", 15))
        self.my_style.configure('Custom.TFrame', background="white")
        self.my_style.configure('Yellow.TButton', background="yellow")
        self.my_style.configure('Green.TButton', background="green", activebackground="green")
        self.my_style.configure('Settings.TLabel', background='white')
        self.my_style.configure("Settings.TLabel", foreground="black", font=('Helvetica normal', 10), background="white")
        self.my_style.configure('Custom.TRadiobutton', background="#d8d8d8")
        self.font_normal = ("Helvetica", 12)
