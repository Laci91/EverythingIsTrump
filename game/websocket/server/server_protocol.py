import json
from autobahn.asyncio.websocket import WebSocketServerProtocol


class EverythingIsTrumpServerProtocol(WebSocketServerProtocol):
    def __init__(self, *args, **kwargs):
        super(WebSocketServerProtocol, self).__init__(*args, **kwargs)
        self.seat = None
    
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
        elif msg["function"] == "bid":
            bid = int(msg["bid"])
            self.factory.make_bid(self.seat, bid)
        elif msg["function"] == "play":
            card = msg["card"]
            self.factory.make_play(self.seat, card)
        else:
            print(msg)
    
    def onClose(self, wasClean, code, reason):
        print("Closing protocol, reason is %s" % reason)
