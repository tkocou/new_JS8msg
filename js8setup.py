##
## JS8msg is a copyrighted program written by Thomas Kocourek, N4FWD
## This program is released under the GPL v3 license
##
## With permission, portions of this program were borrowed from js8spotter 
## written by Joseph D Lyman KF7MIX, MIT License, Copyright 2022
##
import os
import platform
import shutil
import base64
import bz2
import documents as doc
import locals as lc
import template as tp
import DBHandler as dbh

js8msg_db = "js8msg.db"

def setup():
    
    keyList = ['apidoc','copydoc','installdoc','guidedoc','deindoc']
    fileList = {'apidoc':"API.pdf",'copydoc':"COPYING",'installdoc':"INSTALL",'guidedoc':"JS8msg Guide.pdf",'deindoc':"DEINSTALL"}

    keyList2 = ['ldesk','lshell','wdesk','licon','wicon']
    fileList2 = {'ldesk':"JS8msg.desktop",'lshell':"js8msg",'wdesk':"JS8msg.lnk",'licon':"js8msg.png",'wicon':"js8msg.ico"}

    keyList3 = ['25a','205','213','214']
    fileList3 = {'25a':"ics205a_template.html",'205':"ics205_template.html",'213':"ics213_template.html",'214':"ics214_templates.html"}

    sysPlatform = platform.system()

    ## Get the true home dir for multi-platform
    ## Should return absolute path regardless of OS
    homeDir = os.path.expanduser('~')
    os.chdir(homeDir)
    ## Path to Desktop
    desktopDir = os.path.join(homeDir,"Desktop")

    if sysPlatform == "Windows":
        extDocumentPath = os.path.join(homeDir,"Doc")
        extLocalPath = os.path.join(homeDir,"Local")
        extTemplatePath = os.path.join(homeDir,"HtmlTemplates")

        try:
            os.mkdir(extDocumentPath)
            print("Created directory 'Doc'.")
        except: ## directory already exists, do nothing
            pass
        try:
            os.mkdir(extLocalPath)
            print("Created directory 'Local'.")
        except: ## directory already exists, do nothing
            pass
        try:
            os.mkdir(extTemplatePath)
            print("Created directory 'HtmlTemplates'.")
        except: ## directory already exists, do nothing
            pass
    
        for key in keyList:
            fileName = os.path.join(extDocumentPath,fileList[key])
            ## if the file exists, remove and replace it (auto-upgrade of file)
            if os.path.exists(fileName):
                os.remove(fileName)
            stringData = doc.docArray[key]
            byteData = bytes(stringData,'utf-8')
            decodedData = base64.b64decode(byteData)
            rawArray = bz2.decompress(decodedData)
            print("Updating or creating document %s." % fileName)
            with open(fileName,"wb") as f:
                f.write(rawArray)

        for key in keyList2:
            fileName = os.path.join(extLocalPath,fileList2[key])
            ## if the file exists, remove and replace it (auto-upgrade of file)
            if os.path.exists(fileName):
                os.remove(fileName)
            stringData = lc.localArray[key]
            byteData = bytes(stringData,'utf-8')
            decodedData = base64.b64decode(byteData)
            rawArray = bz2.decompress(decodedData)
            print("Updating or creating file %s." % fileName)
            with open(fileName,"wb") as f:
                f.write(rawArray)

        for key in keyList3:
            fileName = os.path.join(extTemplatePath,fileList3[key])
            ## if the file exists, remove and replace it (auto-upgrade of file)
            if os.path.exists(fileName):
                os.remove(fileName)
            stringData = tp.templateArray[key]
            byteData = bytes(stringData,'utf-8')
            decodedData = base64.b64decode(byteData)
            rawArray = bz2.decompress(decodedData)
            print("Updating or creating template %s." % fileName)
            with open(fileName,"wb") as f:
                f.write(rawArray)

        iFile = "JS8msg.lnk"
    
        iconFile = os.path.join(extLocalPath,iFile)
        iconCheck = os.path.join(desktopDir,iFile)
        if not os.path.exists(iconCheck):
            shutil.copy2(iconFile,desktopDir)
            
        filename = os.path.join(extLocalPath,js8msg_db)
        if not os.path.exists(filename):
            # create an empty file
            with open(filename,mode='w'):pass
        init_database()

    if sysPlatform == "Linux":
        iFile = "JS8msg.desktop"
        linuxLocalBinDir = os.path.join(homeDir,"bin")
        linuxShell = os.path.join(linuxLocalBinDir,"js8msg.sh")
        linuxShellTunc = os.path.join(linuxLocalBinDir,"js8msg")
        linuxLocalPath = os.path.join(homeDir,"JS8msg/Local")
        linuxLocalDirFile = os.path.join(linuxLocalPath,"js8msg.sh")
        iconCheck = os.path.join(desktopDir,iFile)
        iconFile = os.path.join(linuxLocalPath,iFile)
        try:
            os.mkdir(linuxLocalBinDir)
        except: ## directory already exists, do nothing
            pass
        try:
            os.mkdir(linuxLocalPath)
        except:
            pass
        if not os.path.exists(linuxShell):
            shutil.copy2(linuxLocalDirFile,linuxLocalBinDir)
            os.chmod(linuxShell,0o755)
            os.rename(linuxShell,linuxShellTunc)
        if not os.path.exists(iconCheck):
            shutil.copy2(iconFile,desktopDir)
            os.chmod(iconCheck,0o755)
        filename = os.path.join(linuxLocalPath,js8msg_db)
        if not os.path.exists(filename):
            # create an empty file
            with open(filename,mode='w'):pass
        init_database()

    return

def init_database():
    
    message = ["CREATE TABLE setting (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE ON CONFLICT IGNORE, value TEXT)",
           "CREATE TABLE profile (id INTEGER PRIMARY KEY AUTOINCREMENT,title  TEXT UNIQUE ON CONFLICT IGNORE,def BOOLEAN DEFAULT (0),bgscan BOOLEAN DEFAULT (0))",
           "CREATE TABLE activity (id INTEGER PRIMARY KEY AUTOINCREMENT, profile_id INTEGER,type TEXT, value TEXT, dial TEXT, snr TEXT, call TEXT, spotdate TIMESTAMP)",
           "CREATE TABLE search (id INTEGER PRIMARY KEY AUTOINCREMENT, profile_id INT, keyword TEXT, last_seen  TIMESTAMP)",
           "INSERT INTO profile(title, def) VALUES ('Default', 1)",
           "INSERT INTO setting (name, value) VALUES ('udp_ip','127.0.0.1'),('udp_port','2242'),('tcp_ip','127.0.0.1'),('tcp_port','2442'),('hide_heartbeat',0),('dark_theme',0)"]

    db_obj = dbh.DB_object(js8msg_db)

    for data in message:
        db_obj.set_SQL(data)
        result = db_obj.exec_SQL()
        if result[0] == False:
            ## ignore errors as database may already exist
            pass

       
    