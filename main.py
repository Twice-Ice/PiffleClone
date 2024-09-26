import pygame
from pygame import Vector2
import globals as gb
from arena import Arena

screen = pygame.display.set_mode((gb.SX, gb.SY), pygame.NOFRAME)

doExit = False
clock = pygame.time.Clock()

arena : Arena = None

def startGame():
    global arena
    arena = Arena(250)

startGame()
while not doExit:
    delta = clock.tick(gb.FPS)/1000
    screen.fill(gb.BG)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            doExit = True

    keys = pygame.key.get_pressed()
    if keys[pygame.K_r]:
        startGame()

    arena.update(screen)

    pygame.display.flip()
pygame.quit()