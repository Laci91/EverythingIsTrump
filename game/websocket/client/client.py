import asyncio
import websockets
import json

from autobahn.asyncio import WebSocketClientFactory, WebSocketClientProtocol


def send_text_message(client, message):
    client.sendMessage(json.dumps(message).encode("utf-8"), isBinary=False)


class MyClientProtocol(WebSocketClientProtocol):
            
    def onMessage(self, payload, isBinary):
        decoded = payload.decode("utf-8")
        msg = json.loads(decoded)
        
        if "function" not in msg:
            print("Malformed message (%s) from client, ignoring" % payload)
            return
        
        if msg["function"] == "seat-trigger":
            print(msg["message"])
            name = input("Name: ")
            seat = int(input("Seat: "))
            send_text_message(self, {"function": "seat", "name": name, "seat": seat})
        elif msg["function"] == "seat" and msg["status"] == "fail":
            print(msg["message"])
            name = input("Name: ")
            seat = int(input("Seat: "))
            send_text_message(self, {"function": "seat", "name": name, "seat": seat})
        elif msg["function"] == "seat" and msg["status"] == "success":
            print("Connection successful, awaiting instructions")
        elif msg["function"] == "info":
            print(msg["message"])
    
        
if __name__ == '__main__':
    factory = WebSocketClientFactory("ws://127.0.0.1:8765")
    factory.protocol = MyClientProtocol

    loop = asyncio.get_event_loop()
    coro = loop.create_connection(factory, '127.0.0.1', 8765)
    loop.run_until_complete(coro)
    loop.run_forever()
    loop.close()
