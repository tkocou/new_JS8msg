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
from tkinter import ttk, messagebox
from threading import *
import create_main_gui as cg




class App(tk.Frame):
    ## event was moved here to create a class variable
    ## which can be referenced by other classes
    event = Event()
    ## Other class variables
    search_strings = []
    bgsearch_strings = []
    current_profile_id = 0
    widget_list = []
    
    def __init__(self,parent):
        super().__init__(parent)
        self.sock = get_socket()
        self.receiver = None
        self.db_conn = ut.get_db_connection()
        self.frame = parent

        ## older GUI uses Notebook style of GUI
        ## switching to menu driven GUI
    
        self.title("JS8msg Version 2")
        self.geometry('800x600')
        self.resizable(width=False,height=False)
        self.menubar = Menu(self)
        
        ## File menu
        self.filemenu = Menu(self.menubar, tearoff=0)
        self.filemenu.add_separator()
        self.filemenu.add_command(label='JS8msg Communication', command = lambda: switch_frame(Tab1))
        self.filename.add_command(label='Config', command = lambda: switch_frame(Tab2))
        self.filename.add_command(label='ICS-213', command = lambda: switch_frame(Tab3))
        self.filename.add_command(label='JS8 Net', command = lambda: switch_frame(Tab4))
        self.filename.add_separator()
        self.filename.add_command(label='Exit', command = self.shutting_down)
        
        ## Help menu
        self.helpmenu = Menu(self.menubar, tearoff=0)
        self.helpmenu.add_command(label='About',command = self.about)
        
        self.menubar.add_cascade(label='File', menu = self.filemenu)
        self.menubar.add_cascade(label='Help', menu = self.helpmenu)
        
        ## initialize GUI to first frame
        self.switch_frame(Tab1)
        




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
        self.db_conn.close()
        ## do a proper shutdown of threaded receivers
        self.stop_receiving()
        ## destroy all existing widgets and then exit tkinter mainloop
        self.destroy()
        
    def switch_frame(self,frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.grid()






def main():
    root = tk.Tk()
    app = App(parent = root)
    app.protocol("WM_DELETE_WINDOW",app.shutting_down)
    app.mainloop()
    
if __name__ == '__main__':
    main()