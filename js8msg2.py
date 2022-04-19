#!/usr/bin/python3
##
## JS8msg Version 2 is a copyrighted program written by Thomas Kocourek, N4FWD
## This program is released under the GPL v3 license
## 
## Main program

import DBHandler as dbh 
import socket
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




class App(tk.Frame):
    ## event was moved here to create a class variable
    ## which can be referenced by other classes
    event = Event()
    ## Other class variables
    search_strings = []
    bgsearch_strings = []
    current_profile_id = 0
    widget_list = []
    
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
        
        #print("frame type:: ",type(self.frame))
        
        #self.tab1 = T1.Tab1(parent)
        #self.tab2 = T2.Tab2(parent)
        #self.tab3 = T3.Tab3(parent)
        #self.tab4 = T4.Tab4(parent)
        
        container = tk.Frame(self)
        container.grid()
        self.frames = {}
        for frm in (T1.Tab1,T2.Tab2,T3.Tab3,T4.Tab4):
            if frm == T1.Tab1:
                page_name = 'JS8msg Communication'
            elif frm == T2.Tab2:
                page_name = 'Config'
            elif frm == T3.Tab3:
                page_name = 'ICS-213'
            elif frm == T4.Tab4:
                page_name = 'JS8 Net'
            #frame = frm(parent=container,controller=self)
            frame = frm(parent=container)
            self.frames[page_name] = frame
        self.show_frame('JS8msg Communication')

        ## older GUI uses Notebook style of GUI
        ## switching to menu driven GUI
    
        self.frame.title("JS8msg Version 2")
        self.frame.geometry('800x600')
        self.frame.resizable(width=False,height=False)
        self.menubar = tk.Menu(self)
        
        ## File menu
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_separator()
        self.filemenu.add_command(label='JS8msg Communication', command = lambda: switch_frame(self.tab1))
        self.filemenu.add_command(label='Config', command = lambda: switch_frame(self.tab2))
        self.filemenu.add_command(label='ICS-213', command = lambda: switch_frame(self.tab3))
        self.filemenu.add_command(label='JS8 Net', command = lambda: switch_frame(self.tab4))
        self.filemenu.add_separator()
        self.filemenu.add_command(label='Exit', command = self.shutting_down)
        
        ## Help menu
        self.helpmenu = tk.Menu(self.menubar, tearoff=0)
        self.helpmenu.add_command(label='About',command = self.about)
        
        self.menubar.add_cascade(label='File', menu = self.filemenu)
        self.menubar.add_cascade(label='Help', menu = self.helpmenu)
        
        ## initialize GUI to first frame
        #self.switch_frame(self.tab1)
        




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
        ## do a proper shutdown of threaded receivers
        self.stop_receiving()
        ## destroy all existing widgets and then exit tkinter mainloop
        self.destroy()
        
    #def switch_frame(self,frame_class):
    #    print("frame type: ",type(frame_class))
    #    new_frame = frame_class(self)
    #    if self._frame is not None:
    #        self._frame.destroy()
    #    self._frame = new_frame
    #    self._frame.grid()

    def show_frame(self,page_name):
        frame = self.frames[page_name]
        frame.tkraise()




def main():
    js.setup()
    root = tk.Tk()
    app = App(master = root)
    #app.Protocol("WM_DELETE_WINDOW",app.shutting_down)
    app.mainloop()
    
if __name__ == '__main__':
    main()