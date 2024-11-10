import pygame
from ray import Ray
from pygame import Vector2
from square import Square
import globals as gb
from BounceRay import BounceRay
from beziers.shapes import BezierCurve

class Arena:
    def __init__(self, boxScale : int = 500):
        p1 = Vector2((gb.SX - boxScale)//2,
                     (gb.SY - boxScale)//2)
        p4 = p1 + Vector2(boxScale, boxScale)
        
        self.sides = [
            Square((0, 0), (p1.x, gb.SY), activeEdges=[False, False, True, False]),
            Square((p1.x, 0), (p4.x, p1.y), activeEdges=[False, True, False, False]),
            Square((p4.x, 0), (gb.SX, gb.SY), activeEdges=[True, False, False, False]),
            Square((p1.x, p4.y), (p4.x, gb.SY), activeEdges=[False, False, False, True]),
            # Square(Vector2(gb.SX//2, gb.SY//2) - Vector2(25, 25), Vector2(gb.SX//2, gb.SY//2) + Vector2(25, boxScale/2 - 20))
        ]

        self.bounceRay = BounceRay(Vector2(gb.SX/2, p4.y - (boxScale/100)))

        self.beziers : list[BezierCurve] = []

        self.grabbedPoints = []

        self.cooldown = 0


    def update(self, screen : pygame.Surface, delta : float = .017):
        colliders : list[Ray] = []
        for square in self.sides:
            colliders += square.getColliders()
            square.update(screen)

        for bezier in self.beziers:
            colliders += bezier.getColliders()

        keys = pygame.key.get_pressed()

        self.bounceRay.update(screen, colliders, keys)

        for bezier in self.beziers:
            bezier.update(screen, 1, Vector2(0, 0), self.grabbedPoints, 0, "lines")

        self.cooldown += delta

        if self.cooldown >= .3:
            if keys[pygame.K_c]:
                self.beziers.append(BezierCurve(pygame.mouse.get_pos(), 5, drawMode="lines"))
                self.cooldown = 0