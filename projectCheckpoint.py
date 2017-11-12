#    15-112: Principles of Programming and Computer Science
#    Project: Zombie Game
#    Name      : Muhammad Ahmad Khan
#    AndrewID  : mkhan2
#    File Created: 10/11/2017
#    Modification History:
#    Start             End
#    10/11 17:21      11/11 01:20
#    11/11 14:00      11/11 24:00


#importing libraries
import pygame
import os
import random
import Tkinter

paused = False

def load_images(foldername):
#   Loads all images in directory. The directory must only contain images.
#   Args:
#       path: The relative or absolute path to the directory to load images from.
#   Returns:
#       List of images

    path = os.path.join(os.path.dirname(os.path.realpath(__file__)),foldername)
    images = []
    for file_name in os.listdir(path):
        image = pygame.image.load(os.path.join(path, file_name))#.convert()
        image = pygame.transform.scale(image, (30, 30))
        images.append(image)

    return images

def spawn_zombie(images):
    spawnpoint = random.randint(1,3)
    if spawnpoint == 1:
        zombie = zombies((background.size[0] * 0.1, background.size[1] * 0.1), images)
    if spawnpoint == 2:
        zombie = zombies((background.size[0] * 0.9, background.size[1] * 0.1), images)
    if spawnpoint == 3:
        zombie = zombies((background.size[0] * 0.9, background.size[1] * 0.9), images)
    all_sprites.add(zombie)

#create class for background
class Background(pygame.sprite.Sprite):
    def __init__(self):
        #call parent class constructor
        super(Background, self).__init__()
        self.image = pygame.image.load('background1.jpg')
        self.size = self.image.get_size()

    def update(self):
        self.image = pygame.image.load('background1.jpg')
        
    

#create class for the player
class Player(pygame.sprite.Sprite):
#   A class for the player character
#   Args:
#       position: where the character should be created
#       images: different sprite images
    def __init__(self, position, images):

        #call parent class constructor
        super(Player, self).__init__()
        self.size = (30, 30) #the size of the player picture

        self.rect = pygame.Rect(position, self.size)
        
        self.images = images
        self.images_right = images
        # Flipping every image.
        self.images_left = [pygame.transform.flip
                            (image, True, False) for image in images]
        self.index = 0
        self.image = images[self.index] #sets current image

        #self.movement = pygame.math.Vector2(0, 0)
        self.vmovement = 0
        self.hmovement = 0
        self.speed = 10

    def move(self,direction):
        if direction == 'up':
            self.vmovement -= self.speed
        if direction == 'down':
            self.vmovement += self.speed
        if direction == 'left':
            self.hmovement -= self.speed
            self.images = self.images_left
        if direction == 'right':
            self.hmovement += self.speed
            self.images = self.images_right
        self.rect.move_ip(self.hmovement,self.vmovement)
        self.vmovement = 0
        self.hmovement = 0
        self.image = self.images[self.index]

#create class for zombies
class zombies(pygame.sprite.Sprite):
    def __init__(self, position, images):
        #call parent class constructor
        super(zombies, self).__init__()
        self.size = (30, 30) 
        self.rect = pygame.Rect(position, self.size)
        self.images = images
        self.images_right = images
        # Flipping every image.
        self.images_left = [pygame.transform.flip
                            (image, True, False) for image in images]
        self.index = 0
        self.image = images[self.index] #sets current image
        self.speed = 5
        self.vmovement = 0
        self.hmovement = 0
    def update(self):
        if player.rect[0] > self.rect[0]:
            self.hmovement += self.speed
        if player.rect[0] < self.rect[0]:
            self.hmovement -= self.speed
        if player.rect[1] > self.rect[1]:
            self.vmovement += self.speed
        if player.rect[0] < self.rect[0]:
            self.vmovement -= self.speed
        self.rect.move_ip(self.hmovement,self.vmovement)
        self.vmovement = 0
        self.hmovement = 0
        
