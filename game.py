import pygame
import time
import random

from pygame.locals import*
from time import sleep

class Sprite():
	def __init__(self, x, y, w, h):
		self.x = x
		self.y = y
		self.w = w
		self.h = h

	def checkCollision(self, s):
		if (self.x + self.w <= s.x):
			return False
		if (self.x >= s.x + s.w):
			return False
		if (self.y + self.h <= s.y):
			return False
		if (self.y >= s.y + s.h):
			return False
		else:
			return True

	def isMario(self):
		return False

	def isBrick(self):
		return False
		
	def isCoin(self):
		return False

class Mario(Sprite):
	def __init__(self, x, y, w, h):
		super().__init__(x, y, w, h)
		self.marioScreenLocation = 150
		self.image1 = pygame.image.load("mario1.png")
		self.image2 = pygame.image.load("mario2.png")
		self.image3 = pygame.image.load("mario3.png")
		self.image4 = pygame.image.load("mario4.png")
		self.image5 = pygame.image.load("mario5.png")
		self.marioImages = [self.image1, self.image2, self.image3, self.image4, self.image5]
		self.marioImageNumber = 0
		self.image = self.marioImages[self.marioImageNumber]
		self.vertVel = 0.0
		self.previousX = 0
		self.previousY = 0
		self.isColliding = False
		self.head = False
		self.foot = False
		self.right = False
		self.left = False
		self.numberOfFrames = 0
		self.numberOfCoinFrames = 0

	def update(self):
		if (not self.isColliding):
			self.vertVel += 1.2
			self.y += self.vertVel
		if (self.y >= 550 - self.h):
			self.foot = True
			self.isColliding = True
			self.vertVel = 0.0
			self.y = 550 - self.h
		if (self.isColliding and self.foot == True):
			self.numberOfFrames = 0
		else:
			self.numberOfFrames += 1
		if (self.isColliding and self.head == True):
			self.numberOfCoinFrames = 0
		else:
			self.numberOfCoinFrames += 1
		self.isColliding = False
		self.head = False
		self.foot = False
		self.right = False
		self.left = False

	def fixCollison(self, b):
		self.isColliding = True
		if(b.isBrick()):
			if (((self.x + self.w) >= b.x) and ((self.previousX + self.w) <= b.x)):
				self.right = True
				self.x = b.x - self.w
			if ((self.x <= (b.x + b.w)) and (self.previousX >= (b.x + b.w))):
				self.left = True
				self.x = b.x + b.w
			if (((self.y + self.h) >= b.y) and ((self.previousY + self.h) <= b.y)):
				self.foot = True
				self.vertVel = 0.0
				self.y = b.y - self.h
			if ((self.y <= (b.y + b.h)) and (self.previousY >= (b.y + b.h))):
				self.head = True
				self.vertVel = 0.0
				self.y = b.y + b.h
				if (self.numberOfCoinFrames > 5):
					b.throwCoin()

	def cycleImages(self):
		if (self.marioImageNumber == 4):
			self.marioImageNumber = 0
		elif (self.marioImageNumber < 4):
			self.marioImageNumber += 1
		self.image = self.marioImages[self.marioImageNumber]

	def jump(self):
		if (self.isColliding and self.numberOfFrames == 0):
			self.vertVel -= 10.1
		elif (self.numberOfFrames < 10):
			self.vertVel -= 3.1

	def isMario(self):
		return True

class Brick(Sprite):
	def __init__(self, x, y, w, h, isCoinBrick, model):
		if (isCoinBrick):
			self.image = pygame.image.load("coinBrick.png")
		else:
			self.image = pygame.image.load("brick.png")
		super().__init__(x, y, w, h)
		self.isCoinBrick = isCoinBrick
		self.model = model
		self.numberOfCoins = 5

	def throwCoin(self):
		if (self.isCoinBrick):
			coin = Coin(self.x + (self.w / 2) - 25, self.y - 50, 50, 50, self.model)
			self.model.sprites.append(coin)
			self.numberOfCoins -= 1
		if (self.numberOfCoins <= 0):
			self.isCoinBrick = False
			self.image = pygame.image.load("brick.png")


	def update(self):
		pass

	def isBrick(self):
		return True

