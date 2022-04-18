## Main program
import DBHandler as dbh 
import socket

js8msg_db = "js8msg.db"

def get_db_connection():
    ## database was initialized during setup
    return dbh.DB_object(js8msg_db)

def get_settings():
    ## database was initialized during setup
    message = "SELECT * FROM setting"
    db_obj = get_db_connection()
    db_obj.set_SQL(message)
    result = db_obj.exec_SQL()
    dbsettings = db_obj.fetch_all_SQL()
    db_obj.close_SQL()
    ## let's make a dictionary from the settings
    settings = {}
    for setting in dbsettings:
        settings[setting[1]]=setting[2]
    return settings

def get_socket():
    ## fetch settings
    settings = get_settings()
    ## set up network connection
    sock = socket.socket(socket.AR_INET, socket.SOCK_STREAM)
    sock.connect((settings['tcp_ip'], int(settings['tcp_port'])))
    return sock




class App(tk.Tk):
    def __init__(self,sock):
        super().__init__()
        self.sock = sock
        self.receiver = None
        db_conn = get_db_connection()


    def shutting_down(self,db_conn):
        db_conn.close()
        self.stop_receiving()
        self.destroy()
        
    def mainloop(self,*args):
        super().mainloop(*args)
        if self.receiver:
            self.receiver.stop()
        


def main():
    tcp_socket = get_socket()
    app = App(tcp_socket)
    app.protocol("WM_DELETE_WINDOW",app.shutting_down)
    app.mainloop()
    
if __name__ == '__main__':
    main()