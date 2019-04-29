import pygame
import time
import os
import sys
import math
# (D,C,H,S) + (A,2,3,4,5,6,7,8,9,0,J,Q,K)   

class Setting:
	def __init__(self):
		self.SCREEN_WIDTH = 1200#1000
		self.SCREEN_HEIGHT = 650#650

		self.background_image = 'background1.jpg'
		self.puke_backface_image = 'puke/back.jpg'
		self.master_image = 'master.jpg'

		self.scale_puke = 0.8
		self.scale_puke_back = 0.2

		self.cards_gap = 500/12

	def load_puke_backface_image(self):
		image = pygame.image.load(self.puke_backface_image)
		rect = image.get_rect()
		width, height = rect.width*self.scale_puke_back, rect.height*self.scale_puke_back
		image = pygame.transform.scale(image, (int(width), int(height)))
		image = pygame.transform.rotate(image, 90)
		return image

	def load_face_image(self, face, role):
		if role=='East' or role=='West':
			angle = 90
			face_image = 'puke/back.jpg'
		else:
			angle = 0
			face_image = 'puke/' + face + '.jpg'

		image = pygame.image.load(face_image)

		width = 84
		height = 120
		image = pygame.transform.scale(image, (width, height))
		# counterclockwise rotation
		
		image = pygame.transform.rotate(image, angle)
		return image

class Button:
	def __init__(self, screen, image, position, color):
		self.image = image
		self.position = position
		self.color = color
		self.screen = screen

	def isPressed(self, px, py):
		x,y = self.position
		w,h = self.image.get_size()
		in_x = x - w/2 < px < x + w/2
		in_y = y - h/2 < py < y + h/2
		return in_x and in_y
	
	def blitme(self):
		w,h = self.image.get_size()
		x,y = self.position
		self.screen.blit(self.image, (x-w/2,y-h/2))


