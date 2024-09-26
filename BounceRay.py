import pygame
from pygame import Vector2
from ray import Ray
import numpy as np

def angleto360(angle):
    return (angle + 3600) % 360

class BounceRay:
    def __init__(self, pos : Vector2|tuple, pos2 : Vector2|tuple = (-1, -1), iterations : int = 100):
        self.p1 = Vector2(pos)
        self.p2 = Vector2(pygame.mouse.get_pos()) if pos2 != (-1, -1) else Vector2(pos2)
        self.ray : Ray = Ray(self.p1, self.p2)
        self.color = (255, 255, 255, 255)
        self.child = ChildBounceRay(self.color, iterations - 1)
        self.angleOffset : float = 0
        self.angleOffsetChange : float = 0.0001

    def update(self, 
               screen : pygame.Surface, 
               colliders : list[Ray], 
               keys : list):
        if keys[pygame.K_LEFT]:
            self.angleOffset -= self.angleOffsetChange
        elif keys[pygame.K_RIGHT]:
            self.angleOffset += self.angleOffsetChange

        self.p2 = Vector2(pygame.mouse.get_pos())
        self.ray.pos2 = self.p2
        angle = self.ray.getAngle() + self.angleOffset
        dist = self.ray.getRayLength()
        self.p2 = Vector2(np.cos(np.radians(angle)) * dist, np.sin(np.radians(angle)) * dist)
        self.ray.pos2 = self.p2
        
        closestCollision = None
        for ray in colliders:
            data = self.ray.lineCollisionPoint(ray)

            #draws Normals
            drawNormals = False
            if drawNormals:
                angle = angleto360(ray.getNormal())
                pygame.draw.line(screen, (255, 0, 0), ray.getMidPoint(), ray.getMidPoint() + Vector2(np.cos(np.radians(angle)) * 10, np.sin(np.radians(angle)) * 10))

            if data != None:
                data += ray.getNormal(),
                if closestCollision == None:
                    closestCollision = data
                elif data[1] < closestCollision[1]:
                    closestCollision = data
        
        if closestCollision != None:
            pygame.draw.line(screen, self.color, self.p1, closestCollision[0], 1)
            # pygame.draw.circle(screen, (255, 0, 255), closestCollision[0], 3)
            if self.child != None:
                normal = closestCollision[2]
                rayAngle = self.ray.getAngle()
                relAngle = rayAngle - normal
                angle = normal - relAngle + 180
                self.child.update(screen, colliders, closestCollision[0], angle)
        else:
            pygame.draw.line(screen, self.color, self.p1, pygame.mouse.get_pos(), 1)

class ChildBounceRay:
    def __init__(self, color : tuple, iterations : int = 1, collisionDistance : float = 1000) -> None:
        self.p1 = Vector2(-1, -1)
        self.p2 = Vector2(-1, -1)

        self.color = color

        self.ray = Ray(self.p1, self.p2)
        self.dist = collisionDistance
        self.iterations = iterations

        self.child : ChildBounceRay|None = None
        print(iterations)
        if iterations > 1:
            self.child = ChildBounceRay(self.color, iterations - 1)

    def update(self,
               screen : pygame.Surface,
               colliders : list[Ray],
               newP1 : Vector2|tuple,
               angle : float):
        self.p1 = Vector2(newP1)
        self.ray.pos1 = self.p1

        self.p2 = self.p1 + Vector2(np.cos(np.radians(angle)) * self.dist, np.sin(np.radians(angle)) * self.dist)
        self.ray.pos2 = self.p2
        
        collisionPoints = []
        closestCollision = None
        for ray in colliders:
            data = self.ray.lineCollisionPoint(ray)
            if data != None:
                data += ray.getNormal(),
                collisionPoints.append(data)
                if data[1] != 0 and closestCollision == None:
                    closestCollision = data
                elif data[1] != 0 and data[1] < closestCollision[1]:
                    closestCollision = data

        if closestCollision != None:
            if self.p1 == closestCollision[0]:
                pass
        
        if closestCollision != None:
            pygame.draw.line(screen, (255, 255, 255), self.p1, closestCollision[0], 1)
            # pygame.draw.circle(screen, (255, 0, 255), closestCollision[0], 3)
            if self.child != None:
                normal = closestCollision[2]
                rayAngle = self.ray.getAngle()
                relAngle = rayAngle - normal
                angle = normal - relAngle + 180
                self.child.update(screen, colliders, closestCollision[0], angle)
        else:
            pygame.draw.line(screen, (255, 255, 255), self.p1, Vector2(np.cos(np.radians(angle)) * self.dist, np.sin(np.radians(angle)) * self.dist))