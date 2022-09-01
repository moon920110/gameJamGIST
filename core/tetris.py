import copy
import random
from core.figure import Figure


class Tetris:
    level = 2
    score = 0
    state = "start"
    field = []
    height = 0
    width = 0
    x = 30
    y = 50
    zoom = 25
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
        self.emotion_labels = ['neutral', 'happy', 'angry', 'surprising', 'others']
        self.block_labels = ['Line', 'L', 'T', 'Z', 'SQUARE']
        self.rule = [i for i in range(5)]  # 0-vertical, 1-L, 2-T, 3-z, 4-square
        random.shuffle(self.rule)
        for i in range(5):
            print(f'{self.emotion_labels[i]}:{self.block_labels[i]} | ', end='')

    def new_figure(self):
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
        self.emotion = emotion
        if self.emotion == 0:
            self.level = 10
        elif self.emotion == 1:
            self.level = 2
        elif self.emotion == 2:
            self.level = 6
        elif self.emotion == 3:
            self.level = 4
        else:
            self.level = 8