class Background:
	"""docstring for Background"""
	def __init__(self, screen, setting):
		super(Background, self).__init__()
		self.screen = screen

		background_image = setting.background_image
		self.image = pygame.image.load(background_image)
		self.image = pygame.transform.scale(self.image,(setting.SCREEN_WIDTH, setting.SCREEN_HEIGHT))
		self.rect = self.image.get_rect()
		self.rect.width = setting.SCREEN_WIDTH
		self.rect.height = setting.SCREEN_HEIGHT
		self.roles = ['East', 'North', 'West', 'South']
		self.players = {}
		for role in self.roles:
			player = Player(screen, setting, role)
			self.players[role] = player

		self.buttons = []
		self.clock = pygame.time.Clock()

	def initial(self):
		for role in self.roles:
			self.players[role].initial()

		self.buttons = []

	# add a card in a player
	def add_card(self, card, turn):
		#pygame.time.wait(80)
		role = self.roles[turn]
		self.players[role].add_card(card)

		self.blitme()
		pygame.display.update()

	def push_cards(self, cards, turn):
		pygame.time.wait(50)
		role = self.roles[turn]
		for card in cards:
			self.players[role].push_cards(card)

		self.blitme()
		pygame.display.update()


	def add_cards_over(self, inputs, outputs):
		for player in self.players.values():
			player.sort_cards()

		self.blitme()
		pygame.display.update()

	def turn_over(self):
		pygame.time.wait(100)
		for player in self.players.values():
			player.del_out_cards()
		self.blitme()
		pygame.display.update()


	def text_image(self, text, color, size):
		font = pygame.font.Font('freesansbold.ttf', size)
		textSurface = font.render(text, True, color)
		return textSurface

	def draw_fps(self):
		fps = self.clock.get_fps()
		text = 'FPS: ' + str(int(fps))
		textSurface = self.text_image(text, (255,255,255), 20)
		textRect = textSurface.get_rect()
		textRect.right = 0
		textRect.left = 0

		self.screen.blit(textSurface, textRect)

	def draw_upimage(self,image):
		image = pygame.transform.scale(image,(300,240))
		imageRect = image.get_rect()
		imageRect.top = 0
		imageRect.right = 1265
		self.screen.blit(image,imageRect)
	
	def draw_downimage(self,image):
		image = pygame.transform.scale(image,(300,400))
		imageRect = image.get_rect()
		imageRect.top = 250
		imageRect.right = 1265
		self.screen.blit(image,imageRect)

	def draw_button(self, row, col, color):
		name = 'icon/' + color + '.jpg'			
		image = pygame.image.load(name)
		if color == 'PASS':
			image = pygame.transform.scale(image,(120,30))
			centerx = 1100
			centery = 630
			button = Button(self.screen, image, (centerx, centery), color)
		else:
			width = 30
			height = 40
			image = pygame.transform.scale(image,(width,height))
			centerx =  1000 + col  * 35 + height / 2
			centery =  	260 + row  * 52 + width / 2
			button = Button(self.screen, image, (centerx,centery), color)
		button.blitme()
		if len(self.buttons) < 36:
			self.buttons.append(button)

	def draw_pass(self, turn, width):
		name = 'icon/PASS1.jpg'
		image = pygame.image.load(name)
		image = pygame.transform.scale(image, (40,20))

		top = 40 + turn * 25
		left = 970 + width * 60
		self.screen.blit(image,(left, top))
		pygame.display.update()

	def draw_contract(self, turn, width, color, index):
		name = 'icon/' + color + '.jpg'
		image = pygame.image.load(name)
		image = pygame.transform.scale(image, (20,20))
		text = str(math.floor(index / 5 + 1))
		textSurface = self.text_image(text,(0,0,0), 15)
		top = 40 + turn * 25
		left = 970 + width * 60
		self.screen.blit(textSurface,(left, top))
		self.screen.blit(image,(left+10,top))
		pygame.display.update()

	def update_contract(self, index):
		for i in range(index):
			if self.buttons[i].position[0] != 10000:
				w,h = self.buttons[i].image.get_size()
				image = pygame.image.load('icon/white.jpg')
				image = pygame.transform.scale(image,(w,h))
				left, top = self.buttons[i].position
				left = left - w / 2
				top = top - h / 2 
				self.screen.blit(image,(left,top))
				pygame.display.update()
				self.buttons[i].position = (10000,0)

	def blitme(self):
		self.clock.tick(30)
		self.screen.blit(self.image, self.rect)
		# draw fps
		self.draw_fps()		
		# draw upimage
		upimage = pygame.image.load('icon/up.jpg')
		downimage = pygame.image.load('icon/down.jpg')
		self.draw_upimage(upimage)
		self.draw_downimage(downimage)
		# draw each player
		for player in self.players.values():
			player.blitme()
		
		color_dict = { 0: 'C' , 1:'D', 2:'H', 3: 'S', 4:'NT'}
		for row in range(7):
			for col in range(5):
				self.draw_button(row,col, color_dict[col])
		self.draw_button(-1,-1, 'PASS')

class Puke:
	"""dscreen, settingtring for Puke"""
	def __init__(self, screen, setting, face, role):
		self.screen = screen
		self.face = face

		self.image = setting.load_face_image(face, role)
		self.rect = self.image.get_rect()

	def blitme(self, centerx, centery):
		self.rect.centerx = int(centerx)
		self.rect.centery = int(centery)
		self.screen.blit(self.image, self.rect)
		
