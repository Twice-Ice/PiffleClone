import pygame
from ray import Ray
from pygame import Vector2
from square import Square
import globals as gb
from BounceRay import BounceRay

class Arena:
    def __init__(self, boxScale : int = 500):
        p1 = Vector2((gb.SX - boxScale)//2,
                     (gb.SY - boxScale)//2)
        p4 = p1 + Vector2(boxScale, boxScale)
        
        self.sides = [
            Square((0, 0), (p1.x, gb.SY), activeEdges=[False, False, True, False]),
            Square((p1.x, 0), (p4.x, p1.y), activeEdges=[False, True, False, False]),
            Square((p4.x, 0), (gb.SX, gb.SY), activeEdges=[True, False, False, False]),
            Square((p1.x, p4.y), (p4.x, gb.SY), activeEdges=[False, False, False, True])
        ]

        self.bounceRay = BounceRay(Vector2(gb.SX/2, p4.y - (boxScale/100)))

    def draw(self, screen : pygame.Surface):
        colliders : list[Ray] = []
        for square in self.sides:
            colliders += square.getColliders()
            square.update(screen)

        self.bounceRay.update(screen, colliders)

    def update(self, screen : pygame.Surface):
        self.draw(screen)