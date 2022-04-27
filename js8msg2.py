#!/usr/bin/python3
##
## JS8msg Version 2 is a copyrighted program written by Thomas Kocourek, N4FWD
## This program is released under the GPL v3 license
## 
## Main program

import DBHandler as dbh 
import socket
import sys
import threaded_listening as tl
import tkinter as tk
from tkinter.ttk import *
from tkinter import messagebox
from threading import *
import js8setup as js
import classTab1 as T1
import classTab2 as T2
import classTab3 as T3
import classTab4 as T4
import globalVariables as gv
import create_menu as cm
import database_functions as df 
import utilities as ut

class App(tk.Frame):
    ## event was moved here to create a class variable
    ## which can be referenced by other classes
    event = Event()
    ## Other class variables
    search_strings = []
    bgsearch_strings = []
    current_profile_id = 0
    #self.widget_list_dict = {"Tab1":[],"Tab2":[],"Tab3":[],"Tab4":[]}
    
    def __init__(self,master):
        super().__init__(master)
        master.protocol("WM_DELETE_WINDOW",self.shutting_down)
        ## get_socket will return either a socket or 'None'
        ## this info will help with situations where JS8call
        ## is not running
        self.sock = df.get_socket()
        self.receiver = None
        self.db_conn = df.get_db_connection()
        self.frame = master
        
        ## set up a display frame for program GUIes
        self.container = tk.Frame(master, height="600", width="800" )
        self.container.grid()
        ## create dictionary with frames references
        self.frames = {}
        for F in (T1.Tab1,T2.Tab2,T3.Tab3,T4.Tab4):
            page_name = F.__name__
            self.frames[page_name] = F
            

        ## older GUI uses Notebook style of GUI
        ## switching to menu driven GUI
    
        self.frame.title("JS8msg Version 2")
        self.frame.geometry('800x600')
        self.frame.resizable(width=False,height=False)
        ## create the GUI menu
        cm.make_menu(self,self.container)
        ## assign the default function to be displayed
        self.current_screen = "Tab1"
        self.show_frame(self.current_screen)


######################


    def about(self):
        info = "JS8msg Version 2 \n\n"
        info += "Open Source GNU3 License\n\n"
        info += "written by Thomas Kocourek, N4FWD\n\n"
        info += "Parts were borrowed with permission\n\n"
        info += "from js8spotter written by\n\n"
        info += "Joseph D Lyman, KF7MIX\n\n"
        info += "All copyrights are reserved."
        messagebox.showinfo("About JS8msg",info)
                
    def start_receiver(self):
        self.receiver = tl.TCP_rx(self.sock)
        self.receiver.start()
        
    def stop_receiver(self):
        self.receiver.stop()
        self.receiver.join()
        self.receiver = None
        
    def mainloop(self,*args):
        ## inherit properties from tk.mainloop()
        super().mainloop(*args)
        ## if a threaded receiver is still running, kill it
        if self.receiver:
            self.receiver.stop()
        
    def shutting_down(self):
        ## db_conn is assigned in __init__()
        ## close the database connection
        self.db_conn.close_SQL()
        try:
            ## do a proper shutdown of threaded receivers
            self.stop_receiver()
        ## if threaded receiver was not running, ignore error
        except:
            pass
        ## kill existing process
        sys.exit()

    def show_frame(self,page_name):
        #print(page_name)
        ## is the current GUI screen empty? i.e. never created before
        if gv.widget_list_dict[self.current_screen] == []:
            ## create a new GUI container
            frame = self.frames[page_name](parent=self.container,controller=self)
        ## if the current GUI has been created already.....
        elif gv.widget_list_dict[self.current_screen] != []:
            ## clear the screen
            ut.clearWidgetForm(gv.widget_list_dict[self.current_screen])
            ## clear the list in the dictionary
            gv.widget_list_dict[self.current_screen] = []
            ## create a new GUI
            frame = self.frames[page_name](parent=self.container,controller=self)
        ## the widget dictionary will be updated by the new GUI
        frame.tkraise()
        ## assign new GUI to current_screen
        self.current_screen = page_name




def main():
    js.setup()
    root = tk.Tk()
    app = App(master = root)
    app.mainloop()
    
if __name__ == '__main__':
    main()