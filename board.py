from card import is_higher, Card, Suit, Number
import random


MAX_NUMBER_OF_CARDS_PER_PLAYER = 13


def shuffle():
    cards = [Card(s, n) for s in Suit for n in Number]
    random.shuffle(cards)
    return cards


class Board:
    def __init__(self, client_interface, players, game_round, starting_player):
        self.client_interface = client_interface
        self.num_of_cards = game_round - max(0, game_round - MAX_NUMBER_OF_CARDS_PER_PLAYER)
        self.leading_player = starting_player
        self.players = players
        self.deck = shuffle()
        
        # I don't like it, should be extracted into a class called Trick or something
        self.led_suit = None
    
    def run_round(self, action):
        next_player = self.leading_player
        action_counter = 0
        while action_counter < len(self.players):
            action(next_player, action_counter)
            action_counter += 1
            next_player = (next_player + 1) % len(self.players)
    
    def deal_one_player(self, next_player, action_counter):
        deck_starting_point = action_counter * self.num_of_cards
        self.players[next_player].deal(self.deck[deck_starting_point:deck_starting_point + self.num_of_cards])
    
    def deal(self):
        self.run_round(lambda player, counter: self.deal_one_player(player, counter))
    
    def get_excluded_bid(self):
        previous_bids = [player.bid for player in self.players if player.bid is not None]
        return None if len(previous_bids) != 3 else self.num_of_cards - sum(previous_bids)
    
    def bid(self):
        self.run_round(
            lambda player, counter: self.players[player].make_bid(self.num_of_cards, self.get_excluded_bid()))
    
    def play_cards_one_player(self, player, counter, played_cards):
        played_cards.append(self.players[player].play_card(self.led_suit))
        if counter == 1:
            self.led_suit = played_cards[0].suit
    
    def play_cards_one_round(self, trick_number):
        played_cards = []
        self.run_round(lambda player, player_counter: self.play_cards_one_player(player, player_counter, played_cards))
        
        not_trump = played_cards[0].suit
        high_card = played_cards[0]
        high_card_place = self.leading_player
        counter = 0
        for c in played_cards:
            if is_higher(c, high_card, not_trump):
                high_card = c
                high_card_place = counter
            
            counter += 1
        
        self.leading_player = (self.leading_player + high_card_place) % len(self.players)
        self.players[self.leading_player].tricks += 1
        self.led_suit = None
        self.client_interface.send_trick_evaluation({"trickNumber": trick_number, "taker": self.leading_player})
    
    def play(self):
        trick_number = 0
        while self.num_of_cards > 0:
            trick_number += 1
            self.play_cards_one_round(trick_number)
            self.num_of_cards -= 1
