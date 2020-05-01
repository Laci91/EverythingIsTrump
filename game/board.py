from model import is_higher, Card, Suit, Number, CardFormatException
import random

MAX_NUMBER_OF_CARDS_PER_PLAYER = 13


def shuffle():
    cards = [Card(s, n) for s in Suit for n in Number]
    random.shuffle(cards)
    return cards


class Board:
    def __init__(self, client_interface, players, game_round, starting_player):
        self.client_interface = client_interface
        self.game_round = game_round
        self.num_of_cards = game_round - max(0, game_round - MAX_NUMBER_OF_CARDS_PER_PLAYER) * 2
        self.leading_player = starting_player
        self.players = players
        self.active_player = starting_player
        self.active_played_cards = []
        self.trick_number = 0
        
    def move_active_player(self):
        self.active_player = self.active_player % len(self.players) + 1
    
    ############
    #   Deal   #
    ############
    def deal(self):
        deal_counter = 0
        deck = shuffle()
        while deal_counter < len(self.players):
            deck_starting_point = deal_counter * self.num_of_cards
            self.players[self.active_player].deal(deck[deck_starting_point:deck_starting_point + self.num_of_cards])
            deal_counter += 1
            self.move_active_player()
    
    ############
    #  Bidding #
    ############
    def start_bidding(self):
        self.active_player = self.leading_player
        self.client_interface.communicate_next_bidder(self.active_player)
    
    def register_bid(self, bid):
        player = self.players[self.active_player]
        previous_bids = [player.bid for player in self.players.values() if player.bid is not None]
        excluded = None if len(previous_bids) != 3 else self.num_of_cards - sum(previous_bids)
        
        print("Excluded bid: %s; Submitted bid: %s" % (excluded, bid))
        if excluded is not None and bid == excluded:
            self.client_interface.send_error("The selected bid is forbidden")
            return
        elif bid > self.num_of_cards:
            self.client_interface.send_error("The selected bid is too high")
            return
        elif bid < 0:
            self.client_interface.send_error("The selected bid can't be negative")
            return
        
        player.make_bid(bid)
        self.client_interface.communicate_bid(self.active_player, bid)
        
        if len([player.bid for player in self.players.values() if player.bid is not None]) == 4:
            self.move_active_player()
            self.start_new_play_round()
        else:
            self.move_active_player()
            self.client_interface.communicate_next_bidder(self.active_player)
    
    ############
    #   Play   #
    ############
    def start_new_play_round(self):
        self.active_player = self.leading_player
        self.active_played_cards = []
        self.trick_number = 0
        self.client_interface.communicate_next_card_player(self.active_player)
    
    def register_played_card(self, card_str):
        led_suit = self.active_played_cards[0].suit if len(self.active_played_cards) > 0 else None
        player = self.players[self.active_player]
        try:
            card = Card.from_short_name(card_str)
            print("Trying to play card %s" % (card.__repr__()))
            print("Player has this hand: %s" % player.hand)
            
            if not player.has_card(card):
                self.client_interface.send_error("Don't try to cheat, this card is not in your hand!")
                return
            elif led_suit is not None and card.suit != led_suit and player.has_card_of_suit(led_suit):
                self.client_interface.send_error("You must play a %s since this suit was led" % led_suit)
                return
        except CardFormatException as e:
            self.client_interface.send_error(e.args[0])
            return
        
        player.play_card(card)
        print("Successfully played card, communicating...")
        
        self.client_interface.communicate_play(self.active_player, card)
        self.active_played_cards.append(card)
        
        if len(self.active_played_cards) == 4:
            self.evaluate_trick()
        else:
            self.move_active_player()
            self.client_interface.communicate_next_card_player(self.active_player)
    
    def evaluate_trick(self):
        not_trump = self.active_played_cards[0].suit
        high_card = self.active_played_cards[0]
        high_card_place = 1
        counter = 1
        for c in self.active_played_cards:
            if is_higher(c, high_card, not_trump):
                high_card = c
                high_card_place = counter
            
            counter += 1
        
        self.leading_player = (self.leading_player + high_card_place - 2) % len(self.players) + 1
        self.active_player = self.leading_player
        self.players[self.active_player].tricks += 1
        self.trick_number += 1
        self.active_played_cards = []

        self.client_interface.send_trick_evaluation({"trickNumber": self.trick_number, "taker": self.active_player, "high-card": high_card})
        if self.trick_number == self.num_of_cards:
            self.evaluate()
        else:
            self.client_interface.communicate_next_card_player(self.active_player)
    
    def evaluate(self):
        client_updates = []
        for player in self.players.values():
            print(player)
            if player.tricks == player.bid:
                client_updates.append({"player": player.number, "status": "success", "bid": player.bid,
                                       "tricks": player.tricks, "points": 10 + player.tricks * 2})
                player.award_points(10 + player.tricks * 2)
            else:
                client_updates.append({"player": player.number, "status": "fail", "bid": player.bid,
                                       "tricks": player.tricks, "points": -abs(player.tricks - player.bid) * 2})
                player.award_points(-abs(player.tricks - player.bid) * 2)
        
        self.client_interface.send_round_evaluation(client_updates)
        
        player_list_copy = list(self.players.values())
        player_list_copy.sort(key=lambda pl: pl.points, reverse=True)
        self.client_interface.send_standing_update(
            [{"player": player.number, "points": player.points} for player in player_list_copy])
        self.round_end()
    
    def round_end(self):
        for player in self.players.values():
            player.round_end_cleanup()
            
        if self.game_round == MAX_NUMBER_OF_CARDS_PER_PLAYER * 2 - 1:
            self.client_interface.trigger_end_of_game()
        else:
            self.client_interface.trigger_new_round(self.players, self.game_round + 1)
