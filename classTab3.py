from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mb
import globalVariables as gv
import utilities as ut
import database_config as dc
import ics213_utilities as ics

## Note: the main difference between classes Tab3
## and Tab4 is the focus of the GUI on the respective
## portions of the ICS-213 form.
## Tab 3 focuses on the Originator
## Tab 4 focuses on the Responder

class Tab3(Frame):
    def __init__(self,parent,controller):
        Frame.__init__(self,parent,controller)
        self.controller = controller
        self.frame = parent
        self.widgets = []

        ## Global StringVar used in both subFrames
        self.entryInc = StringVar()
        self.entryTo = StringVar()
        self.entryToPos = StringVar()
        self.entryFrom = StringVar()
        self.entryFromPos = StringVar()
        self.entrySubj = StringVar()
        self.entryDate1 = StringVar()
        self.entryTime1 = StringVar()
        self.entryApprover = StringVar()
        self.entryApprPos = StringVar()
        self.entryName = StringVar()
        self.entryNamePos = StringVar()
        self.rplyDateData = StringVar()
        self.rplyTimeData = StringVar()
        ## next 2 variables needed for save function
        self.origMsg = StringVar()
        self.replyMsg = StringVar()
        self.loadedFileD1 = ""
        self.loadedFileT1 = ""
        self.loadedFileD2 = ""
        self.loadedFileT2 = ""
        self.loadedFlag = False
        self.colWidth = 20
         

        ## Keep track of widgets added to frame
        self.widgets = []

        ## Frame data dictionaries
        ## Read, but not written to
        self.origFieldsText = gv.ics213FieldsText
        self.origFieldKeys = gv.origIcs213FieldKeys
        ## Able to update
        self.ics213FormData = gv.ics213FormData
        #self.origMsg = ""
        self.result = None
        self.rDate = self.rTime = ""

        #### Load up the configuration data
        dc.get_configuration_from_db()
        self.commonConfData = gv.commonConfData
        
        if not self.loadedFlag:
            rDate, rTime = ut.dateAndTime(self.commonConfData["fdate"],self.commonConfData["ftime"],self.commonConfData["fUTC"])
            ## A new or cleared form. Assign the date and time to both
            self.ics213FormData["d2"] = self.ics213FormData["d1"] = rDate
            self.ics213FormData["t2"] = self.ics213FormData["t1"] = rTime
            
        self.fileDropDown = StringVar()

        #### callback functions for Combobox()
        def selectFileOption(event):
            selAction = self.chooseFile.get()
            if selAction == "Save File":
                self.origMsg.set(self.origTextMsg.get(1.0,"end"))
                ics.saveData(self)
                self.chooseFile.set('')
            elif selAction == "Load File":
                ut.clearWidgetForm(self.widgets)
                ics.loadData(self)
                self.origTextMsg.insert(1.0,self.ics213FormData["mg"])
                self.chooseFile.set('')
            elif selAction == "Clear Form":
                ics.clearData(self)
                self.chooseFile.set('')
            #elif selAction == "Update":
            #    ics.updateData(self)
            #    self.chooseFile.set('')


        ## Display the current mode
        self.label = Label(self.frame, text="Originator", bg="#d8f8d8")
        self.widgets.append(self.label)
        self.label.grid(column=0,row = 0, sticky="w")

        ## Get the current date and time
        self.getDtButton = Button(self.frame, text="Get Date & Time", command=lambda:self.localGetDateTimeData(self.origDateEntry,self.origTimeEntry))
        self.widgets.append(self.getDtButton)
        self.getDtButton.grid(column=1,row = 0, sticky="e")

        ## combobox for 'file actions'
        self.comboLabel = Label(self.frame,text = "Select =-> ")
        self.widgets.append(self.comboLabel)
        self.comboLabel.grid(column=3, row=0, sticky="w")
        self.chooseFile = ttk.Combobox(self.frame, width=self.colWidth, textvariable=self.fileDropDown)
        self.widgets.append(self.chooseFile)
        #self.chooseFile['values'] = ["Save File","Load File", "Clear Form", "Update"]
        self.chooseFile['values'] = ["Save File","Load File", "Clear Form"]
        self.chooseFile.grid(column=3, row=0, sticky="w", padx=80)
        ## NOTE: callbacks must be declared before building the combobox widget
        ## If you change any of the 'values' list entries, you must also fix the
        ## callbacks
        self.chooseFile.bind('<<ComboboxSelected>>', selectFileOption)

        ## Quit Button
        #self.quitButton = Button(self.frame, text="Quit", command=lambda:self.quitProgram())
        #self.widgets.append(self.quitButton)
        #self.quitButton.grid(column=3,row=0, sticky="e")
        #self.quitButton.configure(bg="blue", fg="white")

        #### Text sizing variables
        normText = 42
        normText2 = 30

        incRow = 1
        ## Incident
        self.origLabelInc=Label(self.frame, text=self.origFieldsText["inc"], anchor='w')
        self.widgets.append(self.origLabelInc)
        self.origLabelInc.grid(column=0, row=incRow, sticky = 'w')

        self.origEntryInc = Entry(self.frame, textvariable=self.entryInc, width=normText, bg="#d8f8f8")
        self.widgets.append(self.origEntryInc)
        self.origEntryInc.grid(column=1, row=incRow, sticky='w')
        self.origEntryInc.delete(0,END)
        self.origEntryInc.insert(0,self.ics213FormData["inc"])

        ## Date Box
        self.origDateEntry =Entry(self.frame, text=self.entryDate1, bg="#d8f8d8", width=18)
        self.widgets.append(self.origDateEntry)
        self.origDateEntry.grid(column=3, row=incRow, sticky="w")
        self.origDateEntry.delete(0,END)
        ## Need to distinguish between a blank form and a loaded form
        if self.loadedFlag:
            self.origDateEntry.insert(0,"Date: "+self.loadedFileD1) 
        else:
            self.origDateEntry.insert(0,"Date: "+self.ics213FormData["d1"])

        ## Time Box
        self.origTimeEntry =Entry(self.frame, text=self.entryTime1, bg="#d8f8d8", width=18)
        self.widgets.append(self.origTimeEntry)
        self.origTimeEntry.grid(column=3, row=incRow, sticky="e")
        self.origTimeEntry.delete(0,END)
        ## Need to distinguish between a blank form and a loaded form
        if self.loadedFlag:
            self.origTimeEntry.insert(0,"Time: "+self.loadedFileT1) 
        else:
            self.origTimeEntry.insert(0,"Time: "+self.ics213FormData["t1"])
        

        toRow = 2
        ## To 
        self.origLabelTo=Label(self.frame, text=self.origFieldsText["to"], anchor= 'w')
        self.widgets.append(self.origLabelTo)
        self.origLabelTo.grid(column=0, row=toRow, sticky = 'w')

        self.origEntryTo = Entry(self.frame, textvariable=self.entryTo, width=normText, bg="#f8f8d8")
        self.widgets.append(self.origEntryTo)
        self.origEntryTo.grid(column=1, row=toRow, sticky= 'w')
        self.origEntryTo.delete(0,END)
        self.origEntryTo.insert(0,self.ics213FormData["to"])

        ## Position of 'to'
        self.origLabelToPos=Label(self.frame, text=self.origFieldsText["p1"])
        self.widgets.append(self.origLabelToPos)
        self.origLabelToPos.grid(column=2, row=toRow, stick ='e')

        self.origEntryToPos = Entry(self.frame, textvariable=self.entryToPos, width=normText, bg="#f8f8d8")
        self.widgets.append(self.origEntryToPos)
        self.origEntryToPos.grid(column=3, row=toRow, sticky = 'w')
        self.origEntryToPos.delete(0,END)
        self.origEntryToPos.insert(0,self.ics213FormData["p1"])

        fromRow = 3
        ##  From 
        self.origLabelFrom=Label(self.frame, text=self.origFieldsText["fm"], anchor= 'w')
        self.widgets.append(self.origLabelFrom)
        self.origLabelFrom.grid(column=0, row=fromRow, sticky= 'w')

        self.origEntryFrom = Entry(self.frame, textvariable=self.entryFrom, width=normText, bg="#d8f8f8")
        self.widgets.append(self.origEntryFrom)
        self.origEntryFrom.grid(column=1, row=fromRow, sticky= 'w')
        self.origEntryFrom.delete(0,END)
        self.origEntryFrom.insert(0,self.ics213FormData["fm"])

        ## Position of 'from'
        self.origLabelFromPos=Label(self.frame, text=self.origFieldsText["p2"])
        self.widgets.append(self.origLabelFromPos)
        self.origLabelFromPos.grid(column=2, row=fromRow, sticky ='e')

        self.origEntryFromPos = Entry(self.frame, textvariable=self.entryFromPos, width=normText, bg="#d8f8f8")
        self.widgets.append(self.origEntryFromPos)
        self.origEntryFromPos.grid(column=3, row=fromRow, sticky = 'w')
        self.origEntryFromPos.delete(0,END)
        self.origEntryFromPos.insert(0,self.ics213FormData["p2"])

        subjRow = 4
        ## Subject Line
        self.origLabelSubj=Label(self.frame, text=self.origFieldsText["sb"], anchor= 'w')
        self.widgets.append(self.origLabelSubj)
        self.origLabelSubj.grid(column=0, row=subjRow, sticky = 'w')

        self.origEntrySubj = Entry(self.frame, textvariable=self.entrySubj, width=normText, bg="#f8f8d8")
        self.widgets.append(self.origEntrySubj)
        self.origEntrySubj.grid(column=1, row=subjRow, sticky='w')
        self.origEntrySubj.delete(0,END)
        self.origEntrySubj.insert(0,self.ics213FormData["sb"])

        msgRow = 5
        ## Message area
        ## The Text widget allows for multi-line input and must be handled differently
        ## Text entered into this widget must use *.get() & *.set()
        self.origLabelMsg=Label(self.frame, text=self.origFieldsText["mg"], anchor = 'w')
        self.widgets.append(self.origLabelMsg)
        self.origLabelMsg.grid(column=0, row=msgRow, sticky = 'w')

        #print("StrVar is: ",self.origMsg.get())
        #print("Dict is: ",self.ics213FormData["mg"])
        #print("Flag is: ",self.loadedFlag)

        self.origTextMsg=Text(self.frame)
        self.widgets.append(self.origTextMsg)
        self.origTextMsg.grid(column=1, row=msgRow)
        self.origTextMsg.grid_configure(columnspan=3)
        self.origTextMsg.configure(background="green1", wrap='word')
        self.origTextMsg.delete(1.0,"end")
        if self.loadedFlag:
            self.origTextMsg.insert(END,self.origMsg.get())
            self.ics213FormData["mg"] = self.origMsg.get()
        else:
            self.origTextMsg.insert(END,self.ics213FormData["mg"])
        ## needed for save function
            self.origMsg.set(self.ics213FormData["mg"])

        appRow = 7
        ## Approver
        self.origLabelApprove=Label(self.frame, text=self.origFieldsText["s1"], anchor= 'w')
        self.widgets.append(self.origLabelApprove)
        self.origLabelApprove.grid(column=0, row=appRow, sticky= 'w')

        self.origEntryApprove = Entry(self.frame, textvariable=self.entryApprover, width=normText, bg="#c8c8f8")
        self.widgets.append(self.origEntryApprove)
        self.origEntryApprove.grid(column=1, row=appRow, sticky= 'w')
        self.origEntryApprove.delete(0,END)
        self.origEntryApprove.insert(0,self.ics213FormData["s1"])

        ## Appr. Pos
        self.origLabelApprPos=Label(self.frame, text=self.origFieldsText["p3"])
        self.widgets.append(self.origLabelApprPos)  
        self.origLabelApprPos.grid(column=2, row=appRow, stick ='e')

        self.origEntryApprPos = Entry(self.frame, textvariable=self.entryApprPos, width=normText2, bg="#c8c8f8")
        self.widgets.append(self.origEntryApprPos)
        self.origEntryApprPos.grid(column=3, row=appRow, sticky = 'w')
        self.origEntryApprPos.delete(0,END)
        self.origEntryApprPos.insert(0,self.ics213FormData["p3"])
        ## incase we suddenly switch to a different form, update widget dictionary
        gv.widget_list_dict["Tab3"] = self.widgets


    def localGetDateTimeData(self, dateEn, timeEn):
        ## dateEn is the widget reference for the date Entry() display
        ## timeEn is the widget reference for the time Entry() display
        ## The config format data is loaded upfront
        rDate = ""
        rTime = ""
        rDate, rTime = ut.dateAndTime(self.commonConfData["fdate"],self.commonConfData["ftime"],self.commonConfData["fUTC"])
        ## update the text in the date entry box
        dateEn.delete(0,END)
        self.ics213FormData["d1"]=rDate
        dateEn.insert(0,"Date: "+rDate)
        ## update the text in the time entry box
        timeEn.delete(0,END)
        self.ics213FormData["t1"]=rTime
        timeEn.insert(0,"Time: "+rTime)
        
    def quitProgram(self):
        self.controller.shutting_down()