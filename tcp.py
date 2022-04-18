## Python 3 only
## Creator : KN4CRD, Jordan Sherer
## Modifications by N4FWD, Thomas Kocourek
##
## 'Client' is to be used as a communications class
## callable from another Python script
## and returns either a data tuple or None for a problem

from socket import socket, AF_INET, SOCK_STREAM
import json
import time

## insure that the tcp server is enabled in JS8call
server = ('127.0.0.1', 2439)

def from_message(content):
    try:
        return json.loads(content)
    except ValueError:
        return {}

def to_message(typ, value='', params={}):
    if params is None:
        params = {}
    return json.dumps({'type': typ, 'value': value, 'params': params})

class Client(object):
    first = True
    def __init__(self):
        self.rigCommand = ''
        self.rigValue = ""
        self.rigParams = {}

    def process(self, message):
        ## parse the incoming message
        typ = message.get('type', '')
        value = message.get('value', '')
        params = message.get('params', {})
        ## if there is a problem, return None
        if not typ:
            return None
        self.rigCommand = typ
        if value:
            self.rigValue = value
        if params:
            self.rigParams = params
        ## return a tuple
        return (self.rigCommand, self.rigValue, self.rigParams)


    def send(self, *args, **kwargs):
        if len(args) == 3:
            ## *args contains all passed parameters
            ## **kwargs is blank
            ## Assign dictionary from *args to **kwargs
            kwargs = args[2]
            ## parse off the dictionary in *args list
            listing = list(args)
            del listing[2]
            args = tuple(listing)
            ## now the parameters will be in the correct slots
        params = kwargs.get('params', {})
        if '_ID' not in params:
            params['_ID'] = '{}'.format(int(time.time()*1000))
            kwargs['params'] = params
        message = to_message(*args, **kwargs)
        self.sock.send(bytes(message + '\n','utf-8')) # remember to send the newline at the end :)
    
    def connect(self):
        self.sock = socket(AF_INET, SOCK_STREAM)
        try:
            self.sock.connect(server)
        except:
            ## JS8call is not running or is not running the TCP server
            return None
        self.connected = True
        try:
            ## send a query after connected
            self.send(self.rigCommand,self.rigValue,self.rigParams)

            ## listen for a reply by JS8call
            while self.connected:
                content = self.sock.recv(8192)
                if not content:
                    break

                try:
                    message = json.loads(content)
                except ValueError:
                    message = {}

                if not message:
                    continue
                result = self.process(message)

                ## return the result good or bad
                return result

        finally:
            self.sock.close()

    def close(self):
        self.connected = False

    ## method to set up the API 
    def setMessage(self,cmmd,val,parm):
        self.rigCommand = cmmd
        self.rigValue = val
        self.rigParams = parm
