import copy
import random
from collections import deque
from core.figure import Figure
from common.const import *


class Tetris:
    level = 2
    score = 0
    state = "start"
    field = []
    height = 0
    width = 0
    x = int(SIZE[0] * 0.25)  # location of tetris window
    y = int(SIZE[1] * 0.1)  # location of tetris window
    zoom = int(SIZE[0] * 0.015)  # size of tetris square
    figure = None

    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.field = []
        self.score = 0
        self.state = "start"
        for i in range(height):
            new_line = []
            for j in range(width):
                new_line.append(0)
            self.field.append(new_line)

        self.emotion = 0  # init by neutral
        self.emotion_labels = ['NEUTRAL', 'HAPPY', 'ANGRY', 'SURPRISING', 'OTHERS']
        self.block_labels = ['l', 'L', 'T', 'Z', 'O']
        self.emotion_history = deque([], maxlen=10)
        self.rule = [i for i in range(5)]  # 0-vertical, 1-L, 2-T, 3-z, 4-square
        self.speeds = [5, 1, 3, 2, 4]
        random.shuffle(self.rule)

    def new_figure(self, soft_reset=False):
        if soft_reset:
            self.next_figure = Figure(3, 0, self.emotion, self.rule)
        else:
            if self.figure == None:
                self.figure = Figure(3, 0, self.emotion, self.rule)
                self.next_figure = Figure(3, 0, self.emotion, self.rule)
            else:
                self.figure = copy.deepcopy(self.next_figure)
                self.next_figure = Figure(3, 0, self.emotion, self.rule)

    def intersects(self):
        intersection = False
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    if i + self.figure.y > self.height - 1 or \
                            j + self.figure.x > self.width - 1 or \
                            j + self.figure.x < 0 or \
                            self.field[i + self.figure.y][j + self.figure.x] > 0:
                        intersection = True
        return intersection

    def break_lines(self):
        lines = 0
        for i in range(1, self.height):
            zeros = 0
            for j in range(self.width):
                if self.field[i][j] == 0:
                    zeros += 1
            if zeros == 0:
                lines += 1
                for i1 in range(i, 1, -1):
                    for j in range(self.width):
                        self.field[i1][j] = self.field[i1 - 1][j]
        self.score += lines ** 2

    def go_space(self):
        while not self.intersects():
            self.figure.y += 1
        self.figure.y -= 1
        self.freeze()

    def go_down(self):
        self.figure.y += 1
        if self.intersects():
            self.figure.y -= 1
            self.freeze()

    def freeze(self):
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    self.field[i + self.figure.y][j + self.figure.x] = self.figure.color
        self.break_lines()
        self.new_figure()
        if self.intersects():
            self.state = "gameover"

    def go_side(self, dx):
        old_x = self.figure.x
        self.figure.x += dx
        if self.intersects():
            self.figure.x = old_x

    def rotate(self):
        old_rotation = self.figure.rotation
        self.figure.rotate()
        if self.intersects():
            self.figure.rotation = old_rotation

    def set_emotion(self, emotion):
        def most_frequent(List):
            counter = 0
            num = List[0]

            for i in List:
                curr_frequency = List.count(i)
                if (curr_frequency > counter):
                    counter = curr_frequency
                    num = i

            return num

        self.emotion_history.append(emotion)
        freq_emo = most_frequent(self.emotion_history)
        if self.emotion != freq_emo:
            self.emotion = freq_emo
            self.new_figure(True)
            self.level = self.speeds[self.emotion]
