import tkinter
from tkinter import ttk

def create_gui(frame):
    frm = frame
    frm.geometry('900x600')
    frm.title("JS8msg Version 2")
    frm.resizable(width=False,height=False)
    
    ## Menus
    menubar = Menu()
    filemenu = Menu(menubar, tearoff = 0)
    activitymenu = Menu(menubar, tearoff = 0)
    profilemenu = Menu(menubar, tearoff = 0)
    #viewmenu = Menu(menubar, tearoff = 0)
    helpmenu = Menu(menubar, tearoff = 0)
    
    ## Sub-menus
    filemenu.add_cascade(label = 'Switch Profile', menu = profilemenu)
    filemenu.add_separator()
    filename.add_command(label = 'New Profile', command = menu_new)
    filename.add_command(label = 'Edit Profile', command = menu_edit)
    
    