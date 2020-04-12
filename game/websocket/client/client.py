import asyncio
import json
import sys
from autobahn.asyncio import WebSocketClientFactory, WebSocketClientProtocol


NAME = None
SEAT = None


def send_text_message(client, message):
    client.sendMessage(json.dumps(message).encode("utf-8"), isBinary=False)


class MyClientProtocol(WebSocketClientProtocol):
    
    def __init__(self):
        super().__init__()
        self.seat = None
        self.bidding_in_progress = False
        self.cardplay_in_progress = False
        
    def onOpen(self):
        print(NAME)
        print(SEAT)
        send_text_message(self, {"function": "seat", "name": NAME, "seat": SEAT})
            
    def onMessage(self, payload, isBinary):
        decoded = payload.decode("utf-8")
        msg = json.loads(decoded)
        
        if "function" not in msg:
            print("Malformed message (%s) from client, ignoring" % payload)
            return
        
        if msg["function"] == "seat-trigger":
            pass
        elif msg["function"] == "seat" and msg["status"] == "fail":
            print(msg["message"])
            name = input("Name: ")
            seat = int(input("Seat: "))
            send_text_message(self, {"function": "seat", "name": name, "seat": seat})
        elif msg["function"] == "seat" and msg["status"] == "success":
            print("Connection successful, awaiting instructions")
            self.seat = int(msg["seat"])
        elif msg["function"] == "info":
            print(msg["message"])
        elif msg["function"] == "error":
            print(msg["message"])
            if self.bidding_in_progress:
                self.bid()
            elif self.cardplay_in_progress:
                self.play_card()
        elif msg["function"] == "bid-trigger":
            self.bidding_in_progress = True
            self.bid()
        elif msg["function"] == "bid-info":
            print("Player in seat %d bid %d" % (int(msg["seat"]), int(msg["bid"])))
        elif msg["function"] == "play-info":
            print("Player in seat %d played %s" % (int(msg["seat"]), msg["card"]))
        elif msg["function"] == "play-trigger":
            print("Received play trigger")
            self.cardplay_in_progress = True
            self.play_card()
        elif msg["function"] == "standings":
            print("Current standing: ")
            counter = 1
            for update in msg["standings"]:
                print("%d. Player %d, %d points" % (counter, update["player"], update["points"]))
                counter += 1
        elif msg["function"] == "deal":
            print("Your hand: %s" % " ".join(msg["hand"]))
        elif msg["function"] == "next-player":
            print("#%d is the active player now" % (int(msg["seat"])))
            self.bidding_in_progress = False
            self.cardplay_in_progress = False
        elif msg["function"] == "trick":
            print("Player nr. %d took trick #%d" % (int(msg["taker"]), int(msg["number"])))
        elif msg["function"] == "round":
            for update in msg["updates"]:
                print("Player %s failed (bid %d, made %s), got %d points" % (
                    update["player"], update["bid"], update["tricks"], update["points"]))
                
    def bid(self):
        bid = int(input("Bid: "))
        send_text_message(self, {"function": "bid", "bid": bid})
        
    def play_card(self):
        card = input("Card: ")
        send_text_message(self, {"function": "play", "card": card})


if __name__ == '__main__':
    factory = WebSocketClientFactory("ws://127.0.0.1:8765")
    factory.protocol = MyClientProtocol
    
    NAME = sys.argv[1]
    SEAT = int(sys.argv[2])

    loop = asyncio.get_event_loop()
    coro = loop.create_connection(factory, '127.0.0.1', 8765)
    loop.run_until_complete(coro)
    loop.run_forever()
    loop.close()
