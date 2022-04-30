##
## JS8msg V2.1 is a copyrighted program written by Thomas Kocourek, N4FWD
## This program is released under the GPL v3 license
##
import re
import tcp as tcp
import globalVariables as gv
import utilities as ut
from tkinter import messagebox as mb

debug_flag = gv.debug_flag_JS8API

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
    api_results = api(tuple([JS8command,"", {}]))
    if debug_flag:
        print("\nJS8API: getInbox: api_results: ",api_results,'\n\n')
    if api_results is not None:
        ## api_result nesting => tuple( dictionary{ ['MESSAGES']:list[ of dictionaries >>> { ['params'] : dictionary{ with keys of >>> ['FROM':""],['TEXT':""],['TO':""],['ID':""], etc.} } ] })
        
        ## extract dictionary of list of messages
        ## reference 2nd element of tuple and extract the list
        messageList = api_results[2]["MESSAGES"]
        if debug_flag:
            print("\nJS8API: getInbox: messageList: ",messageList)
        
        ## now create a list of messages
        msgList = []
        for x in messageList:
            ## walk though list and append data dictionary of 'params' to list
           msgList.append(x['params'])
            
        ## return the list of message dictionaries
        return msgList
    else:
        return None

def sendToInbox(callsign, textMsg):
    JS8command = gv.inboxStoreMessage
    ## encoding and wrapping the message is done prior to calling this function
    ## JS8call only uses uppercase text
    ## Note the structure of the parameter dictionary below
    params = {'params':{"CMD":"MSG","CALLSIGN":callsign.upper(),"TEXT":textMsg}}
    results = api(tuple([JS8command,"",params]))
    if results is not None:
        return results
    else:
        return None

def sendLive(callsign,textMsg):
    ## Do a check and then send to JS8call
    JS8command = gv.rxGetSelectedCall
    result = api(tuple([JS8command,"", {}]))
    selCall = result[1]
    if selCall != callsign:
        mb.showinfo("ERROR!","Callsign does not match the selected callsign in JS8call. Please select the target callsign in JS8call.")
    else:
        JS8command = gv.txSendMessage
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