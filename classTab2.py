from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mb
import sys
import os
import globalVariables as gv
import utilities as ut

#### ======================== Start of Configuration ===================================
##

commonConfData = gv.commonConfData

## Common Configuration Data
class Tab2(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)

        # Keep track of widgets added to frame
        self.widgets = []

        ## More variables
        self.commonConfText = gv.commonConfText
        self.commonConfKeys = gv.commonConfKeys
        self.commonConfData = gv.commonConfData

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

        # callback function for combobox()
        def selectAction(event):
            selAction = self.chooseConfig.get()
            saveConfData()
            if selAction == "Personal":
                ut.clearWidgetForm(self.widgets)
                personalConf()
                self.chooseConfig.set('')
            elif selAction == "Date/Time":
                ut.clearWidgetForm(self.widgets)
                datetime()
                self.chooseConfig.set('')
            elif selAction == "Radiogram":
                ut.clearWidgetForm(self.widgets)
                radiogramItems()
                self.chooseConfig.set('')
            elif selAction == "Save Configuration to file":
                ut.clearWidgetForm(self.widgets)
                saveData()
                self.chooseConfig.set('')
            elif selAction == "Load Configuration from file":
                ut.clearWidgetForm(self.widgets)
                loadData()
                self.chooseConfig.set('')
            elif selAction == "Clear Configuration":
                ut.clearWidgetForm(self.widgets)
                clearData()
                self.chooseConfig.set('')

        ## Specify column width for form
        colWidth =28
        ## Keep track of which configuration area is being filled in
        self.tableArea = ""

        self.label = Label(self, text="Select =-> ")
        self.label.grid(column=0,row=0, sticky="w")
        self.chooseConfig = ttk.Combobox(self, width=colWidth, textvariable = self.dropdown)
        self.chooseConfig['values'] = ["Personal","Date/Time","Radiogram","Save Configuration to file","Load Configuration from file","Clear Configuration"]
        self.chooseConfig.grid(column=0,row=0, sticky="w",padx=80)
        ## Note callback function must preceed the combobox widget
        self.chooseConfig.bind('<<ComboboxSelected>>', selectAction)

        self.blankLabel = Label(self)
        self.blankLabel.config(text = '     ')
        self.blankLabel.grid(column=2,row=0, sticky="w")

        quitButton = Button(self, text="Quit", command=lambda:self.quitProgram())
        quitButton.grid(column=4,row=0, sticky = "e")
        quitButton.configure(bg="blue", fg="white")

        def personalConf():
            ## Table Entry Area
            self.tableArea = "personal"

            ## widget list keeps track of the displayed widgets
            ## and is used to clear the screen of widgets before
            ## displaying a new set of widgets
            ## reset widget list
            self.widgets = []

            ## Callsign
            callsignRow = 1
            personalCallsignLabel = Label(self,text=self.commonConfText["call"])
            self.widgets.append(personalCallsignLabel)
            personalCallsignLabel.grid(column=0, row= callsignRow, sticky ="w")

            personalCallsignEntry = Entry(self, textvariable = self.callsignEntryData, width=colWidth)
            self.widgets.append(personalCallsignEntry)
            personalCallsignEntry.grid(column=1, row=callsignRow,  columnspan=2, sticky="w")
            ## first clear any text
            personalCallsignEntry.delete(0,END)
            ## Insert any new text
            personalCallsignEntry.insert(0,self.commonConfData["call"])

            ## Name
            nameRow = 2
            personalNameLabel = Label(self,text=self.commonConfText["name"])
            self.widgets.append(personalNameLabel)
            personalNameLabel.grid(column=0, row= nameRow, sticky ="w")

            personalNameEntry = Entry(self, textvariable = self.nameEntryData, width=colWidth)
            self.widgets.append(personalNameEntry)
            personalNameEntry.grid(column=1, row=nameRow,  columnspan=2, sticky="w")
            ## first clear any text
            personalNameEntry.delete(0,END)
            ## Insert any new text
            personalNameEntry.insert(0,self.commonConfData["name"])

            ## Telephone #
            phoneRow = 3
            personalPhoneLabel = Label(self,text=self.commonConfText["phone"])
            self.widgets.append(personalPhoneLabel)
            personalPhoneLabel.grid(column=0, row = phoneRow, sticky="w")

            personalPhoneEntry = Entry(self, textvariable= self.phoneEntryData, width=colWidth)
            self.widgets.append(personalPhoneEntry)
            personalPhoneEntry.grid(column=1, row=phoneRow, columnspan=2, sticky="w")
            ## first clear any text
            personalPhoneEntry.delete(0,END)
            ## Insert any new text
            personalPhoneEntry.insert(0,self.commonConfData["phone"])

            ## Address
            addrRow = 4
            personalAddressLabel= Label(self, text=self.commonConfText["addr"])
            self.widgets.append(personalAddressLabel)
            personalAddressLabel.grid(column=0, row=addrRow, sticky="w")

            personalAddressEntry = Entry(self, textvariable= self.addressEntryData, width=colWidth)
            self.widgets.append(personalAddressEntry)
            personalAddressEntry.grid(column=1, row=addrRow, columnspan=2, sticky="w")
            ## first clear any text
            personalAddressEntry.delete(0,END)
            ## Insert any new text
            personalAddressEntry.insert(0,self.commonConfData["addr"])

            ## City/State/Zip
            cszRow = 5
            personalCszLabel= Label(self, text=self.commonConfText["c-s-z"])
            self.widgets.append(personalCszLabel)
            personalCszLabel.grid(column=0, row=cszRow, sticky="w")

            personalCszEntry = Entry(self, textvariable= self.cityEntryData, width=colWidth)
            self.widgets.append(personalCszEntry)
            personalCszEntry.grid(column=1, row=cszRow, columnspan=2, sticky="w")
            ## first clear any text
            personalCszEntry.delete(0,END)
            ## Insert any new text
            personalCszEntry.insert(0,self.commonConfData["c-s-z"])

            ## Email Address
            emailRow = 6
            personalEmailLabel = Label(self, text=self.commonConfText["email"])
            self.widgets.append(personalEmailLabel)
            personalEmailLabel.grid(column=0, row=emailRow, sticky="w")

            personalEmailEntry = Entry(self, textvariable= self.emailEntryData, width=colWidth)
            self.widgets.append(personalEmailEntry)
            personalEmailEntry.grid(column=1, row=emailRow, columnspan=2, sticky="w")
            ## first clear any text
            personalEmailEntry.delete(0,END)
            ## Insert any new text
            personalEmailEntry.insert(0,self.commonConfData["email"])

        def datetime():
            ## Table Entry Area
            self.tableArea = "datetime"
            ## reset widget list
            self.widgets = []
            
            dtRow = 1
            datetimeDateLabel = Label(self,text=self.commonConfText["fdate"])
            self.widgets.append(datetimeDateLabel)
            datetimeDateLabel.grid(column=0, row= dtRow, sticky ="w")

            dateFormatText = [("YYYY-MM-DD","1"),("YYYY-DD-MM","2"),("MM/DD/YY","3"),("DD/MM/YY","4"),("YYYYMMDD","5")]
            timeFormatText = [("hhmmL","1"),("hh:mmL","2"),("hhmmZ","3"),("hh:mmZ","4"),("hhmm UTC","5"),("hh:mm UTC","6")]

            ## Set up first radiobutton list for date formats
            radioRow = dtRow
            #indexCount = 0
            for format in dateFormatText:
                dateFormat = ttk.Radiobutton(self, text = format[0], value = format[1], variable = self.formatDateEntryData)
                self.widgets.append(dateFormat)
                dateFormat.grid(column=1, row=radioRow, sticky="w")
                radioRow += 1
            self.formatDateEntryData.set(commonConfData["fdate"])

            datetimeTimeLabel = Label(self,text=self.commonConfText["ftime"])
            self.widgets.append(datetimeTimeLabel)
            datetimeTimeLabel.grid(column=2, row=dtRow, sticky="w")

            ## Set up second radiobutton list for time formats
            radioRow = dtRow
            for format in timeFormatText:
                timeFormat = ttk.Radiobutton(self, text = format[0], value = format[1], variable = self.formatTimeEntryData)
                self.widgets.append(timeFormat)
                timeFormat.grid(column=3, row=radioRow, sticky ="w")
                radioRow += 1
            self.formatTimeEntryData.set(commonConfData["ftime"])

        def radiogramItems():
            ## reset widget list
            self.widgets = []
            print("Misc. Items of Form")
            pass
        
        def loadData():
            os.chdir(gv.configPath)
            self.widgets=[]
            fileNameList = [("JS8msg.cfg","*.cfg")]
            funcParam = (gv.configPath,fileNameList)
            result = ut.loadFormData(funcParam)
            if result is not None:
                self.commonConfData = commonConfData = result
                mb.showinfo("Load","Configuration data was loaded")
            else:
                mb.showinfo("Load","ERROR! Configuration data was not loaded")

        def saveData():
            self.widgets=[]
            ## save config in current directory
            fileNameList = [("JS8msg.cfg","*.cfg")]
            funcParam = (gv.configPath,fileNameList,commonConfData,self.commonConfKeys)
            result = ut.saveFormData(funcParam)
            if result is not None:
                mb.showinfo("Save","Configuration data was saved")
            else:
                mb.showinfo("Save","ERROR! Configuration data was not saved")

        def clearData():
            self.widgets=[]
            dtRow = 1
            clearDataLabel = Label(self,text="Clearing configuration data.")
            self.widgets.append(clearDataLabel)
            clearDataLabel.grid(column=0, row= dtRow, sticky ="w")
            for key in self.commonConfKeys:
                if key == "call":
                    commonConfData[key] = ""
                    self.callsignEntryData.set("")
                elif key == "phone":
                    commonConfData[key] = ""
                    self.phoneEntryData.set("")
                elif key == "name":
                    commonConfData[key] = ""
                    self.nameEntryData.set("")
                elif key == "addr":
                    commonConfData[key] = ""
                    self.addressEntryData.set("")
                elif key == "c-s-z":
                    commonConfData[key] = ""
                    self.cityEntryData.set("")
                elif key == "email":
                    commonConfData[key] = ""
                    self.emailEntryData.set("")
                elif key == "fdate":
                    commonConfData[key] = ""
                    self.formatDateEntryData.set("")
                elif key == "ftime":
                    commonConfData[key] = ""
                    self.formatTimeEntryData.set("")
                elif key == "fUTC":
                    commonConfData[key] = ""
            clearDataLabel['text'] = "Configuration data cleared."



        def saveConfData():
            if self.tableArea == "personal":
                for key in self.commonConfKeys:
                    ## Transfer user input from StringVar to data dictionary
                    if key == "call":
                        commonConfData[key] = self.callsignEntryData.get()
                    elif key == "phone":
                        commonConfData[key] = self.phoneEntryData.get()
                    elif key == "name":
                        commonConfData[key] = self.nameEntryData.get()
                    elif key == "addr":
                        commonConfData[key] = self.addressEntryData.get()
                    elif key == "c-s-z":
                        commonConfData[key] = self.cityEntryData.get()
                    elif key == "email":
                        commonConfData[key] = self.emailEntryData.get()
            elif self.tableArea == "datetime":
                for key in self.commonConfKeys:
                    if key == "fdate":
                        commonConfData[key] = self.formatDateEntryData.get()
                    elif key == "ftime":
                        commonConfData[key] = self.formatTimeEntryData.get()
                    elif key == "fUTC":
                        ## Which time format did they select
                        timeValue = self.formatTimeEntryData.get()
                        ## set fUTC to a value determined by the time format
                        if timeValue == "1" or timeValue == "2":
                            commonConfData[key] = "0"
                        elif timeValue == "3" or timeValue == "4":
                            commonConfData[key] = "1"
                        elif timeValue == "5" or timeValue == "6":
                            commonConfData[key] = "2"


                
    def quitProgram(self):
        sys.exit()