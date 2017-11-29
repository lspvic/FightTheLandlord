import random
import itertools
from functools import reduce
from card import Card, CType, CardGroup
from player_agent import Player


class PlayerRandom(Player):
    def __init__(self, game):
        """
        @:param game 游戏对象
        @:param cards 手牌
        @:param cardsDict 去掉花色的手牌
        """
        Player.__init__(self, game)
        self.id = -1
        self.remain = 0
        self.cardDict = dict()
        for i in range(3, 18):
            self.cardDict[i] = 0
        self.cards = list()
        self.cardCate = dict()
        for t in CType.__members__.values():
            self.cardCate[t] = list()

    def set_id(self, _id):
        self.id = _id

    def __repr__(self):
        return 'Player-{}\tRemain:{}\tCards:{}\tCardDict:{}'.format(self.id, self.remain, self.cards, self.cardDict)

    def __str__(self):
        # logger.error(self.cardDict)
        return 'Player-{}\tRemain:{}\t{}'.format(self.id, self.remain, reduce(
            lambda s, i: s + Card.card_str[i[0]]*i[1], self.cardDict.items(), ''))

    def reset(self):
        self.remain = 0
        self.cardDict.clear()
        for i in range(3, 18):
            self.cardDict[i] = 0
        self.cards.clear()
        for t in CType.__members__.values():
            self.cardCate[t].clear()

    def add_card(self, n):
        # logger.debug('add card {} -> {}'.format(n, Card.decode(n)))
        self.cards.append(n)
        self.cardDict[Card.decode(n)] += 1
        self.remain += 1

    def pretreatment(self):
        for (k, v) in self.cardDict.items():
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
                j += 1
            if j == i + 4:
                while j < 15:
                    if self.cardDict[j] == 0:
                        break
                    else:
                        cc = CardGroup(CType.Sequence, j - i + 1, i)
                        for k in range(i, j + 1):
                            cc.cards[k] = 1
                        self.cardCate[CType.Sequence].append(cc)
                        j += 1

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
                    if qua.value != self.cardCate[CType.Single][i].value and \
                                    qua.value != self.cardCate[CType.Single][j].value:
                        cc = CardGroup(CType.FourPlusSingle, 6, qua.value)
                        cc.cards[qua.value] = 4
                        cc.cards[self.cardCate[CType.Single][i].value] = 1
                        cc.cards[self.cardCate[CType.Single][j].value] = 1
                        self.cardCate[CType.FourPlusSingle].append(cc)

        for i in range(0, len(self.cardCate[CType.Pair])):
            for j in range(i + 1, len(self.cardCate[CType.Pair])):
                for qua in self.cardCate[CType.Bomb]:
                    if qua.value != self.cardCate[CType.Pair][i].value and \
                                    qua.value != self.cardCate[CType.Pair][j].value:
                        cc = CardGroup(CType.FourPlusPair, 8, qua.value)
                        cc.cards[qua.value] = 4
                        cc.cards[self.cardCate[CType.Pair][i].value] = 2
                        cc.cards[self.cardCate[CType.Pair][j].value] = 2
                        self.cardCate[CType.FourPlusPair].append(cc)

        for air in self.cardCate[CType.SequenceOfTriplets]:
            cnt = air.num // 3
            if len(self.cardCate[CType.Single]) >= cnt * 2:
                for comb in itertools.combinations([i for i in self.cardCate[CType.Single]
                                                    if i.value not in air.cards.keys()], cnt):
                    cc = CardGroup(CType.AirplanePlusSingle, cnt * 4, air.value)
                    cc.cards = air.cards.copy()
                    for single in comb:
                        cc.cards[single.value] = 1
                    self.cardCate[CType.AirplanePlusSingle].append(cc)

        for air in self.cardCate[CType.SequenceOfTriplets]:
            cnt = air.num // 3
            if len(self.cardCate[CType.Pair]) > cnt * 2:
                for comb in itertools.combinations([i for i in self.cardCate[CType.Pair]
                                                    if i.value not in air.cards.keys()], cnt):
                    cc = CardGroup(CType.AirplanePlusSingle, cnt * 5, air.value)
                    cc.cards = air.cards.copy()
                    for pair in comb:
                        cc.cards[pair.value] = 2
                    self.cardCate[CType.AirplanePlusPair].append(cc)

        if self.cardDict[16] == 1 and self.cardDict[17] == 1:
            cc = CardGroup(CType.Bomb, 2, Card.max_value)
            cc.cards[16] = 1
            cc.cards[17] = 1
            self.cardCate[CType.Bomb].append(cc)

    def play(self):
        """
        出牌
        :return: CardGroup（这次出的牌）
        """
        if self.game.c_id == self.id:    # 自己出牌
            available = reduce(lambda x, y: x + y, self.cardCate.values())
        else:   # 接牌
            available = [cc for cc in self.cardCate[self.game.cc.type]
                         if cc.value > self.game.cc.value and cc.num == self.game.cc.num]
            if self.game.cc.type != CType.Bomb:
                available += self.cardCate[CType.Bomb]
            available.append(CardGroup(CType.Null))

        cc = random.choice(available)

        # logger.error('available: {}'.format([str(i) for i in available]))
        # logger.error('{} before update: {}'.format(Game.cc.type.name, [str(i) for i in self.cardCate[Game.cc.type]]))
        self.update_cate(cc)
        # logger.error('{} after update: {}'.format(Game.cc.type.name, [str(i) for i in self.cardCate[Game.cc.type]]))
        return cc

    def update_cate(self, cc):
        """
        出牌后更新cate
        :param cc: 这一次的出牌（CardGroup）
        """
        if not cc or cc.type == CType.Null:
            return
        self.remain -= cc.num
        for (k, v) in cc.cards.items():
            self.cardDict[k] -= v
        for li in self.cardCate.values():
            sub = list()
            for i in li:
                for (k2, v2) in i.cards.items():
                    if self.cardDict[k2] < v2:
                        sub.append(i)
                        break
            for i in sub:
                li.remove(i)
