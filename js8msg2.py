#!/usr/bin/python3
##
## JS8msg Version 2 is a copyrighted program written by Thomas Kocourek, N4FWD
## This program is released under the GPL v3 license
## 
## Main program

import DBHandler as dbh 
import socket
import sys
import utilities as ut
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

#widget_list = []


class App(tk.Frame):
    ## event was moved here to create a class variable
    ## which can be referenced by other classes
    event = Event()
    ## Other class variables
    search_strings = []
    bgsearch_strings = []
    current_profile_id = 0
    widget_list_dict = {"Tab1":[],"Tab2":[],"Tab3":[],"Tab4":[]}
    
    def __init__(self,master):
        super().__init__(master)
        master.protocol("WM_DELETE_WINDOW",self.shutting_down)
        ## get_socket will return either a socket or 'None'
        ## this info will help with situations where JS8call
        ## is not running
        self.sock = ut.get_socket()
        self.receiver = None
        self.db_conn = ut.get_db_connection()
        self.frame = master
        
        self.container = tk.Frame(master, height="600", width="800" )
        #self.container = master
        self.container.grid()
        #self.container.config()
        ## create dictionary with frames
        self.frames = {}
        #for F in (T1.Tab1,T2.Tab2,T3.Tab3,T4.Tab4):
        for F in (T1.Tab1,T2.Tab2,T3.Tab3):
            page_name = F.__name__
            self.frames[page_name] = F
            
        #self.show_frame("Tab1")

        ## older GUI uses Notebook style of GUI
        ## switching to menu driven GUI
    
        self.frame.title("JS8msg Version 2")
        self.frame.geometry('800x600')
        self.frame.resizable(width=False,height=False)
        self.menubar = tk.Menu(self.container)
        
        ## File menu
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_separator()
        self.filemenu.add_command(label='JS8msg Communication', command = lambda: self.show_frame("Tab1"))
        self.filemenu.add_command(label='Config', command = lambda: self.show_frame("Tab2"))   
        self.filemenu.add_command(label='ICS-213', command = lambda: self.show_frame("Tab3"))
        #self.filemenu.add_command(label='JS8 Net', command = lambda: self.show_frame("Tab4"))
        self.filemenu.add_separator()
        self.filemenu.add_command(label='Exit', command = self.shutting_down)
        
        ## Help menu
        self.helpmenu = tk.Menu(self.menubar, tearoff=0)
        self.helpmenu.add_command(label='About',command = self.about)
        
        self.menubar.add_cascade(label='File', menu = self.filemenu)
        self.menubar.add_cascade(label='Help', menu = self.helpmenu)
        
        self.frame.config(menu = self.menubar)
        ## initialize screen to JS8msg Communication GUI
        self.current_screen = "Tab1"
        self.show_frame(self.current_screen)





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
        ## destroy all existing widgets and then exit tkinter mainloop
        #self.destroy()
        sys.exit()
        
    #def switch_frame(self,frame_class):
    #    print("frame type: ",type(frame_class))
    #    new_frame = frame_class(self)
    #    if self._frame is not None:
    #        self._frame.destroy()
    #    self._frame = new_frame
    #    self._frame.grid()

    
    
    def show_frame(self,page_name):
        ## is the current GUI screen empty? i.e. never created before
        if widget_list_dict[self.current_screen] == []:
            ## create a new GUI container
            frame = self.frames[page_name](parent=self.container,controller=self)
        ## if the current GUI has been created already.....
        elif widget_list_dict[self.current_screen] != []:
            ## clear the screen
            ut.clearWidgetForm(widget_list_dict[self.current_screen])
            ## clear the list in the dictionary
            widget_list_dict[self.current_screen] = []
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
    #app.Protocol("WM_DELETE_WINDOW",app.shutting_down)
    app.mainloop()
    
if __name__ == '__main__':
    main()