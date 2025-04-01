from tkinter import (Tk, Label, PhotoImage, Entry, Button, Frame)
import tkinter as tk
from GUI.Surface.VendorManagementFrame import VendorManagementFrame

class LoginScreen(tk.Frame):

    def __init__(self, parent,controller):
        
        super().__init__(parent)
        self.controller = controller

        def login():
            #TO DO
            parent.switch_frame(VendorManagementFrame)

        login_label = Label(self, text='Login', font=(
            'Arial', 30), fg='#00008b', bg='#808080')
        username_label = Label(self, text='Username', font=(
            'Arial', 16), bg='#808080', fg='white')
        username_entry = Entry(self)
        password_label = Label(self, text='password', font=(
            'Arial', 16), bg='#808080', fg='white')
        password_entry = Entry(self, show='*')
        login_button = Button(self, text='Login', bg='#00008b', fg='white', command = login)

        login_label.grid(row=0, column=0, columnspan=2, sticky='news', pady=40)
        username_label.grid(row=1, column=0)
        username_entry.grid(row=1, column=1, pady=20)
        password_label.grid(row=2, column=0)
        password_entry.grid(row=2, column=1, pady=20)
        login_button.grid(row=3, column=0, columnspan=2)
        
        #Fill the whole parent window
        self.pack()

    


