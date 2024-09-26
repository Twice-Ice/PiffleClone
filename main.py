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
    arena = Arena(750)

lineScreen = pygame.Surface((gb.SX, gb.SY), pygame.SRCALPHA)

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

    lineScreen.fill((0, 0, 0, 0))
    arena.update(lineScreen)

    screen.blit(lineScreen, (0, 0))

    pygame.display.flip()
pygame.quit()