# PYTHON:   version 3.6.0
# AUTHOR:   Annie M Bowman
# PURPOSE:  GUI widgets module for Tkinter Phonebook Tech Academy DRILL
# OS:       Windows 10

from tkinter import *
import tkinter as tk

import phonebook_main
import phonebook_func


def load_gui(self):
    #Labels:
    self.lbl_fname = tk.Label(self.master, text='First Name:')
    self.lbl_fname.grid(row=0,column=0, padx=(27,0),pady=(15,0), sticky='nw')
    self.lbl_fname.config(background='black', foreground='#ff006a',
                          font=('Palatino', 14, 'bold'))
    self.lbl_lname = tk.Label(self.master, text='Last Name:')
    self.lbl_lname.grid(row=2,column=0, padx=(27,0),pady=(15,0), sticky='nw')
    self.lbl_lname.config(background='black', foreground='#ff006a',
                          font=('Palatino', 14, 'bold'))
    self.lbl_phone = tk.Label(self.master, text='Phone Number:')
    self.lbl_phone.grid(row=4,column=0, padx=(27,0),pady=(15,0), sticky='nw')
    self.lbl_phone.config(background='black', foreground='#ff006a',
                          font=('Palatino', 14, 'bold'))
    self.lbl_email = tk.Label(self.master, text='Email Address:')
    self.lbl_email.grid(row=6,column=0, padx=(27,0),pady=(15,0), sticky='nw')
    self.lbl_email.config(background='black', foreground='#ff006a',
                          font=('Palatino', 14, 'bold'))
    self.lbl_entries = tk.Label(self.master, text='Current Entries:')
    self.lbl_entries.grid(row=0,column=2, padx=(0,0),pady=(15,0), sticky='nw')
    self.lbl_entries.config(background='black', foreground='#ff006a',
                         font=('Palatino', 14, 'bold'))


    #Entry fields:
    self.ent_fname = tk.Entry(self.master, text='')
    self.ent_fname.grid(row=1,column=0,columnspan=2,padx=(30,40), sticky='nwe')
    self.ent_lname = tk.Entry(self.master, text='')
    self.ent_lname.grid(row=3,column=0,columnspan=2,padx=(30,40), sticky='nwe')
    self.ent_phone = tk.Entry(self.master, text='')
    self.ent_phone.grid(row=5,column=0,columnspan=2,padx=(30,40), sticky='nwe')
    self.ent_email = tk.Entry(self.master, text='')
    self.ent_email.grid(row=7,column=0,columnspan=2,padx=(30,40), sticky='nwe')


    #Listbox & Scrollbar:
    self.scroll = Scrollbar(self.master, orient=VERTICAL)
    self.list = Listbox(self.master, exportselection=0,
                        yscrollcommand=self.scroll.set)
    self.list.bind('<<ListboxSelect>>',
                   lambda event: phonebook_func.onSelect(self,event))
    self.scroll.config(command=self.list.yview)
    self.scroll.grid(row=1,column=5, rowspan=7, sticky='nse')
    self.list.grid(row=1,column=2, rowspan=7,columnspan=3, sticky='nswe')


    #Buttons:
    self.btn_add = tk.Button(self.master,
                          width=12,height=2, text='ADD',
                          command=lambda: phonebook_func.addToList(self))
    self.btn_add.grid(row=8,column=0, padx=(40,0),pady=(25,10), sticky='w')
    self.btn_add.config(background='#ff006a', foreground='white',
                        font=('Palatino', 12, 'bold'))
    self.btn_update = tk.Button(self.master,
                          width=12,height=2, text='UPDATE',
                          command=lambda: phonebook_func.onUpdate(self))
    self.btn_update.grid(row=8,column=1, padx=(15,0),pady=(25,10), sticky='w')
    self.btn_update.config(background='#ff006a', foreground='white',
                           font=('Palatino', 12, 'bold'))
    self.btn_delete = tk.Button(self.master,
                          width=12,height=2, text='DELETE',
                          command=lambda: phonebook_func.onDelete(self))
    self.btn_delete.grid(row=8,column=2, padx=(15,0),pady=(25,10), sticky='w')
    self.btn_delete.config(background='#ff006a', foreground='white',
                           font=('Palatino', 12, 'bold'))
    self.btn_close = tk.Button(self.master,
                          width=12,height=2, text='CLOSE',
                          command=lambda: phonebook_func.ask_quit(self))
    self.btn_close.grid(row=8,column=4, padx=(15,0),pady=(25,10), sticky='e')
    self.btn_close.config(background='#ff006a', foreground='white',
                          font=('Palatino', 12, 'bold'))


    #call functions:
    phonebook_func.create_db(self)
    phonebook_func.onRefresh(self)



if __name__ == "__main__":
    pass
