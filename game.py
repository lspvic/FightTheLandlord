import os
import random
import itertools
from enum import Enum
import logging.config


os.chdir(os.path.dirname(__file__))
config_file = os.path.join(os.getcwd(), 'logging.conf')
logging.config.fileConfig(str(config_file))
logger = logging.getLogger(__name__)


class Card:
    """一副扑克牌"""
    def __init__(self):
        self.cards = [i for i in range(0, 54)]
        self.remain = 54

    def shuffle(self):
        """洗牌"""
        random.shuffle(self.cards)
        self.remain = 54

    @staticmethod
    def decode(n):
        """
        把0-53转换成3-17权值，其中A（14）、2（15）、小王（16）、大王（17）
        :return: int (3 - 17)
        """
        return (n / 4 + 3) if n < 52 else n - 36


class CType(Enum):
    """单次出牌的类型"""
    Null = 0
    Single = 1
    Pair = 2
    Triplet = 3
    Sequence = 4
    SequenceOfPairs = 5
    SequenceOfTriplets = 6
    TripletPlusSingle = 7
    TripletPlusPair = 8
    AirplanePlusSingle = 9
    AirplanePlusPair = 10
    FourPlusSingle = 11
    FourPlusPair = 12
    Bomb = 13


class Game:
    def __init__(self):
        self.players = [Player() for _ in range(3)]
        self.card = Card()

    def deal_card(self):
        """发牌"""
        self.card.shuffle()
        for i in range(0, 51):
            for j in range(3):
                self.players[j].add_card(i)

    def claim(self):
        """叫地主 抢地主"""
        # set Landlord to player 0
        for i in range(51, 54):
            self.players[0].add_card(i)

    def new_game(self):
        """开始打牌"""
        for player in self.players:
            player.reset()
        self.card.shuffle()
        self.deal_card()
        self.claim()
        pass

    def _play(self):
        for player in self.players:
            player.analysis_cate()
            logger.debug('player {0}', player)
            logger.debug(player.remain)
            logger.debug(player.cards)
            logger.debug(player.cardDict)
            logger.debug(player.cardCate)
        pass


