import pygame, math
import globals as gb
from pygame import Vector2
from ray import Ray

def pointOnScreen(pos, camera : Vector2 = (0, 0), size : float = 1):
		ssPoint = pos + camera #screen space point. Converts pos from ws to ss.
		size = abs(size) #only ever should be a positive value.
		if ssPoint.x + size > 0 and ssPoint.x - size < gb.SX and ssPoint.y + size > 0 and ssPoint.y - size < gb.SY:
			return True
		else:
			return False

class Point:
	def __init__(self, pos : Vector2 = Vector2(0, 0), color : tuple = (255, 255, 255)):
		self.pos = Vector2(pos)
		self.staticPos = pos
		self.color = color
		self.size = 2
		self.active = True
		self.grabbed = False
		self.highlighted = False
	
	#staticPos is the position of the point when it was last grabbed.
	#grabbed points is a list of all points that are held. This is to prevent holding more than one point when adjusting all points.
	def update(self, screen : pygame.surface, grabbedPoints : list, camera : Vector2 = (0, 0)): #draw : bool = True):
		keys = pygame.key.get_pressed()
		maxGrabbed = 1 if not keys[pygame.K_LSHIFT] else 2

		mousePos = Vector2(pygame.mouse.get_pos())
		if math.dist(mousePos, self.pos + camera) <= 5 and len(grabbedPoints) < maxGrabbed: #if the mouse is in range to grab this point and isn't already grabbing a point.
			self.highlighted = True
			if pygame.mouse.get_pressed(3)[0] and not self.grabbed: #if the point is clicked on.
				self.grabbed = True
				grabbedPoints.append(self) #adds itself to the list of all grabbed points.
		elif not self.grabbed: #only will set self.highlighted to False if the point isn't grabbed AND the mouse isn't in range of the point.
			self.highlighted = False

		#if the mouse was close enough to activate the highlighted bool, then the point will be slightly larger.
		#having the code seperate allows for the particle to appear highlighted even though it's not technically in distance because the mouse moves too fast.
		if self.highlighted: 
			self.size = 5 #size when held
		else:
			# self.size = math.dist(mousePos, self.pos + camera)
			self.size = 2 #default size if it's not grabbed.

		if self.active:
			if self.grabbed:
				self.pos = mousePos - camera
				if not pygame.mouse.get_pressed(3)[0]: #when lmb is released. (only calls once)
					self.grabbed = False
					self.highlighted = False
					self.pos = mousePos - camera #position is updated
					self.staticPos = self.pos #updates staticPos
					if self in grabbedPoints:
						grabbedPoints.remove(self) #removed from list of held points.
				if self.pos.x > gb.SX:
					self.pos.x = gb.SX
				pygame.draw.circle(screen, self.color, self.pos + camera, self.size) #draws to self.pos, which == mousePos
			elif pointOnScreen(self.pos, camera, self.size): #culls points when off screen
				#if the point isn't being held by the mouse, then it's position is set to it's position in the world space.
				pygame.draw.circle(screen, self.color, self.pos + camera, self.size)
	
	def updateStaticPos(self):
		self.staticPos = self.pos

	def setPos(self, pos):
		self.pos = pos
		self.updateStaticPos()

