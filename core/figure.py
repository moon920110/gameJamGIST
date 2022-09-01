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

    def __init__(self, x, y, emotion):
        ###
        # emotion:
        # neutral - 0
        # happy - 1
        # angry - 2
        # surprising - 3
        # others - 4
        ###

        self.x = x
        self.y = y
        if emotion == 0 or emotion == 3:
            self.type = random.randint(0, len(self.figures) - 1)
        elif emotion == 1:
            self.type = 0
        else:
            self.type = 1 + random.randint(0, 1)
        self.color = random.randint(1, len(colors) - 1)
        self.rotation = 0

    def image(self):
        return self.figures[self.type][self.rotation]

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.figures[self.type])
