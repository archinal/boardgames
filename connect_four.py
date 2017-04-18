from boardgames.connect_four.game import ConnectFourGame

from boardgames.connect_four.players import HumanConnectFourPlayer, AIConnectFourPlayer


def main():
    print('Starting a game of Connect Four...')
    game = ConnectFourGame(HumanConnectFourPlayer(0), AIConnectFourPlayer(1))
    game.run()

if __name__ == '__main__':
    main()
