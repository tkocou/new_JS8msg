from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mb
import sys
#import os
import globalVariables as gv
import utilities as ut

ics213FormData = gv.ics213FieldsData 
commonConfData =gv.commonConfData
whichFormUsedExt = gv.whichForm
readDataFlag = gv.readDataFlag
readConfFlag = gv.readConfFlag
respIcs213FormData = gv.respIcs213FormData

## ICS-213 Form =================== (dual frame tab) =======================
class Tab3(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)

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

        ## Set up to call the first frame = Originator    
        self._frame = None
        self.switch_frame(Tab3_Frame1)
 
    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.grid()

    ## Referenced by subframes. Do not remove
    def quitProgram(self):
        sys.exit()
      
####========================= ICS-213 Originator =============================
class Tab3_Frame1(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        ## Keep track of widgets added to frame
        self.widgets = []
        ## Init configuration dictionary
        self.commonConfData = commonConfData

        ## Frame data dictionaries
        self.origFieldsText = gv.ics213FieldsText
        self.origFieldKeys = gv.origIcs213FieldKeys
        self.ics213FormData = ics213FormData
        self.origMsg = ""
        self.result = None
        rDate = rTime = ""

        #### Load up the configuration data
        #### Necessary if a cold start
        if ics213FormData["d1"] == "":
            ## The data in the global form dict is empty
            ## fetch configuration if available
            fileNameList = [("JS8msg.cfg","*.cfg")]
            funcParam = (gv.configPath,fileNameList)
            self.result = ut.loadFormData(funcParam)

            ## ut.loadFormData returned a None object, assign default values
            if self.result is None:
                self.result = {}
                self.result["call"]=""
                self.result["phone"]=""
                self.result["name"]=""
                self.result["addr"]=""
                self.result["c-s-z"]=""
                self.result["email"]=""
                self.result["fdate"]="1"
                self.result["ftime"]="1"
                self.result["fUTC"]="0"

                self.commonConfData = self.result
                rDate, rTime = ut.dateAndTime(self.commonConfData["fdate"],self.commonConfData["ftime"],self.commonConfData["fUTC"])

            else:
                ## ut.loadFormData returned a configuration dict
                self.commonConfData = self.result
                rDate, rTime = ut.dateAndTime(self.commonConfData["fdate"],self.commonConfData["ftime"],self.commonConfData["fUTC"])

        else:
            ## a form was loaded, use the global cfg dict
            self.commonConfData = commonConfData
            rDate, rTime = ut.dateAndTime(self.commonConfData["fdate"],self.commonConfData["ftime"],self.commonConfData["fUTC"])

        ## Also need to update Date and Time before setting up GUI
        respIcs213FormData["d2"] = ics213FormData["d2"] = ics213FormData["d1"] = rDate
        respIcs213FormData["t2"] = ics213FormData["t2"] = ics213FormData["t1"] = rTime

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
        self.label = Label(self, text="Orig", bg="#d8f8d8")
        self.widgets.append(self.label)
        self.label.grid(column=0,row = 0, sticky="w")

        # button object with command to replace the frame
        self.button = Button(self, text="Go to Responder Mode", command=lambda: clearForm(Tab3_Frame2))
        self.widgets.append(self.button)
        self.button.grid(column=1,row = 0, sticky="w")

        ## Get the current date and time
        self.getDtButton = Button(self, text="Get Date & Time", command=lambda:self.localGetDateTimeData(self.origDateEntry,self.origTimeEntry))
        self.widgets.append(self.getDtButton)
        self.getDtButton.grid(column=1,row = 0, sticky="e")

        ## combobox for 'file actions'
        self.comboLabel = Label(self,text = "Select =-> ")
        self.widgets.append(self.comboLabel)
        self.comboLabel.grid(column=3, row=0, sticky="w")
        self.chooseFile = ttk.Combobox(self, width=master.colWidth, textvariable=self.fileDropDown)
        self.widgets.append(self.chooseFile)
        self.chooseFile['values'] = ["Save File","Load File", "Clear Form", "Update"]
        self.chooseFile.grid(column=3, row=0, sticky="w", padx=80)
        ## NOTE: callbacks must be declared before building the combobox widget
        ## If you change any of the 'values' list entries, you must also fix the
        ## callbacks
        self.chooseFile.bind('<<ComboboxSelected>>', selectFileOption)

        ## Quit Button
        self.quitButton = Button(self, text="Quit", command=lambda:master.quitProgram())
        self.widgets.append(self.quitButton)
        self.quitButton.grid(column=3,row=0, sticky="e")
        self.quitButton.configure(bg="blue", fg="white")

        #### Text sizing variables
        normText = 42
        normText2 = 30

        incRow = 1
        ## Incident
        self.origLabelInc=Label(self, text=self.origFieldsText["inc"], anchor='w')
        self.widgets.append(self.origLabelInc)
        self.origLabelInc.grid(column=0, row=incRow, sticky = 'w')

        self.origEntryInc = Entry(self, textvariable=master.entryInc, width=normText, bg="#d8f8f8")
        self.widgets.append(self.origEntryInc)
        self.origEntryInc.grid(column=1, row=incRow, sticky='w')
        self.origEntryInc.delete(0,END)
        self.origEntryInc.insert(0,self.ics213FormData["inc"])

        ## Date Box
        self.origDateEntry =Entry(self, text=master.entryDate1, bg="#d8f8d8", width=18)
        self.widgets.append(self.origDateEntry)
        self.origDateEntry.grid(column=3, row=incRow, sticky="w")
        self.origDateEntry.delete(0,END)
        ## Need to distinguish between a blank form and a loaded form
        if master.loadedFlag:
            self.origDateEntry.insert(0,"Date: "+master.loadedFileD1) 
        else:
            self.origDateEntry.insert(0,"Date: "+ics213FormData["d1"])

        ## Time Box
        self.origTimeEntry =Entry(self, text=master.entryTime1, bg="#d8f8d8", width=18)
        self.widgets.append(self.origTimeEntry)
        self.origTimeEntry.grid(column=3, row=incRow, sticky="e")
        self.origTimeEntry.delete(0,END)
        ## Need to distinguish between a blank form and a loaded form
        if master.loadedFlag:
            self.origTimeEntry.insert(0,"Time: "+master.loadedFileT1) 
        else:
            self.origTimeEntry.insert(0,"Time: "+ics213FormData["t1"])
        

        toRow = 2
        ## To 
        self.origLabelTo=Label(self, text=self.origFieldsText["to"], anchor= 'w')
        self.widgets.append(self.origLabelTo)
        self.origLabelTo.grid(column=0, row=toRow, sticky = 'w')

        self.origEntryTo = Entry(self, textvariable=master.entryTo, width=normText, bg="#f8f8d8")
        self.widgets.append(self.origEntryTo)
        self.origEntryTo.grid(column=1, row=toRow, sticky= 'w')
        self.origEntryTo.delete(0,END)
        self.origEntryTo.insert(0,self.ics213FormData["to"])

        ## Position of 'to'
        self.origLabelToPos=Label(self, text=self.origFieldsText["p1"])
        self.widgets.append(self.origLabelToPos)
        self.origLabelToPos.grid(column=2, row=toRow, stick ='e')

        self.origEntryToPos = Entry(self, textvariable=master.entryToPos, width=normText, bg="#f8f8d8")
        self.widgets.append(self.origEntryToPos)
        self.origEntryToPos.grid(column=3, row=toRow, sticky = 'w')
        self.origEntryToPos.delete(0,END)
        self.origEntryToPos.insert(0,self.ics213FormData["p1"])

        fromRow = 3
        ##  From 
        self.origLabelFrom=Label(self, text=self.origFieldsText["fm"], anchor= 'w')
        self.widgets.append(self.origLabelFrom)
        self.origLabelFrom.grid(column=0, row=fromRow, sticky= 'w')

        self.origEntryFrom = Entry(self, textvariable=master.entryFrom, width=normText, bg="#d8f8f8")
        self.widgets.append(self.origEntryFrom)
        self.origEntryFrom.grid(column=1, row=fromRow, sticky= 'w')
        self.origEntryFrom.delete(0,END)
        self.origEntryFrom.insert(0,self.ics213FormData["fm"])

        ## Position of 'from'
        self.origLabelFromPos=Label(self, text=self.origFieldsText["p2"])
        self.widgets.append(self.origLabelFromPos)
        self.origLabelFromPos.grid(column=2, row=fromRow, sticky ='e')

        self.origEntryFromPos = Entry(self, textvariable=master.entryFromPos, width=normText, bg="#d8f8f8")
        self.widgets.append(self.origEntryFromPos)
        self.origEntryFromPos.grid(column=3, row=fromRow, sticky = 'w')
        self.origEntryFromPos.delete(0,END)
        self.origEntryFromPos.insert(0,ics213FormData["p2"])

        subjRow = 4
        ## Subject Line
        self.origLabelSubj=Label(self, text=self.origFieldsText["sb"], anchor= 'w')
        self.widgets.append(self.origLabelSubj)
        self.origLabelSubj.grid(column=0, row=subjRow, sticky = 'w')

        self.origEntrySubj = Entry(self, textvariable=master.entrySubj, width=normText, bg="#f8f8d8")
        self.widgets.append(self.origEntrySubj)
        self.origEntrySubj.grid(column=1, row=subjRow, sticky='w')
        self.origEntrySubj.delete(0,END)
        self.origEntrySubj.insert(0,ics213FormData["sb"])

        msgRow = 5
        ## Message area
        ## The Text widget allows for multi-line input and must be handled differently
        ## Text entered into this widget must use *.get() & *.set()
        self.origLabelMsg=Label(self, text=self.origFieldsText["mg"], anchor = 'w')
        self.widgets.append(self.origLabelMsg)
        self.origLabelMsg.grid(column=0, row=msgRow, sticky = 'w')

        self.origEntryMsg=Text(self)
        self.widgets.append(self.origEntryMsg)
        self.origEntryMsg.grid(column=1, row=msgRow)
        self.origEntryMsg.grid_configure(columnspan=3)
        self.origEntryMsg.configure(background="green1", wrap='word')
        self.origEntryMsg.delete(1.0,"end")
        self.origEntryMsg.insert(END,ics213FormData["mg"])
        ## update the global
        master.origMsg.set(ics213FormData["mg"])

        appRow = 7
        ## Approver
        self.origLabelApprove=Label(self, text=self.origFieldsText["s1"], anchor= 'w')
        self.widgets.append(self.origLabelApprove)
        self.origLabelApprove.grid(column=0, row=appRow, sticky= 'w')

        self.origEntryApprove = Entry(self, textvariable=master.entryApprover, width=normText, bg="#c8c8f8")
        self.widgets.append(self.origEntryApprove)
        self.origEntryApprove.grid(column=1, row=appRow, sticky= 'w')
        self.origEntryApprove.delete(0,END)
        self.origEntryApprove.insert(0,ics213FormData["s1"])

        ## Appr. Pos
        self.origLabelApprPos=Label(self, text=self.origFieldsText["p3"])
        self.widgets.append(self.origLabelApprPos)  
        self.origLabelApprPos.grid(column=2, row=appRow, stick ='e')

        self.origEntryApprPos = Entry(self, textvariable=master.entryApprPos, width=normText2, bg="#c8c8f8")
        self.widgets.append(self.origEntryApprPos)
        self.origEntryApprPos.grid(column=3, row=appRow, sticky = 'w')
        self.origEntryApprPos.delete(0,END)
        self.origEntryApprPos.insert(0,ics213FormData["p3"])

    ## destroy all widgets which were added to the current frame
    ## Then jump to the switching function
        def clearForm(frame_class):
            ## Starting 'clearForm' function.
            ## Before exiting this screen, let's save any entered data
            ## Assign only the originator data to the global dictionary
            for key in gv.origIcs213FieldKeys:
                if key == "inc":
                    ics213FormData[key] = master.entryInc.get()
                elif key == "to":
                    ics213FormData[key] = master.entryTo.get()
                elif key == "fm":
                    ics213FormData[key] = master.entryFrom.get()
                elif key == "p1":
                    ics213FormData[key] = master.entryToPos.get()
                elif key == "p2":
                    ics213FormData[key] = master.entryFromPos.get()
                elif key == "sb":
                    ics213FormData[key] = master.entrySubj.get()
                elif key == "mg":
                    ics213FormData[key] = master.origMsg.get()
                elif key == "s1":
                    ics213FormData[key] = master.entryApprover.get()
                elif key == "p3":
                     ics213FormData[key] = master.entryApprPos.get()
                elif key == "d1":
                    if master.entryDate1.get()[:6] == "Date: ":
                        ics213FormData[key] = master.entryDate1.get()[6:]
                    else:
                        ics213FormData[key] = master.entryDate1.get()
                elif key == "t1":
                    if master.entryTime1.get()[:6] == "Time: ":
                        ics213FormData[key] = master.entryTime1.get()[6:]
                    else:
                        ics213FormData[key] = master.entryTime1.get()
                
                ## transfer configuration data from local to global
                for key in gv.commonConfKeys:
                    commonConfData[key] = self.commonConfData[key]

                ## erase the widgets
                ut.clearWidgetForm(self.widgets)
                master.switch_frame(frame_class)

        def saveData():
            ## message type is hard coded to ICS-213
            ## i.e. 'file' is '213'
            for key in gv.totalIcs213Keys:
                if key == "inc":
                    ics213FormData[key] = master.entryInc.get()
                elif key == "to":
                    ics213FormData[key] = master.entryTo.get()
                elif key == "fm":
                    ics213FormData[key] = master.entryFrom.get()
                elif key == "p1":
                    ics213FormData[key] = master.entryToPos.get()
                elif key == "p2":
                    ics213FormData[key] = master.entryFromPos.get()
                elif key == "sb":
                    ics213FormData[key] = master.entrySubj.get()
                elif key == "mg":
                    ics213FormData[key] = master.origMsg.get()
                elif key == "s1":
                    ics213FormData[key] = master.entryApprover.get()
                elif key == "p3":
                    ics213FormData[key] = master.entryApprPos.get()
                elif key == "d1":
                    if master.entryDate1.get()[:6] == "Date: ":
                        ics213FormData[key] = master.entryDate1.get()[6:]
                    else:
                        ics213FormData[key] = master.entryDate1.get()
                elif key == "t1":
                    if master.entryTime1.get()[:6] == "Time: ":
                        ics213FormData[key] = master.entryTime1.get()[6:]
                    else:
                        ics213FormData[key] = master.entryTime1.get()
                ## for info of responder, transfer read data to secondary dictionary
                elif key == "rp":
                    respIcs213FormData[key] = ics213FormData[key] = master.replyMsg.get()
                elif key == "s2":
                    respIcs213FormData[key] = ics213FormData[key] = master.entryName.get()
                elif key == "p4":
                    respIcs213FormData[key] = ics213FormData[key] = master.entryNamePos.get()
                elif key == "d2":
                    if master.rplyDateData.get()[:6] == "Date: ":
                        respIcs213FormData[key] = ics213FormData[key] = master.rplyDateData.get()[6:]
                    else:
                        respIcs213FormData[key] = ics213FormData[key] = master.rplyDateData.get()
                elif key == "t2":
                    if master.rplyTimeData.get()[:6] == "Time: ":
                        respIcs213FormData[key] = ics213FormData[key] = master.rplyTimeData.get()[6:]
                    else:
                        respIcs213FormData[key] = ics213FormData[key] = master.rplyTimeData.get()
                elif key == "file":
                    ## must be accounted for. Will be needed when calling HTML template
                    respIcs213FormData[key] = ics213FormData[key] = "213"

            fileData = [("ICS-213 Forms","*.213")]
            funcParam = (gv.msgPath,fileData,ics213FormData,gv.totalIcs213Keys)
            ut.saveFormData(funcParam)
            mb.showinfo("Save","ICS-213 Form data was saved")

        def loadData():
            fileData = [("ICS-213 Forms","*.213")]
            funcParam = (gv.msgPath,fileData)
            result = ut.loadFormData(funcParam)
            ## result will be a None object if command was cancelled
            if result is not None:
                ics213FormData = result
                #print("ics213FormData is: ",ics213FormData)
                # Set the flag indicating that a file was loaded
                # Flag will be reset when the form is cleared
                master.loadedFlag = True
                for key in gv.totalIcs213Keys:
                    if key == "inc":
                        master.entryInc.set(ics213FormData[key])
                    elif key == "to":
                        master.entryTo.set(ics213FormData[key])
                    elif key == "fm":
                        master.entryFrom.set(ics213FormData[key])
                    elif key == "p1":
                        master.entryToPos.set(ics213FormData[key])
                    elif key == "p2":
                        master.entryFromPos.set(ics213FormData[key])
                    elif key == "sb":
                        master.entrySubj.set(ics213FormData[key])
                    elif key == "mg":
                        master.origMsg.set(ics213FormData[key])
                        self.origEntryMsg.delete(1.0,"end")
                        self.origEntryMsg.insert(END,ics213FormData["mg"])
                    elif key == "s1":
                        master.entryApprover.set(ics213FormData[key])
                    elif key == "p3":
                        master.entryApprPos.set(ics213FormData[key])
                    elif key == "d1":
                        master.loadedFileD1 = ics213FormData[key]
                        master.entryDate1.set("Date: "+ics213FormData[key])
                    elif key == "t1":
                        master.loadedFileT1 = ics213FormData[key]
                        master.entryTime1.set("Time: "+ics213FormData[key])
                    ## for info of responder, transfer read data to secondary dictionary
                    elif key == "rp":
                        respIcs213FormData[key] = ics213FormData[key]
                        master.replyMsg.set(ics213FormData[key])
                        #print("resp load data: ",key,":",respIcs213FormData[key])
                    elif key == "s2":
                        #print(key,ics213FormData[key])
                        respIcs213FormData[key] = ics213FormData[key]
                        master.entryName.set(ics213FormData[key])
                        #print("resp load data: ",key,":",respIcs213FormData[key])
                    elif key == "p4":
                        #print(key,ics213FormData[key])
                        respIcs213FormData[key] = ics213FormData[key]
                        master.entryNamePos.set(ics213FormData[key])
                        #print("resp load data: ",key,":",respIcs213FormData[key])
                    elif key == "d2":
                        master.loadedFileD2 = ics213FormData[key]
                        respIcs213FormData[key] = ics213FormData[key]
                        master.rplyDateData.set("Date: "+ics213FormData[key])
                        #print("resp load data: ",key,":",respIcs213FormData[key])
                    elif key == "t2":
                        master.loadedFileT2 = ics213FormData[key]
                        respIcs213FormData[key] = ics213FormData[key]
                        master.rplyTimeData.set("Time: "+ics213FormData[key])
                        #print("resp load data: ",key,":",respIcs213FormData[key])
                    elif key == "file":
                        ## must be accounted for. Will be needed when calling HTML template
                        master.tempFile = ics213FormData[key]
                        respIcs213FormData[key] = ics213FormData[key]

                mb.showinfo("Load Command","ICS-213 Form data was loaded")
            else:
                ## must have cancelled the 'load' command
                pass

        def clearData():
            for key in gv.totalIcs213Keys:
                if key == "inc":
                    ics213FormData[key] = ""
                    master.entryInc.set(ics213FormData[key])
                elif key == "to":
                    ics213FormData[key] = ""
                    master.entryTo.set(ics213FormData[key])
                elif key == "fm":
                    ics213FormData[key] = ""
                    master.entryFrom.set(ics213FormData[key])
                elif key == "p1":
                    ics213FormData[key] = ""
                    master.entryToPos.set(ics213FormData[key])
                elif key == "p2":
                    ics213FormData[key] = ""
                    master.entryFromPos.set(ics213FormData[key])
                elif key == "sb":
                    ics213FormData[key] = ""
                    master.entrySubj.set(ics213FormData[key])
                elif key == "mg":
                    ics213FormData[key] = ""
                    self.origEntryMsg.delete("1.0","end")
                    master.origMsg.set(ics213FormData[key])
                elif key == "s1":
                    ics213FormData[key] = ""
                    master.entryApprover.set(ics213FormData[key])
                elif key == "p3":
                    ics213FormData[key] = ""
                    master.entryApprPos.set(ics213FormData[key])
                elif key == "d1":
                    ics213FormData[key] = ""
                    master.loadedFileD1 = ics213FormData[key]
                    master.entryDate1.set(ics213FormData[key])
                elif key == "t1":
                    ics213FormData[key] = ""
                    master.loadedFileT1 = ics213FormData[key]
                    master.entryTime1.set(ics213FormData[key])
                ## for info of responder, transfer read data to secondary dictionary
                elif key == "rp":
                    ics213FormData[key] = ""
                    respIcs213FormData[key] = ics213FormData[key]
                    master.replyMsg.set(ics213FormData[key])
                elif key == "s2":
                    ics213FormData[key] = ""
                    master.entryName.set(ics213FormData[key])
                    respIcs213FormData[key] = ics213FormData[key]
                elif key == "p4":
                    ics213FormData[key] = ""
                    master.entryNamePos.set(ics213FormData[key])
                    respIcs213FormData[key] = ics213FormData[key]
                elif key == "d2":
                    ics213FormData[key] = ""
                    master.loadedFileD2 = ics213FormData[key]
                    respIcs213FormData[key] = ics213FormData[key]
                elif key == "t2":
                    ics213FormData[key] = ""
                    master.loadedFileT2 = ics213FormData[key]
                    respIcs213FormData[key] = ics213FormData[key]
                elif key == "file":
                    ## must be accounted for. Will be needed when calling HTML template
                    respIcs213FormData[key] = ics213FormData[key] = "213"
            master.loadedFlag = False
            ## get the current date & time
            self.localGetDateTimeData(self.origDateEntry,self.origTimeEntry)
            ## set all date & time variables to the same date and time (current)
            respIcs213FormData["d2"] = self.ics213FormData["d2"] = ics213FormData["d1"] = self.ics213FormData["d1"]
            respIcs213FormData["t2"] = self.ics213FormData["t2"] = ics213FormData["t1"] = self.ics213FormData["t1"]

        def updateData():
            for key in gv.totalIcs213Keys:
                if key == "inc":
                    ics213FormData[key] = master.entryInc.get()
                elif key == "to":
                    ics213FormData[key] = master.entryTo.get()
                elif key == "fm":
                    ics213FormData[key] = master.entryFrom.get()
                elif key == "p1":
                    ics213FormData[key] = master.entryToPos.get()
                elif key == "p2":
                    ics213FormData[key] = master.entryFromPos.get()
                elif key == "sb":
                    ics213FormData[key] = master.entrySubj.get()
                elif key == "mg":
                    ics213FormData[key] = self.origEntryMsg.get(1.0,END)
                    master.origMsg.set(ics213FormData[key])
                elif key == "s1":
                    ics213FormData[key] = master.entryApprover.get()
                elif key == "p3":
                    ics213FormData[key] = master.entryApprPos.get()
                elif key == "d1":
                    if master.entryDate1.get()[:6] == "Date: ":
                        ics213FormData[key] = master.entryDate1.get()[6:]
                    else:
                        ics213FormData[key] = master.entryDate1.get()
                elif key == "t1":
                    if master.entryTime1.get()[:6] == "Time: ":
                        ics213FormData[key] = master.entryTime1.get()[6:]
                    else:
                        ics213FormData[key] = master.entryTime1.get()
                ## for info of responder, transfer read data to secondary dictionary
                elif key == "rp":
                    respIcs213FormData[key] = ics213FormData[key] = master.replyMsg.get()
                elif key == "s2":
                    respIcs213FormData[key] = ics213FormData[key] = master.entryName.get()
                elif key == "p4":
                    respIcs213FormData[key] = ics213FormData[key] = master.entryNamePos.get()
                elif key == "d2":
                    if master.rplyDateData.get()[:6] == "Date: ":
                        respIcs213FormData[key] = ics213FormData[key] = master.rplyDateData.get()[6:]
                    else:
                        respIcs213FormData[key] = ics213FormData[key] = master.rplyDateData.get()
                elif key == "t2":
                    if master.rplyTimeData.get()[:6] == "Time: ":
                        respIcs213FormData[key] = ics213FormData[key] = master.rplyTimeData.get()[6:]
                    else:
                        respIcs213FormData[key] = ics213FormData[key] = master.rplyTimeData.get()
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

# second frame for Tab3
#### ============================= ICS-213 Responder ============================
class Tab3_Frame2(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)

        # Keep track of widgets added to frame
        self.widgets = []
        ## Frame data dictionaries
        self.rplyFieldsText = gv.ics213FieldsText
        self.rplyFieldKeys = gv.rplyIcs213FieldKeys
        self.commonConfData = gv.commonConfData
        self.ics213FormData = gv.ics213FieldsData
        self.respIcs213FormData = gv.respIcs213FormData

        #print("init - respdata: ",self.respIcs213FormData)
        #### Assume that Tab3 - Frame 1 has loaded or assigned configuration data
        ## Transfer configuration from global to local
        for key in gv.commonConfKeys:
            self.commonConfData[key] = commonConfData[key]
        
        for key in gv.rplyIcs213FieldKeys:
            #print("resp data from global: ",key,':',ics213FormData[key])
        #    if key == "rp":
        #        self.respIcs213FormData[key] = ics213FormData[key]

            if key == "s2":
        #        respIcs213FormData[key] = ics213FormData[key]
                master.entryName.set(self.respIcs213FormData[key])
            elif key == "p4":
        #        respIcs213FormData[key] = ics213FormData[key]
                master.entryNamePos.set(self.respIcs213FormData[key])
            elif key == "d2":
        #        respIcs213FormData[key] = ics213FormData[key]
                master.rplyDateData.set(self.respIcs213FormData[key])
            elif key == "t2":
        #        respIcs213FormData[key] = ics213FormData[key]
                master.rplyTimeData.set(self.respIcs213FormData[key])
            elif key == "file":
                respIcs213FormData[key] = ics213FormData[key]

        self.fileDropDown = StringVar()

        #### callback function for Combobox()
        def selectRespFileOption(event):
            selRespAction = self.chooseRespFile.get()
            if selRespAction == "Save File":
                saveRespData()
                self.chooseRespFile.set('')
            #elif selRespAction == "Clear Form":
            #    clearRespData()
            #    self.chooseRespFile.set('')
            elif selRespAction == "Update":
                updateRespData()
                self.chooseRespFile.set('')


        self.label = Label(self, text="Resp", bg="#f8d8d8")
        self.widgets.append(self.label)
        # and another button to change it back to the Originator frame
        self.button = Button(self, text="Go to Originator Mode", command=lambda: clearForm(Tab3_Frame1))
        self.widgets.append(self.button)
        self.label.grid(column=0,row=0, sticky="w")
        self.button.grid(column=1,row=0, sticky="w")

        ## Get the current date and time
        self.getDtButton = Button(self, text="Get Date & Time", command=lambda:self.getDateTimeData(self.rplyDateEntry,self.rplyTimeEntry))
        self.widgets.append(self.getDtButton)
        self.getDtButton.grid(column=1,row = 0, sticky="e")

        ## radiobutton for 'file actions'
        self.comboLabel2 = Label(self,text = "Select =-> ")
        self.widgets.append(self.comboLabel2)
        self.comboLabel2.grid(column=3, row=0, sticky="w")

        self.chooseRespFile = ttk.Combobox(self, width=master.colWidth, textvariable=self.fileDropDown)
        self.widgets.append(self.chooseRespFile)
        self.chooseRespFile['values'] = ["Save File", "Update"]
        self.chooseRespFile.grid(column=3, row=0, sticky="w",padx=80)
        ## callbacks must be declared before the combobox widget
        self.chooseRespFile.bind('<<ComboboxSelected>>', selectRespFileOption)

        ## Quit button
        quitButton = Button(self, text="Quit", command=lambda:master.quitProgram())
        self.widgets.append(quitButton)
        quitButton.grid(column=3,row=0, sticky = "e")
        quitButton.configure(bg="blue", fg="white")

        #### Text sizing variable
        normText = 40

        dtRow = 1
        ## Date Box
        self.rplyDateEntry =Entry(self, textvariable=master.rplyDateData, bg="#d8f8d8", width=18)
        self.widgets.append(self.rplyDateEntry)
        self.rplyDateEntry.grid(column=3, row=dtRow, sticky="w")
        self.rplyDateEntry.delete(0,END)
        ## distinguish between blank form and loaded form
        if master.loadedFlag:
            self.rplyDateEntry.insert(0,"Date: "+master.loadedFileD2)
        else:
            self.rplyDateEntry.insert(0,"Date: "+respIcs213FormData["d2"])

        ## Time Box
        self.rplyTimeEntry =Entry(self, textvariable=master.rplyTimeData, bg="#d8f8d8", width=18)
        self.widgets.append(self.rplyTimeEntry)
        self.rplyTimeEntry.grid(column=3, row=dtRow, sticky="e")
        self.rplyTimeEntry.delete(0,END)
         ## distinguish between blank form and loaded form
        if master.loadedFlag:
            self.rplyTimeEntry.insert(0,"Time: "+master.loadedFileT2)
        else:
            self.rplyTimeEntry.insert(0,"Time: "+respIcs213FormData["t2"])

        replyRow= 2
        ## Reply area
        self.replyLabel = Label(self,text=self.rplyFieldsText['rp'])
        self.widgets.append(self.replyLabel)
        self.replyLabel.grid(column=0, row = replyRow, sticky="w")

        self.replyEntryMsg = Text(self)
        self.widgets.append(self.replyEntryMsg)
        self.replyEntryMsg.grid(column=1, row=replyRow)
        self.replyEntryMsg.grid_configure(columnspan=3)
        self.replyEntryMsg.configure(background="#f8f8d8", wrap='word')
        self.replyEntryMsg.delete(1.0,"end")
        self.replyEntryMsg.insert(END,respIcs213FormData["rp"])
        master.replyMsg.set(respIcs213FormData["rp"])

        respRow = 3
        ## Name of responder
        self.replyNameLabel = Label(self, text=self.rplyFieldsText['s2'])
        self.widgets.append(self.replyNameLabel)
        self.replyNameLabel.grid(column=0, row=respRow, sticky="w")

        self.replyEntryName = Entry(self, textvariable=master.entryName, width=normText, bg="#f8e8e8")
        self.widgets.append(self.replyEntryName)
        self.replyEntryName.grid(column=1, row=respRow, sticky="w")
        #print("s2 in respond:",ics213FormData["s2"])
        master.entryName.set(self.respIcs213FormData["s2"])

        ## Position of responder
        self.replyNamePosLabel = Label(self, text=self.rplyFieldsText["p4"])
        self.widgets.append(self.replyNamePosLabel)
        self.replyNamePosLabel.grid(column=2,row=respRow, sticky="w")

        self.replyNamePosEntry = Entry(self, textvariable=master.entryNamePos, width=normText, bg="#f8e8e8")
        self.widgets.append(self.replyNamePosEntry)
        self.replyNamePosEntry.grid(column=3, row=respRow, sticky="w")
        master.entryNamePos.set(self.respIcs213FormData["p4"])

        def clearForm(frame_class):
                ## Save any altered data
                for key in gv.rplyIcs213FieldKeys:
                    if key == "rp":
                        respIcs213FormData[key] = ics213FormData[key] = master.replyMsg.get()
                    elif key == "s2":
                        respIcs213FormData[key] = ics213FormData[key] = master.entryName.get()
                    elif key == "p4":
                        respIcs213FormData[key] = ics213FormData[key] = master.entryNamePos.get()
                    elif key == "d2":
                        respIcs213FormData[key] = ics213FormData[key]
                    elif key == "t2":
                        respIcs213FormData[key] = ics213FormData[key]
                    elif key == "file":
                        respIcs213FormData[key] = ics213FormData[key] = "213"
                ## transfer configuration data from local to global
                for key in gv.commonConfKeys:
                    commonConfData[key] = self.commonConfData[key]

                ## === Clearing widgets and switching to Originator ===
                ut.clearWidgetForm(self.widgets)
                master.switch_frame(frame_class)
        
        ## loadData() is accomplished in the Originator tab

        def saveRespData():
            for key in gv.totalIcs213Keys:
                if key == "inc":
                    ics213FormData[key] = master.entryInc.get()
                elif key == "to":
                    ics213FormData[key] = master.entryTo.get()
                elif key == "fm":
                    ics213FormData[key] = master.entryFrom.get()
                elif key == "p1":
                    ics213FormData[key] = master.entryToPos.get()
                elif key == "p2":
                    ics213FormData[key] = master.entryFromPos.get()
                elif key == "sb":
                    ics213FormData[key] = master.entrySubj.get()
                elif key == "mg":
                    ics213FormData[key] = master.origMsg.get()
                elif key == "s1":
                    ics213FormData[key] = master.entryApprover.get()
                elif key == "p3":
                    ics213FormData[key] = master.entryApprPos.get()
                elif key == "d1":
                    if master.entryDate1.get()[:6] == "Date: ":
                        ics213FormData[key] = master.entryDate1.get()[6:]
                    else:
                        ics213FormData[key] = master.entryDate1.get()
                elif key == "t1":
                    if master.entryTime1.get()[:6] == "Time: ":
                        ics213FormData[key] = master.entryTime1.get()[6:]
                    else:
                        ics213FormData[key] = master.entryTime1.get()
                ## for info of responder, transfer read data to secondary dictionary
                elif key == "rp":
                    respIcs213FormData[key] = ics213FormData[key] = master.replyMsg.get()
                elif key == "s2":
                    respIcs213FormData[key] = ics213FormData[key] = master.entryName.get()
                elif key == "p4":
                    respIcs213FormData[key] = ics213FormData[key] = master.entryNamePos.get()
                elif key == "d2":
                    if master.rplyDateData.get()[:6] == "Date: ":
                        respIcs213FormData[key] = ics213FormData[key] = master.rplyDateData.get()[6:]
                    else:
                        respIcs213FormData[key] = ics213FormData[key] = master.rplyDateData.get()
                elif key == "t2":
                    if master.rplyTimeData.get()[:6] == "Time: ":
                        respIcs213FormData[key] = ics213FormData[key] = master.rplyTimeData.get()[6:]
                    else:
                        respIcs213FormData[key] = ics213FormData[key] = master.rplyTimeData.get()
                elif key == "file":
                    respIcs213FormData[key] = ics213FormData[key] = "213"

            fileData = [("ICS-213 Forms","*.213")]
            funcParam = (gv.msgPath,fileData,ics213FormData,gv.totalIcs213Keys)
            ut.saveFormData(funcParam)
            mb.showinfo("Save","ICS-213 Form data was saved")

        def clearRespData():
            for key in gv.totalIcs213Keys:
                if key == "inc":
                    ics213FormData[key] = ""
                    master.entryInc.set(ics213FormData[key])
                elif key == "to":
                    ics213FormData[key] = ""
                    master.entryTo.set(ics213FormData[key])
                elif key == "fm":
                    ics213FormData[key] = ""
                    master.entryFrom.set(ics213FormData[key])
                elif key == "p1":
                    ics213FormData[key] = ""
                    master.entryToPos.set(ics213FormData[key])
                elif key == "p2":
                    ics213FormData[key] = ""
                    master.entryFromPos.set(ics213FormData[key])
                elif key == "sb":
                    ics213FormData[key] = ""
                    master.entrySubj.set(ics213FormData[key])
                elif key == "mg":
                    ics213FormData[key] = ""
                    #master.origMsg.delete("1.0","end")
                    master.origMsg.set(ics213FormData[key])
                elif key == "s1":
                    ics213FormData[key] = ""
                    master.entryApprover.set(ics213FormData[key])
                elif key == "p3":
                    ics213FormData[key] = ""
                    master.entryApprPos.set(ics213FormData[key])
                elif key == "d1":
                    ics213FormData[key] = ""
                    master.loadedFileD1 = ics213FormData[key]
                    master.entryDate1.set(ics213FormData[key])
                elif key == "t1":
                    ics213FormData[key] = ""
                    master.loadedFileT1 = ics213FormData[key]
                    master.entryTime1.set(ics213FormData[key])
                ## for info of responder, transfer read data to secondary dictionary
                elif key == "rp":
                    ics213FormData[key] = ""
                    respIcs213FormData[key] = ics213FormData[key]
                    master.replyMsg.set(ics213FormData[key])
                elif key == "s2":
                    ics213FormData[key] = ""
                    master.entryName.set(ics213FormData[key])
                    respIcs213FormData[key] = ics213FormData[key]
                elif key == "p4":
                    ics213FormData[key] = ""
                    master.entryNamePos.set(ics213FormData[key])
                    respIcs213FormData[key] = ics213FormData[key]
                elif key == "d2":
                    ics213FormData[key] = ""
                    master.loadedFileD2 = ics213FormData[key]
                    respIcs213FormData[key] = ics213FormData[key]
                elif key == "t2":
                    ics213FormData[key] = ""
                    master.loadedFileT2 = ics213FormData[key]
                    respIcs213FormData[key] = ics213FormData[key]
                elif key == "file":
                    respIcs213FormData[key] = ics213FormData[key] = "213"
            master.loadedFlag = False
            ## get the current date & time
            self.getDateTimeData(self.rplyDateEntry,self.rplyTimeEntry)
            ## set all date & time variables to the same date and time (current)
            respIcs213FormData["d2"] = self.ics213FormData["d2"] = ics213FormData["d1"] = self.ics213FormData["d1"]
            respIcs213FormData["t2"] = self.ics213FormData["t2"] = ics213FormData["t1"] = self.ics213FormData["t1"]

        def updateRespData():
            for key in gv.totalIcs213Keys:
                if key == "inc":
                    ics213FormData[key] = master.entryInc.get()
                elif key == "to":
                    ics213FormData[key] = master.entryTo.get()
                elif key == "fm":
                    ics213FormData[key] = master.entryFrom.get()
                elif key == "p1":
                    ics213FormData[key] = master.entryToPos.get()
                elif key == "p2":
                    ics213FormData[key] = master.entryFromPos.get()
                elif key == "sb":
                    ics213FormData[key] = master.entrySubj.get()
                elif key == "mg":
                    ics213FormData[key] = master.origMsg.get()
                elif key == "s1":
                    ics213FormData[key] = master.entryApprover.get()
                elif key == "p3":
                    ics213FormData[key] = master.entryApprPos.get()
                elif key == "d1":
                    if master.entryDate1.get()[:6] == "Date: ":
                        ics213FormData[key] = master.entryDate1.get()[6:]
                    else:
                        ics213FormData[key] = master.entryDate1.get()
                elif key == "t1":
                    if master.entryTime1.get()[:6] == "Time: ":
                        ics213FormData[key] = master.entryTime1.get()[6:]
                    else:
                        ics213FormData[key] = master.entryTime1.get()
                ## for info of responder, transfer read data to secondary dictionary
                elif key == "rp":
                    ics213FormData[key] = self.replyEntryMsg.get(1.0,END)
                    respIcs213FormData[key] = ics213FormData[key]
                    master.replyMsg.set(ics213FormData[key])
                elif key == "s2":
                    respIcs213FormData[key] = ics213FormData[key] = master.entryName.get()
                elif key == "p4":
                    respIcs213FormData[key] = ics213FormData[key] = master.entryNamePos.get()
                elif key == "d2":
                    if master.rplyDateData.get()[:6] == "Date: ":
                        respIcs213FormData[key] = ics213FormData[key] = master.rplyDateData.get()[6:]
                    else:
                        respIcs213FormData[key] = ics213FormData[key] = master.rplyDateData.get()
                elif key == "t2":
                    if master.rplyTimeData.get()[:6] == "Time: ":
                        respIcs213FormData[key] = ics213FormData[key] = master.rplyTimeData.get()[6:]
                    else:
                        respIcs213FormData[key] = ics213FormData[key] = master.rplyTimeData.get()
                elif key == "file":
                    respIcs213FormData[key] = ics213FormData[key] = "213"

            fileData = [("ICS-213 Forms","*.213")]
            funcParam = (gv.msgPath,fileData,ics213FormData,gv.totalIcs213Keys)
            ut.saveFormData(funcParam)
            mb.showinfo("Save","ICS-213 Form data was saved")

    def getDateTimeData(self, dateEn, timeEn):
        ## dateEn is the widget reference for the date Entry() display
        ## timeEn is the widget reference for the time Entry() display
        ## The config format data is loaded upfront
        rDate = ""
        rTime = ""
        rDate, rTime = ut.dateAndTime(commonConfData["fdate"],commonConfData["ftime"],commonConfData["fUTC"])

        ## update date box
        dateEn.delete(0,END)
        respIcs213FormData["d2"] = ics213FormData["d2"]=rDate
        dateEn.insert(0,"Date: "+ics213FormData["d2"])

        ## update time box
        timeEn.delete(0,END)
        respIcs213FormData["t2"] = self.ics213FormData["t2"]=rTime
        timeEn.insert(0,"Time: "+ics213FormData["t2"])
