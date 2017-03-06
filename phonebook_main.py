# PYTHON:   version 3.6.0
#
# AUTHOR:   Annie M. Bowman
#
# PURPOSE:  Python Phonebook Tutorial DRILL 
#           by Daniel A. Christie @ Tech Academy
#
# OS TEST:  Written and tested on Windows 10

from tkinter import *
import tkinter as tk #so I don't have to type out tkinter every time

#importing other modules (separated to keep code compartmentalized)
import phonebook_gui
import phonebook_func

#ParentWindow class will inherit from Tkinter Frame class!
class ParentWindow(Frame):
    def __init__(self, master, *args, **kwargs): #* & ** allow extra args!
        #call base class constructor
        Frame.__init__(self, master, *args, **kwargs) 

        #master frame config:
        self.master = master
        self.master.minsize(615,345) #W, H in px
        self.master.maxsize(615,345)
        self.master.title('Tkinter Phonebook DRILL')
        self.master.configure(bg='black') #background color

        #call center_window method (to center app on user's screen)
        phonebook_func.center_window(self,615,345)

        #use protocol method on upper corner 'X' and call function to ask
        #if user really wants to close the window
        self.master.protocol('WM_DELETE_WINDOW',
                             lambda: phonebook_func.ask_quit(self))

        #load GUI widgets
        phonebook_gui.load_gui(self)


if __name__ == "__main__":
    root = tk.Tk()
    App = ParentWindow(root)
    root.mainloop()
