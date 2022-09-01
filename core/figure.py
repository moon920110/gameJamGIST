import random

from common.const import *

class Figure:
    x = 0
    y = 0

    figures = [
        [[1, 5, 9, 13], [4, 5, 6, 7]],  # vertical blocks
        [[4, 5, 9, 10], [2, 6, 5, 9]],  # left z blocks
        [[6, 7, 9, 10], [1, 5, 6, 10]],  # right z blocks
        [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],  # p blocks
        [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],  # q blocks
        [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],  # T blocks
        [[1, 2, 5, 6]],  # square block
    ]

    def __init__(self, x, y, emotion, rule):
        ###
        # emotion:
        # neutral 0 - speed 10
        # happy 1 - speed 2
        # angry 2 - speed 6
        # surprising 3 - speed 4
        # others 4 - speed 8
        ###

        self.x = x
        self.y = y
        if emotion is None:
            emotion = 4
        if rule[emotion] == 0:  # vert
            self.type = 0
        elif rule[emotion] == 1:  # L
            self.type = random.randint(3, 4)
        elif rule[emotion] == 2:  # T
            self.type = 5
        elif rule[emotion] == 3:  # z
            self.type = random.randint(1, 2)
        else:  # sqr
            self.type = 6

        self.color = random.randint(1, len(colors) - 1)
        self.rotation = 0

    def image(self):
        return self.figures[self.type][self.rotation]

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.figures[self.type])
