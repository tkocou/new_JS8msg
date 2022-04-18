##
## JS8msg is a copyrighted program written by Thomas Kocourek, N4FWD
## This program is released under the GPL v3 license
##
## With permission, portions of this program were borrowed from js8spotter 
## written by Joseph D Lyman KF7MIX, MIT License, Copyright 2022
##

import socket
import json
import select
import time
from threading import *
from threading import Thread
from io import StringIO as S_IO
import utilities as ut
import DBHandler as dbh



class TCP_rx(Thread):
    def __init__(self,sock):
        super().__init__()
        self.sock = sock
        self.keep_running = True

        
    def stop(self):
        self.keep_running = False
        
    def run(self):
        ## Go to 'utilities.py', run 'get_db_connection()' and assign returned object
        self.db_obj = ut.get_db_connection()
        self.cur = self.db_obj.cursor()
        
        tracked_types = {"RX.ACTIVITY","RX.DIRECTED","RX.SPOT"}
        
        while self.keep_running:
            ## check incoming data every half second
            ## from the select module:
            ## rfds is 'wait until ready for reading'
            ## _wfds is 'wait until ready for writing'
            ## _xfds is 'wait for an “exceptional condition”'
            rfds, _wfds, _xfds = select.select([self.sock], [], [], 0.5)
            if self.sock in rfds:
                try:
                    iodata = self.sock.recv(2048)
                    json_lines = S_IO(str(iodata,'UTF-8'))
                    ## might be multiple lines in returned data
                    for data in json_lines:
                        try:
                            data_json = json.loads(data)
                        except:
                            data_json = {'type':'error'}

                        if data_json['type'] in tracked_types:
                            mesg_call = ""
                            if "CALL" in data_json['params']:
                                mesg_call = data_json['params']['CALL']
                            if "FROM" in data_json['params']:
                                mesg_call = data_json['params']['FROM']
                                
                            mesg_dial = ""
                            if "DIAL" in data_json['params']:
                                mesg_dial = data_json['params']['DIAL']
                            
                            mesg_snr = ""
                            if "SNR" in data_json['params']:
                                mesg_snr = data_json['params']['SNR']
                                
                            save_entry = False
                            
                            searchcheck = App.search_strings.copy()
                            for term in searchcheck:
                                if term in mesg_call:
                                    sql = "UPDATE search SET last_seen = CURRENT_TIMESTAMP WHERE profile_id = {0} AND keyword = {1}".format(App.current_profile_id,term)
                                    self.cur.set_SQL(sql)
                                    self.cur.exec_SQL()
                                    save_entry = True
                                    
                                if term in data_json['value']:
                                    sql = "UPDATE search SET last_seen = CURRENT_TIMESTAMP WHERE profile_id = {0} AND keyword = {1}".format(App.current_profile_id,term)
                                    self.cur.set_SQL(sql)
                                    self.cur.exec_SQL()
                                    save_entry = True
                                    
                            if save_entry == True:
                                sql = "INSERT INTO activity(profile_id,type,value,dial,snr,call,spotdate) VALUES ({0},{1},{2},{3},{4},{5},CURRENT_TIMESTAMP)".format(App.current_profile_id,data_json['type'],data_json['value'],mesg_dial,mesg_snr,mesg_call)
                                self.cur.set_SQL(sql)
                                self.cur.exec_SQL()
                                ## event is a class variable for App() class
                                ## and can be referenced in this manner
                                App.event.set()
                                
                            save_entry = False
                            
                            bgcheck = App.bgsearch_strings.copy()
                            for term in bgcheck.keys():
                                term_profile = bgcheck.get(term)
                                if term in mesg_call:
                                    sql = "UPDATE search SET last_seen = CURRENT_TIMESTAMP WHERE profile_id = {0} AND keyword = {1}".format(term_profile,term)
                                    self.cur.set_SQL(sql)
                                    self.cur.exec_SQL()
                                    sql = "INSERT INTO activity(profile_id,type,value,dial,snr,call,spotdate) VALUES ({0},{1},{2},{3},{4},{5},CURRENT_TIMESTAMP)".format(term_profile,data_json['type'],data_json['value'],mesg_dial,mesg_snr,mesg_call)
                                    self.cur.set_SQL(sql)
                                    self.cur.exec_SQL()
                                    save_entry = True
                                if term in data_json['value']:
                                    sql = "UPDATE search SET last_seen = CURRENT_TIMESTAMP WHERE profile_id = {0} AND keyword = {1}".format(term_profile,term)
                                    self.cur.set_SQL(sql)
                                    self.cur.exec_SQL()
                                    sql = "INSERT INTO activity(profile_id,type,value,dial,snr,call,spotdate) VALUES ({0},{1},{2},{3},{4},{5},CURRENT_TIMESTAMP)".format(term_profile,data_json['type'],data_json['value'],mesg_dial,mesg_snr,mesg_call)
                                    self.cur.set_SQL(sql)
                                    self.cur.exec_SQL()
                                    save_entry = True
                                    
                            if save_entry == True:
                                App.event.set()
                            
                except socket.error as err:
                    print("Error at receiving socket {}".format(err))
                    break