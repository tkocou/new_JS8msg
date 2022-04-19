import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mb
import sys
import os
import webbrowser as wb
import platform
import globalVariables as gv
import utilities as ut
import js8API as api

#ics309FormData = gv.ics309FieldsData 
commonConfData =gv.commonConfData
whichFormUsedExt = gv.whichForm
readDataFlag = gv.readDataFlag
readConfFlag = gv.readConfFlag


#### ======================= ICS-309 Dual Frame Tab ================================
class Tab4(Frame):
    def __init__(self, parent,controller):
        tk.Frame.__init__(self, parent,controller)
        self.controller = controller
        self.frame = parent
        
        self.entryInc = StringVar()
        self.entryNC_Callsign = StringVar()
        self.entryFromDate = StringVar()
        self.entryFromTime = StringVar()
        self.entryDateTime = StringVar()
        self.entryToTime = StringVar()
        self.entryNetName = StringVar()
        self.entryPrepName = StringVar()
        self.entryPrepDate = StringVar()
        self.entryPrepTime = StringVar()


        ## Set up to call the first frame = Originator    
        self._frame = None
        self.switch_frame(Tab4_Frame1)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.grid()

    def quitProgram(self):
        controller.shutting_down()

# first sub-frame for Tab4
####================ ICS-309 Incident frame ====================

class Tab4_Frame1(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.frame = master
        ## Keep track of widgets added to frame
        self.widgets = []
        ## Init configuration dictionary
        self.commonConfData = gv.commonConfData
        # overall form structure
        #self.ics309FieldsData = gv.ics309FieldsData
        self.entryLogTime = StringVar()
        self.msgCallsignFrom = StringVar()
        self.msgCallsignTo = StringVar()
        self.logMsg = StringVar()


        def clearForm(frame_class):
            #
            ut.clearWidgetForm(self.widgets)
            master.switch_frame(frame_class)

        ## Which sub-frame are we in?
        self.labelFrame = Label(self.frame, text="Inc", bg="#d8f8d8")
        self.widgets.append(self.labelFrame)
        self.labelFrame.grid(column=0,row=0,sticky="w")

        ## Click to swap
        self.buttonFrame = Button(self.frame, text="Go to Logging form", command=lambda: clearForm(Tab4_Frame2))
        self.widgets.append(self.buttonFrame)
        self.buttonFrame.grid(column=1,row=0, sticky="w")


        topRow =0
        ## Quit program button
        self.quitButton = Button(self.frame, text="Quit", command=lambda:master.quitProgram())
        self.widgets.append(self.quitButton)
        self.quitButton.configure(bg="blue", fg="white")
        self.quitButton.grid(column=1,row=topRow, sticky = "e", padx=20)
      

# second sub-frame for Tab4
#### ============================= ICS-309 Logging form ============================
class Tab4_Frame2(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.frame = master
        # Keep track of widgets added to frame
        self.widgets = []
        ## Frame data variables
        self.entryLogTime = StringVar()
        self.msgCallsignFrom = StringVar()
        self.msgCallsignTo = StringVar()
        self.logMsg = StringVar()

        # list of dictionaries, each dictionary equals one log entry of net ops
        self.ics309List = gv.ics309List
        # Dictionary of each log entry
        self.ics309ListDataDict = gv.ics309ListDataDict
        # form dict
        self.ics309FieldsData = gv.ics309FieldsData


        def clearForm(frame_class):
            #
            ut.clearWidgetForm(self.widgets)
            master.switch_frame(frame_class)

        ## Which sub-frame are we in?
        self.labelFrame = Label(self.frame, text="Inc", bg="d8f8d8")
        self.widgets.append(self.labelFrame)
        self.labelFrame.grid(column=0,row=0,sticky="w")

        ## Click to swap
        self.buttonFrame = Button(self.frame, text="Go to Logging form", command=lambda: clearForm(Tab4_Frame1))
        self.widgets.append(self.buttonFrame)
        self.buttonFrame.grid(column=1,row=0, sticky="w")


        topRow =0
        ## Quit program button
        self.quitButton = Button(self.frame, text="Quit", command=lambda:master.quitProgram())
        self.widgets.append(self.quitButton)
        self.quitButton.configure(bg="blue", fg="white")
        self.quitButton.grid(column=1,row=topRow, sticky = "e", padx=20)
      