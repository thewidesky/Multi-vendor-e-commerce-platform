from tkinter import (Tk, Label, PhotoImage, Entry, Button, Frame)
import tkinter as tk

class Vendor(tk.Frame):

    def __init__(self, parent):
        
        tk.Frame.__init__(self, parent)

        frame1 = Frame(self)
        frame2 = Frame(self)

        frame1.grid(row=0, column=0, sticky='nsew')
        frame2.grid(row=0, column=1, sticky='nsew')

        frame1.configure(bg='#000000')
        frame2.configure(bg='#FFFFFF')

        self.grid_columnconfigure(0, weight=1, uniform='group1')
        self.grid_columnconfigure(1, weight=1, uniform='group1')
        self.grid_rowconfigure(0, weight=1)
        