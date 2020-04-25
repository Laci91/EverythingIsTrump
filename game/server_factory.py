from autobahn.asyncio.websocket import WebSocketServerFactory
import json

from board import Board
from client_interface import ClientInterface
from waiting_room import WaitingRoom
from server_protocol import EverythingIsTrumpServerProtocol


def _default(self, obj):
    return getattr(obj.__class__, "to_json", _default.default)(obj)


_default.default = json.JSONEncoder().default
json.JSONEncoder.default = _default


def send_text_message(client, message):
    client.sendMessage(json.dumps(message).encode("utf-8"), isBinary=False)


class EverythingIsTrumpServerFactory(WebSocketServerFactory, ClientInterface):
    
    def __init__(self, *args, **kwargs):
        super(EverythingIsTrumpServerFactory, self).__init__(*args, **kwargs)
        self.waiting_room = WaitingRoom()
        self.board = None
        self.seated_clients = {}
        self.unseated_clients = []
    
    def buildProtocol(self, *args, **kwargs):
        protocol = EverythingIsTrumpServerProtocol()
        protocol.factory = self
        return protocol
    
    def open_connection(self, client):
        print("Accepting new connection")
        if self.waiting_room.is_full():
            client.sendClose(code=1000, reason='Game is full, you cant join anymore')
        else:
            self.unseated_clients.append(client)
            player_map = {}
            for seat in self.waiting_room.players:
                player_map[seat] = self.waiting_room.players[seat].name
            send_text_message(client, {"function": "seat-trigger", "players": player_map,
                                       "message": "Please take a seat"})
            
    def close_connection(self, client):
        print ("Player %d left the game" % client.seat)
        if client.seat:
            self.waiting_room.unregister_player(client.seat)
            self.seated_clients.pop(client.seat)
            self.broadcast({"function": "lost-player", "seat": client.seat})
        else:
            self.unseated_clients.remove(client)
    
    def take_seat(self, client, name, seat):
        print("Try seating %s to %d" % (name, seat))
        if seat > 4 or seat < 1:
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
                              {"function": "seat", "status": "success", "seat": seat,
                               "message": "Joined the seat successfully"})
            
            self.waiting_room.register_player(name, seat)
            self.seated_clients[seat] = client
            self.unseated_clients.remove(client)
            client.seat = seat
            self.broadcast({"function": "new-player", "seat": seat, "name": name}, send_to_unseated=True)
            print("Successfully joined the game, %d players are waiting for the game to begin" % len(
                self.waiting_room.players))
        
        if self.waiting_room.is_full():
            for client in self.unseated_clients:
                client.sendClose(code=1000, reason='Game is full, you cant join anymore')
                
            self.start_game(self.waiting_room.players)
    
    def start_game(self, players):
        print("Broadcasting start message")
        self.broadcast({"function": "info", "message": "Let's start"})
        self.trigger_new_round(players, 1)
    
    def make_bid(self, seat, bid):
        if seat != self.board.active_player:
            self.send_error("It is not your turn")
        
        self.board.register_bid(bid)
    
    def make_play(self, seat, card):
        if seat != self.board.active_player:
            self.send_error("It is not your turn")
        
        self.board.register_played_card(card)
    
    def send_error(self, error_message):
        self.send_dedicated_message(self.board.active_player, {"function": "error", "message": error_message})
    
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
        self.send_dedicated_message(next_player, {"function": "bid-trigger"})
        
    def communicate_play(self, seat, card):
        self.broadcast({"function": "play-info", "seat": seat, "card": card})
    
    def communicate_next_card_player(self, next_player):
        self.broadcast({"function": "next-player", "seat": next_player})
        self.send_dedicated_message(next_player, {"function": "play-trigger"})
    
    def trigger_new_round(self, players, next_round):
        self.board = Board(self, players, next_round, (next_round - 1) % len(players) + 1)
        self.board.deal()
        if self.board.num_of_cards == 1:
            hands = {}
            for seat in self.seated_clients:
                hand = self.board.players[seat].hand
                hands[seat] = hand
                
            self.broadcast({"function": "deal", "card-on-forehead": True, "hand": hands})
        else:
            for seat in self.seated_clients:
                client = self.seated_clients[seat]
                hand = self.board.players[seat].hand
                send_text_message(client, {"function": "deal", "card-on-forehead": False, "hand": hand})
        
        self.board.start_bidding()
    
    def trigger_end_of_game(self):
        pass
    
    def broadcast(self, message, send_to_unseated=False):
        for client in self.seated_clients.values():
            send_text_message(client, message)
            
        if send_to_unseated:
            for client in self.unseated_clients:
                send_text_message(client, message)
    
    def send_dedicated_message(self, seat, message):
        client = self.seated_clients[seat]
        send_text_message(client, message)
