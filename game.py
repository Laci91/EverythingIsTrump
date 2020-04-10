from card import Card, Number, Suit, is_higher
import random

MAX_NUMBER_OF_CARDS_PER_PLAYER = 13


def shuffle():
    cards = [Card(s, n) for s in Suit for n in Number]
    random.shuffle(cards)
    return cards


class Game:
    def __init__(self, players):
        self.players = players
    
    def new_game(self):
        for game_round in range(1, MAX_NUMBER_OF_CARDS_PER_PLAYER * 2 - 1):
            board = Board(self.players, game_round, game_round % 4)
            board.deal()
            board.bid()
            board.play()
            self.evaluate()
            self.cleanup()
    
    def evaluate(self):
        for player in self.players:
            if player.tricks == player.bid:
                print("Player %s succeeded (bid %d and made), got %d points" % (
                    player.number, player.bid, 10 + player.tricks * 2))
                player.award_points(10 + player.tricks * 2)
            else:
                print("Player %s failed (bid %d, made %s), got %d points" % (
                    player.number, player.bid, player.tricks, -abs(player.tricks - player.bid) * 2))
                player.award_points(-abs(player.tricks - player.bid) * 2)
        
        print("Current standing: ")
        player_list_copy = list(self.players)
        player_list_copy.sort(key=lambda pl: pl.points, reverse=True)
        for player in player_list_copy:
            print("Player %d, %d points" % (player.number, player.points))
    
    def cleanup(self):
        for player in self.players:
            player.round_end_cleanup()


class Board:
    def __init__(self, players, game_round, starting_player):
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
        self.run_round(lambda player, counter: self.players[player].make_bid(self.num_of_cards, self.get_excluded_bid()))
    
    def play_cards_one_player(self, player, counter, played_cards):
        played_cards.append(self.players[player].play_card(self.led_suit))
        if counter == 1:
            self.led_suit = played_cards[0].suit
    
    def play_cards_one_round(self):
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
        print("Player %s took the trick" % self.leading_player)
    
    def play(self):
        while self.num_of_cards > 0:
            self.play_cards_one_round()
            self.num_of_cards -= 1
