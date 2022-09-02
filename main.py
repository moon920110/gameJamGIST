import pygame
import cv2

from emotion_recognition.emotion_hijacker import emotionHijacker
from core.tetris import Tetris
from common.const import *
import os

def game_main():
    # Initialize the game engine
    pygame.init()
    emotion_hijacker = emotionHijacker()
    emotion_hijacker.ready()

    # Define some colors
    next_block_draw = int(Tetris.zoom * 17), Tetris.zoom * 4
    next_block_size = Tetris.zoom * 5

    screen = pygame.display.set_mode(SIZE)

    pygame.display.set_caption("Tetris")

    # Loop until the user clicks the close button.
    done = False
    clock = pygame.time.Clock()
    game = Tetris(20, 10)
    counter = 0

    pressing_down = False

    while not done:
        if game.figure is None:
            game.new_figure()
        counter += 1
        if counter > 100000:
            counter = 0


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                emotion_hijacker.terminate()
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

        game.set_emotion(emotion_hijacker.hijack())
        if counter % (FPS // game.level // 2) == 0 or pressing_down:
            if game.state == "start":
                game.go_down()

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


        font1 = pygame.font.SysFont('Calibri', 65, True, False)
        font2 = pygame.font.SysFont('Calibri', 25, True, False)
        font3 = pygame.font.SysFont('Calibri', 18, True, False)
        speed = font2.render("Speed: ", True, BLACK)
        speed_num = font2.render(str(game.level), True, RED)
        next = font2.render("Next block", True, BLACK)
        emo = font2.render("Emotion: ", True, BLACK)
        game_emo = game.emotion
        emo_val = font2.render(str(game.emotion_labels[game_emo]), True, RED)
        text_game_over = font1.render("Game Over", True, (255, 125, 0))
        text_game_over1 = font1.render("Press ESC", True, (255, 215, 0))
        title = font2.render("Emotion (Speed) : Block type", True, GRAY)

        block_rules = []
        for i in range(5):
            block_rules.append(game.emotion_labels[i] + ' (' + str(game.speeds[i]) + ')'+ '  :  ' + game.block_labels[game.rule[i]])

        block_rules_0 = font3.render(block_rules[0], True, False)
        block_rules_1 = font3.render(block_rules[1], True, False)
        block_rules_2 = font3.render(block_rules[2], True, False)
        block_rules_3 = font3.render(block_rules[3], True, False)
        block_rules_4 = font3.render(block_rules[4], True, False)

        screen.blit(next, [420, 50])
        screen.blit(speed, [106, 11])
        screen.blit(speed_num, [206, 11])
        screen.blit(emo, [370, 500])
        screen.blit(emo_val, [490, 500])
        screen.blit(title, [180, 580])
        screen.blit(block_rules_0, [160, 610])
        screen.blit(block_rules_1, [160, 630])
        screen.blit(block_rules_2, [160, 650])
        screen.blit(block_rules_3, [360, 610])
        screen.blit(block_rules_4, [360, 630])

        if game.state == "gameover":
            screen.blit(text_game_over, [20, 200])
            screen.blit(text_game_over1, [25, 265])

        canvas, f_c = emotion_hijacker.get_frame()
        directory = "./gray/"
        if not os.path.exists(directory):
            os.makedirs(directory)

        sl = "./gray/img_gray.PNG"
        cv2.imwrite(sl, f_c)
        charImage = pygame.image.load(sl)
        charImage = charImage.convert()
        screen.blit(charImage, (340, 300))
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == '__main__':
    game_main()
