from game.core.model import Card, CardFormatException


class Player:
    def __init__(self, name, number):
        self.name = name
        self.number = number
        self.hand = None
        self.bid = None
        self.tricks = 0
        self.points = 0
        
    def __repr__(self):
        return "%s (%d)" % (self.name, self.number)
    
    def new_board(self):
        self.tricks = 0

    def deal(self, cards):
        self.hand = cards
    
    def award_points(self, points):
        self.points += points
        
    def take_trick(self):
        self.tricks += 1
        
    def round_end_cleanup(self):
        self.tricks = 0
        self.bid = None
        self.hand = None

    def make_bid(self, bid):
        self.bid = bid
        
    def has_card(self, card):
        return card in self.hand
        
    def has_card_of_suit(self, suit):
        return len([c for c in self.hand if c.suit == suit]) > 0

    def play_card(self, card):
        self.hand.remove(card)
