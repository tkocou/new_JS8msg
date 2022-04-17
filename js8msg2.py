## Main program
import DBHandler as dbh 
import socket

js8msg_db = "js8msg.db"

def get_socket():
    ## database was initialized during setup
    message = "SELECT * FROM setting"
    db_obj = dbh.DB_object(js8msg_db)
    db_obj.set_SQL(message)
    result = db_obj.exec_SQL()
    dbsettings = db_obj.fetch_all_SQL()
    ## let's make a dictionary from the settings
    settings = {}
    for setting in dbsettings:
        settings[setting[1]]=setting[2]
    ## set up network connection
    sock = socket.socket(socket.AR_INET, socket.SOCK_STREAM)
    sock.connect((settings['tcp_ip'], int(settings['tcp_port'])))
    return sock

