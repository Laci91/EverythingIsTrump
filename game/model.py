from enum import Enum
from aenum import AutoNumberEnum


class Suit(AutoNumberEnum):
    def __init__(self, strength, short_name, user_friendly_order_number):
        self.strength = strength
        self.short_name = short_name
        self.user_friendly_order_number = user_friendly_order_number
        
    def __repr__(self):
        return self.short_name
    
    def __lt__(self, other):
        return other is not None and self.strength < other.strength

    def __gt__(self, other):
        return other is not None and self.strength > other.strength

    def __eq__(self, other):
        return other is not None and self.strength == other.strength
    
    def __hash__(self):
        return self.strength
       
    @classmethod
    def from_short_name(cls, short_name):
        for s in Suit:
            if s.short_name == short_name:
                return s
            
        raise CardFormatException(short_name + " is not a valid Suit")
        
    SPADES = (4, "S", lambda position_override: 4 if not position_override else position_override[Suit.SPADES])
    HEARTS = (3, "H", lambda position_override: 3 if not position_override else position_override[Suit.HEARTS])
    DIAMONDS = (2, "D", lambda position_override: 1 if not position_override else position_override[Suit.DIAMONDS])
    CLUBS = (1, "C", lambda position_override: 2 if not position_override else position_override[Suit.CLUBS])
    

class Number(AutoNumberEnum):
    def __init__(self, strength, short_name):
        self.strength = strength
        self.short_name = short_name
        
    def __repr__(self):
        return self.short_name

    def __lt__(self, other):
        return other is not None and self.strength < other.strength

    def __gt__(self, other):
        return other is not None and self.strength > other.strength

    def __eq__(self, other):
        return other is not None and self.strength == other.strength
        
    @classmethod
    def from_short_name(cls, short_name):
        for n in Number:
            if n.short_name == short_name:
                return n

        raise CardFormatException(short_name + " is not a valid Number")
            
    ACE = (14, "A")
    KING = (13, "K")
    QUEEN = (12, "Q")
    JACK = (11, "J")
    TEN = (10, "T")
    NINE = (9, "9")
    EIGHT = (8, "8")
    SEVEN = (7, "7")
    SIX = (6, "6")
    FIVE = (5, "5")
    FOUR = (4, "4")
    THREE = (3, "3")
    TWO = (2, "2")
    
    
class CardFormatException(Exception):
    pass
    
    
class Card:
    def __init__(self, suit, number):
        self.suit = suit
        self.number = number
        
    @classmethod
    def from_short_name(cls, short_name):
        suit = short_name[0]
        number = short_name[1]
        return Card(Suit.from_short_name(suit), Number.from_short_name(number))

    def to_json(self):
        return self.__repr__()
    
    def __repr__(self):
        return self.suit.short_name + self.number.short_name
    
    def __eq__(self, other):
        return other is not None and self.suit == other.suit and self.number == other.number
    
    def value(self):
        return self.suit.strength * 14 + self.number.strength
    
    def ordering_value(self, num_of_voids, has_club_void, has_heart_void):
        special_order = None
        if num_of_voids == 1 and has_club_void:
            special_order = {Suit.CLUBS: 0, Suit.DIAMONDS: 1, Suit.SPADES: 2, Suit.HEARTS: 3}
        elif num_of_voids == 1 and has_heart_void:
            special_order = {Suit.HEARTS: 0, Suit.CLUBS: 1, Suit.DIAMONDS: 2, Suit.SPADES: 3}
        return self.suit.user_friendly_order_number(special_order) * 14 + self.number.strength

def is_higher(card1, card2, not_trump):
    if not_trump:
        if card1.suit != not_trump and card2.suit != not_trump:
            return (card1.number > card2.number) or (card1.number == card2.number and card1.suit > card2.suit)
        elif card1.suit == not_trump and card2.suit == not_trump:
            return card1.number > card2.number
        elif card1.suit == not_trump:
            return False
        else:
            return True
