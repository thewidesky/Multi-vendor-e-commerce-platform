import tkinter as tk
from tkinter import font as tkfont
from GUI.loginscreen import LoginScreen

apptitle = ""

class App(tk.Tk):
    
    def __init__(self):
        tk.Tk.__init__(self)

        self._frame = None
        self.switch_frame(LoginScreen)
        
    
    def switch_frame(self,frame_class):
        """Destory current frame and replace it with a new one"""
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
            print('Destory called')
        self._frame = new_frame
        self._frame.pack()

if __name__ == '__main__':
    app = App()
    app.title = "Multi-vendor-e-commerce-platform"
    app.geometry('500x500')
    app.mainloop()