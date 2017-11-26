#    15-112: Principles of Programming and Computer Science
#    Project: Zombie Game
#    Name      : Muhammad Ahmad Khan
#    AndrewID  : mkhan2
#    File Created: 10/11/2017
#    Modification History:
#    Start             End
#    10/11 17:20      11/11 01:20
#    11/11 14:00      12/11 02:00
#    12/11 22:30      13/11 01:00
#    13/11 18:00      13/11 19:00
#    15/11 17:00      15/11 18:30
#    17/11 14:30      17/11 17:30
#    17/11 21:30      18/11 00:20
#    19/11 16:00      20/11 00:20
#    21/11 21:00      22/11 01:10
#	 22/11 22:00      23/11 01:10
#	 24/11 00:00      24/11 05:30
#	 24/11 13:00      24/11 06:30
#	 25/11 00:00      25/11 02:20
#	 25/11 14:30	  25/11 16:20
#	 25/11 22:30	  26/11 00:30

#This program is a zombie shooting game that follows a round based system,
#with each round increasing zombie number, health, and speed.
#Player can upgrade his own attributes to keep up with the zombies :)


#Special thanks to professor Saquib for being so amazing.

#best code viewing experience on sublime

################# Ensure you have pygame installed #################


################# Class (+ 1 Function) definitions ################################
# Input and output explained with function/class definition.
# the code is broken up into a number of classes, and 1 function
#Functions
#1. load_images : this is the only function not in a class. It is used to load 
# 				  individual photos from a folder.
#
#Classes
#1. Background : this class takes care of game background.
#2. Player : this class takes care of the player.
#				Functions: 1 . Move: takes care of player
#						   2 . change_orientation: changes the way the player faces 
#3. Zombie : this class is for the zombies. Has all relevant attributes. 
#4. Bullet : this class is for the bullets the player shoots. 
#       All of the above classes have a update class also, which takes care of 
#       updating relevant information of the object.
#5. healthbar : this is for the healthbar to represent player health
#6. Main: this is the actual game loop.
#		Functions: 1.updateText : this updates text that is displayed
#				   2.upgradeScreen : this takes care of the upgrade screen, which 
# 									 opens after each round
#				   3.killzombies : this kills all zombie objects that have 0 health
#				   4.round : this maintains rounds, including spawning zombies
#				   5.startMenu : this is the start menu
#				   6.pauseMenu : this is the pause menu
#				   7.gameOver : displays a game over screen when player dies
#				   8.spawn_zombie : function used by round() to spawn individual 
#									zombies
#				   9.shoot : takes care of shooting
#				   10.check_zombie_overlap : slightly displaces overlapping zombies
#											 for better visual experience
#				   11.check_collision : takes care of damagin zombie/player depending
#										on event
#				   12.redefine_all : redefines all necessary attributes for restart


#importing libraries
import pygame
#pygame used for overall ai
import os
#os used to access paths to load images/texts in certain relative locations
import random
#random used to generate random numbers for varied speeds and spawnpoint of zombies
import copy
#copy used to make exact copy of certain varaibles
# and background that need to be reset
import math
#math for mathematical functions
import time
#time for tracking time passed and for pause after certain functions

def load_images(foldername, subfolder = None, size=(45, 72)):
#   Loads all images in directory. The directory must only contain images.
#   Args:
#       foldername: the name of the folder to open
#		subfolder: name of subfolder(if there is one) to open
#		size: the size to convert each image to 
#   Returns: 
#       List of images

	# path adds current directory and /game_files/ to ther foldername to get
	# the path for the images
	# if there is a subfolder adds subfolder to path as well
	if subfolder:
		path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
										 'game_files', foldername, subfolder)
	else:
		path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
										 'game_files', foldername)
	#empty list to add images to
	images = []
	#looping throuhg all images in folder and loading to images
	#scales the pictures down: smoothscale instead of scale for better image
	for file_name in os.listdir(path): #this loads all files in path
		image = pygame.image.load(os.path.join(path, file_name))
		image = pygame.transform.smoothscale(image, size) #adjest size to 40x40
		images.append(image)

	return images

#create class for background
class Background(pygame.sprite.Sprite):
	def __init__(self):
		#call parent class constructor
		super(Background, self).__init__()

		#load background image
		self.image = pygame.image.load(os.path.join('game_files',
											 		'background2.jpg'))
		#get the size of background
		self.size = self.image.get_size()
		#create copy of image for update function
		self.imageCopy = copy.copy(self.image)

		#initiate positional limits for player/ bullet position
		self.up_limit = 597
		self.down_limit = 1688
		self.right_limit = 2938
		self.left_limit = 750

	def update(self):
		#this function resets background to original image
		self.image = copy.copy(self.imageCopy)
		

class Player(pygame.sprite.Sprite):
#   A class for the player character
#   Args:
#       position: where the character should be created
#       images: different sprite images
#		background: for access to background image boundaries
	def __init__(self, position, images, background):

		#call parent class constructor
		super(Player, self).__init__()

		#size of player
		self.size = (66, 96)

		#rect for inbuilt collision function of pygame
		self.rect = pygame.Rect(position, self.size)
		
		#initiating image attribute
		self.images = images
		#creating different orientation of images for different
		#shooting directions
		self.images_right = self.images
		# Flipping every image
		self.images_left = [pygame.transform.flip
							(image, True, False) for image in self.images]
		#initiate index for animation of player sprite
		self.index = 0
		#set initial image
		self.image = self.images[self.index]

		#variables for player movement
		self.vmovement = 0
		self.hmovement = 0
		self.up = 0
		self.down = 0
		self.left = 0
		self.right = 0

		#speed determines how fast player will move
		self.speed = 10.0
		#speed_copy exists to allow for fixing diagonal speed 
		#(explained in self.move)
		self.speed_copy = copy.copy(self.speed)

		#initiate background attribute to access boundary limits
		self.background = background
		#initiate player health attribute
		self.health = 1000
		#initiate player life status attribute to allow for 
		#functions to run on death
		self.dead = False					
		

	def move(self):
		#this will move the player
		#get all the movements
		#returns 1 if pressed
		self.up = pygame.key.get_pressed()[pygame.K_w]
		self.down = pygame.key.get_pressed()[pygame.K_s]
		self.left = pygame.key.get_pressed()[pygame.K_a]
		self.right = pygame.key.get_pressed()[pygame.K_d]
		#set boundary to player position
		#left boundary
		if self.rect[0] < self.background.left_limit:
			self.left = 0
		#up boundary
		if self.rect[1] < self.background.up_limit:
			self.up = 0
		#right boundary
		if self.rect[0] > self.background.right_limit:
			self.right = 0
		#down boundary
		if self.rect[1] > self.background.down_limit:
			self.down = 0
		#adjusts speed for diagonal speed
		#!= checks if either both are pressed or neither are pressed (XOR)
		if (self.up != self.down) and (self.left != self.right):
		    self.speed = self.speed / 2**0.5
		    # 2**0.5 is use because diagonal movement is basically 1 vertical
		    # and 1 horizontal, so diagonally thats 2**0.5 units per frame
		#adjusts v/hmovement to allow movement
		if self.up == 1:
			self.vmovement -= self.speed
		if self.down == 1:
			self.vmovement += self.speed
		if self.left == 1:
			self.hmovement -= self.speed
			#adjust index for player animation in left/right plane
			# %6 keeps index below 6			
			self.index = (self.index + self.speed/20) % 6
		if self.right == 1:
			self.hmovement += self.speed
			#adjust index for player animation in left/right plane
			# %6 keeps index below 6
			self.index = (self.index + self.speed/20) % 6
		#moves the position of the player
		self.rect.move_ip(self.hmovement,self.vmovement)
		#reset variables
		self.vmovement = 0
		self.hmovement = 0
		self.speed = self.speed_copy

	def update(self):
		#dying
		if self.health <= 0:
			self.dead = True
		#animation of player by changing through images
		self.image = self.images[int(math.floor(self.index))]

	def change_orientation(self, direction):
		#to change orientaion of player depending on shooting direction
		#changes the images to appropriate oriendtaion and reassigns image to
		# implement change
		if direction == 'left':
			self.images = self.images_left
			self.image = self.images[int(math.floor(self.index))]

		if direction == 'right':
			self.images = self.images_right
			self.image = self.images[int(math.floor(self.index))]



