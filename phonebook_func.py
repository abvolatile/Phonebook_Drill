# PYTHON:   version 3.6.0
# AUTHOR:   Annie M Bowman
# PURPOSE:  GUI widgets module for Tkinter Phonebook Tech Academy DRILL
# OS:       Windows 10

import os
from tkinter import *
import tkinter as tk
from tkinter import messagebox
import sqlite3

import phonebook_main
import phonebook_gui


#Function to CENTER app in the user's screen:
def center_window(self, w, h):
    #get user's screen width & height:
    screen_width = self.master.winfo_screenwidth()
    screen_height = self.master.winfo_screenheight()
    #calculate x & y coords for placing app:
    x = int((screen_width/2)-(w/2)) 
    y = int((screen_height/2)-(h/2))
    #use geometry method to place app on the user's screen:
    centerGeo = self.master.geometry('{}x{}+{}+{}'.format(w,h,x,y))
    return centerGeo

#Function to ask user if they really want to quit when clicking
#either the 'X' @ top-right of window OR the 'Close' button:
def ask_quit(self):
    #display a message box asking user if they want to exit, and if TRUE (ok):
    if messagebox.askokcancel('Exit program', 'Are you sure you want to exit?'):
        #close the app:
        self.master.destroy()
        os._exit(0) #this fully deletes any reference to our widgets from the
                    #user's computer (to free up their memory & prevent bugs


# ---------------------- DATABASE FUNCTIONS --------------------------
def create_db(self):
    conn = sqlite3.connect('phonebook.db')
    with conn:
        cur = conn.cursor()
        #create the Phonebook table & setup ID, FirstName, LastName, etc...
        cur.execute('CREATE TABLE IF NOT EXISTS Phonebook( \
                    ID INTEGER PRIMARY KEY AUTOINCREMENT, \
                    FirstName TEXT, \
                    LastName TEXT, \
                    FullName TEXT, \
                    Phone TEXT, \
                    Email TEXT);')
        #MUST commit() to save changes and close the db connection!
        conn.commit()
    conn.close()
    first_run(self)


def first_run(self):
    data = ('John', 'Doe', 'John Doe', '111-111-1111', 'jdoe@email.com')
    conn = sqlite3.connect('phonebook.db')
    with conn:
        cur = conn.cursor()
        cur,count = count_records(cur)
        if count < 1:
            cur.execute('INSERT INTO Phonebook ( \
                        FirstName, LastName, FullName, \
                        Phone, Email) \
                        VALUES (?,?,?,?,?);',
                        (data))
            conn.commit()
    conn.close()

 
def count_records(cur):
    count = ''
    cur.execute('SELECT COUNT(*) FROM Phonebook;')
    count = cur.fetchone()[0]
    return cur,count


#Function that retrieves info when user selects item in the Listbox:
def onSelect(self,event):
    #self.list widget calls the event:
    var_list = event.widget
    select = var_list.curselection()[0]
    value = var_list.get(select)
    conn = sqlite3.connect('phonebook.db')
    with conn:
        cur = conn.cursor()
        cur.execute('SELECT FirstName, LastName, Phone, Email \
                        FROM Phonebook WHERE FullName = (?);', [value])
        body = cur.fetchall() #returns a tuple
        #we can slice the tuple into 4 parts using data[] during the loop
        for data in body:
            #clear each field, then insert value from each index of tuple
            self.ent_fname.delete(0,'end') 
            self.ent_fname.insert(0,data[0])
            self.ent_lname.delete(0,'end')
            self.ent_lname.insert(0,data[1])
            self.ent_phone.delete(0,'end')
            self.ent_phone.insert(0,data[2])
            self.ent_email.delete(0,'end')
            self.ent_email.insert(0,data[3])


def addToList(self):
    #get user entry & use strip method to remove whitespace before/after:
    fname = self.ent_fname.get().strip()
    lname = self.ent_lname.get().strip()
    #make sure first char in each word is capitalized:
    fname.title()
    lname.title()
    fullname = ('{} {}'.format(fname, lname)) #combine normalized names into one
    print('fullname: {}'.format(fullname)) #just for dev purposes
    phone = self.ent_phone.get().strip()
    email = self.ent_email.get().strip()
    if not '@' in email:
        messagebox.showerror('Incorrect Email Format', 'Please make sure to '
                             'enter a valid email address!')
        return
    elif not '.' in email:
        messagebox.showerror('Incorrect Email Format', 'Please make sure to '
                             'enter a valid email address!')
        return
    #make sure user provides ALL information requested:
    elif (len(fname)>0) and (len(lname)>0) and (len(phone)>0) and (len(email)>0):
        conn = sqlite3.connect('phonebook.db')
        with conn:
            cur = conn.cursor()
            #check to see if that fullname is already in the database:
            cur.execute('SELECT COUNT(FullName) FROM Phonebook \
                        WHERE FullName = "{}";'.format(fullname))
            count = cur.fetchone()[0] #get count value @ index 0
            if count == 0:
                #if the fullname doesn't exist yet, insert user input:
                print('count: {}'.format(count)) #just for dev purposes
                cur.execute('INSERT INTO Phonebook(FirstName, LastName, \
                            FullName, Phone, Email) VALUES (?,?,?,?,?);',
                            (fname, lname, fullname, phone, email))
                #add fullname to the Listbox:
                self.list.insert('end', fullname)
                onClear(self) #clear the entry fields
            else: #if the fullname already exists, show error messagebox:
                messagebox.showerror('Name Error', '"{}" already exists in the'
                        ' database!\nPlease enter data for a different'
                        ' name.'.format(fullname))
                onClear(self)
            conn.commit() #DON'T FORGET TO SAVE!
        conn.close() #close connection to database
    else: #if user didn't enter information into ALL fields:
        messagebox.showerror('Missing Data Error', 'Please make sure to'
                                ' enter data into all fields.')


