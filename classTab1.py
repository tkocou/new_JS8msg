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
import henkankun as hn


#### ======================== JS8msg Control =============================
class Tab1(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)

        ## JS8msg always starts with this frame
        ## Let's check for directory structure
        ## GitHub won't upload an empty directory
        ##
        try:
            os.mkdir(gv.configPath)
        except: ## directory already exists, skip to next directory
            pass

        try:
            os.mkdir(gv.msgPath)
        except:
            pass

        try:
            os.mkdir(gv.tempPath)
        except:
            pass

        sysPlatform = platform.system()



        ## Specify column width for form
        colWidth =23

        ## Some Variables for Tab1
        self.dropdown = StringVar()
        self.group = StringVar()
        self.callsignSelected = ""
        self.callsignSelIndex = 0
        self.formDataToSend = ""
        self.labelText = "No Call"
        self.labelText2 = "No Message"
        self.groupList = ['@ALLCALL']
        self.callsignList = []
        self.messageList = []
        self.msgListIndex = 0
        self.msgSelected = {}
        self.htmlFile = ""
        self.stationCallSign = ""
        self.japaneseList = []
        self.japanFlag = FALSE




        ## build up the callsign list
        def buildCall():
            ## fetch the station callsign from JS8call
            try:
                ## if JS8call is running, the station callsign is returned
                self.stationCallSign = stationCallsign = api.getStationCallsign()
            except:
                mb.showinfo("Error!","Either JS8call is not running or TCP server in JS8call is not running.")
            self.callsignList = []
            ## if we added a group to JS8msg, let's add it to the list
            for x in self.groupList:
                self.callsignList.append(x)
            ## After adding the groups, now add the station callsign
            self.callsignList.append(stationCallsign)
            ## fetch the active callsigns from JS8call
            callList = api.getCallsigns()
            ## Add the active callsigns to the list
            if callList is not None:
                for x in callList:
                ## Only add valid callsigns
                ## Occasionally, the first callsign from JS8call is blank
                    if x:
                        self.callsignList.append(x)
            else:
                mb.showinfo("Error!","Either JS8call is not running or TCP server in JS8call is not running.")
                callList = []
            ## clear out any old list being displayed
            self.chooseList.delete(0,'end')
            ## Add the list of callsigns / groups to the callsign Listbox widget
            index=0
            for x in self.callsignList:
                self.chooseList.insert(index,x)
                index += 1

        def buildMsgList():
            ## self.messageList is a list of dictionaries
            ## Clear any existing message being displayed
            self.chooseMessage.delete(0,"end")
            ## Add the list of groups/callsigns to the messages Listbox widget
            index = 0
            for x in self.messageList:
                self.chooseMessage.insert(index,x["from"]+', '+x["iden"])
                index += 1

        def getGroup():
            ## read the group entered in the group Entry widget
            result=self.group.get().upper()
            if result != "":
                self.groupList.append(self.group.get().upper())
                buildCall()
                ## clear the displayed group from the Entry widget
                self.group.set("")

        ## Callbacks for Combobox()
        def selectMsgOption(event):
            selAction = self.chooseAction.get()
            if selAction == "Load Form":
                loadSourceData()
                self.chooseAction.set('')
            elif selAction == "Send Form Message":
                sendTxMessage()
                self.chooseAction.set('')
            elif selAction == "Store Form Message to Inbox":
                storeMessage()
                self.chooseAction.set('')
            elif selAction == "Get All Messages from Inbox":
                getMessages()
                self.chooseAction.set('')
            elif selAction == "Send Text Area":
                sendTextArea()
                self.chooseAction.set('')
            elif selAction == "Store Text Area to Inbox":
                storeTextArea()
                self.chooseAction.set('')
            elif selAction == "Activate Henkankun":
                self.japanFlag = TRUE
                setHenkankunButtons()
                self.chooseAction.set('')
            elif selAction == "Deactivate Henkankun":
                self.japanFlag = FALSE
                ut.clearWidgetForm(self.japaneseList)
                self.chooseAction.set('')

        ## Callback for ListBox Button
        def retrieve():

            ## self.chooseList.curselection() returns a tuple
            ## select the first element and assign to 'index'
            index = self.chooseList.curselection()
            if index != ():
                select = index[0]
                self.callsignSelected = self.callsignList[select]
                self.callsignSelIndex = select
                self.labelText = "Selected: "+self.callsignSelected
            else:
                ## if someone clicks on the button without selecting
                ## Default to the first element = @ALLCALL
                self.callsignSelected = self.callsignList[0]
                self.callsignSelIndex = 0
                self.labelText = "Selected: "+self.callsignList[0]

            ## Display the selected callsign
            listBoxLabel = Label(self)
            listBoxLabel.grid(column=0,row=1, sticky="sw", padx=13)
            listBoxLabel.configure(text=self.labelText, bg="#d8b8d8", pady=6, width = 23)

        def msgDisplay():
            ##
            ## this function will require modification to accomodate other forms
            ##
            formDataDict = {}
            textKey = ""
            index=self.chooseMessage.curselection()
            if index != ():
                select = index[0]
                
                ## transfer dictionary from list of dictionaries
                self.msgSelected = self.messageList[select]
                self.labelText2 = self.msgSelected["from"]+', '+self.msgSelected["iden"]

                ## the message could be wrapped and encoded
                if self.msgSelected["mesg"][:8] == 'EMCOMMG=':

                    ## pull out message from dictionary. Unwrap and decode it
                    formDecoded = ut.decodeMessage(ut.unwrapMsg(self.msgSelected["mesg"]))

                    ## the decoded message will be a string dictionary
                    ## and it has a bunch of extraneous characters which
                    ## need to be stripped out
                    ##
                    ## remove extra quotes from the string
                    formD2List = formDecoded[1:-1].replace('\"','')
                    ## remove \' from the string
                    formDList = formD2List.replace("\\'","'")
                    ## break up the long string into a list
                    formListing = formDList.split(', ')
                    ## walk through the list and build the data dictionary
                    for x in formListing:
                        ## split the string into key and data
                        xList = x.split(': ')
                        ## look for multiline text
                        ## need to add other form multi-line text data keys
                        if xList[0] == "mg":
                            textKey = "mg"
                        elif xList[0] == "rp":
                            textKey = "rp"
                        try:
                            key = xList[0]
                            data = xList[1]
                            ## add a proper key:data pair to the dictionary
                            formDataDict[key] = data
                        except IndexError:
                            ## found multiline text, concatenate lines
                            if len(x[0]) > 0:
                                formDataDict[textKey] = formDataDict[textKey]+'\n'+xList[0]
                    
                    formData = formDataDict

                    ## save data in case a reply is needed
                    ## create a unique file name to save the dictionary
                    ## Use the extension which is part of the data dictionary
                    ##
                    ## need to extract file extension and reference it
                    saveFile = self.stationCallSign+self.msgSelected["iden"]+'_recvd.'+formData["file"]
                    ## complete the path
                    saveFilePath = os.path.join(gv.msgPath,saveFile)
                    fh = open(saveFilePath, "w")
                    ##
                    ## use file ext. to reference appropriate key list
                    ##
                    if formData["file"] == "213":
                        keyFile = gv.totalIcs213Keys
                    ##
                    ## write each line out based on the key
                    for key in keyFile:
                        fh.write(key+':'+formData[key]+'\n')
                    fh.close()

                    ## formdata is dictionary
                    #formKeys = gv.totalIcs213Keys
                    templateFile = ""
                    if formData["file"] == "213":
                        templateFile = os.path.join(gv.templatePath,"ics213_template.html")
                    ## add 'elif' to use a HTML template for other forms

                    ## outputHtml gives back a HTML document
                    ## parse off the 'file' key from the formKeys, not needed!
                    result = ut.outputHtml(formData, keyFile[:-1], templateFile)

                    ## write the form to a file for the web browser
                    self.htmlFile = gv.tempPath+"temp.html"
                    fh = open(self.htmlFile,"w")
                    for x in result:
                        fh.writelines(x)
                    fh.close()

                    ## clear out text box
                    self.messageTextBox.delete(1.0,END)
                    ## build the URL for the web browser
                    url = 'file://'+os.path.realpath(self.htmlFile)
                    ## open the HTML file in a web browser
                    wb.open(url)
                    self.messageTextBox.delete(1.0,END)
                    self.messageTextBox.insert(END,"If you do not see a webpage, check a web browser for ICS Form")
                    ## Sometimes the web browser will send extra messages to the
                    ## Python console
                    ## Clear the Python console of messages from web browser
                    x =1
                    while x < 3:
                        ## wait 1 second and then clear
                        ut.clearConsole()
                        x += 1

                else:
                    ## display regular text in Text box
                    formData = self.msgSelected["mesg"]
                    self.messageTextBox.delete(1.0,END)
                    if formData[:6] == "ENC IN" :
                        self.messageTextBox.insert(END,formData[:-2])
                        self.japanFlag = TRUE
                        setHenkankunButtons()
                    else:
                        self.messageTextBox.insert(END,formData+'\n')
                ## update the display and show the selected message id
                listBoxLabel2 = Label(self)
                listBoxLabel2.grid(column=0,row=1, sticky="se", padx=13)
                listBoxLabel2.configure(text=self.labelText2, bg="#d8b8d8", pady=6, width = 23)

        def setHenkankunButtons():
            ## reset list variable
            self.japaneseList = []

            ## add buttons and track widgets

            encodeButton1 = Button(self, text="Encode Shift-JIS", command=encodeTextAreaJIS)
            encodeButton1.configure(bg="yellow1", width=12, height=2)
            encodeButton1.grid(column=1,row=3, sticky="nw", pady=0, padx=10)
            self.japaneseList.append(encodeButton1)

            decodeButton1 = Button(self, text="Decode Shift-JIS", command=decodeTextAreaJIS)
            decodeButton1.configure(bg="green1", width=12, height=2)
            decodeButton1.grid(column=1,row=4, sticky="nw", pady=0, padx=10)
            self.japaneseList.append(decodeButton1)

            encodeButton2 = Button(self, text="Encode UTF-8", command=encodeTextAreaUTF8)
            encodeButton2.configure(bg="yellow1", width=12, height=2)
            encodeButton2.grid(column=1,row=5, sticky="nw", pady=0, padx=10)
            self.japaneseList.append(encodeButton2)

            decodeButton2 = Button(self, text="Decode UTF-8", command=decodeTextAreaUTF8)
            decodeButton2.configure(bg="green1", width=12, height=2)
            decodeButton2.grid(column=1,row=6, sticky="nw", pady=0, padx=10)
            self.japaneseList.append(decodeButton2)

        def encodeTextAreaJIS():
            if self.japanFlag:
                hn.encodeShiftJIS(self.messageTextBox)
            else:
                pass

        def decodeTextAreaJIS():
            if self.japanFlag:
                hn.decodeShiftJIS(self.messageTextBox)
            else:
                pass

        def encodeTextAreaUTF8():
            if self.japanFlag:
                hn.encodeUTF8(self.messageTextBox)
            else:
                pass

        def decodeTextAreaUTF8():
            if self.japanFlag:
                hn.decodeUTF8(self.messageTextBox)
            else:
                pass
        
        #### main display of widgets ####
        topRow =0
        ## Add a label and combobox to the display
        self.label = Label(self, text="Select =-> ")
        self.label.grid(column=0,row=topRow, sticky="w")
        self.chooseAction = ttk.Combobox(self, width=colWidth, textvariable = self.dropdown, background="#f8d8d8")
        self.chooseAction['values'] = ["Load Form","Send Form Message","Store Form Message to Inbox","Get All Messages from Inbox","Send Text Area","Store Text Area to Inbox","Activate Henkankun","Deactivate Henkankun"]
        self.chooseAction.grid(column=0,row=topRow, sticky="w", padx=80)
        ## Note: callback function must preceed the combobox widget
        self.chooseAction.bind('<<ComboboxSelected>>', selectMsgOption)

        ## Add a group widgets
        self.groupLabel = Button(self, text="Add Group and Click =-> ", command=getGroup)
        self.groupLabel.grid(column=0, row=topRow, sticky="e", padx=120)
        self.groupEntry = Entry(self, textvariable=self.group, width=14, bg="green1")
        self.groupEntry.grid(column=0, row=topRow, sticky="e")


        ## Quit program button
        quitButton = Button(self, text="Quit", command=lambda:self.quitProgram())
        quitButton.configure(bg="blue", fg="white")
        quitButton.grid(column=1,row=topRow, sticky = "w", padx=10)

        ## set the height of the scrollbars
        vertPad = 32

        ## Next few widgets need to be populated from live JS8call
        listRow = 1
        selRow = 2

        ## Added an Update button for callsigns Listbox
        self.updateButton = Button(self, text = "Update Callsigns", command=buildCall)
        self.updateButton.grid(column=0, row=listRow, sticky="nw")
        self.updateButton.configure(bg="yellow1", width=22)

        ## Add a button to select a callsign from the Listbox for transmitting or the JS8call inbox
        self.listBoxButton = Button(self, text = "Select Callsign & Click here", command=retrieve)
        self.listBoxButton.configure(bg="yellow1", width=22)
        self.listBoxButton.grid(column=0, row=selRow, sticky="w")

        ## Add the callsign Listbox widget
        self.chooseList = Listbox(self, selectmode=SINGLE, selectbackground="#f8f8d8", bg="green1", width=23)
        buildCall()
        self.chooseList.grid(column=0,row = listRow, padx = 15, pady=vertPad, sticky="nw")
        self.chooseList.activate(self.callsignSelIndex)
        self.chooseList.see(self.callsignSelIndex)
        ## add a scrollbar widget for when the callsign list size exceeds the displayed area
        self.scrollBar = Scrollbar(self, orient=VERTICAL, command=self.chooseList.yview)
        self.scrollBar.grid(column=0, row= listRow, pady=vertPad, sticky="nsw")
        ## Link the scrollbar widget to the Listbox widget
        self.chooseList['yscrollcommand'] = self.scrollBar.set


        ## Added button for selecting from the message list 
        self.listMsgButton = Button(self, text = "Select Message & Click here", command=msgDisplay)
        self.listMsgButton.configure(bg="green1", width=22)
        self.listMsgButton.grid(column=0, row=selRow, sticky="se")
        ## Added the messages Listbox widget
        self.chooseMessage = Listbox(self, selectmode=SINGLE, selectbackground="#f8f8d8",bg="green1", width=24)
        buildMsgList()
        self.chooseMessage.grid(column=0, row=listRow, padx=0, pady=vertPad, sticky="ne")
        self.chooseMessage.activate(self.msgListIndex)
        self.chooseMessage.see(self.msgListIndex)
        ## Added a scrollbar widget for when the messages list size exceeds the displayed area
        self.msgScrollBar = Scrollbar(self, orient=VERTICAL, command=self.chooseMessage.yview)
        ## adjust offset per OS due to font differences
        if sysPlatform == "Windows":
            self.msgScrollBar.grid(column=0, row=listRow, pady=vertPad, sticky="nse", padx=150) # windows?
        elif sysPlatform == "Linux":
            self.msgScrollBar.grid(column=0, row=listRow, pady=vertPad, sticky="nse", padx=196) # linux?
        ## Link the scrollbar widget to the Listbox widget
        self.chooseMessage['yscrollcommand'] = self.msgScrollBar.set

        self.clearTextAreaButton = Button(self, text="Clear Text Area", command=lambda: clearTextArea())
        self.clearTextAreaButton.configure(bg="blue", fg="white", width=22)
        self.clearTextAreaButton.grid(column=0, row=selRow, sticky="sew", padx=200)
                


        txtRow = 3
        ## Added a general purpose Text area to the display
        self.messageTextBox = Text(self)
        self.messageTextBox.grid(column=0, row=txtRow, sticky="nse", padx=0, rowspan=4)
        self.messageTextBox.configure(background="#f8d8d8", wrap="word", height=15, width=73)
        self.messageTextBox.delete(1.0,END)
        self.messageTextBox.insert(END,self.formDataToSend)
        ## add a scrollbar widget for when the callsign list size exceeds the displayed area
        self.scrollBarText = Scrollbar(self, orient=VERTICAL, command=self.messageTextBox.yview)
        self.scrollBarText.grid(column=0, row= txtRow, sticky="nsw", rowspan =4)
        ## Link the scrollbar widget to the Listbox widget
        self.messageTextBox['yscrollcommand'] = self.scrollBar.set

        ## added buttons to invoke the Japanese encoding functions written by JE6VGZ
        if self.japanFlag:
            setHenkankunButtons()
