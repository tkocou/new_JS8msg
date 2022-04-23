import globalVariables as gv
import DBHandler as dbh
import utilities as ut

def get_configuration_from_db():
    ## database was initialized during setup
    message = "SELECT * FROM configuration"
    print(message)
    db_obj = ut.get_db_connection()
    db_obj.set_SQL(message)
    result = db_obj.exec_SQL()
    dbsettings = db_obj.fetch_all_SQL()
    db_obj.close_SQL()
    # remove boolean from answer
    dbset = dbsettings[1:]
    #print("within get_configuration_from_db, dbset type is: ",type(dbset))
    print("Checking dbset is: ",dbset)
    ## populate the global configuration variable
    for sett in dbset:
        for setting in sett:
            try:
                gv.commonConfData[setting[1]]=setting[2]
            except:
                pass

def save_configuration_to_db():
    #"INSERT INTO configuration (name, value) VALUES ('call','None'),('phone','None'),('uname','Nobody'),('addr','None'),('c-s-z','Nowhere'),('email','None'),('fdate','1'),('ftime','1'),('fUTC','0')"
    db_obj = ut.get_db_connection()
    print("At save_configuration, input is: ",gv.commonConfData)
    ## delete old data
    #message = "DELETE FROM configuration WHERE id=0"
    #db_obj.set_SQL(message)
    #result = db_obj.exec_SQL()
    #print("Delete ops result is: ",result[0],result[1])
    #message = "INSERT INTO configuration (name,value) VALUES ('call','{0}'),('phone','{1}'),('uname','{2}'),('addr','{3}'),('c-s-z','{4}'),('email','{5}'),('fdate','{6}'),('ftime','{7}'),('fUTC','{8}')".format(gv.commonConfData['call'],gv.commonConfData['phone'],gv.commonConfData['uname'],gv.commonConfData['addr'],gv.commonConfData['c-s-z'],gv.commonConfData['email'],gv.commonConfData['fdate'],gv.commonConfData['ftime'],gv.commonConfData['fUTC'])
    message = "UPDATE configuration SET call = '{0}', phone = '{1}', uname = '{2}', addr = '{3}', c-s-z = '{4}', email = '{5}', fdate = '{6}', ftime = '{7}', fUTC = '{8}'".format(gv.commonConfData['call'],gv.commonConfData['phone'],gv.commonConfData['uname'],gv.commonConfData['addr'],gv.commonConfData['c-s-z'],gv.commonConfData['email'],gv.commonConfData['fdate'],gv.commonConfData['ftime'],gv.commonConfData['fUTC'])
    #message = '"""'+message+'"""'
    print("Checking save_configuration_to_db: ",message)
    ## write new data
    db_obj.set_SQL(message)
    db_obj.exec_SQL()
    result = db_obj.fetch_all_SQL()
    #print("Insert ops result is: ",result[0])
    print("Update ops result is: ",result[0],result[1])
    db_obj.close_SQL()
    return result