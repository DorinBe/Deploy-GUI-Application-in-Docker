import tkinter as tk

import pyautogui as pg

from GUI import MyFrames
from GUI.Styles import MyStyle

MAX_X, MAX_Y = 1200, 800


class StartGUI:
    def __init__(self):
        window = tk.Tk()  # create root window
        ms = MyStyle()
        window.title(f"PyGames")  # title of the GUI window
        place_center(window, width=MAX_X, height=MAX_Y)
        MyFrames.GuiLogic(window)
        window.mainloop()


def place_center(w1, width, height):  # Placing the window in the center of the screen
    reso = pg.size()
    rx = reso[0]
    ry = reso[1]
    x = int((rx / 2) - (MAX_X / 2))
    y = int((ry / 2) - (MAX_Y / 2))
    width_str = str(width)
    height_str = str(height)
    w1.geometry(width_str + "x" + height_str + "+" + str(x) + "+" + str(y))
