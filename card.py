import random
from enum import Enum
from functools import reduce


class Card:
    """一副扑克牌"""
    def __init__(self):
        self.cards = [i for i in range(0, 54)]
        self.remain = 54

    def shuffle(self):
        """洗牌"""
        random.shuffle(self.cards)
        self.remain = 54

    max_value = 1000

    @staticmethod
    def decode(n):
        """
        把0-53转换成3-17权值，其中A（14）、2（15）、小王（16）、大王（17）
        :return: int (3 - 17)
        """
        return (n // 4 + 3) if n < 52 else n - 36

    card_str = 'XXX3456789TJQKA2@#'


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

    def __repr__(self):
        return 'Type:{}\tNum:{}\tValue:{}\tCards{}'.format(self.type.name, self.num, self.value, self.cards)

    def __str__(self):
        return '{}_Num({})_Value({})_{}'.format(self.type.name, self.num, self.value, reduce(
            lambda s, i: s + Card.card_str[i[0]]*i[1], self.cards.items(), ''))