class drawnShape:
	def __init__(self, pos : Vector2 = Vector2(gb.SX/2, gb.SY/2), iterations : int = 10, drawColor : tuple = (150, 150, 150), drawMode : str = "points", p1Pos : Vector2 = None, p2Pos : Vector2 = None):
		self.pos = pos
		self.iterations = iterations
		self.drawColor = drawColor
		self.wheel = 0
		self.drawMode = drawMode

		self.cooldown = 0
		self.cPoint = Point(self.pos, (0, 255, 0))
		self.p1 = Point(self.pos + Vector2(0, 100), (0, 0, 255))
		self.p2 = Point(self.pos + Vector2(100, 0), (255, 0, 0))

		if p1Pos != None:
			self.p1.setPos(p1Pos)
		if p2Pos != None:
			self.p2.setPos(p2Pos)

		self.updateCPointPos()

	def update(self, screen, delta, camera, grabbedPoints, wheel, drawMode):
		if self.cooldown > 0:
			self.cooldown -= delta
		else:
			self.cooldown = 0

		self.wheel = wheel
		self.drawMode = drawMode

		# keys = pygame.key.get_pressed()
		# #flips the shape on the x and y axis
		# if keys[pygame.K_f] and self.cooldown == 0 and (self.p1.highlighted or self.p2.highlighted or self.cPoint.highlighted):
		# 	self.cooldown = CD
		# 	tempPos = self.p2.pos
		# 	self.p2.setPos(self.p1.pos)
		# 	self.p1.setPos(tempPos)
		# #flips the shape on the x axis
		# if keys[pygame.K_x] and self.cooldown == 0 and (self.p1.highlighted or self.p2.highlighted or self.cPoint.highlighted):
		# 	self.cooldown = CD
		# 	tempX = self.p1.pos.x
		# 	self.p1.setPos(Vector2(self.p2.pos.x, self.p1.pos.y))
		# 	self.p2.setPos(Vector2(tempX, self.p2.pos.y))
		# #flips the shape on the y axis
		# elif keys[pygame.K_y] and self.cooldown == 0 and (self.p1.highlighted or self.p2.highlighted or self.cPoint.highlighted):
		# 	self.cooldown = CD
		# 	tempY = self.p1.pos.y
		# 	self.p1.setPos(Vector2(self.p1.pos.x, self.p2.pos.y))
		# 	self.p2.setPos(Vector2(self.p2.pos.x, tempY))

		if self.cPoint.grabbed:
			#updates each of the points to it's relative position before cPoint was grabbed and adds the mouse (or, cPoint.pos)
			self.p1.pos = self.p1.staticPos + (self.cPoint.pos - self.cPoint.staticPos)
			self.p2.pos = self.p2.staticPos + (self.cPoint.pos - self.cPoint.staticPos)
			#When cPoint is released. This is only called once.
			if not pygame.mouse.get_pressed(3)[0]:
				#updates the static position of x and y Points.
				self.p1.updateStaticPos()
				self.p2.updateStaticPos()
		elif self.cPoint.grabbed == False or self.p1.grabbed or self.p2.grabbed:
			#updates the cPoint if p1 or p2 is grabbed.
			self.updateCPointPos()
		
		#when scrollwheel is used, the wheel function is called
		if (self.p1.highlighted or self.p2.highlighted or self.cPoint.highlighted):
			if self.wheel != 0:
				self.wheelFunction()

		#draws all points/lines in the shape based on the self.drawMode.
		#has to happen before the points update to avoid inconcistency issues.
		self.draw(screen, camera)

		#updates cPoint and draws to the screen.
		self.cPoint.update(screen, grabbedPoints, camera)

		#updates x and y points and draws them to the screen.
		self.p1.update(screen, grabbedPoints, camera)
		self.p2.update(screen, grabbedPoints, camera)

	#updates the cPoints to where the cPoint should be relative to p1 and p2. This function should set cPoint's pos to whatever your equation for it's pos is.
	def updateCPointPos(self):
		raise SyntaxError("Why tf are you supering this lmao")

	#handles what happens when self.wheel != 0. (or when the scrollwheel is used.)
	def wheelFunction(self):
		self.iterations += self.wheel
		if self.iterations < 1:
			self.iterations = 1

	#draws the shape based on the drawMode of the shape.
	def draw(self, screen, camera):
		#points uses self.getPoints to store a list of Vector2s for positions of all points along the shape that should be drawn.
		points = self.getPoints()
		#from there the points will be drawn depending on the draw mode.
		if self.drawMode == "points":
			for i in range(len(points)):
				if pointOnScreen(points[i], camera, 1): #culls points when off screen.
					pygame.draw.circle(screen, self.drawColor, points[i] + camera, 1)
		elif self.drawMode == "lines":
			for i in range(len(points) - 1):
				if pointOnScreen(points[i], camera, 1) or pointOnScreen(points[i + 1], camera, 1):
					pygame.draw.line(screen, self.drawColor, points[i] + camera, points[i + 1] + camera, 1)
		else:
			raise TypeError(f"{self.drawMode} is not a valid drawMode.")
	
	#returns a list of Vector2s for all positions of each point in the shape. (based on the #iterations.)
	def getPoints(self):
		raise SyntaxError("Why tf are you supering this lmao")

	def saveData(self):
		points = self.getPoints()
		saveString = f"{type(self)}; {self.p1.pos}; {self.p2.pos}; {self.iterations}\n"
		for point in range(len(points)):
			saveString += f"({points[point].x}, {points[point].y})"
			if point < len(points) - 1:
				saveString += "; "
			elif point == len(points) - 1:
				saveString += "\n"
		return saveString
	
	def getColliders(self, offset : Vector2|tuple = (0, 0)) -> list[Ray]:
		offset = Vector2(offset)
		points = self.getPoints()
		return [Ray(points[i] + offset, points[i+1] + offset) for i in range(len(points)-1)]
	
