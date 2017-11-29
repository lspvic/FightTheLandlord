import logging
import logging.config
from card import Card, CType, CardGroup

logger = logging.getLogger('main.game')


class Game:
    def __init__(self):
        """
        @:param players 对弈的人，0-地主 1-地主下家 2-地主上家
        @:param status 游戏状态，0-未开始 1-发牌 2-叫地主 3-打牌中 4-游戏结束
        @:param card 一副扑克牌
        @:param winner 赢家
        @:param cnt 出排序号
        @:param c_id 上一次出牌的人
        @:param cc 上一次出的牌
        @:param historyCards 已经出掉的牌集合
        :return:
        """
        self.players = []
        self.status = 0
        self.card = Card()
        self.winner = None
        self.cnt = 0
        self.c_id = 0
        self.cc = None
        self.historyCards = dict()

    def add_player(self, player):
        if len(self.players) < 3:
            self.players.append(player)
            return True
        else:
            return False

    def deal_card(self):
        """发牌"""
        self.status = 1
        self.card.shuffle()
        for i in range(0, 51, 3):
            for j in range(0, 3):
                self.players[j].add_card(self.card.cards[i + j])

    def claim(self):
        """叫地主 抢地主"""
        self.status = 2
        # set Landlord to player 0
        for i in range(0, 3):
            self.players[i].set_id(i)
        self.c_id = self.players[0].id
        for i in range(51, 54):
            self.players[0].add_card(self.card.cards[i])

    def _test_deal_claim(self):
        for i in range(0, 18):
            self.players[0].add_card(i)

    def reset(self):
        self.status = 0
        self.cnt = 0
        self.winner = None
        self.c_id = self.players[0].id
        self.cc = CardGroup(CType.Null)
        self.historyCards.clear()
        for i in range(3, 18):
            self.historyCards[i] = 0
        for player in self.players:
            player.reset()

    def start(self):
        """开始打牌"""
        assert len(self.players) == 3
        self.reset()
        self.card.shuffle()
        self.deal_card()
        self.claim()
        # self._test_deal_claim()
        for player in self.players:
            player.pretreatment()
        self.rounds()

    def rounds(self):
        """
        play rounds after claim and player.pretreatment, Called by method new_game
        """
        self.status = 3
        while not self.winner:
            for i in range(0, 3):
                self.cnt += 1
                logger.debug('Sequence-{} {}'.format(self.cnt, self.players[i]))
                temp_cc = self.players[i].play()
                logger.debug('Play cards: {}'.format(temp_cc))
                if temp_cc and temp_cc.type != CType.Null:
                    self.cc = temp_cc
                    self.c_id = self.players[i].id
                    for (k, v) in self.cc.cards.items():
                        self.historyCards[k] += v
                # logger.debug('History cards: {}'.format(self.historyCards))
                if self.players[i].remain == 0:
                    self.winner = self.players[i]
                    break
        self.gameover()

    def gameover(self):
        self.status = 4
        logger.info('Winner is {}'.format(self.winner))

