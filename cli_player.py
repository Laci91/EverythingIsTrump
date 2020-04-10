from player import Player
from card import Card


class CLIPlayer(Player):
    def __init__(self, number):
        super().__init__(number)

    def make_bid(self, number_of_cards, excluded):
        print("Your hand is " + ",".join([str(c) for c in self.hand]))
        if excluded is not None:
            print("You cannot bid " + str(excluded))
        bid = excluded
        
        while bid == excluded:
            bid = int(input("[" + str(self.number) + "] Please make a bid: "))
            
        self.bid = bid
        
    def played_led_suit_if_possible(self, led_suit, chosen_card):
        if not chosen_card or chosen_card.suit == led_suit:
            return True
        
        return len([c for c in self.hand if c.suit == led_suit]) == 0

    def play_card(self, led_suit):
        card = None
        print("Your hand is " + ",".join([str(c) for c in self.hand]))
        while card not in self.hand or not self.played_led_suit_if_possible(led_suit, card):
            card = Card.from_short_name(input("[" + str(self.number) + "] Please play a card: "))
        
        self.hand.remove(card)
        return card
