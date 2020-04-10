from game import Game
from player import Player
from cli_client_interface import CLIClientInterface


if __name__ == "__main__":
    client_interface = CLIClientInterface()
    players = [Player(client_interface, 0),
               Player(client_interface, 1),
               Player(client_interface, 2),
               Player(client_interface, 3)]
    game = Game(client_interface, players)
    game.new_game()
