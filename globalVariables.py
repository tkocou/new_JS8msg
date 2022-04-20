##
## JS8msg is a copyrighted program written by Thomas Kocourek, N4FWD
## This program is released under the GPL v3 license
##
## Global variables - defining variables used through out JS8msg
##
## Global Paths
import os
import platform
from tkinter.constants import FALSE

## Probably need to get system platform information
pathSep = ""
sysPlatform = platform.system()
if sysPlatform == "Linux":
    pathSep = "/"
    clearConsoleCmd = "clear"
elif sysPlatform == "Windows":
    pathSep = "\\"
    clearConsoleCmd = "cls"

configPath = os.getcwd()+pathSep+"Config"
msgPath = os.getcwd()+pathSep+"Messages"
localPath = os.getcwd()+pathSep+"Local"
templatePath = os.getcwd()+pathSep+"HtmlTemplates"+pathSep
binPath = os.path.dirname(__file__)
tempPath = os.getcwd()+pathSep+"Tmp"+pathSep

## database for net opps
js8msg_db = "js8msg.db"

## GUI tracking
widget_list_dict = {"Tab1":[],"Tab2":[],"Tab2a":[],"Tab3":[],"Tab4":[]}

##
## JS8Call APIs
txSendMessage = 'TX.SEND_MESSAGE'
rxGetBandActivityText = 'RX.GET_TXT'
txGetText = 'TX.GET_TEXT'
rxGetBandActivity = 'RX.GET_BAND_ACTIVITY'
rxGetCallActivity = 'RX.GET_CALL_ACTIVITY'
rxGetSelectedCall = 'RX.GET_CALL_SELECTED'
inboxGetMessages = 'INBOX.GET_MESSAGES'
inboxStoreMessage = 'INBOX.STORE_MESSAGE'
getStationID = 'STATION.GET_CALLSIGN'
getRigFreq = 'RX.GET_FREQ'
pingJS8 = 'PING'

##
## some variables for facilitating the reading of messages from JS8call
##
stationCallsign = ""
messageDict = {"from":"","mesg":"","iden":""}
messageDictKeys = ["from","mesg","iden"]

# keep track of which form is being used
whichForm = {"form":""}

## flag for japanese use
japanFlag = FALSE

## Some path variables
## 
binPath = ""
auxPath = ""
storePath = ""
templatesPath = ""
tmpPath = ""
configurePath = ""

##
## Configuration dictionary terms
##
commonConfData = {'call':"", 'phone':"", 'name':"", 'addr':"", 'c-s-z':"", 'email':"", 'fdate':"", 'ftime':"", 'fUTC':""}
commonConfText = {'call':"Callsign:", 'phone':"Phone#:", 'name':"Name: ", 'addr':"Address: ", 'c-s-z':"City/St/Zip:", 'email':"Email: ", 'fdate':"Date Fmt: ", 'ftime':"Time Fmt: ", 'fUTC':"Timezone: "}
commonConfKeys = ['call','phone','name','addr', 'c-s-z','email','fdate', 'ftime','fUTC']
readConfFlag = False
readDataFlag = False

## 
## A set of dictionaries and lists for ICS-213
## 
ics213FieldsData = {'inc':"",'to':"",'fm':"",'p1':"",'p2':"",'sb':"",'d1':"",'t1':"",'mg':"",'s1':"",'p3':"",'rp':"",'d2':"",'t2':"",'s2':"",'p4':"","file":"213"}
ics213FieldsText =  {'inc':"Inc: ",'to':"To: ",'fm':"Fm: ",'p1':"Pos.: ",'p2':"Pos.: ",'sb':"Sub.: ",'d1':"Date: ",'t1':"Time: ",'mg':"Message",'s1':"Appr. ",'p3':"Pos. ",'rp':"Reply:  ",'d2':"Date:   ",'t2':"Time:   ",'s2':"Name: ",'p4':"Pos.:","file":"ICS-213"}
origIcs213FieldKeys = ['inc','to','fm','p1','p2','sb','d1','t1','mg','s1','p3']
rplyIcs213FieldKeys = ['rp','d2','t2','s2','p4','file']
respIcs213FormData = {'rp':"",'d2':"",'t2':"",'s2':"",'p4':"",'file':""}
totalIcs213Keys = ['inc','to','p1','fm','p2','sb','d1','t1','mg','s1','p3','rp','s2','p4','d2','t2','file']

##
## A set of dictionaries and lists for ICS-214
##
ics214FieldsData = {'inc':"",'dat':"",'tim':"",'und':"",'unl':"",'opp':"",'pre':"",'pps':"",'file':"214"}
ics214FieldsText = {'inc':"Inc:",'dat':"Dat:",'tim':"Tim:",'und':"Und:",'unl':"Unl:",'opp':"Opp:",'pre':"Pre:",'pps':"Pps:",'file':"ICS-214"}
ics214FieldsKeys = ['inc','dat','tim','und','unl','opp','pre','pps','file']
ics214ListData = [{'nam':"",'pos':"",'hom':"",'atm':"",'evt':""}]
ics214ListText = {'nam':"Name",'pos':"Position",'hom':"Homebase",'atm':"Activity Time",'evt':"Event"}
ics214ListKeys = ['nam','dat','tim','und','unl','opp','pre','pps','file']

##
## A set of dictionaries and lists for ICS-309
##
ics214FieldsData = {'inc':"",'rop':"",'frm':"",'tm1':"",'to1':"",'tm2':"",'net':"",'pre':"",'pps':"",'dt1':"",'tm3':"",'file':"214"}
ics214FieldsText = {'inc':"Inc:",'rop':"Rop:",'frm':"",'tm1':"Time:",'to1':"To:",'tm2':"Time:",'net':"Net:",'pre':"Preparer:",'pps':"Position:",'dt1':"Date:",'tm3':"Time:",'file':"ICS-214"}
ics214FieldsKeys = ['inc','rop','frm','tm1','to1','tm2','net','pre','pps','dt1','tm3','file']
ics214ListData = [{'nam':"",'fro':"",'to2':"",'msg':"",'file':"309"}]
ics214ListText = {'nam':"Name:",'fro':"From:",'to2':"To:",'msg':"Message",'file':"ICS-309"}
ics214ListKeys = ['nam','fro','to2','msg','file']

##
## TODO: add more dictionaries for other forms
##