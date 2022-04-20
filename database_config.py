import globalVariables as gv
import DBHandler as dbh
import utilities as ut

def get_configuration_from_db():
    ## database was initialized during setup
    message = "SELECT * FROM configuration"
    db_obj = ut.get_db_connection()
    db_obj.set_SQL(message)
    result = db_obj.exec_SQL()
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
    message = "UPDATE configuration() VALUES ({0},{1},{2},{3},{4},{5},{6},{7},{8},CURRENT_TIMESTAMP)".format(gv.commonConfData['call'],gv.commonConfData['phone'],gv.commonConfData['uname'],gv.commonConfData['addr'],gv.commonConfData['c-s-z'],gv.commonConfData['email'],gv.commonConfData['fdate'],gv.commonConfData['ftime'],gv.commonConfData['fUTC'])
    db_obj = ut.get_db_connection()
    db_obj.set_SQL(message)
    result = db_obj.exec_SQL()
    db_obj.close_SQL()
    return result