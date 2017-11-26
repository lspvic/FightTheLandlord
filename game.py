import random
from enum import Enum


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

    def run(self):
        """开始打牌"""
        pass


class Player:
    def __init__(self):
        """
        @:param cards 手牌
        @:param cardsDict 去掉花色的手牌
        """
        self.cardsDict = dict()
        for i in range(3, 18):
            self.cardsDict[i] = 0
        self.cards = list()

    def reset(self):
        self.cardsDict = dict()
        for i in range(3, 18):
            self.cardsDict[i] = 0
        self.cards = list()

    def add_card(self, n):
        self.cards.append(n)
        self.cardsDict[Card.decode(n)] += 1


class CardCate:
    def __init__(self):
        """
        @:param value 权重,用来比较同类牌
        @:param num 牌的数量
        """
        self.type = CType.Null
        self.cards = dict()
        self.num = 0
        self.value = 0

    def clear(self):
        self.type = CType.Null
        self.cards.clear()
        self.num = 0
        self.value = 0

    def add(self, card, n=1):
        pass