class Player:
	"""dscreen, settingtring for Player"""
	def __init__(self, screen, setting, role):
		self.screen = screen
		self.setting = setting
		self.gap = setting.cards_gap
		width, height = setting.SCREEN_WIDTH, setting.SCREEN_HEIGHT
		if role == 'East':
			self.centerx = width - width / 10 - 200
			self.centery = height / 2
			self.out_centerx = 7 * width / 10 - 200
		elif role == 'South':
			self.centerx = width / 2 - 150
			self.centery = height - height / 10 
			self.out_centery = 7 * height /  10 
		elif role == 'West':
			self.centerx = width / 20 
			self.centery = height / 2
			self.out_centerx = 3 * width / 10
		else:
			self.centerx = width / 2  - 150
			self.centery = height / 10
			self.out_centery = 3 * height / 10

		self.role = role
		self.cards = []
		self.out_cards = []


	def initial(self):
		for card in self.cards:
			del card
		for card in self.out_cards:
			del card
		self.cards = []
		self.out_cards = []
		self.master = False

	def add_card(self, face):
		new_card = Puke(self.screen, self.setting, face, self.role)
		self.cards.append(new_card)

	

	def sort_cards(self):
		colors = ('H', 'S', 'D', 'C')
		nums = ('A', 'K', 'Q', 'J', '0', '9','8','7','6','5','4','3','2')
		power = {nums[index]: index for index in range(13)}
		cards = []
		color_cards = {color: [] for color in colors}
		for card in self.cards:
			face = card.face
			color, num = face[0], face[1]
			color_cards[color].append((power[num], card))
 
		for L in color_cards.values():
			L.sort(key=lambda e: e[0])
		self.cards = cards

	def push_cards(self, face):
		for card in self.cards.copy():
			if card.face == face:
				self.out_cards.append(card)
				self.cards.remove(card)
				return

	def add_left_cards(self, inputs, outputs):
		for face in inputs:
			self.add_card(face)

		for face in outputs:
			self.push_cards(face)

		self.del_out_cards()

	def del_out_cards(self):
		for card in self.out_cards:
			del card
		self.out_cards = []		

	def blitme(self):
		#draw master
		# draw cards in hand of each player
		n = len(self.cards)
		if self.role == 'West':
			y1 = (2*self.centery - (n-1)*self.gap)/2
			for a in range(n):
				self.cards[a].blitme(self.centerx, y1)
				y1 += self.gap
		elif self.role == 'East':
			yn = (2*self.centery + (n-1)*self.gap)/2
			for a in range(n):
				self.cards[a].blitme(self.centerx, yn)
				yn -= self.gap
		elif self.role == 'South':
			x1 = (2*self.centerx - (n-1)*self.gap)/2
			for a in range(n):
				self.cards[a].blitme(x1, self.centery)
				x1 += self.gap
		else:
			xn = (2*self.centerx + (n-1)*self.gap)/2
			for a in range(n):
				self.cards[a].blitme(xn, self.centery)
				xn -= self.gap

		# draw the cards pushing out
		m = len(self.out_cards)
		if m == 0:
			return
		if self.role == 'West':
			y = (2*self.centery - (m-1)*self.gap)/2
			for a in range(m):
				self.out_cards[a].blitme(self.out_centerx, y)
				y += self.gap
		elif self.role == 'East':
			y = (2*self.centery + (m-1)*self.gap)/2
			for a in range(m):
				self.out_cards[a].blitme(self.out_centerx, y)
				y -= self.gap
		elif self.role == 'South':
			x = (2*self.centerx - (m-1)*self.gap)/2
			for a in range(m):
				self.out_cards[a].blitme(x, self.out_centery)
				x += self.gap
		else:
			x = (2*self.centerx + (m-1)*self.gap)/2
			for a in range(m):
				self.out_cards[a].blitme(x, self.out_centery)
				x -= self.gap

def check_events(flag = 0, background = None, role = -1, turn = -1):
	"""Respond to keypresses and mouse events."""
	while(True):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			elif event.type == pygame.KEYDOWN and event.key == pygame.K_q:
				sys.exit()
			elif not flag:
				return
			elif event.type == pygame.MOUSEBUTTONDOWN:
				mouse_x, mouse_y = pygame.mouse.get_pos()
				for i, button in enumerate(background.buttons):
					if button.isPressed(mouse_x, mouse_y):
						if i == (len(background.buttons) - 1): # if pressed PASS
							background.draw_pass(turn, role)
						else:
							background.draw_contract(turn, role, button.color, i)
							background.update_contract(i+1)
						return 

	
