from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mb
import sys
import os
import globalVariables as gv
import utilities as ut
import create_menu as cm
import database_config as dc

#### ======================== Start of Configuration ===================================
##

commonConfData = gv.commonConfData

## Common Configuration Data
class Tab2(Frame):
    def __init__(self,parent,controller):
        Frame.__init__(self,parent,controller)
        self.controller = controller
        self.frame = parent
        # Keep track of widgets added to frame
        self.widgets = []
        self.widgets_top = []

        ## More variables
        self.commonConfText = gv.commonConfText
        self.commonConfKeys = gv.commonConfKeys
        #self.commonConfData = gv.commonConfData
        self.loadData()

        ## textvariable for combobox()
        self.dropdown = StringVar()

        ## textvariables for the configuration data entries   
        self.callsignEntryData = StringVar()
        self.phoneEntryData = StringVar()
        self.nameEntryData = StringVar()
        self.addressEntryData = StringVar()
        self.cityEntryData = StringVar()
        self.emailEntryData = StringVar()
        self.formatDateEntryData = StringVar()
        self.formatTimeEntryData = StringVar()
        self.fileEntryData = StringVar()
        self.colWidth = 28

        # callback function for combobox()
        def selectAction(event):
            selAction = self.chooseConfig.get()
            #saveConfData()
            if selAction == "Radiogram":
                ut.clearWidgetForm(self.widgets)
                gv.widget_list_dict["Tab2"] = []
                self.radiogramItems()
                self.chooseConfig.set('')
            elif selAction == "Save Configuration to file":
                ut.clearWidgetForm(self.widgets)
                gv.widget_list_dict["Tab2"] = []
                self.saveData()
                self.chooseConfig.set('')
            elif selAction == "Load Configuration from file":
                ut.clearWidgetForm(self.widgets)
                gv.widget_list_dict["Tab2"] = []
                self.loadData()
                self.chooseConfig.set('')
            elif selAction == "Clear Configuration":
                ut.clearWidgetForm(self.widgets)
                gv.widget_list_dict["Tab2"] = []
                self.clearData()
                self.chooseConfig.set('')

        ## Keep track of which configuration area is being filled in
        #self.tableArea = ""

        #self.label = Label(self.frame, text="Select =-> ", width=15)
        self.label = Label(self.frame, text="Select =-> ")
        self.label.grid(column=0,row=0, sticky="w")
        #self.label.grid(column=0,row=0, sticky="e")
        self.widgets_top.append(self.label)
        
        self.chooseConfig = ttk.Combobox(self.frame, width=self.colWidth, textvariable = self.dropdown)
        self.chooseConfig['values'] = ["Radiogram","Save Configuration to file","Load Configuration from file","Clear Configuration"]
        #self.chooseConfig.grid(column=1,row=0, sticky="w",padx=80)
        self.chooseConfig.grid(column=1,row=0, sticky="w")
        ## Note callback function must preceed the combobox widget
        self.chooseConfig.bind('<<ComboboxSelected>>', selectAction)
        self.widgets_top.append(self.chooseConfig)

        self.blankLabel = Label(self.frame)
        self.blankLabel.config(text = '     ')
        self.blankLabel.grid(column=2,row=0, sticky="w")
        self.widgets_top.append(self.blankLabel)

        self.quitButton = Button(self.frame, text="Quit", command=lambda:self.quitProgram())
        self.quitButton.grid(column=3,row=0, sticky = "e")
        self.quitButton.configure(bg="blue", fg="white")
        self.widgets_top.append(self.quitButton)
        
        #self.personalConf()
        #self.datetime()
        ## keep track of static widgets on screen
        #gv.widget_list_dict["Tab2"] = self.widgets

    #def personalConf(self):
        ## Table Entry Area
        #self.tableArea = "personal"

        ## widget list keeps track of the displayed widgets
        ## and is used to clear the screen of widgets before
        ## displaying a new set of widgets
        ## reset widget list
        #self.widgets = []

        label_col = 0
        
        colRow = 1
        self.blankLabel = Label(self.frame)
        self.blankLabel.config(text = '     ')
        self.blankLabel.grid(column=2,row=colRow, sticky="w")
        self.widgets_top.append(self.blankLabel)
        
        ## Callsign
        callsignRow = 2
        self.personalCallsignLabel = Label(self.frame,text=self.commonConfText["call"])
        self.widgets.append(self.personalCallsignLabel)
        self.personalCallsignLabel.grid(column=label_col, row= callsignRow, sticky ="w")

        self.personalCallsignEntry = Entry(self.frame, textvariable = self.callsignEntryData, width=self.colWidth)
        self.widgets.append(self.personalCallsignEntry)
        #self.personalCallsignEntry.grid(column=1, row=callsignRow,  columnspan=2, sticky="e")
        self.personalCallsignEntry.grid(column=1, row=callsignRow,  columnspan=2, sticky="w")
        ## first clear any text
        self.personalCallsignEntry.delete(0,END)
        ## Insert any new text
        self.personalCallsignEntry.insert(0,self.commonConfData["call"])

        ## Name
        nameRow = 3
        self.personalNameLabel = Label(self.frame,text=self.commonConfText["uname"])
        self.widgets.append(self.personalNameLabel)
        self.personalNameLabel.grid(column=label_col, row= nameRow, sticky ="w")

        self.personalNameEntry = Entry(self.frame, textvariable = self.nameEntryData, width=self.colWidth)
        self.widgets.append(self.personalNameEntry)
        #self.personalNameEntry.grid(column=1, row=nameRow,  columnspan=2, sticky="e")
        self.personalNameEntry.grid(column=1, row=nameRow,  columnspan=2, sticky="w")
        ## first clear any text
        self.personalNameEntry.delete(0,END)
        ## Insert any new text
        self.personalNameEntry.insert(0,self.commonConfData["uname"])

        ## Telephone #
        phoneRow = 4
        self.personalPhoneLabel = Label(self.frame,text=self.commonConfText["phone"])
        self.widgets.append(self.personalPhoneLabel)
        self.personalPhoneLabel.grid(column=label_col, row = phoneRow, sticky="w")

        self.personalPhoneEntry = Entry(self.frame, textvariable= self.phoneEntryData, width=self.colWidth)
        self.widgets.append(self.personalPhoneEntry)
        #self.personalPhoneEntry.grid(column=1, row=phoneRow, columnspan=2, sticky="e")
        self.personalPhoneEntry.grid(column=1, row=phoneRow, columnspan=2, sticky="w")
        ## first clear any text
        self.personalPhoneEntry.delete(0,END)
        ## Insert any new text
        self.personalPhoneEntry.insert(0,self.commonConfData["phone"])

        ## Address
        addrRow = 5
        self.personalAddressLabel= Label(self.frame, text=self.commonConfText["addr"])
        self.widgets.append(self.personalAddressLabel)
        self.personalAddressLabel.grid(column=label_col, row=addrRow, sticky="w")

        self.personalAddressEntry = Entry(self.frame, textvariable= self.addressEntryData, width=self.colWidth)
        self.widgets.append(self.personalAddressEntry)
        #self.personalAddressEntry.grid(column=1, row=addrRow, columnspan=2, sticky="e")
        self.personalAddressEntry.grid(column=1, row=addrRow, columnspan=2, sticky="w")
        ## first clear any text
        self.personalAddressEntry.delete(0,END)
        ## Insert any new text
        self.personalAddressEntry.insert(0,self.commonConfData["addr"])

        ## City/State/Zip
        cszRow = 6
        self.personalCszLabel= Label(self.frame, text=self.commonConfText["c-s-z"])
        self.widgets.append(self.personalCszLabel)
        self.personalCszLabel.grid(column=label_col, row=cszRow, sticky="w")

        self.personalCszEntry = Entry(self.frame, textvariable= self.cityEntryData, width=self.colWidth)
        self.widgets.append(self.personalCszEntry)
        #self.personalCszEntry.grid(column=1, row=cszRow, columnspan=2, sticky="e")
        self.personalCszEntry.grid(column=1, row=cszRow, columnspan=2, sticky="w")
        ## first clear any text
        self.personalCszEntry.delete(0,END)
        ## Insert any new text
        self.personalCszEntry.insert(0,self.commonConfData["c-s-z"])

        ## Email Address
        emailRow = 7
        self.personalEmailLabel = Label(self.frame, text=self.commonConfText["email"])
        self.widgets.append(self.personalEmailLabel)
        self.personalEmailLabel.grid(column=label_col, row=emailRow, sticky="w")

        self.personalEmailEntry = Entry(self.frame, textvariable= self.emailEntryData, width=self.colWidth)
        self.widgets.append(self.personalEmailEntry)
        #self.personalEmailEntry.grid(column=1, row=emailRow, columnspan=2, sticky="e")
        self.personalEmailEntry.grid(column=1, row=emailRow, columnspan=2, sticky="w")
        ## first clear any text
        self.personalEmailEntry.delete(0,END)
        ## Insert any new text
        self.personalEmailEntry.insert(0,self.commonConfData["email"])
        ## keep track of which set of dynamic widgets are displayed
        #gv.widget_list_dict["Tab2a"] = self.widgets

    #def datetime(self):
        ## Table Entry Area
        #self.tableArea = "datetime"
        ## reset widget list
        #self.widgets = []
        
        dtRow0 = 8
        self.blankLabel = Label(self.frame)
        self.blankLabel.config(text = '     ')
        self.blankLabel.grid(column=2,row=dtRow0, sticky="w")
        self.widgets_top.append(self.blankLabel)
        
        #dtRow = 1
        dtRow = 9
        self.datetimeDateLabel = Label(self.frame,text=self.commonConfText["fdate"])
        self.widgets.append(self.datetimeDateLabel)
        self.datetimeDateLabel.grid(column=0, row= dtRow, sticky ="w")

        dateFormatText = [("YYYY-MM-DD","1"),("YYYY-DD-MM","2"),("MM/DD/YY","3"),("DD/MM/YY","4"),("YYYYMMDD","5")]
        timeFormatText = [("hhmmL","1"),("hh:mmL","2"),("hhmmZ","3"),("hh:mmZ","4"),("hhmm UTC","5"),("hh:mm UTC","6")]

        ## Set up first radiobutton list for date formats
        radioRow = dtRow
        #indexCount = 0
        for format in dateFormatText:
            self.dateFormat = ttk.Radiobutton(self.frame, text = format[0], value = format[1], variable = self.formatDateEntryData)
            self.widgets.append(self.dateFormat)
            self.dateFormat.grid(column=1, row=radioRow, sticky="w")
            #self.dateFormat.grid(column=0, row=radioRow, sticky="e")
            radioRow += 1
        self.formatDateEntryData.set(self.commonConfData["fdate"])

        self.datetimeTimeLabel = Label(self.frame,text=self.commonConfText["ftime"])
        self.widgets.append(self.datetimeTimeLabel)
        self.datetimeTimeLabel.grid(column=2, row=dtRow, sticky="w")
        #self.datetimeTimeLabel.grid(column=1, row=dtRow, sticky="w")
        
        ## Set up second radiobutton list for time formats
        radioRow = dtRow
        for format in timeFormatText:
            self.timeFormat = ttk.Radiobutton(self.frame, text = format[0], value = format[1], variable = self.formatTimeEntryData)
            self.widgets.append(self.timeFormat)
            self.timeFormat.grid(column=3, row=radioRow, sticky ="w")
            #self.timeFormat.grid(column=1, row=radioRow, sticky ="e")
            radioRow += 1
        self.formatTimeEntryData.set(self.commonConfData["ftime"])
        gv.widget_list_dict["Tab2"] = self.widgets

    def radiogramItems(self):
        ## reset widget list
        self.widgets = []
        print("Misc. Items of Form")
        pass
        
    def loadData(self):
        #### Load up the configuration data
        dc.get_configuration_from_db()
        self.commonConfData = gv.commonConfData
        print("Checking LOAD: ",self.commonConfData)


    def saveData(self):
        for key in self.commonConfKeys:
            ## Transfer user input from StringVar to data dictionary
            if key == "call":
                self.commonConfData[key] = self.callsignEntryData.get()
            elif key == "phone":
                self.commonConfData[key] = self.phoneEntryData.get()
            elif key == "name":
                self.commonConfData[key] = self.nameEntryData.get()
            elif key == "addr":
                self.commonConfData[key] = self.addressEntryData.get()
            elif key == "c-s-z":
                self.commonConfData[key] = self.cityEntryData.get()
            elif key == "email":
                self.commonConfData[key] = self.emailEntryData.get()
            elif key == "fdate":
                self.commonConfData[key] = self.formatDateEntryData.get()
            elif key == "ftime":
                self.commonConfData[key] = self.formatTimeEntryData.get()
            elif key == "fUTC":
                ## Which time format did they select
                timeValue = self.formatTimeEntryData.get()
                ## set fUTC to a value determined by the time format
                if timeValue == "1" or timeValue == "2":
                    self.commonConfData[key] = "0"
                elif timeValue == "3" or timeValue == "4":
                    self.commonConfData[key] = "1"
                elif timeValue == "5" or timeValue == "6":
                    self.commonConfData[key] = "2"
        print("Checking xfer: ",self.commonConfData)                
        gv.commonConfData = self.commonConfData
        print("Checking Global: ",gv.commonConfData)
        dc.save_configuration_to_db()


    def clearData(self):
        self.widgets=[]
        dtRow = 1
        self.clearDataLabel = Label(self.frame,text="Clearing configuration data.")
        self.widgets.append(self.clearDataLabel)
        self.clearDataLabel.grid(column=0, row= dtRow, sticky ="w")
        for key in self.commonConfKeys:
            if key == "call":
                self.commonConfData[key] = ""
                self.callsignEntryData.set("")
            elif key == "phone":
                self.commonConfData[key] = ""
                self.phoneEntryData.set("")
            elif key == "name":
                self.commonConfData[key] = ""
                self.nameEntryData.set("")
            elif key == "addr":
                self.commonConfData[key] = ""
                self.addressEntryData.set("")
            elif key == "c-s-z":
                self.commonConfData[key] = ""
                self.cityEntryData.set("")
            elif key == "email":
                self.commonConfData[key] = ""
                self.emailEntryData.set("")
            elif key == "fdate":
                self.commonConfData[key] = ""
                self.formatDateEntryData.set("")
            elif key == "ftime":
                self.commonConfData[key] = ""
                self.formatTimeEntryData.set("")
            elif key == "fUTC":
                self.commonConfData[key] = ""
        self.clearDataLabel['text'] = "Configuration data cleared."
        gv.widget_list_dict["Tab2"] = self.widgets
                
    def quitProgram(self):
        ut.clearWidgetForm(self.widgets_top)
        self.controller.shutting_down()