#create class for zombies
class zombies(pygame.sprite.Sprite):
#	    Args:
#       position: where the zombie should be created
#       images: different sprite images
#		player: to allow zombie to track player
#		size: size of zombie images
#		deltaspeed: to allow for varying speeds of zombie
#       delathealth: to vary health with round
	def __init__(self, position, images, player, size, deltaspeed, deltahealth):
		#call parent class constructor
		super(zombies, self).__init__()

		#creating images attribute
		self.images = images

		#size of zombie
		self.size = size

		#defining rect for collision detection
		self.rect = pygame.Rect(position, self.size)

		#different image orientation to allow for left/right orientation of zombies
		self.images_right = self.images
		# Flipping every image.
		self.images_left = [pygame.transform.flip
							(image, True, False) for image in self.images]
		#for animation
		self.index = 0
		self.image = self.images[self.index] #sets initial image
		
		#speed + variable speed
		self.speed = 2.0 + deltaspeed
		self.speed_copy = copy.copy(self.speed)
		
		#to allow zombie movement
		self.vmovement = 0
		self.hmovement = 0

		#for movement of zombie
		self.h = 0
		self.v = 0
		
		#instancing player
		self.player = player

		#setting zombie health
		self.health = deltahealth - 10

		#setting alive
		self.dead = False

	def update(self):
		#move/ kill zombie
		#changes orientation also

		#checks if zombie should die
		if self.health <= 0:
			self.dead = True

		#this sees if zombie should be moved, by checking difference 
		#in position with playerand seeing if its higher than speed

		#right
		if self.player.rect[0] - self.rect[0] > self.speed:
			self.h = 1
		#left
		elif self.player.rect[0] - self.rect[0] < -self.speed:
			self.h = -1
		#down
		if self.player.rect[1] - self.rect[1] > self.speed:
			self.v = 1
		#up
		elif self.player.rect[1] -  self.rect[1] < -self.speed:
			self.v = -1

		#fix diagonal speed
		if self.v != 0 and self.h != 0:
			self.speed = self.speed / 2**0.5

		#moves zombies
		if self.h == 1:
			self.hmovement += self.speed
			#change orientation
			self.images = self.images_right
		if self.h == -1:
			self.hmovement -= self.speed
			#change orientation
			self.images = self.images_left
		if self.v == 1:
			self.vmovement += self.speed
		if self.v == -1:
			self.vmovement -= self.speed

		#reset variabls
		self.speed = self.speed_copy
		self.h = 0
		self.v = 0


		#move zombie
		self.rect.move_ip(self.hmovement,self.vmovement)

		#reset variables
		self.vmovement = 0
		self.hmovement = 0

		#animation of zombie
		#increment zombie image index to switch between frames
		self.index = (self.index + self.speed/10) %6
		self.image = self.images[int(math.floor(self.index))]


class Bullets(pygame.sprite.Sprite):
	#creation of bullets
	#Args: rect: obtain position to create bullet
	#	   background: to access boundary limits
	#	   direction: for direction of bullet movement
	#	   image: picture of bullets
	#	   penetration: how many zombies 1 bullet hits
	def __init__(self, rect, background, direction, image, penetration):
		#call parent class constructor
		super(Bullets, self).__init__()

		#direction of bullet
		self.direction = direction
		#position of bullet (for collision function)
		self.rect = pygame.Rect((rect[0] + 2, rect[1] + 11) , (10, 10))

		#create background attribute to access boundary
		self.background = background
		
		#set image
		self.image = image
		#rotate image based on direction
		if self.direction == 'down':
			self.image = pygame.transform.rotate(self.image, 180)
		if self.direction == 'left':
			self.image = pygame.transform.rotate(self.image, 90)
		if self.direction == 'right':
			self.image = pygame.transform.rotate(self.image, 270)

		#penetration (same mechanism as health)
		self.health = penetration

	def update(self):
		#moves bullet, and kills bullet if they reach boundary
		#move by 40 units in relevant direction
		if self.direction == 'up':
			self.rect.move_ip(0, -40)
			if self.rect[1] < self.background.up_limit:
				self.kill()
		if self.direction == 'down':
			self.rect.move_ip(0, 40)
			if self.rect[1] > self.background.down_limit:
				self.kill()
		if self.direction == 'left':
			self.rect.move_ip(-40, 0)
			if self.rect[0] < self.background.left_limit:
				self.kill()
		if self.direction == 'right':
			self.rect.move_ip(40, 0)
			if self.rect[0] > self.background.right_limit:
				self.kill()

		#kill bullet once penetration limit reached
		if self.health == 0:
			self.kill()

class healthbar(pygame.sprite.Sprite):
	#creation of bullets
	def __init__(self):
		#call parent class constructor
		super(healthbar, self).__init__()

		#image of healthbar
		self.image = pygame.image.load(os.path.join('game_files',
												 'HealthBar.png'))
		#transfrom to usable size
		self.image = pygame.transform.smoothscale(self.image, (410,20))


		
		
		