class Player:
    def __init__(self):
        """
        @:param cards 手牌
        @:param cardsDict 去掉花色的手牌
        """
        self.remain = 0
        self.cardDict = dict()
        for i in range(3, 18):
            self.cardDict[i] = 0
        self.cards = list()
        self.cardCate = dict()
        for t in CType.__members__.values():
            self.cardCate[t] = list()

    def reset(self):
        self.remain = 0
        self.cardDict.clear()
        for i in range(3, 18):
            self.cardDict[i] = 0
        self.cards.clear()
        self.cardCate.clear()
        for t in CType.__members__.values():
            self.cardCate[t].clear()

    def add_card(self, n):
        self.cards.append(n)
        self.cardDict[Card.decode(n)] += 1
        self.remain += 1

    def analysis_cate(self):
        for k, v in self.cardDict:
            if v > 3:
                cc = CardGroup(CType.Bomb, 4, k)
                cc.cards[k] = 4
                self.cardCate[CType.Bomb].append(cc)
            if v > 2:
                cc = CardGroup(CType.Triplet, 3, k)
                cc.cards[k] = 3
                self.cardCate[CType.Triplet].append(cc)
            if v > 1:
                cc = CardGroup(CType.Pair, 2, k)
                cc.cards[k] = 2
                self.cardCate[CType.Pair].append(cc)
            if v > 0:
                cc = CardGroup(CType.Single, 1, k)
                cc.cards[k] = 1
                self.cardCate[CType.Single].append(cc)

        for i in range(3, 11):
            j = i
            while j < i + 4 and self.cardDict[j] > 0:
                j -= 1
            if j == i + 4:
                while j < 15:
                    if self.cardDict[j] == 0:
                        break
                    else:
                        cc = CardGroup(CType.Sequence, j - i + 1, i)
                        for k in range(i, j + 1):
                            cc.cards[k] = 1
                            self.cardCate[CType.Sequence].append(cc)

        for i in range(3, 13):
            if self.cardDict[i] > 1 and self.cardDict[i + 1] > 1:
                for j in range(i + 2, 15):
                    if self.cardDict[j] < 2:
                        break
                    else:
                        cc = CardGroup(CType.SequenceOfPairs, (j - i + 1) * 2, i)
                        for k in range(i, j + 1):
                            cc.cards[k] = 2
                            self.cardCate[CType.SequenceOfPairs].append(cc)

        for i in range(3, 14):
            if self.cardDict[i] > 2:
                for j in range(i + 1, 15):
                    if self.cardDict[j] < 3:
                        break
                    else:
                        cc = CardGroup(CType.SequenceOfTriplets, (j - i + 1) * 3, i)
                        for k in range(i, j + 1):
                            cc.cards[k] = 3
                            self.cardCate[CType.SequenceOfTriplets].append(cc)

        for triplet in self.cardCate[CType.Triplet]:
            for single in self.cardCate[CType.Single]:
                if triplet.value != single.value:
                    cc = CardGroup(CType.TripletPlusSingle, 4, triplet.value)
                    cc.cards[triplet.value] = 3
                    cc.cards[single.value] = 1
                    self.cardCate[CType.TripletPlusSingle].append(cc)

        for triplet in self.cardCate[CType.Triplet]:
            for pair in self.cardCate[CType.Pair]:
                if triplet.value != pair.value:
                    cc = CardGroup(CType.TripletPlusPair, 5, triplet.value)
                    cc.cards[triplet.value] = 3
                    cc.cards[pair.value] = 2
                    self.cardCate[CType.TripletPlusPair].append(cc)

        for i in range(0, len(self.cardCate[CType.Single])):
            for j in range(i + 1, len(self.cardCate[CType.Single])):
                for qua in self.cardCate[CType.Bomb]:
                    cc = CardGroup(CType.FourPlusSingle, 6, qua.value)
                    cc.cards[qua.value] = 4
                    cc.cards[self.cardCate[CType.Single][i].value] = 1
                    cc.cards[self.cardCate[CType.Single][j].value] = 1
                    self.cardCate[CType.FourPlusSingle].append(cc)

        for i in range(0, len(self.cardCate[CType.Pair])):
            for j in range(i + 1, len(self.cardCate[CType.Pair])):
                for qua in self.cardCate[CType.Bomb]:
                    cc = CardGroup(CType.FourPlusSingle, 8, qua.value)
                    cc.cards[qua.value] = 4
                    cc.cards[self.cardCate[CType.Pair][i].value] = 2
                    cc.cards[self.cardCate[CType.Pair][j].value] = 2
                    self.cardCate[CType.FourPlusPair].append(cc)

        for air in self.cardCate[CType.SequenceOfTriplets]:
            cnt = air.num / 3
            if len(self.cardCate[CType.Single]) > cnt * 2:
                sub = list()
                for i in self.cardCate[CType.Single]:
                    if i in air.cards.keys():
                        sub.append(i)
                for comb in itertools.combinations([i for i in self.cardCate[CType.Single] if i not in sub], cnt):
                    cc = CardGroup(CType.AirplanePlusSingle, cnt * 4, air.value)
                    cc.cards = air.cards.copy()
                    for single in comb:
                        cc.cards[single.value] = 1
                    self.cardCate[CType.AirplanePlusSingle].append(cc)

        for air in self.cardCate[CType.SequenceOfTriplets]:
            cnt = air.num / 3
            if len(self.cardCate[CType.Pair]) > cnt * 2:
                sub = list()
                for i in self.cardCate[CType.Pair]:
                    if i in air.cards.keys():
                        sub.append(i)
                for comb in itertools.combinations([i for i in self.cardCate[CType.Pair] if i not in sub], cnt):
                    cc = CardGroup(CType.AirplanePlusSingle, cnt * 5, air.value)
                    cc.cards = air.cards.copy()
                    for pair in comb:
                        cc.cards[pair.value] = 2
                    self.cardCate[CType.AirplanePlusPair].append(cc)

        if 16 in self.cardDict.keys() and 17 in self.cardDict.keys():
            cc = CardGroup(CType.Bomb, 2, 100)
            cc.cards[16] = 1
            cc.cards[17] = 1
            self.cardCate[CType.Bomb].append(cc)


class CardGroup:
    def __init__(self, ctype=CType.Null, num=0, value=0):
        """
        @:param value 权重,用来比较同类牌
        @:param num 牌的数量
        """
        self.type = ctype
        self.cards = dict()
        self.num = num
        self.value = value

    def clear(self):
        self.type = CType.Null
        self.cards.clear()
        self.num = 0
        self.value = 0

    def add(self, card, num=1):
        self.cards[card] = num


if __name__ == '__main__':
    Game().new_game()
