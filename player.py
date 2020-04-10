from card import Card, CardFormatException


class Player:
    def __init__(self, client_interface, number):
        self.client_interface = client_interface
        self.number = number
        self.hand = None
        self.bid = None
        self.tricks = 0
        self.points = 0
    
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

    def make_bid(self, number_of_cards, excluded):
        bid = excluded
    
        while bid == excluded or bid > number_of_cards or bid < 0:
            bid = int(self.client_interface.query_bid(self.hand, excluded))
        
            if bid == excluded:
                self.client_interface.send_error("The selected bit is forbidden")
            elif bid > number_of_cards:
                self.client_interface.send_error("The selected bid is too high")
            elif bid < 0:
                self.client_interface.send_error("The selected bid can't be negative")
    
        self.bid = bid

    def played_led_suit_if_possible(self, led_suit, chosen_card):
        if not chosen_card or chosen_card.suit == led_suit:
            return True
    
        return len([c for c in self.hand if c.suit == led_suit]) == 0

    def play_card(self, led_suit):
        card = None
        while card not in self.hand or not self.played_led_suit_if_possible(led_suit, card):
            try:
                card = Card.from_short_name(self.client_interface.query_card_play(self.hand, led_suit))

                if card not in self.hand:
                    self.client_interface.send_error("Don't try to cheat, this card is not in your hand!")
                elif not self.played_led_suit_if_possible(led_suit, card):
                    self.client_interface.send_error("You must play a %s since this suit was led" % led_suit)
            except CardFormatException as e:
                self.client_interface.send_error(e.args[0])
    
        self.hand.remove(card)
        return card