def main(w):
    w.destroy()
    pygame.init()

    display_width = 800
    display_height = 600
    
    global background
    background = Background()

    gameDisplay = pygame.display.set_mode((display_width,display_height)) #sets the display and its size

    pygame.display.set_caption('Alien Invasion') #changes window title

    clock = pygame.time.Clock() #it creates a timer, and can be used to set fps

    done = False

    playerImages = load_images("player")
    zombieImages = load_images("zombie")
    global player
    player = Player((background.size[0]/2,background.size[1]/2), playerImages)
    global all_sprites
    all_sprites = pygame.sprite.Group(player)  # Creates a sprite group and adds 'player'
    spawn_zombie(zombieImages)

    while not done:
            for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                            done = True
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            paused = PauseScreen()
            up = pygame.key.get_pressed()[pygame.K_w]
            down = pygame.key.get_pressed()[pygame.K_s]
            left = pygame.key.get_pressed()[pygame.K_a]
            right = pygame.key.get_pressed()[pygame.K_d]
            if up == 1:
                    player.move('up')
            if down == 1:
                    player.move('down')
            if left == 1:
                    player.move('left')
            if right == 1:
                    player.move('right')

            all_sprites.update()
            all_sprites.draw(background.image)
            gameDisplay.blit(background.image, (0,0),
                             (player.rect[0]-display_width/2, player.rect[1]-display_height/2,
                              display_width,display_height))
            pygame.display.update()
            #think about how to avoid loading image twice
            background.update()
            clock.tick(50)
    pygame.quit()

class StartScreen():
    def __init__(self): #feeding in a main window
        self.w = Tkinter.Tk()
        self.frame = Tkinter.Frame(self.w) 
        self.frame.pack()
        self.gamename = Tkinter.Label(self.frame, text="Zombie Shooter")
        self.StartButton = Tkinter.Button(self.frame, text="Start Game", command=lambda:self.StartGame())
        self.OptionsButton = Tkinter.Button(self.frame, text="Options", command=lambda:self.ShowOptions())
        self.ExitButton = Tkinter.Button(self.frame, text="Exit", command=lambda:self.w.destroy())

        self.gamename.grid(column = 1, row = 1, columnspan= 5, rowspan = 5)
        self.StartButton.grid(column = 1, row = 10)
        self.OptionsButton.grid(column = 2, row = 10)
        self.ExitButton.grid(column = 3, row = 10)
        self.w.title("Start Screen")
        self.w.geometry('800x600')
        self.w.mainloop()
    def StartGame(self):
        game = main(self.w)

class PauseScreen():
    def __init__(self): #feeding in a main window
        self.w = Tkinter.Tk()
        self.frame = Tkinter.Frame(self.w) 
        self.frame.pack()
        self.gamename = Tkinter.Label(self.frame, text="Paused")
        self.StartButton = Tkinter.Button(self.frame, text="Resume Game", command=lambda:self.ResumeGame())
        self.OptionsButton = Tkinter.Button(self.frame, text="Options", command=lambda:self.ShowOptions())
        self.ExitButton = Tkinter.Button(self.frame, text="Exit", command=lambda:self.w.destroy())

        self.gamename.grid(column = 1, row = 1, columnspan= 5, rowspan = 5)
        self.StartButton.grid(column = 1, row = 10)
        self.OptionsButton.grid(column = 2, row = 10)
        self.ExitButton.grid(column = 3, row = 10)
        self.w.title("Pause Screen")
        self.w.geometry('800x600')
        self.w.mainloop()
    def ResumeGame(self):
        global pause
        pause = False
        self.w.destroy()

x = StartScreen()

##def game_intro():
##
##    intro = True
##
##    while intro:
##        for event in pygame.event.get():
##            if event.type == pygame.QUIT:
##                pygame.quit()
##                quit()
##                
##        gameDisplay.fill(white)
##        largeText = pygame.font.Font('freesansbold.ttf',115)
##        TextSurf, TextRect = text_objects("A bit Racey", largeText)
##        TextRect.center = ((display_width/2),(display_height/2))
##        gameDisplay.blit(TextSurf, TextRect)
##        pygame.display.update()
##        clock.tick(15)


#game_intro()
