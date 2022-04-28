from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mb
import globalVariables as gv
import utilities as ut
import database_functions as df
import ics213_utilities as ics

## Note: the main difference between classes Tab3
## and Tab4 is the focus of the GUI on the respective
## portions of the ICS-213 form.
## Tab 3 focuses on the Originator
## Tab 4 focuses on the Responder

class Tab4(Frame):
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
        df.get_configuration_from_db()
        self.commonConfData = gv.commonConfData
        
        if not self.loadedFlag:
            rDate, rTime = ut.dateAndTime(self.commonConfData["fdate"],self.commonConfData["ftime"],self.commonConfData["fUTC"])
            ## A new or cleared form. Assign the date and time to both
            self.ics213FormData["d2"] = self.ics213FormData["d1"] = rDate
            self.ics213FormData["t2"] = self.ics213FormData["t1"] = rTime

        self.fileDropDown = StringVar()
        
        #### callback function for Combobox()
        def selectRespFileOption(event):
            selAction = self.chooseRespFile.get()
            if selAction == "Save File":
                self.replyMsg.set(self.replyTextMsg.get('1.0',"end"))
                ics.saveData(self)
                self.chooseRespFile.set('')
            elif selAction == "Load File":
                ics.loadData(self)
                self.update_Text_box()
                self.chooseRespFile.set('')
            elif selAction == "Clear Form":
                ics.clearData(self)
                self.update_Text_box()
                self.chooseRespFile.set('')
            #elif selAction == "Update":
            #    ics.updateData(self)
            #    self.chooseRespFile.set('')
                
        self.label = Label(self.frame, text="Responder", bg="#f8d8d8")
        self.widgets.append(self.label)
        self.label.grid(column=0,row = 0, sticky="w")
        
        ## Get the current date and time
        self.getDtButton = Button(self.frame, text="Get Date & Time", command=lambda:self.localGetDateTimeData(self.rplyDateEntry,self.rplyTimeEntry))
        self.widgets.append(self.getDtButton)
        self.getDtButton.grid(column=1,row = 0, sticky="e")
        
        ## radiobutton for 'file actions'
        self.comboLabel2 = Label(self.frame,text = "Select =-> ")
        self.widgets.append(self.comboLabel2)
        self.comboLabel2.grid(column=3, row=0, sticky="w")
        
        self.chooseRespFile = ttk.Combobox(self.frame, width=self.colWidth, textvariable=self.fileDropDown)
        self.widgets.append(self.chooseRespFile)
        ##self.chooseRespFile['values'] = ["Save File","Load File", "Clear Form", "Update"]
        self.chooseRespFile['values'] = ["Save File","Load File", "Clear Form"]
        self.chooseRespFile.grid(column=3, row=0, sticky="w",padx=80)
        ## callbacks must be declared before the combobox widget
        self.chooseRespFile.bind('<<ComboboxSelected>>', selectRespFileOption)
        
        ## Quit button
        #self.quitButton = Button(self.frame, text="Quit", command=lambda:self.quitProgram())
        #self.widgets.append(self.quitButton)
        #self.quitButton.grid(column=3,row=0, sticky = "e")
        #self.quitButton.configure(bg="blue", fg="white")
        
        #### Text sizing variable
        normText = 40
        
        dtRow = 1
        ## Date Box
        self.replyDateLabel = Label(self.frame, text="Date: ", bg="#d8f8d8", width=6)
        self.widgets.append(self.replyDateLabel)
        self.replyDateLabel.grid(column=0, row=dtRow, sticky="w")
        
        self.DateEntry = Entry(self.frame, textvariable=self.rplyDateData, bg="#d8f8d8", width=18)
        self.widgets.append(self.DateEntry)
        self.DateEntry.grid(column=1, row=dtRow, sticky="w")
        self.DateEntry.delete(0,END)
        ## distinguish between blank form and loaded form
        if self.loadedFlag:
            self.DateEntry.insert(0,self.loadedFileD2)
        else:
            self.DateEntry.insert(0,self.ics213FormData["d2"])

        ## Time Box
        self.TimeLabel = Label(self.frame, text="Time: ", bg="#d8f8d8", width=6)
        self.widgets.append(self.TimeLabel)
        self.TimeLabel.grid(column=2, row=dtRow, sticky="w")
        
        self.TimeEntry =Entry(self.frame, textvariable=self.rplyTimeData, bg="#d8f8d8", width=18)
        self.widgets.append(self.TimeEntry)
        self.TimeEntry.grid(column=3, row=dtRow, sticky="w",padx = 20 )
        self.TimeEntry.delete(0,END)
         ## distinguish between blank form and loaded form
        if self.loadedFlag:
            self.TimeEntry.insert(0,self.loadedFileT2)
        else:
            self.TimeEntry.insert(0,self.ics213FormData["t2"])

        replyRow= 2
        ## Reply area
        self.replyLabel = Label(self.frame,text=gv.ics213FieldsText['rp'])
        self.widgets.append(self.replyLabel)
        self.replyLabel.grid(column=0, row = replyRow, sticky="w")

        #print("StrVar is: ",self.replyMsg.get())
        #print("Dict is: ",self.ics213FormData["rp"])
        #print("Flag is: ",self.loadedFlag)
        if not self.loadedFlag:
            self.replyTextMsg = Text(self.frame)
            self.widgets.append(self.replyTextMsg)
            self.replyTextMsg.grid(column=1, row=replyRow)
            self.replyTextMsg.grid_configure(columnspan=3)
            self.replyTextMsg.configure(background="#f8f8d8", wrap='word')
            self.replyTextMsg.delete('1.0',"end")
            self.replyTextMsg.insert(END,self.ics213FormData["rp"])
            self.replyMsg.set(self.ics213FormData["rp"])


        respRow = 3
        ## Name of responder
        self.replyNameLabel = Label(self.frame, text=gv.ics213FieldsText['s2'])
        self.widgets.append(self.replyNameLabel)
        self.replyNameLabel.grid(column=0, row=respRow, sticky="w")

        self.replyEntryName = Entry(self.frame, textvariable=self.entryName, width=normText, bg="#f8e8e8")
        self.widgets.append(self.replyEntryName)
        self.replyEntryName.grid(column=1, row=respRow, sticky="w")
        self.entryName.set(self.ics213FormData["s2"])

        ## Position of responder
        self.replyNamePosLabel = Label(self.frame, text=gv.ics213FieldsText["p4"])
        self.widgets.append(self.replyNamePosLabel)
        self.replyNamePosLabel.grid(column=2,row=respRow, sticky="w")

        self.replyNamePosEntry = Entry(self.frame, textvariable=self.entryNamePos, width=normText, bg="#f8e8e8")
        self.widgets.append(self.replyNamePosEntry)
        self.replyNamePosEntry.grid(column=3, row=respRow, sticky="w")
        self.entryNamePos.set(self.ics213FormData["p4"])
        gv.widget_list_dict["Tab4"] = self.widgets
        
        
    def localGetDateTimeData(self, dateEn, timeEn):
        ## dateEn is the widget reference for the date Entry() display
        ## timeEn is the widget reference for the time Entry() display
        ## The config format data is loaded upfront
        rDate = ""
        rTime = ""
        rDate, rTime = ut.dateAndTime(gv.commonConfData["fdate"],gv.commonConfData["ftime"],gv.commonConfData["fUTC"])

        ## update date box
        dateEn.delete(0,END)
        self.ics213FormData["d2"]=rDate
        dateEn.insert(0,self.ics213FormData["d2"])

        ## update time box
        timeEn.delete(0,END)
        self.ics213FormData["t2"]=rTime
        timeEn.insert(0,self.ics213FormData["t2"])
        
    def update_Text_box(self):
        replyRow= 2
        self.replyTextMsg = Text(self.frame)
        self.widgets.append(self.replyTextMsg)
        self.replyTextMsg.grid(column=1, row=replyRow)
        self.replyTextMsg.grid_configure(columnspan=3)
        self.replyTextMsg.configure(background="#f8f8d8", wrap='word')
        self.replyTextMsg.delete('1.0',"end")
        self.replyTextMsg.insert(END,self.ics213FormData["rp"])
        self.replyMsg.set(self.ics213FormData["rp"])
        self.loadedFlag = False
        
    def quitProgram(self):
        self.controller.shutting_down()