##
## JS8msg is a copyrighted program written by Thomas Kocourek, N4FWD
## This program is released under the GPL v3 license
##
## With permission, portions of this program were borrowed from js8spotter 
## written by Joseph D Lyman KF7MIX, MIT License, Copyright 2022
##

import socket
import DBHandler as dbh 
from threading import *
from threading import Thread
from io import StringIO


js8msg_db = "js8msg.db"

class TCP_rx(Thread):
    def __init__(self,sock):
        super().__init__()
        self.sock = sock
        self.keep_running = True
        
    def stop(self):
        self.keep_running = False
        
    def run(self):
        pass
        
