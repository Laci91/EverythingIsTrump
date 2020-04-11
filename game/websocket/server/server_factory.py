from autobahn.asyncio.websocket import WebSocketServerFactory
import json

from core.board import Board
from core.client_interface import ClientInterface
from game.websocket.server.waiting_room import WaitingRoom
from game.websocket.server.server_protocol import EverythingIsTrumpServerProtocol


def send_text_message(client, message):
    client.sendMessage(json.dumps(message).encode("utf-8"), isBinary=False)


class EverythingIsTrumpServerFactory(WebSocketServerFactory, ClientInterface):
    
    def __init__(self, *args, **kwargs):
        super(EverythingIsTrumpServerFactory, self).__init__(*args, **kwargs)
        self.waiting_room = WaitingRoom()
        self.board = None
        self.clients = {}
    
    def buildProtocol(self, *args, **kwargs):
        protocol = EverythingIsTrumpServerProtocol()
        protocol.factory = self
        return protocol
    
    def open_connection(self, client):
        print("Accepting new connection")
        if self.waiting_room.is_full():
            client.sendClose("Sorry, this game is full, you can't join")
        else:
            send_text_message(client, {"function": "seat-trigger", "message": "Please take a seat"})
    
    def take_seat(self, client, name, seat):
        if seat > 4 or seat < 0:
            send_text_message(client,
                              {"function": "seat", "status": "fail",
                               "message": "Seats are numbered 1-4, please select one from these"})
        if seat in self.waiting_room.get_taken_seats():
            print("Seat is taken")
            send_text_message(client,
                              {"function": "seat", "status": "fail",
                               "message": "That seat is taken, please choose another one"})
        else:
            print("Seat is free")
            send_text_message(client,
                              {"function": "seat", "status": "success",
                               "message": "Joined the seat successfully"})
            
            self.waiting_room.register_player(name, seat)
            self.clients[seat] = client
            print("Successfully joined the game, %d players are waiting for the game to begin" % len(
                self.waiting_room.players))
        
        if self.waiting_room.is_full():
            self.start_game()
    
    def start_game(self):
        print("Broadcasting start message")
        self.broadcast({"function": "info", "message": "Let's start"})
        self.trigger_new_round(1)
    
    def make_bid(self, seat, bid):
        self.game.current_board.register_bid(seat, bid)
    
    def send_error(self, seat, error_message):
        self.send_dedicated_message(seat, {"function": "error", "message": error_message})
    
    def send_trick_evaluation(self, trick_status_message):
        self.broadcast({"function": "trick", "number": trick_status_message["trickNumber"],
                        "taker": trick_status_message["taker"]})
    
    def send_round_evaluation(self, result_updates):
        self.broadcast({"function": "round", "updates": result_updates})
    
    def send_standing_update(self, standing_update):
        self.broadcast({"function": "standings", "standings": standing_update})
    
    def communicate_bid(self, seat, bid):
        self.broadcast({"function": "bid-info", "seat": seat, "bid": bid})
    
    def communicate_next_bidder(self, next_player):
        self.broadcast({"function": "next-player", "seat": next_player})
        self.send_dedicated_message(self.clients[next_player], {"function": "bid-trigger"})
    
    def communicate_next_card_player(self, next_player):
        self.broadcast({"function": "next-player", "seat": next_player})
        self.send_dedicated_message(self.clients[next_player], {"function": "play-trigger"})
    
    def trigger_new_round(self, next_round):
        self.board = Board(self.client_interface, self.players, next_round, (next_round - 1) % len(self.players))
        self.board.deal()
        for seat in self.clients.values():
            client = self.client[seat]
            hand = self.game.players[seat].hand
            send_text_message(client, {"function": "deal", "hand": hand})
        
        self.board.start_bidding()
    
    def trigger_end_of_game(self):
        pass
    
    def broadcast(self, message):
        for client in self.clients.values():
            send_text_message(client, message)
    
    def send_dedicated_message(self, seat, message):
        client = self.clients[seat]
        send_text_message(client, message)
