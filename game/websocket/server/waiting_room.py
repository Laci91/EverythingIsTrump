from game.core.player import Player


class WaitingRoom:
    def __init__(self):
        self.players = {}
        
    def register_player(self, name, seat):
        self.players[seat] = Player(name, seat)
        
    def unregister_player(self, seat):
        self.players.pop(seat)
        
    def get_taken_seats(self):
        return [p.number for p in self.players.values()]
        
    def is_full(self):
        return len(self.players) == 4