class main():
	def __init__(self):
		pygame.init()
		#initialize necessary variables

		self.display_width = 1200
		self.display_height = 700
		#creating a background object
		self.background = Background()

		#sets the display and its size
		self.gameDisplay = pygame.display.set_mode((self.display_width,
										self.display_height))
		
		pygame.display.set_caption('Determined death') #changes window title

		#create timer,  used to set fps
		self.clock = pygame.time.Clock()
		self.fps = 50

		#highscore
		#open txt file and read first line which stores highscore
		file = open(os.path.join('game_files', 'highscore.txt'), 'r')
		self.highscore = file.readline()
		file.close()
		
		#for while loop
		self.done = False
		#for start menu
		self.notstarted = True
		#for pause menu
		self.pause = False

		#amount of coins for buying upgrades
		self.coins = 0
		#text to blit
		self.coins_text = pygame.font.SysFont('Consolas', 32).render(
			('Coins: ' + str(self.coins)), True, pygame.color.Color('gold'))

		#ammo for bullet shoot limit
		self.ammo = 2500
		#text to blit
		self.ammo_text = pygame.font.SysFont('Consolas', 24).render(
			('Ammo: ' + str(self.ammo)), True, pygame.color.Color('gray76'))

		#Start Menu Relevant Text
		#game title
		self.game_text = pygame.font.SysFont('Monospace', 64).render(
			'Determined Death', True, pygame.color.Color('White'))
		#start game tag
		self.start_text = pygame.font.SysFont('Monospace', 48).render(
			'Start Game', True, pygame.color.Color('White'))
		#Controls tag
		self.controls_text = pygame.font.SysFont('Monospace', 48).render(
			'Controls', True, pygame.color.Color('White'))
		#Exit tag
		self.exit_text = pygame.font.SysFont('Monospace', 48).render(
			'Exit', True, pygame.color.Color('White'))
		#(start menu) control menu picture
		self.contols_image = pygame.image.load(os.path.join('game_files',
														 'controls.png'))



		#Pause Menu Relevant Text
		#Paused text caption
		self.pause_text = pygame.font.SysFont('Consolas', 64).render(
			'PAUSED', True, pygame.color.Color('White'))
		#resume tag
		self.resume_text = pygame.font.SysFont('Consolas', 48).render(
			'Resume', True, pygame.color.Color('White'))
		#restart tag
		self.restart_text = pygame.font.SysFont('Consolas', 48).render(
			'Restart', True, pygame.color.Color('White'))
		#quit tag
		self.quit_text = pygame.font.SysFont('Consolas', 48).render(
			'Quit', True, pygame.color.Color('White'))

		#load necessary images
		#bullet image
		self.bulletimage = pygame.image.load(os.path.join('game_files',
														 'bulletred.png'))
		#resizing bullet image
		self.bulletimage = pygame.transform.scale(self.bulletimage, (40, 40))
		
		#player images, to be loaded at size 66x96
		self.playerImages = load_images("player", size=(66,96))
		
		#loading different types of zombies
		self.zombie_image_list = []
		for i in range(1,6):
			zombieImages = load_images('zombie', str(i))
			self.zombie_image_list.append(zombieImages)
		#resizing zombie type 4 (index 3) for aesthetic purposes
		for i in range(len(self.zombie_image_list[3])):
				self.zombie_image_list[3][i] = pygame.transform.smoothscale(
										self.zombie_image_list[3][i], (36,60))

		#create player and add to all_sprites group
		self.player = Player((self.background.size[0]/2,
				 self.background.size[1]/2), self.playerImages, self.background)

		self.all_sprites = pygame.sprite.Group(self.player)

		#create sprite groups for zombie and bullet for collision detection
		self.bullet_sprites = pygame.sprite.Group()
		self.zombie_sprites = pygame.sprite.Group()

		#create attribute for bullet damage and penetration
		self.bulletDamage = 1
		self.bulletPenetration = 1

		#create healthbar
		self.healthbar = healthbar()

		#variables to manage rounds
		#round no.
		self.round_RoundNo = 1
		#to create 'waves' within rounds
		self.round_continueSpawn = True
		self.round_noSpawned = 0 
		self.round_noKilled = 0
		self.round_counter = 0

		#for displaying how many zombies left for round end(initially 50)
		self.zombies_remaining = 20


		#all the text to display continuously in main game
		self.RoundNo_text =  pygame.font.SysFont('Consolas', 32).render(('Round  ' 
			+ str(self.round_RoundNo)), True, pygame.color.Color('darkorange1'))
		self.highscore_text = pygame.font.SysFont('Consolas', 16).render(
			('Highscore : ' + str(self.highscore)), True, pygame.color.Color('white'))
		self.remainingZombies_text =  pygame.font.SysFont('Consolas', 16).render(
			('Zombies Remaining:  ' + str(self.zombies_remaining)),
			 True, pygame.color.Color('White'))


		#Upgrade Screen Relevant text/variables
		#this is an image with the possible upgrades written
		self.upgradeScreen_picture = pygame.image.load(os.path.join('game_files',
															 'UpgradeScreen.png'))
		#upgrade texts say 'upgrade' followed by cost in parenthesis
		#for bullet damage
		self.upgrade_text1 = pygame.font.SysFont('Consolas', 30).render(
			'upgrade(' +str(self.bulletDamage * 100) + ')', True,
			 pygame.color.Color('orange'))
		#for bullet penetration
		self.upgrade_text2 = pygame.font.SysFont('Consolas', 30).render(
			'upgrade(' +str(self.bulletPenetration * 100) + ')', True,
			 pygame.color.Color('orange'))
		#for player speed
		self.upgrade_text3 = pygame.font.SysFont('Consolas', 30).render(
			'upgrade(' +str((int(self.player.speed) - 9) * 300) + ')', True,
			 pygame.color.Color('orange'))

		#says 'buy' followed by cost in parenthesis
		#for ammo
		self.buy_text1 = pygame.font.SysFont('Consolas', 30).render(
			'buy(200)', True, pygame.color.Color('orange'))
		#for health
		self.buy_text2 = pygame.font.SysFont('Consolas', 30).render(
			'buy(' + str(1000-self.player.health) + ')', True,
			 pygame.color.Color('orange'))
		#gives current value of upgradeable attribute
		#bullet damage
		self.cv1_text = pygame.font.SysFont('Consolas', 30).render(
			str(self.bulletDamage), True, pygame.color.Color('white'))
		#bullet penetration
		self.cv2_text = pygame.font.SysFont('Consolas', 30).render(
			str(self.bulletPenetration), True, pygame.color.Color('white'))
		#player speed
		self.cv3_text = pygame.font.SysFont('Consolas', 30).render(
			str(int(self.player.speed)), True, pygame.color.Color('white'))
		#ammo
		self.cv4_text = pygame.font.SysFont('Consolas', 30).render(
			str(self.ammo), True, pygame.color.Color('white'))
		#player health
		self.cv5_text = pygame.font.SysFont('Consolas', 30).render(
			str(self.player.health), True, pygame.color.Color('white'))

		#gives value after upgrade
		#bullet damage
		self.uv1_text = pygame.font.SysFont('Consolas', 30).render(
			str(self.bulletDamage + 1), True, pygame.color.Color('white'))
		#bullet penetration
		self.uv2_text = pygame.font.SysFont('Consolas', 30).render(
			str(self.bulletPenetration + 1), True, pygame.color.Color('white'))
		#player speed
		self.uv3_text = pygame.font.SysFont('Consolas', 30).render(
			str(int(self.player.speed) + 1), True, pygame.color.Color('white'))
		#ammo
		self.uv4_text = pygame.font.SysFont('Consolas', 30).render(
			str(self.ammo + 1000), True, pygame.color.Color('white'))
		#player health
		self.uv5_text = pygame.font.SysFont('Consolas', 30).render(
			str(1000), True, pygame.color.Color('white'))

		#game over relevant text
		#this says you died
		self.gameOver_text = pygame.font.SysFont('Consolas', 60).render(
			'YOU DIED', True, pygame.color.Color('red'))
		#this is displayed when a new highscore is achieved
		self.newHS_text = pygame.font.SysFont('Consolas', 20).render(
			'Congratulations! New Highscore', True, pygame.color.Color('black'))
		#new round tag
		self.newRound_text = pygame.font.SysFont('Consolas', 48).render(
			'New Round', True, pygame.color.Color('White'))
		#main menu tag
		self.return_text = pygame.font.SysFont('Consolas', 48).render(
			'Main Menu', True, pygame.color.Color('White'))


		#mainloop
		while not self.done:
			#make mouse invisible
			pygame.mouse.set_visible(False)

			#checks if startmenu should be loaded
			if self.notstarted == True:
				self.startMenu()

			#game over for when player dies
			if self.player.dead:
				self.done = True
				self.gameOver()

			#pauses game
			if self.pause == True:
				self.pauseMenu()

			for event in pygame.event.get():
				#checks if game closed
				if event.type == pygame.QUIT:
					self.done = True
				#checks if trying to pause
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						self.pause = True

			#manage rounds and spawn zombies (check function for description)
			self.round()
			
			#checks if player attempted to shoot
			#	I have disabled up/down shooting for better gameplay
			#uncomment triple commented lines to return functionality
			left = pygame.key.get_pressed()[pygame.K_LEFT]
			right = pygame.key.get_pressed()[pygame.K_RIGHT]
			### up = pygame.key.get_pressed()[pygame.K_UP]
			#### down = pygame.key.get_pressed()[pygame.K_DOWN]

			### if up == 1:
			### 	self.shoot('up')
			### elif down == 1:
			### 	self.shoot('down')
			#if player shoots, call shoot function (defined below)
			if left == 1:
				self.shoot('left')
			#elif to allow only one side at a time
			elif right == 1:
				self.shoot('right')
			
			#moves player (defined below)
			self.player.move()

			#makes sure 2 zombies do not completely overlap
			self.check_zombie_overlap()

			#checks for zombie/bullet collision and player/zombie collision
			self.check_collision()

			#kill Zombies
			self.killZombies()

			#calls update function for all sprites
			self.all_sprites.update()

			#draws all sprites on background
			self.all_sprites.draw(self.background.image)
			#draws relevant part of background onto screen
			#this achieves map motion affect
			self.gameDisplay.blit(self.background.image, (0,0),
							 (self.player.rect[0]-self.display_width/2,
							  self.player.rect[1]-self.display_height/2,
							  self.display_width,self.display_height))

			#drawing healthbar
			self.gameDisplay.blit(self.healthbar.image, (10,10))
			#draw a line for health: surface, color, start_pos, end_pos, width
			#this line gets shorter as player health decreases
			pygame.draw.line(self.gameDisplay, pygame.color.Color('red'),
				 (13,19), (14 + self.player.health * 0.4, 19), 16)

			#round number text blit
			self.gameDisplay.blit(self.RoundNo_text,
				([self.display_width * 0.46, self.display_height * 0.01]))
			#highscore text blit
			self.gameDisplay.blit(self.highscore_text,
				([self.display_width * 0.47, self.display_height * 0.045]))
			#coins text blit
			self.gameDisplay.blit(self.coins_text,
				([self.display_width * 0.01, self.display_height * 0.05]))
			#ammo text blit
			self.gameDisplay.blit(self.ammo_text,
				([self.display_width * 0.87, self.display_height * 0.95]))
			#remaining zombies text blit
			self.gameDisplay.blit(self.remainingZombies_text,
				([self.display_width * 0.82, self.display_height * 0.01]))


			#update display
			pygame.display.update()
			#resets background
			self.background.update()

			#fps
			self.clock.tick(self.fps)

		pygame.quit

	def updateText(self):
		#this function updates text that is displayed so latest data is shown
		#current round number
		self.RoundNo_text =  pygame.font.SysFont('Consolas', 32).render(('Round  ' 
			+ str(self.round_RoundNo)), True, pygame.color.Color('darkorange1'))
		#no. of remaining zombies
		self.remainingZombies_text =  pygame.font.SysFont('Consolas', 16).render((
			'Zombies Remaining:  ' + str(self.zombies_remaining)),
			 True, pygame.color.Color('White'))
		#all current value texts (for upgrade screen)
		#bullet damage
		self.cv1_text = pygame.font.SysFont('Consolas', 30).render(
			str(self.bulletDamage), True, pygame.color.Color('white'))
		#bullet penetration
		self.cv2_text = pygame.font.SysFont('Consolas', 30).render(
			str(self.bulletPenetration), True, pygame.color.Color('white'))
		#player speed
		self.cv3_text = pygame.font.SysFont('Consolas', 30).render(
			str(int(self.player.speed)), True, pygame.color.Color('white'))
		#ammo
		self.cv4_text = pygame.font.SysFont('Consolas', 30).render(
			str(self.ammo), True, pygame.color.Color('white'))
		#player health
		self.cv5_text = pygame.font.SysFont('Consolas', 30).render(
			str(self.player.health), True, pygame.color.Color('white'))

		#all upgraded value texts (for upgrade screen)
		#bullet damage
		self.uv1_text = pygame.font.SysFont('Consolas', 30).render(
			str(self.bulletDamage + 1), True, pygame.color.Color('white'))
		#bullet penetration
		self.uv2_text = pygame.font.SysFont('Consolas', 30).render(
			str(self.bulletPenetration + 1), True, pygame.color.Color('white'))
		#player speed
		self.uv3_text = pygame.font.SysFont('Consolas', 30).render(
			str(int(self.player.speed) + 1), True, pygame.color.Color('white'))
		#ammo
		self.uv4_text = pygame.font.SysFont('Consolas', 30).render(
			str(self.ammo + 1000), True, pygame.color.Color('white'))
		#player health
		self.uv5_text = pygame.font.SysFont('Consolas', 30).render(
			str(1000), True, pygame.color.Color('white'))

		#amount of coins
		self.coins_text = pygame.font.SysFont('Consolas', 32).render(('Coins: '
						 + str(self.coins)), True, pygame.color.Color('gold'))

	def upgradeScreen(self):
		#this screen opens at the end of each round for 30s for upgrades
		#theses timers are to count 30s
		start = time.time()
		end = time.time()

		#blit upgrade screen picture
		self.gameDisplay.blit(self.upgradeScreen_picture, (0,0))

		#make mouse visible
		pygame.mouse.set_visible(True)

		#run for 30 seconds : end is constantly updated, so when difference
		# is greater than 30 loop ends
		while end - start < 30:
			#create timer text for the next round (countdown from 30)
			timer = pygame.font.SysFont('Consolas', 30).render('Round ' + 
				str(self.round_RoundNo) + ' in: ' + 
				str(int(math.floor(30-end+start))), True, pygame.color.Color('red'))

			#these gray backgrounds are so that when the text is updated it is not
			#writing over text (it writes over gray background that cover past text)
			#for upgrade/buy texts
			#upgrade1
			self.gameDisplay.fill(pygame.color.Color('gray'), ((955,170),(205,40)))
			#upgrade2
			self.gameDisplay.fill(pygame.color.Color('gray'), ((955,240),(205,40)))
			#upgrade3		
			self.gameDisplay.fill(pygame.color.Color('gray'), ((955,310),(205,40)))
			#buy1
			self.gameDisplay.fill(pygame.color.Color('gray'), ((955,380),(205,40)))
			#buy2
			self.gameDisplay.fill(pygame.color.Color('gray'), ((955,450),(205,40)))

			#for timer text
			self.gameDisplay.fill(pygame.color.Color('gray'), 
				((self.display_width * 0.009, self.display_height * 0.90),(250,30)))

			#for 5 upgrade value texts
			#uv1			
			self.gameDisplay.fill(pygame.color.Color('gray'), ((775,170),(90,40)))
			#uv2
			self.gameDisplay.fill(pygame.color.Color('gray'), ((775,240),(90,40)))
			#uv3
			self.gameDisplay.fill(pygame.color.Color('gray'), ((775,310),(90,40)))
			#uv4
			self.gameDisplay.fill(pygame.color.Color('gray'), ((775,380),(90,40)))
			#uv5
			self.gameDisplay.fill(pygame.color.Color('gray'), ((775,450),(90,40)))

			#for 5 current value texts
			#cv1
			self.gameDisplay.fill(pygame.color.Color('gray'), ((475,170),(90,40)))
			#cv2
			self.gameDisplay.fill(pygame.color.Color('gray'), ((475,240),(90,40)))
			#cv3
			self.gameDisplay.fill(pygame.color.Color('gray'), ((475,310),(90,40)))
			#cv4
			self.gameDisplay.fill(pygame.color.Color('gray'), ((475,380),(90,40)))
			#cv4
			self.gameDisplay.fill(pygame.color.Color('gray'), ((475,450),(90,40)))

			#for coins_text
			self.gameDisplay.fill(pygame.color.Color('olivedrab1'), 
				((self.display_width * 0.01, self.display_height * 0.05),(220,35)))
			#for ammo text
			self.gameDisplay.fill(pygame.color.Color('olivedrab1'),
			 ((self.display_width * 0.87, self.display_height * 0.95),(140,25)))


			#draw coin text
			self.gameDisplay.blit(self.coins_text,
				([self.display_width * 0.01, self.display_height * 0.05]))
			#draw ammo text
			self.gameDisplay.blit(self.ammo_text,
				([self.display_width * 0.87, self.display_height * 0.95]))

			#draw timer text
			self.gameDisplay.blit(timer,
				([self.display_width * 0.01, self.display_height * 0.90]))

			#draw 3 upgrade buttons
			#upgrade text 1
			self.gameDisplay.blit(self.upgrade_text1,
				([self.display_width * 0.8, self.display_height * 0.25]))
			#upgrade text 2
			self.gameDisplay.blit(self.upgrade_text2,
				([self.display_width * 0.8, self.display_height * 0.35]))
			#upgrade text 3
			self.gameDisplay.blit(self.upgrade_text3,
				([self.display_width * 0.8, self.display_height * 0.45]))
			#draw buy buttons
			#buy1
			self.gameDisplay.blit(self.buy_text1,
				([self.display_width * 0.8, self.display_height * 0.55]))
			#buy2
			self.gameDisplay.blit(self.buy_text2,
				([self.display_width * 0.8, self.display_height * 0.65]))

			#draw 5 current value texts
			#cv1
			self.gameDisplay.blit(self.cv1_text,
				([self.display_width * 0.4, self.display_height * 0.25]))
			#cv2
			self.gameDisplay.blit(self.cv2_text,
				([self.display_width * 0.4, self.display_height * 0.35]))
			#cv3
			self.gameDisplay.blit(self.cv3_text,
				([self.display_width * 0.4, self.display_height * 0.45]))
			#cv4
			self.gameDisplay.blit(self.cv4_text,
				([self.display_width * 0.4, self.display_height * 0.55]))
			#cv5
			self.gameDisplay.blit(self.cv5_text,
				([self.display_width * 0.4, self.display_height * 0.65]))

			#draw 5 upgraded value texts
			#uv1
			self.gameDisplay.blit(self.uv1_text,
				([self.display_width * 0.65, self.display_height * 0.25]))
			#uv2
			self.gameDisplay.blit(self.uv2_text,
				([self.display_width * 0.65, self.display_height * 0.35]))
			#uv3
			self.gameDisplay.blit(self.uv3_text,
				([self.display_width * 0.65, self.display_height * 0.45]))
			#uv4
			self.gameDisplay.blit(self.uv4_text,
				([self.display_width * 0.65, self.display_height * 0.55]))
			#uv5
			self.gameDisplay.blit(self.uv5_text,
				([self.display_width * 0.65, self.display_height * 0.65]))

			#following is to give buttons functionality
			#check if cursor in x-range of buttons
			if 955 <= pygame.mouse.get_pos()[0] <= 1160:
				# all costs are calculated by a formula I thought appropriate
				#check if mouse over upgrade1 button
				if 170 <= pygame.mouse.get_pos()[1] <= 210:
					#make button yellow
					self.upgrade_text1 = pygame.font.SysFont('Consolas', 30).render(
						'upgrade(' +str(self.bulletDamage * 100) + ')', True,
						 pygame.color.Color('yellow'))
					#if pressed and sufficient coins for purchase
					if pygame.mouse.get_pressed()[0] == 1 and self.coins >= self.bulletDamage * 100:
						#minus cost from coins
						self.coins -= self.bulletDamage * 100
						#raise bullet damage
						self.bulletDamage += 1
						#update text to reflect new values
						self.updateText()
						#pause for 1 second to avoid accidentally repurchasing
						#(without this each item gets purchased multiple times)
						time.sleep(1)

				#check if mouse over upgrade2 button
				elif 240 <= pygame.mouse.get_pos()[1] <= 280:
					#make button yellow
					self.upgrade_text2 = pygame.font.SysFont('Consolas', 30).render(
						'upgrade(' +str(self.bulletPenetration * 100) + ')', True,
						 pygame.color.Color('yellow'))
					#if pressed and sufficient coins for purchase
					if pygame.mouse.get_pressed()[0] == 1 and self.coins >= self.bulletPenetration* 100:
						#minus cost from coins
						self.coins -= self.bulletPenetration * 100
						#raise bullet pentration
						self.bulletPenetration += 1
						#update text to reflect new values
						self.updateText()
						#pause for 1 second to avoid accidentally repurchasing
						#(without this each item gets purchased multiple times)
						time.sleep(1)

				#check if mouse over upgrade3 button
				elif 310 <= pygame.mouse.get_pos()[1] <= 350:
					self.upgrade_text3 = pygame.font.SysFont('Consolas', 30).render(
						'upgrade(' +str((int(self.player.speed) - 9) * 300) + ')', True,
						 pygame.color.Color('yellow'))
					#if pressed and sufficient coins for purchase
					if pygame.mouse.get_pressed()[0] == 1 and self.coins >= (int(self.player.speed) - 9) * 300:
						#remove cost from coins
						self.coins -= (int(self.player.speed) - 9) * 300
						#raise player speed
						self.player.speed += 1
						#raise player speed copy (see player class for explanation)
						self.player.speed_copy += 1
						#update text to reflect new values
						self.updateText()
						#pause for 1 second to avoid accidentally repurchasing
						#(without this each item gets purchased multiple times)
						time.sleep(1)

				#check if mouse over buy1 button
				elif 380 <= pygame.mouse.get_pos()[1] <= 420:
					#make button yellow
					self.buy_text1 = pygame.font.SysFont('Consolas', 30).render(
						'buy(200)', True, pygame.color.Color('yellow'))
					#if pressed and sufficient coins for purchase
					if pygame.mouse.get_pressed()[0] == 1 and self.coins >= 200:
						#remove cost from coins
						self.coins -= 200
						#raise ammo by 1000
						self.ammo += 1000
						#update ammo text to display new value
						self.ammo_text = pygame.font.SysFont('Consolas', 24).render((
							'Ammo: ' + str(self.ammo)), True,
							 pygame.color.Color('gray76'))
						#update text to reflect new values
						self.updateText()
						#pause for 1 second to avoid accidentally repurchasing
						#(without this each item gets purchased multiple times)
						time.sleep(1)

				#check if mouse over buy2 button
				elif 450 <= pygame.mouse.get_pos()[1] <= 490:
					#make button yellow
					self.buy_text2 = pygame.font.SysFont('Consolas', 30).render(
						'buy(' + str(1000-self.player.health) + ')', True,
						 pygame.color.Color('yellow'))
					#if pressed and sufficient coins for purchase
					if pygame.mouse.get_pressed()[0] == 1 and self.coins >= (1000-self.player.health):
						self.coins -= (1000-self.player.health)
						self.player.health = 1000
						#update text to reflect new values
						self.updateText()
						#pause for 1 second to avoid accidentally repurchasing
						#(without this each item gets purchased multiple times)
						time.sleep(1)
				else:
					#reset text colors if nothing is hovered over
					#upgrade text 1
					self.upgrade_text1 = pygame.font.SysFont('Consolas', 30).render(
						'upgrade(' +str(self.bulletDamage * 100) + ')', True,
						 pygame.color.Color('orange'))
					#upgrade text 2
					self.upgrade_text2 = pygame.font.SysFont('Consolas', 30).render(
						'upgrade(' +str(self.bulletPenetration * 100) + ')', True,
						 pygame.color.Color('orange'))
					#upgrade text 3
					self.upgrade_text3 = pygame.font.SysFont('Consolas', 30).render(
						'upgrade(' +str((int(self.player.speed) - 9) * 300) + ')', True,
						 pygame.color.Color('orange'))
					#buy text 1
					self.buy_text1 = pygame.font.SysFont('Consolas', 30).render(
						'buy(200)', True, pygame.color.Color('orange'))
					#buy text 2
					self.buy_text2 = pygame.font.SysFont('Consolas', 30).render(
						'buy(' + str(1000-self.player.health) + ')', True,
						 pygame.color.Color('orange'))
			else:
				#reset text colors if nothing is hovered over		
				#upgrade text 1
				self.upgrade_text1 = pygame.font.SysFont('Consolas', 30).render(
					'upgrade(' +str(self.bulletDamage * 100) + ')', True,
					 pygame.color.Color('orange'))
				#upgrade text 2
				self.upgrade_text2 = pygame.font.SysFont('Consolas', 30).render(
					'upgrade(' +str(self.bulletPenetration * 100) + ')', True,
					 pygame.color.Color('orange'))
				#upgrade text 3
				self.upgrade_text3 = pygame.font.SysFont('Consolas', 30).render(
					'upgrade(' +str((int(self.player.speed) - 9) * 300) + ')', True,
					 pygame.color.Color('orange'))
				#buy text 1
				self.buy_text1 = pygame.font.SysFont('Consolas', 30).render(
					'buy(200)', True, pygame.color.Color('orange'))
				#buy text 2
				self.buy_text2 = pygame.font.SysFont('Consolas', 30).render(
					'buy(' + str(1000-self.player.health) + ')', True,
					 pygame.color.Color('orange'))

			#get events
			for event in pygame.event.get():
				#check if player wants to exit screen early
				if event.type == pygame.KEYDOWN:
					#check for resume button
					if event.key == pygame.K_ESCAPE:
						#by reducing start we have made 30 seconds pass,
						# so next round starts
						start -= 30

				#close game (exit)
				if event.type == pygame.QUIT:
					self.done = True
					start -= 30
			#check current time
			end = time.time()
			#update display
			pygame.display.update()


	def killZombies(self):
		#this functions kills zombies and updates all related variables
		#loop through each existing xombie
		for zombie in self.zombie_sprites:
			#check if they are supposed to die
			if zombie.dead == True:
				#kill those that are suppoed to die
				zombie.kill()
				#update relevant values/texts 
				self.round_noKilled += 1
				self.zombies_remaining -= 1
				self.coins += 5
				self.updateText()


	def round(self):
		#this maintains rounds and spawns zombies
		#check if suffiecient zombies for round have spawned
		if self.round_noSpawned >= 20 * self.round_RoundNo:
			#stop spawning zmobies
			self.round_continueSpawn = False
			#check if all zombies have been killed
			if len(self.zombie_sprites) == 0:
				#end round if yes
				#update/reset relevant variables
				self.round_RoundNo += 1 #current round no.
				self.round_noSpawned = 0 #no. of zombies spawned for round
				self.round_counter = 0 #just a counter, to spawn zombies slowly
				self.round_noKilled = 0 #how many zombies killed
				self.round_continueSpawn = True
				self.zombies_remaining = 20 * self.round_RoundNo
				#increase health of player by 200 after each round
				self.player.health += 200
				if self.player.health > 1000:
					self.player.health = 1000
				pygame.draw.line(self.gameDisplay, pygame.color.Color('red'),
				 (13,19), (14 + self.player.health * 0.4, 19), 16)
				#increase coins
				self.coins += (50 + self.round_RoundNo * 50)
				#increase ammo and update ammo text
				self.ammo += 1000
				self.ammo_text = pygame.font.SysFont('Consolas', 24).render(
					('Ammo: ' + str(self.ammo)), True, pygame.color.Color('gray76'))
				self.updateText()
				#call upgrade screen
				self.upgradeScreen()

		#spawn zombies
		if self.round_continueSpawn == True:
			#first wave of zombies for each round
			#for each round, initial wave number increases by 10
			if self.round_noSpawned < (40 + 10 * self.round_RoundNo):
				#spawn every 5 secs
				if self.round_counter == 0:
					for i in range(5):
						self.spawn_zombie()
					self.round_noSpawned += 5


			if self.round_noKilled >= 40:
				#subsequent wave, after 40 zombies have been killed
				if self.round_counter == 0:
					for i in range(5):
						self.spawn_zombie()
					self.round_noSpawned += 5

			#this resets noKilled to 40 for 3rd round and onwards
			if self.round_noKilled >= 80:
				self.round_noKilled = 40

			#increment counter, so that it is zero every 5secs
			self.round_counter = (self.round_counter + 1) % (5*self.fps)


	def startMenu(self):
		#this is the start menu that is loaded at the beginning

		#reinstancing display to ensure it exists for when a game
		# is quit through pauseMenu
		self.gameDisplay = pygame.display.set_mode((self.display_width,
										self.display_height))
		#variable for determining whether to display controls or not
		blitControl = False

		#until player leaves start menu
		while self.notstarted:
			#make background black
			self.gameDisplay.fill(pygame.color.Color('black'))

			#make mouse visible
			pygame.mouse.set_visible(True)

			#blit text
			#game name
			self.gameDisplay.blit(self.game_text,
				([self.display_width * 0.42, self.display_height/3]))
			#start button
			self.gameDisplay.blit(self.start_text,
				([self.display_width * 0.15, 3 * self.display_height/4]))
			#controls button
			self.gameDisplay.blit(self.controls_text,
				([self.display_width * 0.49, 3 * self.display_height/4]))
			#exit button
			self.gameDisplay.blit(self.exit_text,
				([self.display_width * 0.80, 3 * self.display_height/4]))

			#check if cursor in y-range of buttons
			if 520 <= pygame.mouse.get_pos()[1] <= 571:
				#check if mouse over start button
				if 175 <= pygame.mouse.get_pos()[0] <= 450:
					#make start red
					self.start_text = pygame.font.SysFont('Monospace', 48).render(
						'Start Game', True, pygame.color.Color('red'))

					#start the  game
					if pygame.mouse.get_pressed()[0] == 1:
						#close start menu
						self.notstarted = False
						#reset color of button
						self.start_text = pygame.font.SysFont('Monospace', 48).render(
							'Start Game', True, pygame.color.Color('White'))

				#check if mouse over controls button
				elif 575 <= pygame.mouse.get_pos()[0] <= 835:
					#make controls red
					self.controls_text = pygame.font.SysFont('Monospace', 48).render(
						'Controls', True, pygame.color.Color('red'))

					if pygame.mouse.get_pressed()[0] == 1:
						blitControl = True

				#check if mouse over exit button
				elif 960 <= pygame.mouse.get_pos()[0] <= 1070:
					#make exit red
					self.exit_text = pygame.font.SysFont('Monospace', 48).render(
						'Exit', True, pygame.color.Color('red'))

					#exit game
					if pygame.mouse.get_pressed()[0] == 1:
						quit()


				#reset colors
				else:
					#start button
					self.start_text = pygame.font.SysFont('Monospace', 48).render(
						'Start Game', True, pygame.color.Color('White'))
					#controls button
					self.controls_text = pygame.font.SysFont('Monospace', 48).render(
						'Controls', True, pygame.color.Color('White'))
					#exit button
					self.exit_text = pygame.font.SysFont('Monospace', 48).render(
						'Exit', True, pygame.color.Color('White'))

			#reset colors
			else:
				#start button
				self.start_text = pygame.font.SysFont('Monospace', 48).render(
					'Start Game', True, pygame.color.Color('White'))
				#controls button
				self.controls_text = pygame.font.SysFont('Monospace', 48).render(
					'Controls', True, pygame.color.Color('White'))
				#exit button
				self.exit_text = pygame.font.SysFont('Monospace', 48).render(
					'Exit', True, pygame.color.Color('White'))
			#note: color reset twice for both y-axis range and x-axis range

			#get events
			for event in pygame.event.get():
				#close game (exit)
				if event.type == pygame.QUIT:
					quit()
				#close controls if esc clicked
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						blitControl = False

			#blit controls image if button clicked
			if blitControl:
				self.gameDisplay.blit(self.contols_image, (0,0))


			pygame.display.update()


	def pauseMenu(self):
		#this takes care of the pause menu
		while self.pause:

			#make mouse visible
			pygame.mouse.set_visible(True)

			#blit text
			#paused
			self.gameDisplay.blit(self.pause_text,
				([self.display_width * 0.43, self.display_height/3]))
			#resume
			self.gameDisplay.blit(self.resume_text,
				([self.display_width * 0.15, 3 * self.display_height/4]))
			#restart
			self.gameDisplay.blit(self.restart_text,
				([self.display_width * 0.44, 3 * self.display_height/4]))
			#quit
			self.gameDisplay.blit(self.quit_text,
				([self.display_width * 0.80, 3 * self.display_height/4]))

			#check if cursor in y-range of buttons
			if 520 <= pygame.mouse.get_pos()[1] <= 571:

				#check if mouse over resume button
				if 175 <= pygame.mouse.get_pos()[0] <= 340:
					#make resume red
					self.resume_text = pygame.font.SysFont('Consolas', 48).render(
						'Resume', True, pygame.color.Color('red'))
					
					#unpause game if clicked
					if pygame.mouse.get_pressed()[0] == 1:
						self.pause = False

				#check if mouse over restart button
				elif 525 <= pygame.mouse.get_pos()[0] <= 710:
					#make restart red
					self.restart_text = pygame.font.SysFont('Consolas', 48).render(
						'Restart', True, pygame.color.Color('red'))

					#restart game
					if pygame.mouse.get_pressed()[0] == 1:
						#redefine all redefines relevant attributes
						self.redefine_all()
						#unpause
						self.pause = False

				#check if mouse over quit button
				elif 960 <= pygame.mouse.get_pos()[0] <= 1070:
					#make quit red
					self.quit_text = pygame.font.SysFont('Consolas', 48).render(
						'Quit', True, pygame.color.Color('red'))

					#quit game
					if pygame.mouse.get_pressed()[0] == 1:
						#redefine all incase game is stared again
						self.redefine_all()
						#enable start menu
						self.notstarted = True
						#unpause
						self.pause = False
						self.done = False

				#reset colors
				else:
					self.resume_text = pygame.font.SysFont('Consolas',
					 48).render('Resume', True, pygame.color.Color('White'))
					self.restart_text = pygame.font.SysFont('Consolas',
					 48).render('Restart', True, pygame.color.Color('White'))
					self.quit_text = pygame.font.SysFont('Consolas',
					 48).render('Quit', True, pygame.color.Color('White'))

			#reset colors
			else:
				#resume
				self.resume_text = pygame.font.SysFont('Consolas',
				 48).render('Resume', True, pygame.color.Color('White'))
				#restart
				self.restart_text = pygame.font.SysFont('Consolas',
				 48).render('Restart', True, pygame.color.Color('White'))
				#quit
				self.quit_text = pygame.font.SysFont('Consolas',
				 48).render('Quit', True, pygame.color.Color('White'))
			#note: color reset twice for both y-axis range and x-axis range

			#get events
			for event in pygame.event.get():
				#unpause
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						self.pause = False
				#close game (exit)
				if event.type == pygame.QUIT:
					self.done = True
					self.pause = False


			pygame.display.update()

	def gameOver(self):
		#this screen is displayed if player dies
		#variable run is to know if while loop should continue to function
		run = True
		#newHS checks whether player reached a new HS
		newHS = False
		if self.round_RoundNo - 1 > int(self.highscore):
			#if yes, update highscore text file
			file = open(os.path.join('game_files', 'highscore.txt'), 'w')
			file.write(str(self.round_RoundNo - 1))
			file.close()
			#make newHS true so highscore text is displayed
			newHS = True

		#make mouse visible
		pygame.mouse.set_visible(True)
		#run indefinitely until player does something
		while run:
			#blit everything
			#game oever
			self.gameDisplay.blit(self.gameOver_text,
				([self.display_width * 0.43, self.display_height/3]))
			#new round
			self.gameDisplay.blit(self.newRound_text,
				([self.display_width * 0.15, 3 * self.display_height/4]))
			#return to main menu
			self.gameDisplay.blit(self.return_text,
				([self.display_width * 0.75, 3 * self.display_height/4]))
			#blit highscore text if there is a new highscore
			if newHS == True:
				self.gameDisplay.blit(self.newHS_text,
					([self.display_width * 0.38, self.display_height/2]))

			#allow game to be closed
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					quit()

			#check if cursor in y-range of buttons
			if 520 <= pygame.mouse.get_pos()[1] <= 571:

				#check if mouse over new round button
				if 175 <= pygame.mouse.get_pos()[0] <= 420:
					#make new round blue
					self.newRound_text = pygame.font.SysFont('Consolas',
						 48).render('New Round', True, pygame.color.Color('blue'))

					#if pressed
					if pygame.mouse.get_pressed()[0] == 1:
						#redefine everything and exit game over screen
						self.redefine_all()
						self.done = False
						run = False

				#check if over main menu button
				elif 890 <= pygame.mouse.get_pos()[0] <= 1140:
					#make blue
					self.return_text = pygame.font.SysFont('Consolas',
					 	48).render('Main Menu', True, pygame.color.Color('blue'))

					#if pressed
					if pygame.mouse.get_pressed()[0] == 1:
						#redefine everything, exit game menu and enter start menu
						self.redefine_all()
						self.notstarted = True
						self.done = False
						run = False

				else:
					#make everything white
					#new round
					self.newRound_text = pygame.font.SysFont('Consolas',
					 	48).render('New Round', True, pygame.color.Color('White'))
					#main menu
					self.return_text = pygame.font.SysFont('Consolas',
					 	48).render('Main Menu', True, pygame.color.Color('White'))

			else:
				#make everything white
				#new round
				self.newRound_text = pygame.font.SysFont('Consolas',
				 	48).render('New Round', True, pygame.color.Color('White'))
				#main menu
				self.return_text = pygame.font.SysFont('Consolas',
				 	48).render('Main Menu', True, pygame.color.Color('White'))

			pygame.display.update()



	def spawn_zombie(self):

		#size of zombie
		size = (45, 72)
		#to select type of zombie randomly
		image_set = random.randint(0,4)
		#selects zombie type [image_list contains 
		#different images for different zombies]
		images = self.zombie_image_list[image_set]
		#correcting size for zombie type 4 (index 3)
		if image_set == 3:
			size = (36,60)

		#randomly pick a spawnpoint
		spawnpoint = random.randint(1,3)

		#variable speed
		deltaspeed = random.randint(-1,3) + self.round_RoundNo
		#vary zombie health depending on round
		deltahealth = self.round_RoundNo * 30

		#creates zombie at relevant position
		if spawnpoint == 1:
			zombie = zombies((self.background.size[0] * 0.1,
							  self.background.size[1] * 0.1),
							 images, self.player, size, deltaspeed, deltahealth)
		if spawnpoint == 2:
			zombie = zombies((self.background.size[0] * 0.9,
							  self.background.size[1] * 0.1),
							 images, self.player, size, deltaspeed, deltahealth)
		if spawnpoint == 3:
			zombie = zombies((self.background.size[0] * 0.9,
							  self.background.size[1] * 0.9),
							 images, self.player, size, deltaspeed, deltahealth)

		#adds zombie to all_sprites group
		self.all_sprites.add(zombie)
		self.zombie_sprites.add(zombie)

	#function that deals with shooting bullets
	def shoot(self, direction):
		#make sure there is sufficient ammo
		if self.ammo > 0:
			#create a bullet
			bullet = Bullets(self.player.rect, self.background,
					 direction, self.bulletimage, self.bulletPenetration)
			#add bullet to sprite groups
			self.all_sprites.add(bullet)
			self.bullet_sprites.add(bullet)
			#rotate bullet depending on shooting direction
			self.player.change_orientation(direction)
			self.ammo -= 1
			#update ammo text
			self.ammo_text = pygame.font.SysFont('Consolas', 24).render(
				('Ammo: ' + str(self.ammo)), True, pygame.color.Color('gray76'))

	#check if 2 zombies have completely equal position
	def check_zombie_overlap(self):
		#loop through all zombie
		for zombie1 in self.zombie_sprites:
			#for each zombie, compare to every other zombie
			for zombie2 in self.zombie_sprites:
				#check that the 2 zombies are not the same zombie
				if zombie1 != zombie2:
					#check if they have same position
					if zombie1.rect == zombie2.rect:
						#move overlapping zombies by a random about in x and y axis
						deltapos = random.randint(-5, 5)
						zombie2.rect[0] = zombie1.rect[0] + deltapos
						zombie2.rect[1] = zombie1.rect[1] + deltapos

	#collision detection
	def check_collision(self):
		#empty list
		collision_list = []

		#check bullet and zombie collision
		for bullet in self.bullet_sprites:
			#creates list of everthing bullet collides with
			collision_list = pygame.sprite.spritecollide(bullet,
									 	self.zombie_sprites, False)
			#False means do not automatically kill sprites involved
			
			#if collision
			if collision_list != []:
				#damaging only fisrt zombie in the list
				zombie = collision_list[0]
				zombie.health -= self.bulletDamage
				#reduce bullet health
				bullet.health -= 1
				#kill bullet if it reacher zero
				if bullet.health <= 0:
					bullet.kill()

		#check if player colliding with zombies
		player_collision_list = pygame.sprite.spritecollide(self.player,
											 self.zombie_sprites, False)
		#damage player
		self.player.health -= len(player_collision_list)

	#redefine everything
	def redefine_all(self):
		#kill all existing sprites
		for sprite in self.all_sprites:
			sprite.kill()

		#redefine everything to default value

		#highscore
		file = open(os.path.join('game_files', 'highscore.txt'), 'r')
		self.highscore = file.readline()
		file.close()

		self.coins = 0
		self.ammo = 2500

		#create player and add to all_sprites group
		self.player = Player((self.background.size[0]/2,
		 		self.background.size[1]/2), self.playerImages, self.background)

		self.all_sprites.add(self.player)

		self.bulletDamage = 1
		self.bulletPenetration = 1

		#create healthbar
		self.healthbar = healthbar()

		#manage rounds
		self.round_RoundNo = 1
		self.round_continueSpawn = True
		self.round_noSpawned = 0
		self.round_noKilled = 0
		self.round_counter = 0

		self.zombies_remaining = 20

		#redefine texts
		self.ammo_text = pygame.font.SysFont('Consolas', 24).render(
				('Ammo: ' + str(self.ammo)), True, pygame.color.Color('gray76'))
		self.highscore_text = pygame.font.SysFont('Consolas', 16).render(
			('Highscore : ' + str(self.highscore)), True, pygame.color.Color('white'))
		self.updateText()



main = main()


