from abc import ABC, abstractmethod


class ClientInterface(ABC):
    @abstractmethod
    def send_error(self, error_message):
        pass
    
    @abstractmethod
    def send_trick_evaluation(self, trick_status_message):
        pass
    
    @abstractmethod
    def send_round_evaluation(self, result_updates):
        pass
    
    @abstractmethod
    def send_standing_update(self, sending_update):
        pass
    
    @abstractmethod
    def query_bid(self, hand, excluded_bid):
        pass
    
    @abstractmethod
    def query_card_play(self, hand, led_suit):
        pass