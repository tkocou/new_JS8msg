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

project_dir = os.getcwd()
project_dir = project_dir[10:]
if project_dir != "Projects":
    project_dir = "None"

## version of JS8msg
version_text = "Version 2.2"

homeDir = os.path.expanduser('~')
os.chdir(homeDir)
JS8msg_dir = os.path.join(homeDir,"JS8msg")
try:
    os.mkdir(JS8msg_dir)
except:
    pass
msgPath = os.path.join(JS8msg_dir,"Messages")
localPath = os.path.join(JS8msg_dir,"Local")
templatePath = os.path.join(JS8msg_dir,"HtmlTemplates")
documentPath = os.path.join(JS8msg_dir,"Doc")
tempPath = os.path.join(JS8msg_dir,"Tmp")
## Probably need to get system platform information

sysPlatform = platform.system()
if sysPlatform == "Linux":
    clearConsoleCmd = "clear"
elif sysPlatform == "Windows":
    clearConsoleCmd = "cls"

if project_dir == "Projects":
    project_dir += "/js8msg2"
    msgPath = os.path.join(project_dir,"Messages")
    localPath = os.path.join(project_dir,"Local")
    templatePath = os.path.join(project_dir,"HtmlTemplates")
    documentPath = os.path.join(project_dir,"Doc")
    tempPath = os.path.join(project_dir,"Tmp")


## database for net opps
## js8msg_db will hold the paltform dependent path to 'db_name'
js8msg_db = ""
db_name = "js8msg.db"

## GUI tracking
widget_list_dict = {"Tab1":[],"Tab2":[],"Tab3":[],"Tab4":[],"Tab5":[]}

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

## background monitoring of JS8Call activity
keep_running = False
receiver = None
sock = None

## flag for japanese use
japanFlag = False

## default size of chunks when sending a form
## the purpose for chunking of the form data is to comply with ID regulations
size_of_data = 26

## flags to enable print statements
debug_flag_database_functions = False
debug_flag_DBHandler = False
debug_flag_JS8API = False
debug_flag_utilities = False
debug_flag_Tab1 = False
debug_flag_Tab2 = False
debug_flag_Tab3 = False
debug_flag_Tab4 = False
debug_flag_receiving_inbox = False
## turning off flags must be done manually
if debug_flag_receiving_inbox:
    debug_flag_JS8API = True
    debug_flag_utilities = True
    debug_flag_Tab1 = True
## flag for threaded debugging
debug_flag_threaded = False

## these are used in tcp.py
## Which type of port to listen/talk on
tcp_address = ""
tcp_port = ""
udp_address = ""
udp_port = ""
TCP = True
server_data_keys=['udp_ip','udp_port','tcp_ip','tcp_port','hide_heartbeat','dark_theme']
## size of receive buffer
recv_buffer_size = 1000000
##
## some variables for facilitating the reading of messages from JS8call via JS8API
##
stationCallsign = ""
messageDict = {"from":"","mesg":"","iden":""}
messageDictKeys = ["from","mesg","iden"]

html_file = ""


##
## Configuration dictionary terms
##
commonConfData = {'call':"", 'phone':"", 'uname':"", 'addr':"", 'c-s-z':"", 'email':"", 'fdate':"", 'ftime':"", 'fUTC':"", 'blksz':"26"}
commonConfText = {'call':"Callsign:", 'phone':"Phone#:", 'uname':"Name: ", 'addr':"Address: ", 'c-s-z':"City/St/Zip:", 'email':"Email: ", 'fdate':"Date Fmt: ", 'ftime':"Time Fmt: ", 'fUTC':"Timezone: ", 'blksz':"Block_size: "}
commonConfKeys = ['call','phone','uname','addr', 'c-s-z','email','fdate', 'ftime','fUTC','blksz']

## 
## A set of dictionaries and lists for ICS-213
## 
ics213FormData = {'inc':"",'to':"",'fm':"",'p1':"",'p2':"",'sb':"",'d1':"",'t1':"",'mg':"",'s1':"",'p3':"",'rp':"",'d2':"",'t2':"",'s2':"",'p4':"","file":"213"}
ics213FieldsText =  {'inc':"Inc: ",'to':"To: ",'fm':"Fm: ",'p1':"Pos.: ",'p2':"Pos.: ",'sb':"Sub.: ",'d1':"Date: ",'t1':"Time: ",'mg':"Message",'s1':"Appr. ",'p3':"Pos. ",'rp':"Reply:  ",'d2':"Date:   ",'t2':"Time:   ",'s2':"Name: ",'p4':"Pos.:","file":"ICS-213"}
origIcs213FieldKeys = ['inc','to','fm','p1','p2','sb','d1','t1','mg','s1','p3']
rplyIcs213FieldKeys = ['rp','d2','t2','s2','p4','file']
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