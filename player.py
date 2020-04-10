from abc import ABC, abstractmethod


class Player(ABC):
    def __init__(self, number):
        self.number = number
        self.hand = None
        self.bid = None
        self.tricks = 0
        self.points = 0
        
    @abstractmethod
    def make_bid(self, number_of_cards, excluded):
        pass
    
    @abstractmethod
    def play_card(self, led_suit):
        pass
    
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
