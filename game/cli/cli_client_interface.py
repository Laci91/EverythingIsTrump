from game.core.client_interface import ClientInterface


class CLIClientInterface(ClientInterface):
    
    def send_error(self, error_message):
        print(error_message)
        
    def send_trick_evaluation(self, trick_status_message):
        print("Player %s took the trick #%d" % (trick_status_message["taker"], trick_status_message["trickNumber"]))
    
    def send_round_evaluation(self, client_updates):
        for update in client_updates:
            print("Player %s failed (bid %d, made %s), got %d points" % (
                update["player"], update["bid"], update["tricks"], update["points"]))
            
    def send_standing_update(self, standing_update):
        print("Current standing: ")
        counter = 1
        for update in standing_update:
            print("%d. Player %d, %d points" % (counter, update["player"], update["points"]))
            counter += 1
    
    def query_bid(self, hand, excluded_bid):
        print("Your hand is " + ",".join([str(c) for c in hand]))
        return input("Please make a bid: ")
    
    def query_card_play(self, hand, led_suit):
        print("Your hand is " + ",".join([str(c) for c in hand]))
        return input("Please play a card: ")
