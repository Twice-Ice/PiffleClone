import pygame
from pygame import Vector2
from ray import Ray

class Square:
    def __init__(self, 
                 pos : Vector2|tuple, 
                 endPos : Vector2|tuple, 
                 activeEdges : list[bool] = [True, True, True, True],
                 drawn : bool = True) -> None:
        """
        p1 -- p2
         |    |
        p4 -- p3

        Active edges assigned as [Left, Bottom, Right, Top]
        """
        p1 = Vector2(pos)
        p3 = Vector2(endPos)
        p2 = Vector2(p1.x, p3.y)
        p4 = Vector2(p3.x, p1.y)

        self.points = [p1, p2, p3, p4]
        self.activeEdges = activeEdges

        self.color = (0, 255, 0)

    def getColliders(self) -> list[Ray]:
        rays = []
        for i in range(len(self.points)):
            if self.activeEdges[i]:
                rays.append(Ray(self.points[i], self.points[(i+1) % len(self.points)]))
        return rays

    def draw(self, screen : pygame.Surface) -> None:
        pygame.draw.polygon(screen, self.color, self.points)

    def update(self, screen : pygame.Surface) -> None:
        self.draw(screen)