#### Form messages will be 'wrapped' so as to destinguish between normal text
#### and a form which will need displaying in the web browser
        def sendTxMessage():
            ## valid if you selected a destination callsign
            if self.callsignSelected:
                ## use the contents of the Text area
                ## which is stored in self.formDataToSend
                ## send it to JS8call for transmitting immediately
                ## self.formDataToSend is encoded and wrapped in 'api.sendLive'

                result = api.sendLive(self.callsignSelected,self.formDataToSend)
                if result is None:
                    mb.showwarning(None,"Problem with JS8call transmitting message.")
            else:
                ## remind them to select a destination callsign
                mb.showinfo("No callsign selected","Select one from the list of callsigns.")

        def sendTextArea():
            result = loadTextArea()
            if result == None:
                return result
            if self.callsignSelected:
                if self.japanFlag:
                    self.formDataToSend = "MSG "+self.formDataToSend
                result = api.sendLiveText(self.callsignSelected,self.formDataToSend)
                if result is None:
                    mb.showwarning(None,"Problem with JS8call transmitting message.")
            else:
                ## remind them to select a destination callsign
                mb.showinfo("No callsign selected","Select one from the list of callsigns.")

        def storeTextArea():
            result = loadTextArea()
            if result == None:
                return result
            if self.callsignSelected:
                #if self.japanFlag:
                #    self.formDataToSend = "MSG "+self.formDataToSend
                result = api.sendTextAreaToInbox(self.callsignSelected,self.formDataToSend)
                if result is not None:
                    mb.showinfo("Result","Message is stored in Inbox!")
                else:
                    mb.showwarning(None,"Problem with JS8call storing message.")
            else:
                mb.showinfo("No callsign selected","Select one from the list of callsigns.")

        def storeMessage():
            ## valid if you selected a destination callsign
            if self.callsignSelected:
                ## self.formDataToSend is encoded and wrapped in 'api.sendToInbox'
                result = api.sendToInbox(self.callsignSelected,self.formDataToSend)
                if result is not None:
                    mb.showinfo("Result","Message is stored in Inbox!")
                else:
                    mb.showwarning(None,"Problem with JS8call storing message.")
            else:
                mb.showinfo("No callsign selected","Select one from the list of callsigns.")

        def getMessages():
            ## getInbox returns a list of dictionaries from JS8call
            result = api.getInbox()
            if result:
                ## self.messageList will hold a list of dictionaries
                ## each dictionary will hold callsign, message text, and messageID
                ## if wrapped, the message remains the same
                ## display needs the wrap to differenciate between forms and text
                self.messageList = result
                self.chooseMessage.delete(0,END)
                index = 0
                for x in self.messageList:
                    self.chooseMessage.insert(index,x["from"]+', '+x["iden"])
                    index += 1
            else:
                mb.showwarning(None,"Problem fetching messages from inbox")



        def loadSourceData():
            fileData = [("ICS-213 Forms","*.213")]
            funcParam = (gv.msgPath,fileData)
            ## returns a dictionary
            result = ut.loadFormData(funcParam)
            ## convert from a dictionary to a string 
            formDataToSend = ut.dictToString(result)
            ## update Text box
            self.messageTextBox.delete(1.0,END)
            self.messageTextBox.insert(END,formDataToSend+'\n')
            self.formDataToSend = formDataToSend

        def loadTextArea():
            ## fetch the text within the Text box
            try:
                self.formDataToSend = self.messageTextBox.get(1.0,END)
                #print("Length of text: ", len(self.formDataToSend))
                if len(self.formDataToSend) == 1:
                    mb.showwarning(None,"Type a text message in the Text Area.")
                    return None
                return self.formDataToSend
            except:
                mb.showwarning(None,"Problem fetching text.")
                return None

        def clearTextArea():
            self.messageTextBox.delete(1.0,END)
            return
            

    def quitProgram(self):
        ## check if the temporary HTML file exists
        if self.htmlFile:
            ## delete it
            os.remove(self.htmlFile)
        sys.exit()