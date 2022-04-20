from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mb
import sys
#import os
import globalVariables as gv
import utilities as ut
import create_menu as cm
import database_config as dc

class Tab3(Frame):
    def __init__(self,parent,controller):
        Frame.__init__(self,parent,controller)
        self.controller = controller
        self.frame = parent
        self.widgets = []
        self.mode = ""

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
        self.origMsg = StringVar()
        self.replyMsg = StringVar()
        self.loadedFileD1 = ""
        self.loadedFileT1 = ""
        self.loadedFileD2 = ""
        self.loadedFileT2 = ""
        self.loadedFlag = False
        self.colWidth = 20
         
        self.whichFormUsedExt = gv.whichForm
        self.readDataFlag = gv.readDataFlag
        self.readConfFlag = gv.readConfFlag

 ## Keep track of widgets added to frame
        self.widgets = []

        ## Frame data dictionaries
        ## Read, but not written to
        self.origFieldsText = gv.ics213FieldsText
        self.origFieldKeys = gv.origIcs213FieldKeys
        ## Able to update
        self.ics213FormData = gv.ics213FormData
        #self.respIcs213FormData = gv.respIcs213FormData
        self.origMsg = ""
        self.result = None
        self.rDate = self.rTime = ""

        #### Load up the configuration data
        dc.get_configuration_from_db()
        
        self.commonConfData = gv.commonConfData
        rDate, rTime = ut.dateAndTime(self.commonConfData["fdate"],self.commonConfData["ftime"],self.commonConfData["fUTC"])

        ## Also need to update Date and Time before setting up GUI
        #self.respIcs213FormData["d2"] = self.ics213FormData["d2"] = self.ics213FormData["d1"] = rDate
        #respIcs213FormData["t2"] = ics213FormData["t2"] = ics213FormData["t1"] = rTime
        self.ics213FormData["d2"] = self.ics213FormData["d1"] = rDate
        self.ics213FormData["t2"] = self.ics213FormData["t1"] = rTime

        self.fileDropDown = StringVar()

        #### callback functions for Combobox()
        def selectFileOption(event):
            selAction = self.chooseFile.get()
            if selAction == "Save File":
                saveData()
                self.chooseFile.set('')
            elif selAction == "Load File":
                loadData()
                self.chooseFile.set('')
            elif selAction == "Clear Form":
                clearData()
                self.chooseFile.set('')
            elif selAction == "Update":
                updateData()
                self.chooseFile.set('')


        ## ICS-213 Mode Switch - Originator vs Reply
        ##
        ## For any supported forms, widgets[] is used to keep track of widgets added to the form.
        ## When changing the displayed page, widgets[] is used to destroy stored widget references
        ## there by clearing the display for the next display.
        ## Before destroying the widgets, any data is transferred to the form data dictionary
        ##
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
        self.chooseFile['values'] = ["Save File","Load File", "Clear Form", "Update"]
        self.chooseFile.grid(column=3, row=0, sticky="w", padx=80)
        ## NOTE: callbacks must be declared before building the combobox widget
        ## If you change any of the 'values' list entries, you must also fix the
        ## callbacks
        self.chooseFile.bind('<<ComboboxSelected>>', selectFileOption)

        ## Quit Button
        self.quitButton = Button(self.frame, text="Quit", command=lambda:self.quitProgram())
        self.widgets.append(self.quitButton)
        self.quitButton.grid(column=3,row=0, sticky="e")
        self.quitButton.configure(bg="blue", fg="white")

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
            self.origDateEntry.insert(0,"Date: "+ics213FormData["d1"])

        ## Time Box
        self.origTimeEntry =Entry(self.frame, text=self.entryTime1, bg="#d8f8d8", width=18)
        self.widgets.append(self.origTimeEntry)
        self.origTimeEntry.grid(column=3, row=incRow, sticky="e")
        self.origTimeEntry.delete(0,END)
        ## Need to distinguish between a blank form and a loaded form
        if self.loadedFlag:
            self.origTimeEntry.insert(0,"Time: "+self.loadedFileT1) 
        else:
            self.origTimeEntry.insert(0,"Time: "+ics213FormData["t1"])
        

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
        self.origEntryFromPos.insert(0,ics213FormData["p2"])

        subjRow = 4
        ## Subject Line
        self.origLabelSubj=Label(self.frame, text=self.origFieldsText["sb"], anchor= 'w')
        self.widgets.append(self.origLabelSubj)
        self.origLabelSubj.grid(column=0, row=subjRow, sticky = 'w')

        self.origEntrySubj = Entry(self.frame, textvariable=self.entrySubj, width=normText, bg="#f8f8d8")
        self.widgets.append(self.origEntrySubj)
        self.origEntrySubj.grid(column=1, row=subjRow, sticky='w')
        self.origEntrySubj.delete(0,END)
        self.origEntrySubj.insert(0,ics213FormData["sb"])

        msgRow = 5
        ## Message area
        ## The Text widget allows for multi-line input and must be handled differently
        ## Text entered into this widget must use *.get() & *.set()
        self.origLabelMsg=Label(self.frame, text=self.origFieldsText["mg"], anchor = 'w')
        self.widgets.append(self.origLabelMsg)
        self.origLabelMsg.grid(column=0, row=msgRow, sticky = 'w')

        self.origEntryMsg=Text(self.frame)
        self.widgets.append(self.origEntryMsg)
        self.origEntryMsg.grid(column=1, row=msgRow)
        self.origEntryMsg.grid_configure(columnspan=3)
        self.origEntryMsg.configure(background="green1", wrap='word')
        self.origEntryMsg.delete(1.0,"end")
        self.origEntryMsg.insert(END,ics213FormData["mg"])
        ## update the global
        self.origMsg.set(ics213FormData["mg"])

        appRow = 7
        ## Approver
        self.origLabelApprove=Label(self.frame, text=self.origFieldsText["s1"], anchor= 'w')
        self.widgets.append(self.origLabelApprove)
        self.origLabelApprove.grid(column=0, row=appRow, sticky= 'w')

        self.origEntryApprove = Entry(self.frame, textvariable=self.entryApprover, width=normText, bg="#c8c8f8")
        self.widgets.append(self.origEntryApprove)
        self.origEntryApprove.grid(column=1, row=appRow, sticky= 'w')
        self.origEntryApprove.delete(0,END)
        self.origEntryApprove.insert(0,ics213FormData["s1"])

        ## Appr. Pos
        self.origLabelApprPos=Label(self.frame, text=self.origFieldsText["p3"])
        self.widgets.append(self.origLabelApprPos)  
        self.origLabelApprPos.grid(column=2, row=appRow, stick ='e')

        self.origEntryApprPos = Entry(self.frame, textvariable=self.entryApprPos, width=normText2, bg="#c8c8f8")
        self.widgets.append(self.origEntryApprPos)
        self.origEntryApprPos.grid(column=3, row=appRow, sticky = 'w')
        self.origEntryApprPos.delete(0,END)
        self.origEntryApprPos.insert(0,ics213FormData["p3"])
        ## incase we suddenly switch to a different form, update widget dictionary
        gv.widget_list_dict["Tab3"] = self.widgets

        def saveData():
            ## message type is hard coded to ICS-213
            ## i.e. 'file' is '213'
            for key in gv.totalIcs213Keys:
                if key == "inc":
                    self.ics213FormData[key] = self.entryInc.get()
                elif key == "to":
                    self.ics213FormData[key] = self.entryTo.get()
                elif key == "fm":
                    self.ics213FormData[key] = self.entryFrom.get()
                elif key == "p1":
                    self.ics213FormData[key] = self.entryToPos.get()
                elif key == "p2":
                    self.ics213FormData[key] = self.entryFromPos.get()
                elif key == "sb":
                    self.ics213FormData[key] = self.entrySubj.get()
                elif key == "mg":
                    self.ics213FormData[key] = self.origMsg.get()
                elif key == "s1":
                    self.ics213FormData[key] = self.entryApprover.get()
                elif key == "p3":
                    self.ics213FormData[key] = self.entryApprPos.get()
                elif key == "d1":
                    if self.entryDate1.get()[:6] == "Date: ":
                        self.ics213FormData[key] = self.entryDate1.get()[6:]
                    else:
                        self.ics213FormData[key] = self.entryDate1.get()
                elif key == "t1":
                    if self.entryTime1.get()[:6] == "Time: ":
                        self.ics213FormData[key] = self.entryTime1.get()[6:]
                    else:
                        self.ics213FormData[key] = self.entryTime1.get()
                ## for info of responder, transfer read data to secondary dictionary
                elif key == "rp":
                    self.ics213FormData[key] = self.replyMsg.get()
                elif key == "s2":
                    self.ics213FormData[key] = self.entryName.get()
                elif key == "p4":
                    self.ics213FormData[key] = self.entryNamePos.get()
                elif key == "d2":
                    self.ics213FormData[key] = self.rplyDateData.get()
                elif key == "t2":
                    self.ics213FormData[key] = self.rplyTimeData.get()
                elif key == "file":
                    ## must be accounted for. Will be needed when calling HTML template
                    self.ics213FormData[key] = "213"

            fileData = [("ICS-213 Forms","*.213")]
            funcParam = (gv.msgPath,fileData,self.ics213FormData,gv.totalIcs213Keys)
            ut.saveFormData(funcParam)
            mb.showinfo("Save","ICS-213 Form data was saved")

        def loadData():
            fileData = [("ICS-213 Forms","*.213")]
            funcParam = (gv.msgPath,fileData)
            result = ut.loadFormData(funcParam)
            ## result will be a None object if command was cancelled
            if result is not None:
                self.ics213FormData = result
                #print("ics213FormData is: ",ics213FormData)
                # Set the flag indicating that a file was loaded
                # Flag will be reset when the form is cleared
                self.loadedFlag = True
                for key in gv.totalIcs213Keys:
                    if key == "inc":
                        self.entryInc.set(self.ics213FormData[key])
                    elif key == "to":
                        self.entryTo.set(self.ics213FormData[key])
                    elif key == "fm":
                        self.entryFrom.set(self.ics213FormData[key])
                    elif key == "p1":
                        self.entryToPos.set(self.ics213FormData[key])
                    elif key == "p2":
                        self.entryFromPos.set(self.ics213FormData[key])
                    elif key == "sb":
                        self.entrySubj.set(self.ics213FormData[key])
                    elif key == "mg":
                        self.origMsg.set(self.ics213FormData[key])
                        self.origEntryMsg.delete(1.0,"end")
                        self.origEntryMsg.insert(END,self.ics213FormData["mg"])
                    elif key == "s1":
                        self.entryApprover.set(self.ics213FormData[key])
                    elif key == "p3":
                        self.entryApprPos.set(self.ics213FormData[key])
                    elif key == "d1":
                        self.loadedFileD1 = self.ics213FormData[key]
                        self.entryDate1.set("Date: "+self.ics213FormData[key])
                    elif key == "t1":
                        self.loadedFileT1 = self.ics213FormData[key]
                        self.entryTime1.set("Time: "+self.ics213FormData[key])
                    elif key == "rp":
                        self.replyMsg.set(self.ics213FormData[key])
                    elif key == "s2":
                        self.entryName.set(self.ics213FormData[key])
                    elif key == "p4":
                        self.entryNamePos.set(self.ics213FormData[key])
                    elif key == "d2":
                        self.loadedFileD2 = self.ics213FormData[key]
                        self.rplyDateData.set("Date: "+self.ics213FormData[key])
                    elif key == "t2":
                        self.loadedFileT2 = self.ics213FormData[key]
                        self.rplyTimeData.set("Time: "+self.ics213FormData[key])
                    elif key == "file":
                        ## must be accounted for. Will be needed when calling HTML template
                        self.tempFile = self.ics213FormData[key]


                mb.showinfo("Load Command","ICS-213 Form data was loaded")
            else:
                ## must have cancelled the 'load' command
                pass

        def clearData():
            for key in gv.totalIcs213Keys:
                if key == "inc":
                    ics213FormData[key] = ""
                    self.entryInc.set(ics213FormData[key])
                elif key == "to":
                    ics213FormData[key] = ""
                    self.entryTo.set(ics213FormData[key])
                elif key == "fm":
                    ics213FormData[key] = ""
                    self.entryFrom.set(ics213FormData[key])
                elif key == "p1":
                    ics213FormData[key] = ""
                    self.entryToPos.set(ics213FormData[key])
                elif key == "p2":
                    ics213FormData[key] = ""
                    self.entryFromPos.set(ics213FormData[key])
                elif key == "sb":
                    ics213FormData[key] = ""
                    self.entrySubj.set(ics213FormData[key])
                elif key == "mg":
                    ics213FormData[key] = ""
                    self.origEntryMsg.delete("1.0","end")
                    self.origMsg.set(ics213FormData[key])
                elif key == "s1":
                    ics213FormData[key] = ""
                    self.entryApprover.set(ics213FormData[key])
                elif key == "p3":
                    ics213FormData[key] = ""
                    self.entryApprPos.set(ics213FormData[key])
                elif key == "d1":
                    ics213FormData[key] = ""
                    self.loadedFileD1 = ics213FormData[key]
                    self.entryDate1.set(ics213FormData[key])
                elif key == "t1":
                    ics213FormData[key] = ""
                    self.loadedFileT1 = ics213FormData[key]
                    self.entryTime1.set(ics213FormData[key])
                ## for info of responder, transfer read data to secondary dictionary
                elif key == "rp":
                    ics213FormData[key] = ""
                    respIcs213FormData[key] = ics213FormData[key]
                    self.replyMsg.set(ics213FormData[key])
                elif key == "s2":
                    ics213FormData[key] = ""
                    self.entryName.set(ics213FormData[key])
                    respIcs213FormData[key] = ics213FormData[key]
                elif key == "p4":
                    ics213FormData[key] = ""
                    self.entryNamePos.set(ics213FormData[key])
                    respIcs213FormData[key] = ics213FormData[key]
                elif key == "d2":
                    ics213FormData[key] = ""
                    self.loadedFileD2 = ics213FormData[key]
                    respIcs213FormData[key] = ics213FormData[key]
                elif key == "t2":
                    ics213FormData[key] = ""
                    self.loadedFileT2 = ics213FormData[key]
                    respIcs213FormData[key] = ics213FormData[key]
                elif key == "file":
                    ## must be accounted for. Will be needed when calling HTML template
                    respIcs213FormData[key] = ics213FormData[key] = "213"
            self.loadedFlag = False
            ## get the current date & time
            self.localGetDateTimeData(self.origDateEntry,self.origTimeEntry)
            ## set all date & time variables to the same date and time (current)
            respIcs213FormData["d2"] = self.ics213FormData["d2"] = ics213FormData["d1"] = self.ics213FormData["d1"]
            respIcs213FormData["t2"] = self.ics213FormData["t2"] = ics213FormData["t1"] = self.ics213FormData["t1"]

        def updateData():
            for key in gv.totalIcs213Keys:
                if key == "inc":
                    ics213FormData[key] = self.entryInc.get()
                elif key == "to":
                    ics213FormData[key] = self.entryTo.get()
                elif key == "fm":
                    ics213FormData[key] = self.entryFrom.get()
                elif key == "p1":
                    ics213FormData[key] = self.entryToPos.get()
                elif key == "p2":
                    ics213FormData[key] = self.entryFromPos.get()
                elif key == "sb":
                    ics213FormData[key] = self.entrySubj.get()
                elif key == "mg":
                    ics213FormData[key] = self.origEntryMsg.get(1.0,END)
                    self.origMsg.set(ics213FormData[key])
                elif key == "s1":
                    ics213FormData[key] = self.entryApprover.get()
                elif key == "p3":
                    ics213FormData[key] = self.entryApprPos.get()
                elif key == "d1":
                    if self.entryDate1.get()[:6] == "Date: ":
                        ics213FormData[key] = self.entryDate1.get()[6:]
                    else:
                        ics213FormData[key] = self.entryDate1.get()
                elif key == "t1":
                    if self.entryTime1.get()[:6] == "Time: ":
                        ics213FormData[key] = self.entryTime1.get()[6:]
                    else:
                        ics213FormData[key] = self.entryTime1.get()
                ## for info of responder, transfer read data to secondary dictionary
                elif key == "rp":
                    respIcs213FormData[key] = ics213FormData[key] = self.replyMsg.get()
                elif key == "s2":
                    respIcs213FormData[key] = ics213FormData[key] = self.entryName.get()
                elif key == "p4":
                    respIcs213FormData[key] = ics213FormData[key] = self.entryNamePos.get()
                elif key == "d2":
                    if self.rplyDateData.get()[:6] == "Date: ":
                        respIcs213FormData[key] = ics213FormData[key] = self.rplyDateData.get()[6:]
                    else:
                        respIcs213FormData[key] = ics213FormData[key] = self.rplyDateData.get()
                elif key == "t2":
                    if self.rplyTimeData.get()[:6] == "Time: ":
                        respIcs213FormData[key] = ics213FormData[key] = self.rplyTimeData.get()[6:]
                    else:
                        respIcs213FormData[key] = ics213FormData[key] = self.rplyTimeData.get()
                elif key =="file":
                    ## must be accounted for. Will be needed when calling HTML template
                    respIcs213FormData[key] = ics213FormData[key] = "213"

            fileData = [("ICS-213 Forms","*.213")]
            funcParam = (gv.msgPath,fileData,ics213FormData,gv.totalIcs213Keys)
            ut.saveFormData(funcParam)
            mb.showinfo("Save","ICS-213 Form data was saved")

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
        dateEn.insert(0,"Date: "+ics213FormData["d1"])
        ## update the text in the time entry box
        timeEn.delete(0,END)
        self.ics213FormData["t1"]=rTime
        timeEn.insert(0,"Time: "+ics213FormData["t1"])
        

    ## Referenced by subframes. Do not remove
    def quitProgram():
        self.controller.shutting_down()