from tkinter import *
import pyautogui


class Screen():
    def __init__(self):
        self.scr = Tk()
        self.scr.title("SAP MQTT utility")
        self.scr.geometry(str(pyautogui.size()[0]) + "x" + str(pyautogui.size()[1]))

    def start(self):
        scrWindow = Text()
        scrWindow.pack()
        self.scr.mainloop()