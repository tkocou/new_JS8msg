##
## JS8msg is a copyrighted program written by Thomas Kocourek, N4FWD
## This program is released under the GPL v3 license
## 
import globalVariables as gv
import DBHandler as dbh
from socket import socket, AF_INET, SOCK_STREAM

debug_flag = gv.debug_flag_database_functions

def get_db_connection():
    ## database was initialized during setup
    ## 'js8msg_db' is defined in file 'globalVariables.py'
    return dbh.DB_object(gv.js8msg_db)

def get_settings(self):
    ## database was initialized during setup
    message = "SELECT * FROM setting"
    db_obj = get_db_connection()
    if debug_flag:
        print("get_settings: db_obj: ",db_obj)
    db_obj.set_SQL(message)
    result = db_obj.exec_SQL()
    if debug_flag:
        print("get_settings: result: ",result)
    dbsettings = db_obj.fetch_all_SQL()
    if debug_flag:
        print("get_settings: dbsettings: ",dbsettings)
    db_obj.close_SQL()
    # remove boolean from answer
    dbset = dbsettings[1:]
    if debug_flag:
        print("get_settings: dbset is: ",dbset)
    ## let's make a dictionary from the settings
    settings = {}
    for sett in dbset:
        for setting in sett:
            try:
                settings[setting[1]]=setting[2]
            except:
                pass
    return settings

def get_socket(self):
    ## fetch settings
    settings = get_settings(self)
    ## set up network connection
    sock = socket(AF_INET, SOCK_STREAM)
    try:
        sock.connect((settings['tcp_ip'], int(settings['tcp_port'])))
        return sock
    except:
        return None
    
def get_configuration_from_db():
    ## database was initialized during setup
    message = "SELECT * FROM configuration"
    db_obj = get_db_connection()
    db_obj.set_SQL(message)
    dbsettings = db_obj.fetch_all_SQL()
    db_obj.close_SQL()
    # remove boolean from answer
    dbset = dbsettings[1:]
    ## populate the global configuration variable
    for sett in dbset:
        for setting in sett:
            try:
                gv.commonConfData[setting[1]]=setting[2]
            except:
                pass

def save_configuration_to_db():
    ## configuration data has been loaded into gv.commonConfData
    db_obj = get_db_connection()
    ## delete old data
    message = "DELETE FROM configuration;"
    db_obj.set_SQL(message)
    result = db_obj.exec_SQL()
    if debug_flag:
        print("database_config: Delete ops result is: ",result[0])
    ## insert settings from gv.commonConfData into SQL message
    message = "INSERT INTO configuration (name,value) VALUES ('call','{0}'),('phone','{1}'),('uname','{2}'),('addr','{3}'),('c-s-z','{4}'),('email','{5}'),('fdate','{6}'),('ftime','{7}'),('fUTC','{8}'),('blksz','{9}')".format(gv.commonConfData['call'],gv.commonConfData['phone'],gv.commonConfData['uname'],gv.commonConfData['addr'],gv.commonConfData['c-s-z'],gv.commonConfData['email'],gv.commonConfData['fdate'],gv.commonConfData['ftime'],gv.commonConfData['fUTC'],gv.commonConfData['blksz'])
    ## write new data
    db_obj.set_SQL(message)
    result = db_obj.exec_SQL()
    if debug_flag:
        print("database_config: Insert ops result is: ",result[0])
    db_obj.close_SQL()
    ## return True or False
    return result[0]

def check_stored_configuration():
    ## used during debugging
    db_obj = get_db_connection()
    message = "SELECT * FROM configuration"
    db_obj.set_SQL(message)
    records = db_obj.fetch_all_SQL()
    if debug_flag:
        print("database_config: Total rows are:  ", len(records[1]))
        print("database_config: Printing records: ",records[1:])
    db_obj.close_SQL()
        
def save_settings_to_db(self):
    ## first retrieve the current settings
    settings =  get_settings(self)
     ## server settings data has been loaded into global
    db_obj = get_db_connection()
    ## delete old data
    message = "DELETE FROM setting;"
    db_obj.set_SQL(message)
    result = db_obj.exec_SQL()
    if debug_flag:
        print("database_config: Delete ops result is: ",result[0])
    ## insert settings from gv.commonConfData into SQL message
    message = "INSERT INTO setting (name,value) VALUES ('udp_ip','{0}'),('udp_port','{1}'),('tcp_ip','{2}'),('tcp_port','{3}'),('hide_heartbeat','{4}'),('dark_theme','{5}')".format(gv.udp_address, gv.udp_port, gv.tcp_address, gv.tcp_port, settings['hide_heartbeat'], settings['dark_theme'])
    ## write new data
    db_obj.set_SQL(message)
    result = db_obj.exec_SQL()
    if debug_flag:
        print("database_config: Insert ops result is: ",result[0])
    db_obj.close_SQL()
    ## return True or False
    return result[0]