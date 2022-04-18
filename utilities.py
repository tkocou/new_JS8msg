##
## JS8msg is a copyrighted program written by Thomas Kocourek, N4FWD
## This program is released under the GPL v3 license
##
from datetime import timezone
import datetime as dt
from tkinter.constants import FALSE, TRUE
from tkinter.filedialog import asksaveasfile, askopenfile
import bz2
import base64
import json
import zlib
import re
import os
import time
import globalVariables as gv


def dateAndTime(formatDate, formatTime, UTC):
    # The passed variables are the string references from the data dict.
    # UTC = 0 for local time, 1 for Zulu time and 2 for UTC time

    # create date and time string
    result = ""

    if UTC == "0":
        #print("Local Time")
        result = dt.datetime.now()
    elif UTC == "1" or UTC == "2":
        #print("UTC Time")
        result = dt.datetime.now(timezone.utc)
    ## 'result' will be the date & time from the system in one string
    ## Activate this next line to see the actual information from the system
    #print("result = ",result)
     
    ## separate date from time and put into a list (element 0 = date and element 1 = time)
    dateAndTime = str(result).split(' ',1)

    ## Activate this next line to see the list
    #print(dateAndTime)
    
    # break date string into 'year month day' variables
    year,month,day = dateAndTime[0].split('-')

    # Parse off the seconds and use only hours and minutes (example: "13:24:26.789" becomes "13:24")
    rTime = dateAndTime[1][:5] 
    # break time into 'hour minute'
    hour, minute = rTime.split(':') 

    if formatDate == "1": # First choice 
        newDate = year+'-'+month+'-'+day
    elif formatDate == "2":
        newDate = year+'-'+day+'-'+month
    elif formatDate == "3":
        newDate = month+'/'+day+'/'+year[2:]
    elif formatDate == "4":
        newDate = day+"/"+month+"/"+year[2:]
    elif formatDate == "5":
        newDate = year+month+day

    ## calculate the time format and set UTC variable accordingly
    if formatTime == "1" or formatTime == "3" or formatTime == "5": 
        newTime = hour+minute
    if formatTime == "2" or formatTime == "4" or formatTime == "6":
        newTime = hour+':'+minute
    if UTC == "0":
        newTime += " L"
    elif UTC == "1":
        newTime += " Z"
    else:
        newTime += " UTC"
    return newDate, newTime

def saveFormData(Parameters):
    ## Parameters is a tuple ()
    fileDir = Parameters[0]
    fileData = Parameters[1]
    dataDict = Parameters[2]
    dataKeys = Parameters[3]
    ## fileData is a list of tuples consisting of
    ## [("type of file","file extension")]
    fh = asksaveasfile(filetypes = fileData, defaultextension = fileData, initialdir=fileDir)
    ## Check for a cancelled 'save'
    ## A cancelled save will return 'fh as a 'NoneType' object
    ## and lacks a 'write' or 'close' attribute
    if fh is not None:
        for key in dataKeys:
            fh.write(key+':'+dataDict[key]+'\n')
        fh.close()
        return dataDict
    else:
        return None

def loadFormData(myParam):
    ## a tuple is passed
    fileDir = myParam[0]
    fileData = myParam[1]
    fh = askopenfile(mode='r', filetypes= fileData, initialdir=fileDir)
    if fh is not None:
        dataFromFile =fh.readlines()
        fh.close()
    else:
        ## Either a file error or a cancellation
        return None
    ## Valid data, parse it and return a dictionary
    return(parseStringData(dataFromFile))


def clearWidgetForm(widgetList):
    for widget in widgetList:
        widget.destroy()

def encodeMessage(message):
    ## 'message' is a string object
    ## Convert input to byte object
    byteData = bytes(message,'utf-8')
    ## compress the data
    compressedData = bz2.compress(byteData)
    ## base32 encode (Caps & numbers only)
    encoded32Data = str(base64.b32encode(compressedData))
    ## return parsed string
    return encoded32Data[2:-1]

