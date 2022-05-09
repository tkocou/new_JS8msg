##
## JS8msg is a copyrighted program written by Thomas Kocourek, N4FWD
## This program is released under the GPL v3 license
## 
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
import henkankun as hn
#from operator import itemgetter, attrgetter

debug_flag = gv.debug_flag_Tab1

#### ======================== JS8msg Control =============================
class Tab1(Frame):
    def __init__(self,parent,controller):
        Frame.__init__(self,parent,controller)
        self.controller = controller
        self.frame = parent
        self.widgets = []

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
        colWidth =28

        ## Some Variables for Tab1
        self.dropdown = StringVar()
        self.group = StringVar()
        self.callsignSelected = ""
        self.callsignSelIndex = 0
        self.formDataToSend = ""
        self.webpage_display = ""
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
        self.japanFlag = False
        self.japan_encoded_flag = False
        self.segmented_messages = []
        self.chunked = True

        ## build up the callsign list
        def buildCall():
            ## fetch the station callsign from JS8call
            try:
                ## if JS8call is running, the station callsign is returned
                self.stationCallSign = api.getStationCallsign()
            except:
                mb.showinfo("Error!","Either JS8call is not running or TCP server in JS8call is not running.")
            self.callsignList = []
            ## if we added a group to JS8msg, let's add it to the list
            for x in self.groupList:
                self.callsignList.append(x)
            ## After adding the groups, now add the station callsign
            self.callsignList.append(self.stationCallSign)
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
                mb.showinfo("Error!","Either JS8call is not running or TCP/UDP server in JS8call is not running.")
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
                if result[:1] != '@':
                    result = '@'+result
                self.groupList.append(result)
                buildCall()
                ## clear the displayed group from the Entry widget
                self.group.set("")

        ## Callbacks for Combobox()
        def selectMsgOption(event):
            selAction = self.chooseAction.get()
            if selAction == "Load Form":
                loadSourceData()
                self.chooseAction.set('')
            elif selAction == "Send Form Live":
                sendTxMessage()
                self.chooseAction.set('')
            elif selAction == "Store Form Message to Inbox":
                storeMessage()
                clearTextArea()
                self.chooseAction.set('')
            elif selAction == "Display form in webpage":
                webpage_form()
                self.chooseAction.set('')
            elif selAction == "Get All Messages from Inbox":
                if debug_flag:
                    print("Invoking function getMessages.\n")
                getMessages()
                self.chooseAction.set('')
            elif selAction == "Send Text Area Chunked":
                sendTextArea()
                self.chooseAction.set('')
            elif selAction == "Send Text Area As Is":
                self.chunked = False
                sendTextArea()
                self.chunked = True
                self.chooseAction.set('')
            elif selAction == "Store Text Area Chunked to Inbox":
                storeTextArea()
                self.chooseAction.set('')
            elif selAction == "Store Text Area As Is to Inbox":
                self.chunked = False
                storeTextArea()
                self.chunked = True
                self.chooseAction.set('')
            elif selAction == "Activate Henkankun":
                self.japanFlag = TRUE
                setHenkankunButtons()
                self.chooseAction.set('')
            elif selAction == "Deactivate Henkankun":
                self.japanFlag = FALSE
                ut.clearWidgetForm(self.japaneseList)
                self.japaneseList = []
                self.chooseAction.set('')

        ## Callback for ListBox Button
        def retrieve():

            ## self.chooseList.curselection() returns a tuple
            ## select the first element and assign to 'index'
            index = self.chooseList.curselection()
            if debug_flag:
                print("index: ",index)
            if index != ():
                select = index[0]
                if debug_flag:
                    print("callsignList: ",self.callsignList[select])
                self.callsignSelected = self.callsignList[select]
                self.callsignSelIndex = select
                self.labelText = "Selected: "+self.callsignSelected
            else:
                ## if someone clicks on the button without selecting
                ## Default to the first element = @ALLCALL
                self.callsignSelected = self.callsignList[0]
                self.callsignSelIndex = 0
                self.labelText = "Selected: "+self.callsignList[0]

        def msgDisplay():
            ##
            ## this function will require modification to accomodate other forms
            ##
            formDataDict = {}
            textKey = ""
            index=self.chooseMessage.curselection()
            if debug_flag:
                print("classTab1: msgDisplay: index: ",index)
            if index != ():
                ## if no message was selected, default to the first message
                select = index[0]
                
                ## transfer dictionary from list of dictionaries
                self.msgSelected = self.messageList[select]
                self.labelText2 = self.msgSelected["from"]+', '+self.msgSelected["iden"]
                if debug_flag:
                    print("classTab1: msgDisplay: self.msgSelected: ",self.msgSelected)
                ## the message could be wrapped and encoded
                if self.msgSelected["mesg"][:8] == 'EMCOMMG^':

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
                    html_result = ut.outputHtml(formData, keyFile[:-1], templateFile)

                    ## write the form to a file for the web browser
                    self.htmlFile = os.path.join(gv.tempPath,"temp.html")
                    fh = open(self.htmlFile,"w")
                    for x in html_result:
                        fh.writelines(x)
                    fh.close()
                    gv.html_file = self.htmlFile

                    ## clear out text box
                    self.messageTextBox.delete(1.0,END)
                    ## build the URL for the web browser
                    url = 'file://'+os.path.realpath(self.htmlFile)
                    if debug_flag:
                        print("classTab1: msgDisplay: self.htmlFile: ",self.htmlFile)
                        print("classTab1: msgDisplay: url: ",url)
                    ## open the HTML file in a web browser
                    wb.open(url)
                    self.messageTextBox.delete(1.0,END)
                    mb_text_message = """If you do not see a webpage, check an existing, opened web browser for ICS Form.
                    \nThe web browser might print extranous messages to the Python console.
                    \nAny new reports will overwite the existing HTML file.
                    \n\nTo make a hard copy of the report, use the print function of the web browser.
                    """
                    self.messageTextBox.insert(END,mb_text_message)
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

            else:
                mb.showinfo("Error!","The message box is empty. Please get the messages from the JS8call inbox.")

        def setHenkankunButtons():
            ## reset list variable
            self.japaneseList = []
            buttonRow = 6
            ## add buttons and track widgets

            encodeButton1 = Button(self.frame, text="Encode Shift-JIS", command=encodeTextAreaJIS)
            encodeButton1.configure(bg="yellow1", width=12, height=2)
            encodeButton1.grid(column=1,row=buttonRow, sticky="nw", pady=0, padx=10)
            self.japaneseList.append(encodeButton1)


            decodeButton1 = Button(self.frame, text="Decode Shift-JIS", command=decodeTextAreaJIS)
            decodeButton1.configure(bg="green1", width=12, height=2)
            decodeButton1.grid(column=1,row=buttonRow+1, sticky="nw", pady=0, padx=10)
            self.japaneseList.append(decodeButton1)
    

            encodeButton2 = Button(self.frame, text="Encode UTF-8", command=encodeTextAreaUTF8)
            encodeButton2.configure(bg="yellow1", width=12, height=2)
            encodeButton2.grid(column=1,row=buttonRow+2, sticky="nw", pady=0, padx=10)
            self.japaneseList.append(encodeButton2)


            decodeButton2 = Button(self.frame, text="Decode UTF-8", command=decodeTextAreaUTF8)
            decodeButton2.configure(bg="green1", width=12, height=2)
            decodeButton2.grid(column=1,row=buttonRow+3, sticky="nw", pady=0, padx=10)
            self.japaneseList.append(decodeButton2)


        def encodeTextAreaJIS():
            if self.japanFlag:
                hn.encodeShiftJIS(self.messageTextBox)
                self.japan_encoded_flag = True
            else:
                pass

        def decodeTextAreaJIS():
            if self.japanFlag:
                hn.decodeShiftJIS(self.messageTextBox)
                self.japan_encoded_flag = False
            else:
                pass

        def encodeTextAreaUTF8():
            if self.japanFlag:
                hn.encodeUTF8(self.messageTextBox)
                self.japan_encoded_flag = True
            else:
                pass

        def decodeTextAreaUTF8():
            if self.japanFlag:
                hn.decodeUTF8(self.messageTextBox)
                self.japan_encoded_flag = False
            else:
                pass
        

        ##
        ## Do an initial check to see if JS8call is running
        try:
            ## if JS8call is running, the station callsign is returned
            self.stationCallSign = api.getStationCallsign()
        except:
            mb.showinfo("Error!","Either JS8call is not running or TCP server in JS8call is not running.")
            
        #### main display of widgets ####
        topRow = 0
        buttonRow = 2
        listRow = 1
        listBoxRow = 3
        seldCM_Row = 4
        selCMRow = 5
        selTextRow = 6
        ## Add a label and combobox to the display
        self.label = tk.Label(self.frame, text="Select =-> ")
        self.label.grid(column=0,row=topRow, sticky="w")
        self.widgets.append(self.label)
        self.chooseAction = ttk.Combobox(self.frame, width=colWidth, textvariable = self.dropdown, background="#f8d8d8")
        self.chooseAction['values'] = ["Load Form","Send Form Live","Store Form Message to Inbox","Display form in webpage","Get All Messages from Inbox","Send Text Area Chunked","Send Text Area As Is","Store Text Area Chunked to Inbox","Store Text Area As Is to Inbox","Activate Henkankun","Deactivate Henkankun"]
        self.chooseAction.grid(column=0,row=topRow, sticky="w", padx=80)
        ## Note: callback function must preceed the combobox widget
        self.chooseAction.bind('<<ComboboxSelected>>', selectMsgOption)
        self.widgets.append(self.chooseAction)


        ## Add a group widgets
        self.groupLabel = tk.Button(self.frame, text="Add Group and Click =->", command=getGroup)
        self.groupLabel.grid(column=0, row=topRow, sticky="e", padx=90)
        self.widgets.append(self.groupLabel)
        
        self.groupEntry = tk.Entry(self.frame, textvariable=self.group, width=10, bg="green1")
        self.groupEntry.grid(column=0, row=topRow, sticky="e")
        self.widgets.append(self.groupEntry)

        ## Display the selected callsign
        self.listBoxLabel = Label(self,text=self.labelText)
        self.listBoxLabel.grid(column=0,row=buttonRow, sticky="w", padx=50)
        self.listBoxLabel.configure( bg="#d8b8d8", pady=6, width = 23)
        self.widgets.append(self.listBoxLabel)
        
        self.listBoxLabel2 = Label(self,text=self.labelText2)
        self.listBoxLabel2.grid(column=0,row=buttonRow, sticky="e", padx=50)
        self.listBoxLabel2.configure( bg="#d8b8d8", pady=6, width = 23)
        self.widgets.append(self.listBoxLabel2)
        
        ## set the height of the scrollbars
        vertPad = 6

        ## Added an Update button for callsigns Listbox
        self.updateButton = tk.Button(self.frame, text = "Update Callsigns", command=buildCall)
        self.updateButton.grid(column=0, row=listRow, sticky="nw")
        self.updateButton.configure(bg="yellow1")
        self.widgets.append(self.updateButton)
 
        ## Add a button to select a callsign from the Listbox for transmitting or the JS8call inbox
        self.listBoxButton = tk.Button(self.frame, text = "Select Callsign & Click here", command=retrieve)
        self.listBoxButton.configure(bg="yellow1", width=22)
        self.listBoxButton.grid(column=0, row=selCMRow, sticky="nw")
        self.widgets.append(self.listBoxButton)

        ## Add the callsign Listbox widget
        ######
        self.chooseList = tk.Listbox(self.frame, selectmode=SINGLE, selectbackground="#f8f8d8", bg="green1", width=23)
        buildCall()
        self.chooseList.grid(column=0,row = listBoxRow, padx = 15, pady=vertPad, sticky="nw")
        self.chooseList.activate(self.callsignSelIndex)
        self.chooseList.see(self.callsignSelIndex)
        self.widgets.append(self.chooseList)
        ## add a scrollbar widget for when the callsign list size exceeds the displayed area
        self.scrollBar = tk.Scrollbar(self.frame, orient=VERTICAL, command=self.chooseList.yview)
        self.scrollBar.grid(column=0, row= listBoxRow, pady=vertPad, sticky="nsw")
        ## Link the scrollbar widget to the Listbox widget
        self.chooseList['yscrollcommand'] = self.scrollBar.set
        self.widgets.append(self.scrollBar)

        ## Added button for selecting from the message list 
        self.listMsgButton = tk.Button(self.frame, text = "Select Message & Click here", command=msgDisplay)
        self.listMsgButton.configure(bg="green1", width=22)
        self.listMsgButton.grid(column=0, row=selCMRow, sticky="ne")
        self.widgets.append(self.listMsgButton)
        
        ## Added the messages Listbox widget
        ######
        self.chooseMessage = tk.Listbox(self.frame, selectmode=SINGLE, selectbackground="#f8f8d8",bg="green1", width=24)
        buildMsgList()
        self.chooseMessage.grid(column=0, row=listBoxRow, padx=0, pady=vertPad, sticky="ne")
        self.chooseMessage.activate(self.msgListIndex)
        self.chooseMessage.see(self.msgListIndex)
        self.widgets.append(self.chooseMessage)
        ## Added a scrollbar widget for when the messages list size exceeds the displayed area
        self.msgScrollBar = tk.Scrollbar(self.frame, orient=VERTICAL, command=self.chooseMessage.yview)
        ## adjust offset per OS due to font differences
        if sysPlatform == "Windows":
            self.msgScrollBar.grid(column=0, row=listBoxRow, pady=vertPad, sticky="nse", padx=150) # windows?
        elif sysPlatform == "Linux":
            self.msgScrollBar.grid(column=0, row=listBoxRow, pady=vertPad, sticky="nse", padx=196) # linux?
        ## Link the scrollbar widget to the Listbox widget
        self.chooseMessage['yscrollcommand'] = self.msgScrollBar.set
        self.widgets.append(self.msgScrollBar)

        self.clearTextAreaButton = tk.Button(self.frame, text="Clear Text Area", command=lambda: clearTextArea())
        self.clearTextAreaButton.configure(bg="blue", fg="white", width=22)
        self.clearTextAreaButton.grid(column=0, row=selCMRow, sticky="new", padx=200)
        self.widgets.append(self.clearTextAreaButton)

        ## Added a general purpose Text area to the display
        ######
        vert_pady = 6
        self.messageTextBox = tk.Text(self.frame)
        self.messageTextBox.grid(column=0, row=selTextRow, sticky="nse", padx=0, rowspan=4, pady = vert_pady)
        self.messageTextBox.configure(background="#f8d8d8", wrap="word", height=17, width=73)
        self.messageTextBox.delete(1.0,END)
        self.messageTextBox.insert(END,self.formDataToSend)
        self.widgets.append(self.messageTextBox)
        ## add a scrollbar widget for when the callsign list size exceeds the displayed area
        self.scrollBarText = tk.Scrollbar(self.frame, orient=VERTICAL, command=self.messageTextBox.yview)
        self.scrollBarText.grid(column=0, row= selTextRow, sticky="nsw", rowspan =4, pady = vert_pady)
        ## Link the scrollbar widget to the Listbox widget
        self.messageTextBox['yscrollcommand'] = self.scrollBar.set
        self.widgets.append(self.scrollBarText)
        
        ## we've collected a list of widgets, let's transfer it to the global dictionary
        gv.widget_list_dict["Tab1"] = self.widgets
        

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
                ## after encoding it and then wrapping it
                intermediate_data = ut.wrapMsg(ut.encodeMessage(self.formDataToSend))
                list_to_send = create_data_list(intermediate_data)
                for text_mesg in list_to_send:
                    text_mesg = "MSG "+text_mesg
                    result = api.sendLive(self.callsignSelected,text_mesg)
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
                if self.chunked:
                    if self.japan_encoded_flag: 
                        self.formDataToSend = "MSG "+self.formDataToSend
                    list_to_send = create_data_list(self.formDataToSend)
                    for text_mesg in list_to_send:
                        result = api.sendLive(self.callsignSelected,text_mesg)
                        if result is None:
                            mb.showwarning(None,"Problem with JS8call transmitting message.")
                else:
                    result = api.sendLive(self.callsignSelected,text_mesg)
                    if result is None:
                        mb.showwarning(None,"Problem with JS8call transmitting message.")
                mb.showinfo("Result","Text Area was sent")
            else:
                ## remind them to select a destination callsign
                mb.showinfo("No callsign selected","Select one from the list of callsigns.")

        def storeTextArea():
            result = loadTextArea()
            if result == None:
                return result
            if self.callsignSelected:
                if self.chunked:
                    list_to_send = create_data_list(self.formDataToSend)
                    for text_mesg in list_to_send:
                        result = api.sendToInbox(self.callsignSelected,text_mesg)
                        if result is None:
                            mb.showwarning(None,"Problem with JS8call storing message.")
                else:
                    result = api.sendToInbox(self.callsignSelected,text_mesg)
                    if result is None:
                        mb.showwarning(None,"Problem with JS8call storing message.")
                mb.showinfo("Result","Text Area is stored in Inbox!")
            else:
                mb.showinfo("No callsign selected","Select one from the list of callsigns.")

        def storeMessage():
            ## valid if you selected a destination callsign
            if self.callsignSelected:
                intermediate_data = ut.wrapMsg(ut.encodeMessage(self.formDataToSend))
                list_to_send = create_data_list(intermediate_data)
                if debug_flag:
                    print("list_to_send: ",list_to_send)
                for text_mesg in list_to_send:
                    if debug_flag:
                        print("test_mesg: ",text_mesg)
                    result = api.sendToInbox(self.callsignSelected,text_mesg)
                    if debug_flag:
                        print("storeMessage result: ",result)
                    if result is None:
                        mb.showwarning(None,"Problem with JS8call storing message.")
                mb.showinfo("Result","Message block is stored in Inbox!")
            else:
                mb.showinfo("No callsign selected","Select one from the list of callsigns.")

        def getMessages():
            ## getInbox returns a list of dictionaries from JS8call
            api_result = None
            try:
                if debug_flag:
                    print("\ninvoking JS8API.getInbox.")
                api_result = api.getInbox()
                if debug_flag:
                    print("\nclassTab1: getMessages: api_result: ",api_result)
            except:
                pass
            if api_result:
                ## result will hold a list of dictionaries
                ## each dictionary will hold callsign, message text, and messageID
                ##
                ## Check for segmented message
                mm_list = []
                plain_list = []
                self.chooseMessage.delete(0,END)
                #self.messageList = []
                if debug_flag:
                    print("\n\nclassTab1: getMessages: len(z): ",len(api_result))
                for z in api_result:
                    if debug_flag:
                        print("\nclassTab1: getMessages: Dict: ",z)
                    if z["TEXT"][:5] == "TAG0X":
                        if debug_flag:
                            print("\nclassTab1: getMessages: z['TEXT']:",z["TEXT"])
                        ## we have a segmented message, process it
                        multi_message = {}
                        multi_message["from"] = z["FROM"]
                        pieces = z["TEXT"].split(":",2)
                        if debug_flag:
                            print("\nclassTab1: getMessages: pieces:",pieces)
                        multi_message["tag"]=pieces[0][3:]
                        multi_message["seq"]=pieces[1]
                        multi_message["tbit"]=pieces[2]
                        mm_list.append(multi_message)
                        if debug_flag:
                            print("\npieces seq",pieces[1])
                    else:
                        plain_dict = {}
                        plain_dict["from"] = z["FROM"]
                        plain_dict["mesg"] = z["TEXT"]
                        plain_dict["iden"] = z["_ID"]
                        plain_list.append(plain_dict)
                ##
                ## we have walked through the list of messages 
                ## and ID'ed the tagged messages as well as separated the plain text messages
                self.messageList = []
                ##
                ## Process plain text messages first
                index = 0
                for x in plain_list:
                    self.chooseMessage.insert(index,x["from"]+', '+x["iden"])
                    self.messageList.append(x)
                    index += 1

                ## now process the segmented messages
                ## 'mm_list' is a list of dictionaries
                ## NOTE: processing will take several passes to sort out the 'mess'
                ## JS8call does not store messages in any particular order
                ##
                tag_list = []
                ## lets gather the tags
                for x in mm_list:
                    tag_list.append(x["tag"])
                    
                tags_unique = []                
                ## let's filter out the duplicates
                for x in tag_list:
                    if x not in tags_unique:
                        tags_unique.append(x)
                if debug_flag:
                    print("\nclassTab1: getMessages: Unique tags: ",tags_unique)
                ## let's separate out all the pieces of each unique message
                for tag in tags_unique:
                    message_count = 0
                    bundle = []
                    if debug_flag:
                        print("\nclassTab1: getMessages: tag: ",tag)
                    for mesg in mm_list:
                        #if debug_flag:
                        #    print("\nclassTab1: getMessages: mesg in mm_list: ",mesg)
                        if mesg['tag'] == tag:
                            mesg_unique = {}
                            from_key_data = mesg["from"]
                            iden_key_data = tag
                            ## build a dictionary of all the pieces of a message
                            mesg_unique["tag"] = mesg["tag"]
                            mesg_unique["from"] = mesg["from"]
                            mesg_unique["seq"] = mesg["seq"]
                            mesg_unique["tbit"] = mesg["tbit"]
                            ## make a list of the dictionary segments
                            if debug_flag:
                                print("\nclassTab1: getMessages: mesg_unique: ",mesg_unique)
                            bundle.append(mesg_unique)
                            message_count += 1
                    if debug_flag:
                        print("\nclassTab1: getMessages: message_count: ",message_count)
                        print("\nclassTab1: getMessages: bundle: ",bundle)
                    ## now sort the list of dictionaries
                    sorted_list = dictionary_bubble_sort(bundle)
                    if debug_flag:
                        print("\nclassTab1: getMessages: len(sorted_list): ",len(sorted_list))
                    if debug_flag:
                        print("\nclassTab1: getMessages: sorted_list: ",sorted_list)
                    result_text = ""
                    reconstructed_mesg = {}
                    ## concantanate the text pieces
                    for y in sorted_list:
                        result_text += y["tbit"]
                           
                    reconstructed_mesg["from"] = from_key_data
                    reconstructed_mesg["mesg"] = result_text
                    reconstructed_mesg["iden"] = iden_key_data
                    if debug_flag:
                        print("\nclassTab1: getMessage: tag/reconstructed_mesg: ",reconstructed_mesg["iden"],' / ',reconstructed_mesg)
                    ## Let's append the recon'd message 
                    self.segmented_messages.append(reconstructed_mesg)
                    ## add the reconstructed message to the List widget
                    self.chooseMessage.insert(index,reconstructed_mesg["from"]+', '+reconstructed_mesg["iden"])
                    self.messageList.append(reconstructed_mesg)
                    sorted_list = []
                    ## 'index' continues from the last position in 'self.chooseMessage'
                    index += 1
            else:
                mb.showwarning(None,"Message Inbox is empty.")

        def webpage_form():
            ## load a file and return the dictionary
            webpage_display = loadSourceData()
            templateFile = ""
            if webpage_display["file"] == "213":
                ## create a path to the appropriate html template
                templateFile = os.path.join(gv.templatePath,"ics213_template.html")
                keyFile = gv.totalIcs213Keys
            ## A string is returned
            html_result = ut.outputHtml(webpage_display, keyFile[:-1], templateFile)
            
            ## write the form to a file for the web browser
            self.htmlFile = os.path.join(gv.tempPath,"temp.html")
            fh = open(self.htmlFile,"w")
            for x in html_result:
                fh.writelines(x)
            fh.close()
            gv.html_file = self.htmlFile
            ## build the URL for the web browser
            url = 'file://'+os.path.realpath(self.htmlFile)
            ## open the HTML file in a web browser
            wb.open(url)
            self.messageTextBox.delete(1.0,END)
            mb_text_message = """If you do not see a webpage, check an existing, opened web browser for ICS Form.
            \nThe web browser might print extranous messages to the Python console.
            \nAny new reports will overwite the existing HTML file.
            \n\nTo make a hard copy of the report, use the print function of the web browser.
            """
            self.messageTextBox.insert(END,mb_text_message)
             ## Clear the Python console of messages from web browser
            x =1
            while x < 3:
                ## wait 1 second and then clear
                ut.clearConsole()
                x += 1

            

        def loadSourceData():
            ## fix for additional ICS forms
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
            ## return a dictionary. 
            ## Should be ignored for functions not looking for a returned result
            return result

        def loadTextArea():
            ## fetch the text within the Text box
            try:
                self.formDataToSend = self.messageTextBox.get(1.0,END)
                if debug_flag:
                    print("classTab1: loadTextArea: Length of text: ", len(self.formDataToSend))
                if len(self.formDataToSend) == 1:
                    mb.showwarning(None,"Type a text message in the Text Area or Load a form.")
                    return None
                return self.formDataToSend
            except:
                mb.showwarning(None,"Problem fetching text.")
                return None

        def clearTextArea():
            self.messageTextBox.delete(1.0,END)
            self.japan_encoded_flag = False
            return
        
        def create_data_list(data_text):
            ## data holds the text message to send
            ## data_list will hold the text message broken into multiple
            ## 'msg' for sending
            mesg_tag = ut.makeCRC32(data_text)
            
            data_list = [data_text[index:index+gv.size_of_data] for index in range(0,len(data_text),gv.size_of_data)]
            ## Next assign position of each chunk to said message
            count = 0
            final_count = len(data_list)
            ## For a list of 10 messages, make messages read 1_of_10::..., 2_of_10::..., 3_of_10::..., etc.
            ## The double colon will be the delineator for separating the chunks
            for text_index in data_list:
                if debug_flag:
                    print("classTab1: create_data_list: text_index type: ",type(text_index))
                #data_list[count]= 'TAG'+mesg_tag+':'+str(count+1)+'_OF_'+str(final_count)+':'+data_list[count]
                data_list[count]= 'TAG'+mesg_tag+':'+str(count+1)+':'+data_list[count]
                
                if count < final_count-1:
                    count += 1
            if debug_flag:
                print("classTab1: create_data_list: data_list: ",data_list)
            return data_list
        
        def dictionary_bubble_sort(list_dictionaries):
            n = len(list_dictionaries)
            list_dict = list_dictionaries
            for i in range(n-1):
                for j in range(0, n-i-1):
                    first_dict = list_dict[j]
                    second_dict = list_dict[j+1]
                    ## now we have 2 dictionaries
                    ## let's compare the sequence numbers
                    if int(first_dict['seq']) > int(second_dict['seq']):
                        # swap dictionaries
                        list_dict[j], list_dict[j + 1] = list_dict[j + 1], list_dict[j]
            return list_dict
            
            
            

    def quitProgram(self):
        ## if the Henkankun widgets are showing, clear them before returning
        if self.japaneseList != []:
            ut.clearWidgetForm(self.japaneseList)
        ## delete the temporary HTML file if it exists
        if self.htmlFile:
            os.remove(self.htmlFile)
        self.controller.shutting_down()