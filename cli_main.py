from game import Game
from cli_player import CLIPlayer


if __name__ == "__main__":
    players = [CLIPlayer(0), CLIPlayer(1), CLIPlayer(2), CLIPlayer(3)]
    game = Game(players)
    game.new_game()