def decodeMessage(packedMessage):
    ## 'packedMessage' is a string 
    ## convert to bytes
    packedBytes = bytes(packedMessage,'utf-8')
    ## base32 decode (Caps & numbers only)
    decoded32Data = base64.b32decode(packedBytes)
    ## decompress the data
    decodedMessage = str(bz2.decompress(decoded32Data))
    ## return a parsed string
    return decodedMessage[2:-1]

def dictToString(data):
    ## input is a dictionary object, like {key1:data1,key2:data2}
    try:
        ## return a string
        return json.dumps(data)
    except:
        ## any kind of problem, return an empty dictionary string
        return "{}"

def stringToDict(data):
    ## input is a string object, like "{key1:data1,key2:data2}"
    try:
        ## return a dictionary
        return json.loads(data)
    except:
        ## any kind of problem, return an empty dictionary
        return {}

def dictFromFile(fileName):
    with open(fileName,"r") as fh:
        if fh is not None:
            data =fh.readlines()
        else:
        ## Either a file error or a cancellation
            return None
    ## Valid data, parse it
    return(parseStringData(data))

def parseStringData(readData):
    dataDict = {}
    for x in readData:
        ## strip '\n' from lines
        x = x[:len(x)-1]
        ## split the line of data into 2 parts
        x = x.split(':',1)
        ## x[0] will equal the key, x[1] will be the data

        ## Trap a multi-line message and append the parts
        if x[0] == "mg":
            textKey = "mg"
        elif x[0] == "rp":
            textKey = "rp"

        ## Trap the jflag in the configuration data
        if x[0] == "jflag":
            if x[1] == "FALSE":
                gv.japanFlag = FALSE
            elif x[1] == "TRUE":
                gv.japanFlag = TRUE

        ## what will happen now is if we encountered a
        ## multiline Text() message, textKey will be set
        ## to that key.
        ## If there is no IndexError, 'textKey' is ignored
        ## Otherwise, using textKey, the extra lines are appended

        try:
            key = x[0]
            data = x[1]
            dataDict[key] = data
        except IndexError:
            if len(x[0]) > 0:
                dataDict[textKey] = dataDict[textKey]+'\n'+x[0]
    return dataDict

def makeCRC32(text):
    byteText = bytes(text,'utf-8')
    output = hex(zlib.crc32(byteText)& 0xffffffff)
    ## length of 'output' is 10 characters
    return output.upper()

def wrapMsg(text):
    crc = makeCRC32(text)
    return 'EMCOMMG='+text+crc

def unwrapMsg(text):
    return text[8:-10]

def checkCRC32(message):
    ## grab the CRC32 from the message
    msgCRC = message[-10:]
    ## separate the text from the wrap
    text = message[8:-10]
    ## compute the CRC32 from the text
    crc = makeCRC32(text)
    ## return True if both match, else False if no match
    return (msgCRC == crc)

def outputHtml(formData, formKeys, templateFilename):
    ## formData is a dictionary
    ## formKeys is a list of keys for formData
    outputHtml = ""
   
    fh = open(templateFilename,"r")
    for key in formKeys:
        found = False
        while not found:
            keyString = ':'+key+':'
            lineText = fh.readline()
            result = re.search(keyString,lineText)
            if result is None:
                outputHtml += lineText
            elif result is not None:
                found = True
                if key != "mg":
                    outputHtml += lineText.replace(keyString,formData[key])
                elif key == "mg" or key == "rp":
                    outputHtml += formData[key]

    ## transfer the last of the HTML template
    flag = True
    while flag:
        lineText = fh.readline()
        ## if real text was read, add the text
        if lineText:
            outputHtml += lineText
        ## an empty string = EOF
        else:
            flag=False

    fh.close()

    return outputHtml

def clearConsole():
    time.sleep(1)
    os.system(gv.clearConsoleCmd)
