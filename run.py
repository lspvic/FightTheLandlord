import config
import logging
from game import Game
from player_random import PlayerRandom

logger = logging.getLogger('main')

if __name__ == '__main__':
    game = Game()
    logger.info('create game')
    for i in range(0, 3):
        game.add_player(PlayerRandom(game))
    logger.info('add new random agent')
    wins = [0, 0, 0]
    for i in range(0, 1000):
        game.start()
        wins[game.winner.id] += 1
    logger.info('wins: {}'.format(wins))
