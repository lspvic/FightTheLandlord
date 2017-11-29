from abc import ABCMeta, abstractmethod


class Player:
    __metaclass__ = ABCMeta

    def __init__(self, game):
        self.game = game

    @abstractmethod
    def set_id(self, _id):
        """
        设置id
        :param _id: 0-地主 1-地主下方 2-地主上方
        :return:
        """
        pass

    @abstractmethod
    def add_card(self, n):
        """
        发牌（该方法会连续调用，直到发牌完成）
        :param n: 0-53（从3到大王，带花色，eg：0123对应3,4567对应4,52对应小王，53对应大王）
        :return:
        """
        pass

    @abstractmethod
    def pretreatment(self):
        """
        发完牌，开始出牌之前的预处理
        :return:
        """
        pass

    @abstractmethod
    def reset(self):
        """
        情况状态，准备开始新的一局
        :return:
        """
        pass

    @abstractmethod
    def play(self):
        """
        出牌
        :return: CardGroup（这次出的牌）
        """
        pass

