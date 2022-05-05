##
## JS8msg is a copyrighted program written by Thomas Kocourek, N4FWD
## This program is released under the GPL v3 license
## 
from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mb
import globalVariables as gv
import utilities as ut



def saveData(self):
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
                self.ics213FormData[key] = self.entryDate1.get()[-6:]
                #print(self.ics213FormData[key])
            else:
                self.ics213FormData[key] = self.entryDate1.get()
        elif key == "t1":
            if self.entryTime1.get()[:6] == "Time: ":
                self.ics213FormData[key] = self.entryTime1.get()[-6:]
                #print(self.ics213FormData[key])
            else:
                self.ics213FormData[key] = self.entryTime1.get()
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

def loadData(self):
    fileData = [("ICS-213 Forms","*.213")]
    funcParam = (gv.msgPath,fileData)
    result = ut.loadFormData(funcParam)
    ## result will be a None object if command was cancelled
    if result is not None:
        ## transfer returned dictionary to internal dictionary
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
            elif key == "s1":
                self.entryApprover.set(self.ics213FormData[key])
            elif key == "p3":
                self.entryApprPos.set(self.ics213FormData[key])
            elif key == "d1":
                self.loadedFileD1 = self.ics213FormData[key]
                self.entryDate1.set(self.ics213FormData[key])
            elif key == "t1":
                self.loadedFileT1 = self.ics213FormData[key]
                self.entryTime1.set(self.ics213FormData[key])
            elif key == "rp":
                self.replyMsg.set(self.ics213FormData[key])
            elif key == "s2":
                self.entryName.set(self.ics213FormData[key])
            elif key == "p4":
                self.entryNamePos.set(self.ics213FormData[key])
            elif key == "d2":
                self.loadedFileD2 = self.ics213FormData[key]
                self.rplyDateData.set(self.ics213FormData[key])
            elif key == "t2":
                self.loadedFileT2 = self.ics213FormData[key]
                self.rplyTimeData.set(self.ics213FormData[key])
            elif key == "file":
                ## must be accounted for. Will be needed when calling HTML template
                self.tempFile = self.ics213FormData[key]


        mb.showinfo("Load Command","ICS-213 Form data was loaded")
    else:
        ## must have cancelled the 'load' command
        pass
    return

def clearData(self):
    ## resetting form to new condition
    for key in gv.totalIcs213Keys:
        self.ics213FormData[key] = ""
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
        elif key == "s1":
            self.entryApprover.set(self.ics213FormData[key])
        elif key == "p3":
            self.entryApprPos.set(self.ics213FormData[key])
        elif key == "d1":
            self.loadedFileD1 = self.ics213FormData[key]
            self.entryDate1.set(self.ics213FormData[key])
        elif key == "t1":
            self.loadedFileT1 = self.ics213FormData[key]
            self.entryTime1.set(self.ics213FormData[key])
        elif key == "rp":
            self.replyMsg.set(self.ics213FormData[key])
        elif key == "s2":
            self.entryName.set(self.ics213FormData[key])
        elif key == "p4":
            self.entryNamePos.set(self.ics213FormData[key])
        elif key == "d2":
            self.loadedFileD2 = self.ics213FormData[key]
        elif key == "t2":
            self.loadedFileT2 = self.ics213FormData[key]
        elif key == "file":
            ## must be accounted for. Will be needed when calling HTML template
            self.ics213FormData[key] = "213"
    self.loadedFlag = False
    ## get the current date & time
    self.localGetDateTimeData(self.DateEntry,self.TimeEntry)
    ## set all date & time variables to the same date and time (current)
    self.ics213FormData["d2"] = self.ics213FormData["d1"]
    self.ics213FormData["t2"] = self.ics213FormData["t1"]

def updateData():
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
            self.ics213FormData[key] = self.origTextMsg.get(1.0,END)
            #self.origMsg.set(self.ics213FormData[key])
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
        elif key == "rp":
            self.ics213FormData[key] = self.replyMsg.get()
        elif key == "s2":
            self.ics213FormData[key] = self.entryName.get()
        elif key == "p4":
            self.ics213FormData[key] = self.entryNamePos.get()
        elif key == "d2":
            if self.rplyDateData.get()[:6] == "Date: ":
                self.ics213FormData[key] = self.rplyDateData.get()[6:]
            else:
                self.ics213FormData[key] = self.rplyDateData.get()
        elif key == "t2":
            if self.rplyTimeData.get()[:6] == "Time: ":
                self.ics213FormData[key] = self.rplyTimeData.get()[6:]
            else:
                self.ics213FormData[key] = self.rplyTimeData.get()
        elif key =="file":
            ## must be accounted for. Will be needed when calling HTML template
            self.ics213FormData[key] = "213"

    fileData = [("ICS-213 Forms","*.213")]
    funcParam = (gv.msgPath,fileData,self.ics213FormData,gv.totalIcs213Keys)
    ut.saveFormData(funcParam)
    mb.showinfo("Save","ICS-213 Form data was saved")
