from abc import ABC, abstractmethod


class ClientInterface(ABC):
    @abstractmethod
    def send_error(self, seat, error_message):
        pass
    
    @abstractmethod
    def send_trick_evaluation(self, trick_status_message):
        pass
    
    @abstractmethod
    def send_round_evaluation(self, result_updates):
        pass
    
    @abstractmethod
    def send_standing_update(self, standing_update):
        pass

    @abstractmethod
    def communicate_bid(self, seat, bid):
        pass

    @abstractmethod
    def communicate_next_bidder(self, next_player):
        pass

    @abstractmethod
    def communicate_next_card_player(self, next_player):
        pass
    
    @abstractmethod
    def trigger_new_round(self, next_round):
        pass

    @abstractmethod
    def trigger_end_of_game(self):
        pass
