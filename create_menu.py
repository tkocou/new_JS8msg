import tkinter as tk
from tkinter.ttk import *

def make_menu(self, display_frame):
    
    self.menubar = tk.Menu(display_frame)
        
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