import pygame
from pygame import Vector2
from ray import Ray
import numpy as np

class BounceRay:
    def __init__(self, pos : Vector2|tuple, iterations = 1):
        self.p1 = Vector2(pos)
        self.p2 = Vector2(pygame.mouse.get_pos())
        self.ray : Ray = Ray(self.p1, self.p2)
        self.color = (255, 255, 255)

    def draw(self, screen : pygame.Surface):
        self.ray.draw(screen, self.color, 1)

    def update(self, screen : pygame.Surface, colliders : list[Ray]):
        self.p2 = Vector2(pygame.mouse.get_pos())
        self.ray.pos2 = self.p2
        self.draw(screen)
        
        collisionPoints = []
        closestCollision = None
        for ray in colliders:
            data = ray.lineCollisionPoint(self.ray)
            if data != None:
                collisionPoints.append(data)
                if closestCollision == None:
                    closestCollision = data
                elif data[1] > closestCollision[1] or data[1] < closestCollision[1]:
                    closestCollision = data
        
        if len(collisionPoints) == 2:
            pass

        if closestCollision != None:
            pygame.draw.circle(screen, (255, 255, 255), closestCollision[0], 3)