def onDelete(self): #when user clicks the DELETE button
    try:
        select = self.list.get(self.list.curselection()) #get the user selected name
        conn = sqlite3.connect('phonebook.db')
        with conn:
            cur = conn.cursor()
            #make sure they're not trying to delete the only record in the db
            cur.execute('SELECT COUNT(*) FROM Phonebook;')
            count = cur.fetchone()[0]
            if count > 1: #if there's at least 2 records left in database:
                confirm = messagebox.askokcancel('Confirm Delete',
                            'All information associated with "{}"\
                            \nwill be permanently deleted from the database. \
                            \n\nAre you sure you want to continue?'.format(select))
                if confirm: #if they choose OK:
                    #conn = sqlite3.connect('phonebook.db') #don't need this!
                    #with conn: #if conn already open above, 
                        #cur = conn.cursor() #shouldn't need to redefine these.
                    #can just put this under 'if confirm:':
                    cur.execute('DELETE FROM Phonebook \
                                    WHERE FullName = "{}";'.format(select))
                    #call function to clear entry fields AND Listbox index selected
                    onDeleted(self)
                    conn.commit() #SAVE CHANGES!!
                else:
                    onClear(self)
            else: #if the selected name is the only one in the Listbox/database
                confirm = messagebox.showerror('Only Record Error',
                            '"{}" is the only record in the database and'
                            ' cannot be deleted.\n\nPlease add another record'
                            ' before deleting "{}".'.format(select,select))
                onClear(self)
        conn.close()
    except:
        messagebox.showerror('No Record Selected', 'Please select a name from '
                             'the list before deleting')


def onDeleted(self):
    #first clear text in entry fields:
    onClear(self)
    #then delete user selection in Listbox (at that index):
    try:
        index = self.list.curselection()[0]
        self.list.delete(index)
    except IndexError:
        #pass #if this throws an index error, just skip it...
        onRefresh(self)


def onClear(self):
    #clear the text in the entry fields:
    self.ent_fname.delete(0, 'end')
    self.ent_lname.delete(0, 'end')
    self.ent_phone.delete(0, 'end')
    self.ent_email.delete(0, 'end')


def onRefresh(self):
    #repopulate and refresh Listbox items
    self.list.delete(0, 'end')
    conn = sqlite3.connect('phonebook.db')
    with conn:
        cur = conn.cursor()
        cur.execute('SELECT COUNT(*) FROM Phonebook;')
        count = cur.fetchone()[0]
        i = 0
        while i < count:
            cur.execute('SELECT FullName FROM Phonebook;')
            var_list = cur.fetchall()[i]
            for item in var_list:
                self.list.insert('end', str(item)) #shouldn't this be ('end',...)?
                i += 1
    conn.close() #no need to commit, since no change to db...


def onUpdate(self): #when user selects a name from Listbox and clicks update btn
    try:
        select = self.list.curselection()[0] #index of the user selection
        value = self.list.get(select) #value of user's selection
    except: #if nothing selected when user clicks Update button:
        messagebox.showinfo('Missing Selection', 'No name was selected'
                ' from the list.\nCancelling request to update.')
        return #leave the function...
    #user can only update phone/email. Must start over for name changes.
    phone = self.ent_phone.get().strip()
    email = self.ent_email.get().strip()
    if not '@' in email:
        messagebox.showerror('Incorrect Email Format', 'Please make sure to '
                             'enter a valid email address!')
        return
    elif not '.' in email:
        messagebox.showerror('Incorrect Email Format', 'Please make sure to '
                             'enter a valid email address!')
        return
    elif(len(phone)>0) and (len(email)>0): #if entry fields for BOTH phone & email
        conn = sqlite3.connect('phonebook.db')
        with conn:
            cur = conn.cursor()
            cur.execute('SELECT COUNT(Phone) FROM Phonebook \
                        WHERE Phone = "{}";'.format(phone))
            count = cur.fetchone()[0] #get count from phone search
            print(count)
            cur.execute('SELECT COUNT(Email) FROM Phonebook \
                        WHERE Email = "{}";'.format(email))
            count2 = cur.fetchone()[0] #get count from email search
            print(count2)
            if count == 0 or count2 == 0: #if EITHER are not already in db:
                response = messagebox.askokcancel('Update Request',
                        'The following changes will be made for "{}":'
                        '\nNew phone: "{}", new email: "{}".'
                        '\n\nPlease confirm OK!'.format(value, phone, email))
                print(response)
                if response:
                    #with conn: #again - don't need this here if conn is
                        #cur = conn.cursor() #already open...
                    cur.execute('UPDATE Phonebook SET Phone = "{}", \
                            Email = "{}" \
                            WHERE FullName = "{}";'.format(phone,email,value))
                    onClear(self) #call function to clear entry fields
                    conn.commit() #SAVE CHANGES to db!!
                else: #cancel...
                    messagebox.showinfo('Cancel Update',
                            'No changes have been made to "{}"'.format(value))
            else: #if change to email and phone are already same in database:
                messagebox.showinfo('No Changes Detected',
                        'Both "{}" and "{}" \nalready exist in the database ' 
                        'for "{}".\nUpdate request has been cancelled.'.format(
                            phone, email, value))
            onClear(self) #clear entry fields
        conn.close() #close connection to db
    else: #if entry fields do not have info for one or the other (phone, email)
        messagebox.showerror('Missing Information', 'Please select a name from '
                             'the list, \nthen edit the phone or email for that'
                             ' name.')
    onClear(self) #clear entry fields
            



if __name__ == "__main__":
    pass
