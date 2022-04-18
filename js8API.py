##
## JS8msg is a copyrighted program written by Thomas Kocourek, N4FWD
## This program is released under the GPL v3 license
##
import re
import tcp as tcp
import globalVariables as gv
import utilities as ut
from tkinter import messagebox as mb

def api(data):
    ## data is a tuple consisting of (command, value, dictionary)
    command  = data[0]
    value = data[1]
    params = data[2]
    ## open a connection to JS8call
    s = tcp.Client()
    ## Set up API for JS8call
    s.setMessage(command,value,params)
    ## execute command and get result
    result =  s.connect()
    s.close()
    return result

def getCallsigns():
    ## API to use
    JS8command = gv.rxGetCallActivity
    ## Pass 3 parameters: API command, Any values as a string, Any params as a dictionary
    ## =-> setMessage(testCmd,"",{"params":""})
    results = api(tuple([JS8command,"", {}]))
    if results is not None:
        ## results is a tuple returned
        stringDict = ut.dictToString(results[2])
        keyList = []
        try:
            while True:
                search = re.search('\"\w*?\"\: \{', stringDict)
                end = search.end()
                call = search.group(0)[1:-4]
                keyList.append(call)
                stringDict = stringDict[end+3:]
        except:
            pass

        return keyList
    else:
        return None

def getInbox():
    JS8command = gv.inboxGetMessages
    msgDict = gv.messageDict
    results = api(tuple([JS8command,"", {}]))

    if results is not None:
        ## A list of messages are returned from JS8call
        ## results[2] is a dictionary
        ## extract list of messages
        messageList = results[2]["MESSAGES"]
        msgList = []
        for x in messageList:
            formDic = x
            form = formDic['params']
            message = ut.dictToString(form)
            ## Parse the list of messages and extract the messages
            try:
                while True:
                ## Who is the message from
                    search = re.search('\"FROM\"\: \"', message)
                    end = search.end()
                ## Prune to beginning of callsign
                    message = message[end:]
                    search = re.search(', ', message)
                    end = search.start()-1
                ## extract callsign
                    msgDict["from"] = message[:end]
                ## lop off callsign
                    message = message[end:]
                    search = re.search('TEXT', message)
                ## set the split point
                    end = search.end()+4
                ## prune beginning text
                    message = message[end:]
                ## find the end of the message
                    search = re.search(', ', message)
                ## set the new split point
                    end = search.start()-1
                ## extract 'TEXT' message
                    textMsg = message[:end]

                ## At this point, pass the message "As Is"
                ## The display function will need the 'EMCOMMG='
                ## to differenciate what sort of message is displayed
                    msgDict["mesg"] = textMsg

                ## prune the 'TEXT' message and start another search for 'TEXT'
                    message = message[end:]
                    search = re.search('\"_ID\"\: \"', message)
                    end = search.end()
                    message = message[end:]
                    msgDict["iden"] = message[:12]
                    msgList.append(msgDict)
                    msgDict = {}
    ## use the generated error to stop the loop
            except:
                pass
        ## return the list of dictionaries
        return msgList
    else:
        return None

def sendToInbox(callsign, textMsg):
    JS8command = gv.inboxStoreMessage
    ## encode and wrap the message
    msgData = ut.wrapMsg(ut.encodeMessage(textMsg))
    ## JS8call only uses uppercase text
    ## Note the structure of the parameter dictionary below
    params = {'params':{"CMD":"MSG","CALLSIGN":callsign.upper(),"TEXT":msgData}}
    results = api(tuple([JS8command,"",params]))
    if results is not None:
        return results
    else:
        return None

def sendTextAreaToInbox(callsign, textMsg):
    JS8command = gv.inboxStoreMessage
    ## encode and wrap the message
    msgData = textMsg
    ## JS8call only uses uppercase text
    ## Note the structure of the parameter dictionary below
    params = {'params':{"CMD":"MSG","CALLSIGN":callsign.upper(),"TEXT":msgData}}
    results = api(tuple([JS8command,"",params]))
    if results is not None:
        return results
    else:
        return None

def sendLive(callsign,textMsg):
    JS8command = gv.rxGetSelectedCall
    result = api(tuple([JS8command,"", {}]))
    selCall = result[1]
    if selCall != callsign:
        mb.showinfo("ERROR!","Callsign does not match the selected callsign in JS8call. Please select the target callsign in JS8call.")
    else:
        JS8command = gv.txSendMessage
        msgData = ut.wrapMsg(textMsg.upper())
        results = api(tuple([JS8command,msgData,{}]))
        if results is not None:
            return results[2]
        else:
            return None

def sendLiveText(callsign,textMsg):
    JS8command = gv.rxGetSelectedCall
    result = api(tuple([JS8command,"", {}]))
    selCall = result[1]
    if selCall != callsign:
        mb.showinfo("ERROR!","Callsign does not match the selected callsign in JS8call. Please select the target callsign in JS8call.")
    else:
        JS8command = gv.txSendMessage
        ## Send unencoded text from Text area
        msgData = textMsg.upper()
        results = api(tuple([JS8command,msgData,{}]))
        if results is not None:
            return results[2]
        else:
            return None

def getStationCallsign():
    JS8command = gv.getStationID
    result = api(tuple([JS8command,"", {}]))
    if result is not None:
        station = result[1]
        return station
    else:
        return None

def getRxText():
    JS8command = gv.rxGetText
    result = api(tuple([JS8command,"", {}]))
    if result is not None:
        rxPanel = result[1]
        return rxPanel
    else:
        return None