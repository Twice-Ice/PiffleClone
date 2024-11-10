import pygame, time, random, os
from pygame import Vector2
import numpy as np
import globals as gb

class Ray:
    def __init__(self, 
                 pos1 : Vector2|tuple, 
                 pos2 : Vector2|tuple,
                 flippedNormal : bool = False) -> None:
        self.pos1 = Vector2(pos1)
        self.pos2 = Vector2(pos2)

        if flippedNormal:
            temp = self.pos1
            self.pos1 = self.pos2
            self.pos2 = temp

    def lineCollision(self, 
                     ray) -> tuple[bool, float, float] | tuple[bool]:
        """
        returns the collision bool, t, and s
        """
        x1 = gb.halfRound(self.pos1.x, 1)
        y1 = gb.halfRound(self.pos1.y, 1)
        x2 = gb.halfRound(self.pos2.x, 1)
        y2 = gb.halfRound(self.pos2.y, 1)
        x3 = gb.halfRound(ray.pos1.x, 1)
        y3 = gb.halfRound(ray.pos1.y, 1)
        x4 = gb.halfRound(ray.pos2.x, 1)
        y4 = gb.halfRound(ray.pos2.y, 1)

        determinant = (x2 - x1) * (y4 - y3) - (y2 - y1) * (x4 - x3)

        if determinant == 0:
            return False,

        t = ((x3 - x1) * (y4 - y3) - (y3 - y1) * (x4 - x3))/determinant

        s = ((x3 - x1) * (y2 - y1) - (y3 - y1) * (x2 - x1))/determinant

        if (t >= 0  and t <= 1) and (s >= 0 and s <= 1):
            return True, t, s
        else:
            return False,
        
    def lineCollisionList(self,
                          rayList : list,
                          maxCollisions : int = 1) -> int:
        """
            rayList : List[Ray|tuple]

            Returns if a ray has collided with a list of other rays
            Returns true and stops checking after just a single ray has collided

            Make sure your list is properly formated!!!!
        """
        collisions = 0
        if maxCollisions == -1:
            maxCollisions = "inf"

        if len(rayList) > 0:
            if type(rayList[0]) == Ray:
                for ray in rayList:
                    if self.lineCollision(ray):
                        collisions += 1
                        if type(maxCollisions) == int|float:
                            if collisions >= maxCollisions:
                                return collisions

            if type(rayList[0]) == tuple or type(rayList[0]) == Vector2:
                for i in range(1, len(rayList)):
                    if self.lineCollision(Ray(rayList[i - 1], rayList[i])):
                        collisions += 1
                        if type(maxCollisions) == int|float:
                            if collisions >= maxCollisions:
                                return collisions
        
        return collisions
    
    def getRayLength(self) -> float:
        return self.pos1.distance_to(self.pos2)
    
    def lineCollisionPoint(self, ray, selfAligned : bool = True) -> tuple[Vector2, float]|None:
        """if collided, returns the position of collision and the distance for the collision"""
        collisionData = self.lineCollision(ray)
        if collisionData[0] == True:
            collided, t, s = collisionData
            if selfAligned:
                distance = self.getRayLength() - 1
                collisionDistance = distance * t
                angle = np.atan2(self.pos2.y - self.pos1.y, self.pos2.x - self.pos1.x)
                return self.pos1 + Vector2(np.cos(angle) * collisionDistance, np.sin(angle) * collisionDistance), collisionDistance
            else:
                distance = ray.getRayLength() - 1
                collisionDistance = distance * s
                angle = np.atan2(ray.pos2.y - ray.pos1.y, self.pos2.x - self.pos1.x)
                return ray.pos1 + Vector2(np.cos(angle) * collisionDistance, np.sin(angle) * collisionDistance), collisionDistance
        
    def getAngle(self) -> float:
        return np.degrees(np.atan2(self.pos2.y - self.pos1.y, self.pos2.x - self.pos1.x))

    def getNormal(self) -> float:
        return self.getAngle() + 90
    
    def getMidPoint(self) -> Vector2:
        return self.pos1 + (self.pos2 - self.pos1) * .5

    def draw(self, screen : pygame.display, color : tuple = (255, 255, 255), size : int = 1, points : bool = False) -> None:
        pygame.draw.line(screen, color, self.pos1, self.pos2, size)

        if points:
            pygame.draw.circle(screen, (255, 255, 255), self.pos1, size)
            pygame.draw.circle(screen, (255, 255, 255), self.pos2, size)

if __name__ == "__main__":
    collisionTimes = []
    creationTimes = []
    testSize = 1000000
    """
    10k tests
    Creation time mean : 0.0017 ms
    Creation time avg : 0.00185531 ms

    Collision time mean : 0.0037 ms
    Collision time avg : 0.00393104 ms

    1M tests
    Creation time mean : 0.0015 ms
    Creation time avg : 0.0016205068000000001 ms

    Collision time mean : 0.003 ms
    Collision time avg : 0.0033541012999999996 ms
    """
    for i in range(testSize):
        def createRay(pos1 : Vector2, pos2 : Vector2):
            createStart = time.perf_counter_ns()
            ray = Ray(pos1, pos2)
            createEnd = time.perf_counter_ns()
            creationTimes.append(createEnd - createStart)
            return ray
        
        ray1 = createRay(Vector2(random.randint(0, 1000), random.randint(0, 1000)), Vector2(random.randint(0, 1000), random.randint(0, 1000)))
        ray2 = createRay(Vector2(random.randint(0, 1000), random.randint(0, 1000)), Vector2(random.randint(0, 1000), random.randint(0, 1000)))

        collisionStart = time.perf_counter_ns()
        ray1.lineCollision(ray2)
        collisionEnd = time.perf_counter_ns()
        collisionTimes.append(collisionEnd - collisionStart)

        print(f"Test progress : {(i/testSize) * 100}")

    def toMs(value : int):
        return value / 1000000

    os.system("cls")
    print("Test done!\n")
    creationTimes.sort()
    print(f"Creation time mean : {toMs(creationTimes[len(creationTimes)//2])} ms")
    sum = 0
    for i in range(len(creationTimes)):
        sum += creationTimes[i]
    avg = sum/len(creationTimes)
    print(f"Creation time avg : {toMs(avg)} ms\n")

    collisionTimes.sort()
    print(f"Collision time mean : {toMs(collisionTimes[len(collisionTimes)//2])} ms")
    sum = 0
    for i in range(len(collisionTimes)):
        sum += collisionTimes[i]
    avg = sum/len(collisionTimes)
    print(f"Collision time avg : {toMs(avg)} ms")