class Coin(Sprite):
	def __init__(self, x, y, w, h, model):
		super().__init__(x, y, w, h)
		self.model = model
		self.image = pygame.image.load("coin.png")
		self.randNum = random.randrange(-8, 8)
		self.horizVel = self.randNum
		self.vertVel = -10

	def update(self):
		self.x += self.horizVel
		self.vertVel += 1.2
		self.y += self.vertVel
		if (self.y > 500):
			self.model.sprites.remove(self)

	def isCoin(self):
		return True


class Model():
	def __init__(self):
		self.sprites = []
		self.mario = Mario(100, 380, 60, 95)
		self.brick0 = Brick(-200, 300, 200, 200, False, self)
		self.brick1 = Brick(-200, 500, 200, 200, False, self)
		self.brick2 = Brick(0, 500, 200, 200, False, self)
		self.brick3 = Brick(200, 500, 200, 200, False, self)
		self.brick4 = Brick(400, 500, 200, 200, False, self)
		self.brick5 = Brick(600, 500, 200, 200, False, self)
		self.brick6 = Brick(600, 300, 200, 200, False, self)
		self.brick7 = Brick(200, 100, 200, 200, True, self)
		self.brick8 = Brick(0, 100, 200, 200, False, self)
		self.sprites.append(self.mario)
		self.sprites.append(self.brick0)
		self.sprites.append(self.brick1)
		self.sprites.append(self.brick2)
		self.sprites.append(self.brick3)
		self.sprites.append(self.brick4)
		self.sprites.append(self.brick5)
		self.sprites.append(self.brick6)
		self.sprites.append(self.brick7)
		self.sprites.append(self.brick8)
		self.m = None
		self.backgroundPos = -200

	def update(self):
		for s in self.sprites:
			s.update()
		self.checkCollision1()

	def checkCollision1(self):
		for s in self.sprites:
			if (s.isMario()):
				self.m = s
			if ((not s.isMario()) and self.m != None):
				if (self.m.checkCollision(s)):
					self.m.fixCollison(s)


class View():
	def __init__(self, model):
		screen_size = (800,600)
		self.screen = pygame.display.set_mode(screen_size, 32)
		self.model = model

	def update(self):
		self.screen.fill([0,200,100])
		self.backgroundImage = pygame.image.load("background.png")
		self.screen.blit(self.backgroundImage, (self.model.backgroundPos, 0))
		for s in self.model.sprites:
			self.model.rect = s.image.get_rect()
			self.screen.blit(s.image, (s.x - self.model.mario.x + self.model.mario.marioScreenLocation, s.y))
		pygame.display.flip()

class Controller():
	def __init__(self, model):
		self.model = model
		self.keep_going = True

	def update(self):
		self.model.mario.previousX = self.model.mario.x
		self.model.mario.previousY = self.model.mario.y
		for event in pygame.event.get():
			if event.type == QUIT:
				self.keep_going = False
			elif event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					self.keep_going = False
			elif event.type == pygame.MOUSEBUTTONUP:
				self.model.set_dest(pygame.mouse.get_pos())
		keys = pygame.key.get_pressed()
		if keys[K_LEFT]:
			self.model.mario.x -= 10
			self.model.backgroundPos +=1
			self.model.mario.cycleImages()
		if keys[K_RIGHT]:
			self.model.mario.x += 10
			self.model.backgroundPos -=1
			self.model.mario.cycleImages()
		if keys[K_SPACE]:
			self.model.mario.jump()

print("Use the arrow keys to move. Press Esc to quit.")
pygame.init()
m = Model()
v = View(m)
c = Controller(m)
while c.keep_going:
	c.update()
	m.update()
	v.update()
	sleep(0.04)
print("Goodbye")