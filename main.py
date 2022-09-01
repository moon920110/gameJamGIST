import pygame
import random
import copy

from emotion_recognition.emotion_hijacker import emotionHijacker

colors = [
    (0, 0, 0),
    (120, 37, 179),
    (100, 179, 179),
    (80, 34, 22),
    (80, 134, 22),
    (180, 34, 22),
    (180, 34, 122),
]


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

    def new_figure(self):
        if self.figure == None:
            self.figure = Figure(3, 0, self.emotion)
            self.next_figure = Figure(3, 0, self.emotion)
        else:
            self.figure = copy.deepcopy(self.next_figure)
            self.next_figure = Figure(3, 0, self.emotion)

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


# Initialize the game engine
pygame.init()
emotion_hijacker = emotionHijacker()
emotion_hijacker.ready()

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

size = (500, 600)
next_block_draw = int(Tetris.zoom * 13.1), Tetris.zoom * 9
next_block_size = Tetris.zoom * 5

screen = pygame.display.set_mode(size)

pygame.display.set_caption("Tetris")

# Loop until the user clicks the close button.
MAX_LEVEL = 30
INIT_LEVEL = 2
done = False
clock = pygame.time.Clock()
fps = 60
game = Tetris(20, 10)
counter = 0

pressing_down = False

while not done:
    if game.figure is None:
        game.new_figure()
    counter += 1
    if counter > 100000:
        counter = 0

    if counter % (fps // game.level // 2) == 0 or pressing_down:
        game.emotion = emotion_hijacker.hijack()
        if game.emotion == 0:
            if game.level < MAX_LEVEL/2:
                game.level += 1
        else:
            game.level = INIT_LEVEL
        if game.state == "start":
            game.go_down()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                game.rotate()
            if event.key == pygame.K_DOWN:
                pressing_down = True
            if event.key == pygame.K_LEFT:
                game.go_side(-1)
            if event.key == pygame.K_RIGHT:
                game.go_side(1)
            if event.key == pygame.K_SPACE:
                game.go_space()
            if event.key == pygame.K_ESCAPE:
                game.__init__(20, 10)

    if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                pressing_down = False

    screen.fill(WHITE)

    for i in range(game.height):
        for j in range(game.width):
            pygame.draw.rect(screen, GRAY, [game.x + game.zoom * j, game.y + game.zoom * i, game.zoom, game.zoom], 1)
            if game.field[i][j] > 0:
                pygame.draw.rect(screen, colors[game.field[i][j]],
                                 [game.x + game.zoom * j + 1, game.y + game.zoom * i + 1, game.zoom - 2, game.zoom - 1])

    if game.figure is not None:
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in game.figure.image():
                    pygame.draw.rect(screen, colors[game.figure.color],
                                     [game.x + game.zoom * (j + game.figure.x) + 1,
                                      game.y + game.zoom * (i + game.figure.y) + 1,
                                      game.zoom - 2, game.zoom - 2])

    pygame.draw.rect(screen, GRAY, [next_block_draw[0], next_block_draw[1], next_block_size, next_block_size])
    
    if game.next_figure is not None:
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in game.next_figure.image():
                    pygame.draw.rect(screen, colors[game.next_figure.color],
                                     [next_block_draw[0] + game.zoom * (j + game.next_figure.x-2),
                                      next_block_draw[1] + game.zoom * (i + game.next_figure.y+1),
                                      game.zoom - 2, game.zoom - 2])


    font = pygame.font.SysFont('Calibri', 25, True, False)
    font1 = pygame.font.SysFont('Calibri', 65, True, False)
    font2 = pygame.font.SysFont('Calibri', 25, True, False)
    text = font.render("Score: " + str(game.score), True, BLACK)
    speed = font2.render("Speed: " + str(game.level), True, BLACK)
    next = font2.render("Next block", True, BLACK)
    text_game_over = font1.render("Game Over", True, (255, 125, 0))
    text_game_over1 = font1.render("Press ESC", True, (255, 215, 0))

    screen.blit(text, [106, 11])
    screen.blit(next, [330, 180])
    screen.blit(speed, [330, 410])
    if game.state == "gameover":
        screen.blit(text_game_over, [20, 200])
        screen.blit(text_game_over1, [25, 265])

    pygame.display.flip()
    clock.tick(fps)

pygame.quit()