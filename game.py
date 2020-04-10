from board import Board, MAX_NUMBER_OF_CARDS_PER_PLAYER


class Game:
    def __init__(self, client_interface, players):
        self.client_interface = client_interface
        self.players = players
    
    def new_game(self):
        for game_round in range(1, MAX_NUMBER_OF_CARDS_PER_PLAYER * 2 - 1):
            board = Board(self.client_interface, self.players, game_round, game_round % len(self.players))
            board.deal()
            board.bid()
            board.play()
            self.evaluate()
            self.cleanup()
    
    def evaluate(self):
        client_updates = []
        for player in self.players:
            if player.tricks == player.bid:
                client_updates.append({"player": player.number, "status": "success", "bid": player.bid,
                                       "tricks": player.tricks, "points": 10 + player.tricks * 2})
                player.award_points(10 + player.tricks * 2)
            else:
                client_updates.append({"player": player.number, "status": "fail", "bid": player.bid,
                                       "tricks": player.tricks, "points": -abs(player.tricks - player.bid) * 2})
                player.award_points(-abs(player.tricks - player.bid) * 2)
        
        self.client_interface.send_round_evaluation(client_updates)
        
        player_list_copy = list(self.players)
        player_list_copy.sort(key=lambda pl: pl.points, reverse=True)
        self.client_interface.send_standing_update(
            [{"player": player.number, "points": player.points} for player in player_list_copy])
    
    def cleanup(self):
        for player in self.players:
            player.round_end_cleanup()
