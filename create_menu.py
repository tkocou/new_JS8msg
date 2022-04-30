#!/usr/bin/python3
##
## JS8msg Version 2.1 is a copyrighted program written by Thomas Kocourek, N4FWD
## This program is released under the GPL v3 license
## 
import tkinter as tk
from tkinter.ttk import *

def make_menu(self, display_frame):
    
    self.menubar = tk.Menu(display_frame)
        
    ## File menu
    self.filemenu = tk.Menu(self.menubar, tearoff=0)
    self.filemenu.add_separator()
    self.filemenu.add_command(label='JS8msg Communication', command = lambda: self.show_frame("Tab1"))
    self.filemenu.add_command(label='Config', command = lambda: self.show_frame("Tab2"))
    self.filemenu.add_separator()
    self.sub_menu = tk.Menu(self.filemenu, tearoff=0)
    self.sub_menu.add_command(label='Originator', command = lambda: self.show_frame("Tab3"))
    self.sub_menu.add_command(label='Responder', command = lambda: self.show_frame("Tab4"))
    self.filemenu.add_cascade(label="ICS-213", menu = self.sub_menu)
    self.filemenu.add_separator()
    self.filemenu.add_command(label='Exit', command = self.shutting_down)
        
    ## Help menu
    self.helpmenu = tk.Menu(self.menubar, tearoff=0)
    self.helpmenu.add_command(label='About',command = self.about)
        
    self.menubar.add_cascade(label='File', menu = self.filemenu)
    self.menubar.add_cascade(label='Help', menu = self.helpmenu)
        
    self.frame.config(menu = self.menubar)