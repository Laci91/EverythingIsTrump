import json
from autobahn.asyncio.websocket import WebSocketServerProtocol


class EverythingIsTrumpServerProtocol(WebSocketServerProtocol):
    def __init__(self, *args, **kwargs):
        super(WebSocketServerProtocol, self).__init__(*args, **kwargs)
    
    def onOpen(self):
        self.factory.open_connection(self)
    
    def onMessage(self, payload, isBinary):
        if isBinary:
            print("Binary message format not accepted, ignoring")
            return
        
        decoded = payload.decode("utf-8")
        msg = json.loads(decoded)
        if "function" not in msg:
            print("Malformed message (%s) from client, ignoring" % payload)
            return
        
        if msg["function"] == "seat":
            seat = int(msg["seat"])
            name = msg["name"]
            self.factory.take_seat(self, name, seat)
        if msg["function"] == "bid":
            seat = int(msg["seat"])
            bid = int(msg["bid"])
            self.factory.make_bid(seat, bid)
    
    def onClose(self, wasClean, code, reason):
        print("Closing protocol, reason is %s" % reason)