class Line(drawnShape):
	def __init__(self, pos : Vector2 = Vector2(gb.SX//2, gb.SY//2), iterations : int = 1, drawColor : tuple = (150, 150, 150), drawMode : str = "points", p1Pos : Vector2 = None, p2Pos : Vector2 = None):
		super().__init__(pos, iterations, drawColor, drawMode, p1Pos, p2Pos)
		self.active = True

	def updateCPointPos(self):
		#half the distance from p2.
		self.cPoint.setPos(self.p2.pos + Vector2((self.p1.pos.x - self.p2.pos.x) * .5, (self.p1.pos.y - self.p2.pos.y) * .5))

	def getPoints(self):
		#len of p1 compared to p2
		len = self.p1.pos - self.p2.pos
		
		returnPoints = []
		#defines (#self.iterations) points along the line
		for i in range(self.iterations + 1):
			percent = i / self.iterations
			#points are a percent of len away from p2.
			pos = self.p2.pos + Vector2(len.x * percent, len.y * percent)

			returnPoints.append(pos)
		return returnPoints
	
	def update(self, screen, delta, camera, grabbedPoints, wheel, drawMode):
		if self.active:
			return super().update(screen, delta, camera, grabbedPoints, wheel, drawMode)

class BezierCurve(drawnShape):
	def __init__(self, pos : Vector2 = Vector2(gb.SX//2, gb.SY//2), iterations : int = 28, drawColor : tuple = (150, 150, 150), drawMode: str = "points", p1Pos : Vector2 = None, p2Pos : Vector2 = None, p3Pos : Vector2 = None):
		super().__init__(pos, iterations, drawColor, drawMode, p1Pos, p2Pos)
		self.p3 = Point(self.pos + Vector2(60, 60), (100, 255, 255))
		if p3Pos != None:
			self.p3.setPos(p3Pos)

		self.active = True

	def updateCPointPos(self):
		self.cPoint.setPos(self.p2.pos + (self.p1.pos - self.p2.pos) * .5)

	def getPoints(self):
		returnPoints = []
		
		line1List = []
		line1Dist = self.p1.pos - self.p3.pos
		line2List = []
		line2Dist = self.p2.pos - self.p3.pos

		for i in range(self.iterations):
			percent = (1/self.iterations) * i
			line1List.append(self.p1.pos - line1Dist * percent)
			line2List.append(self.p2.pos - line2Dist * percent)

		linesList = []
		for i in range(self.iterations):
			linesList.append([line1List[i], line2List[len(line2List) - i - 1]])

		for i in range(len(linesList) - 1):
			dist = linesList[i][1] - linesList[i][0]
			percent = (1/(len(linesList) - 1)) * i
			returnPoints.append(linesList[i][0] + dist * percent)
		
		returnPoints.append(linesList[len(linesList)-1][1])

		# for i in range(self.iterations):
		# 	returnPoints.append(line1List[i])
		# 	returnPoints.append(line2List[len(line2List) - i - 1])

		return returnPoints



		# #len of p1 compared to p2
		# len = self.p1.pos - self.p2.pos
		
		# returnPoints = []
		# #defines (#self.iterations) points along the line
		# for i in range(self.iterations + 1):
		# 	percent = i / self.iterations
		# 	#points are a percent of len away from p2.
		# 	pos = self.p2.pos + Vector2(len.x * percent, len.y * percent)

		# 	returnPoints.append(pos)
		# return returnPoints
	
	def saveData(self):
		points = self.getPoints()
		saveString = f"{type(self)}; {self.p1.pos}; {self.p2.pos}; {self.p3.pos}; {self.iterations}\n"
		for point in range(len(points)):
			saveString += f"({points[point].x}, {points[point].y})"
			if point < len(points) - 1:
				saveString += "; "
			elif point == len(points) - 1:
				saveString += "\n"
		return saveString

	def update(self, screen, delta, camera, grabbedPoints, wheel, drawMode):
		if self.active:
			if self.cooldown > 0:
				self.cooldown -= delta
			else:
				self.cooldown = 0

			self.wheel = wheel
			self.drawMode = drawMode

			if self.cPoint.grabbed:
				#updates each of the points to it's relative position before cPoint was grabbed and adds the mouse (or, cPoint.pos)
				self.p1.pos = self.p1.staticPos + (self.cPoint.pos - self.cPoint.staticPos)
				self.p2.pos = self.p2.staticPos + (self.cPoint.pos - self.cPoint.staticPos)
				self.p3.pos = self.p3.staticPos + (self.cPoint.pos - self.cPoint.staticPos)
				#When cPoint is released. This is only called once.
				if not pygame.mouse.get_pressed(3)[0]:
					#updates the static position of x and y Points.
					self.p1.updateStaticPos()
					self.p2.updateStaticPos()
					self.p3.updateStaticPos()
			elif self.cPoint.grabbed == False or self.p1.grabbed or self.p2.grabbed or self.p3.grabbed:
				#updates the cPoint if p1 or p2 is grabbed.
				self.updateCPointPos()
			
			#when scrollwheel is used, the wheel function is called
			if (self.p1.highlighted or self.p2.highlighted or self.p3.highlighted or self.cPoint.highlighted):
				if self.wheel != 0:
					self.wheelFunction()

			#draws all points/lines in the shape based on the self.drawMode.
			#has to happen before the points update to avoid inconcistency issues.
			self.draw(screen, camera)

			#updates cPoint and draws to the screen.
			self.cPoint.update(screen, grabbedPoints, camera)

			#updates x and y points and draws them to the screen.
			self.p1.update(screen, grabbedPoints, camera)
			self.p2.update(screen, grabbedPoints, camera)
			self.p3.update(screen, grabbedPoints, camera)