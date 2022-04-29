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
import globalVariables as gv

def setup():
    
    keyList = ['apidoc','copydoc','installdoc','guidedoc','deindoc']
    fileList = {'apidoc':"API.pdf",'copydoc':"COPYING",'installdoc':"INSTALL",'guidedoc':"JS8msg Guide.pdf",'deindoc':"DEINSTALL"}

    keyList2 = ['wdesk','licon','wicon']
    fileList2 = {'wdesk':"JS8msg.lnk",'licon':"js8msg.png",'wicon':"js8msg.ico"}

    keyList3 = ['25a','205','213','214']
    fileList3 = {'25a':"ics205a_template.html",'205':"ics205_template.html",'213':"ics213_template.html",'214':"ics214_templates.html"}

    sysPlatform = platform.system()

    ## Get the true home dir for multi-platform
    ## Should return absolute path regardless of OS
    homeDir = os.path.expanduser('~')
    os.chdir(homeDir)
    ## Path to Desktop
    desktopDir = os.path.join(homeDir,"Desktop")

    ## make directory in home directory to hold JS8msg subdirectories
    try:
        os.mkdir(gv.JS8msg_dir)
    except:
        pass
    try:
        os.mkdir(gv.documentPath)
        #print("Created directory 'Doc'.")
    except: ## directory already exists, do nothing
        pass
    try:
        os.mkdir(gv.localPath)
        #print("Created directory 'Local'.")
    except: ## directory already exists, do nothing
        pass
    try:
        os.mkdir(gv.templatePath)
        #print("Created directory 'HtmlTemplates'.")
    except: ## directory already exists, do nothing
        pass
    try:
        os.mkdir(gv.msgPath)
        #print("Creating directory 'Messages'.")
    except:
        pass
    try:
        os.mkdir(gv.tempPath)
        #print("Creating directory 'Tmp'.")
    except:
        pass
        
        
    for key in keyList:
        fileName = os.path.join(gv.documentPath,fileList[key])
        ## if the file exists, remove and replace it (auto-upgrade of file)
        if os.path.exists(fileName):
            os.remove(fileName)
        stringData = doc.docArray[key]
        byteData = bytes(stringData,'utf-8')
        decodedData = base64.b64decode(byteData)
        rawArray = bz2.decompress(decodedData)
        #print("Updating or creating document %s." % fileName)
        with open(fileName,"wb") as f:
            f.write(rawArray)

    for key in keyList2:
        fileName = os.path.join(gv.localPath,fileList2[key])
        ## if the file exists, remove and replace it (auto-upgrade of file)
        if os.path.exists(fileName):
            os.remove(fileName)
        stringData = lc.localArray[key]
        byteData = bytes(stringData,'utf-8')
        decodedData = base64.b64decode(byteData)
        rawArray = bz2.decompress(decodedData)
        #print("Updating or creating file %s." % fileName)
        with open(fileName,"wb") as f:
            f.write(rawArray)

    for key in keyList3:
        fileName = os.path.join(gv.templatePath,fileList3[key])
        ## if the file exists, remove and replace it (auto-upgrade of file)
        if os.path.exists(fileName):
            os.remove(fileName)
        stringData = tp.templateArray[key]
        byteData = bytes(stringData,'utf-8')
        decodedData = base64.b64decode(byteData)
        rawArray = bz2.decompress(decodedData)
        #print("Updating or creating template %s." % fileName)
        with open(fileName,"wb") as f:
            f.write(rawArray)
                
    if sysPlatform == "Windows":
        iFile = "JS8msg.lnk"
        iconFile = os.path.join(gv.localPath,iFile)
        iconCheck = os.path.join(desktopDir,iFile)
        if not os.path.exists(iconCheck):
            shutil.copy2(iconFile,desktopDir)
    
    ## check if we are running js8msg2 from within the development directory        
    if gv.project_dir == "None":
        ## we are running a live system, not development
        ## if the target OS is not Linux, we will need another section
        if sysPlatform == "Linux":
            ## let's create a desktop launcher
            launcher = "JS8msg.desktop"
            desktop_launcher_path = os.path.join(desktopDir,launcher)
            ## get the path towhere js8msg2 is executing from
            exec_path = os.path.join(homeDir,"bin/js8msg2")
            icon_picture_path = os.path.join(gv.localPath,"js8msg.png")
            ## updating launcher internals
            with open(desktop_launcher_path, "w") as fh:
                fh.write("[Desktop Entry]\n")
                fh.write("Version=1.0\n")
                fh.write("Type=Application\n")
                fh.write("Terminal=false\n")
                fh.write("Icon="+icon_picture_path+'\n')
                fh.write("Icon[en_US]="+icon_picture_path+'\n')
                fh.write("Name[en_US]=JS8msg\n")
                fh.write("Exec="+exec_path+'\n')
                fh.write("Comment[en_US]=EMCOMM message support for JS8call\n")
                fh.write("Name=JS8msg\n")
                fh.write("Comment=EMCOMM message support for JS8call\n")
            os.chmod(desktop_launcher_path,0o755)
        
    gv.js8msg_db = os.path.join(gv.localPath,gv.db_name)
    init_database()

    return

def init_database():
    
    message = ["CREATE TABLE setting (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE ON CONFLICT IGNORE, value TEXT)",
           "CREATE TABLE profile (id INTEGER PRIMARY KEY AUTOINCREMENT,title  TEXT UNIQUE ON CONFLICT IGNORE,def BOOLEAN DEFAULT (0),bgscan BOOLEAN DEFAULT (0))",
           "CREATE TABLE activity (id INTEGER PRIMARY KEY AUTOINCREMENT, profile_id INTEGER,type TEXT, value TEXT, dial TEXT, snr TEXT, call TEXT, spotdate TIMESTAMP)",
           "CREATE TABLE configuration (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE ON CONFLICT IGNORE, value VARCHAR)",
           "CREATE TABLE search (id INTEGER PRIMARY KEY AUTOINCREMENT, profile_id INT, keyword TEXT, last_seen  TIMESTAMP)",
           "INSERT INTO profile(title, def) VALUES ('Default', 1)",
           "INSERT INTO setting (name, value) VALUES ('udp_ip','127.0.0.1'),('udp_port','2242'),('tcp_ip','127.0.0.1'),('tcp_port','2442'),('hide_heartbeat',0),('dark_theme',0)",
           "INSERT INTO configuration (name, value) VALUES ('call','None'),('phone','None'),('uname','Nobody'),('addr','None'),('c-s-z','Nowhere'),('email','None'),('fdate','1'),('ftime','1'),('fUTC','0'),('blksz','26')"]

    if os.path.exists(gv.js8msg_db):
        ## do not reinitialize an existing database
        pass
    else:
        ## create a new database and initialize it
        with open(gv.js8msg_db,mode='w'):pass
        db_obj = dbh.DB_object(gv.js8msg_db)

        for data in message:
            #print("js8setup: SQL message is: ", data)
            db_obj.set_SQL(data)
            result = db_obj.exec_SQL()
            print("result in js8setup is: ",result)
            if result[0] == False:
                ## ignore errors as database may already exist
                print("Error with DB")
                pass

    