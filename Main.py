import pygame
from pygame.locals import * #everything that makes you start the game

pygame.init() #basic code that makes py.game started up

clock = pygame.time.Clock()
fps = 60

screen_width = 500 #the resolution of my in-game window (x)
screen_height = 500 #variables for the screen resolution (y)

screen = pygame.display.set_mode((screen_width, screen_height)) #this function creates a game window for my game
pygame.display.set_caption('OblaK Jumper') #The name of the game. 

#define game variables
tile_size = 25

#load images
sun_img = pygame.image.load('./sun.png')
bg_img = pygame.image.load('./sky.png')

#def draw_grid(): #this is just a define draw grid function so im just going through a range and drawing bunch of a lines onto the screen.  
    #for line in range(0, 20): #with a color of white and these are the x and y coordinates.
        #pygame.draw.line(screen, (255, 255, 255), (0, line * tile_size), (screen_width, line * tile_size))
        #pygame.draw.line(screen, (255, 255, 255), (line * tile_size, 0), (line * tile_size, screen_height))



class Player():
    def __init__(self, x, y):
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0 #This will help me to control the speed at which animation runs through
        for num in range(1, 5): #iterations like this arent going to include that the last number so its only gonna go through to four
            img_right = pygame.image.load(f'./guy{num}.png')
            img_right = pygame.transform.scale(img_right, (20, 40))
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)
        self.image = self.images_right[self.index]  
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y 
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0 
        self.jumped = False 
        self.direction = 0 
        
    def update(self): 
        dx = 0 #this means basically change,  
        dy = 0
        walk_cooldown = 5 
        
        #get keypresses
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE] and self.jumped == False:
            self.vel_y = -15
            self.jumped = True 
        if key[pygame.K_SPACE] == False: #when youre checking for an if statement youve got to use two of them but, when you set to something you set one
            self.jumped = False 
        if key[pygame.K_LEFT]: #so when i press the left key I just want my dx coordinate or the x variable to be decreased by 5 because Im moving left so the x coordinate decreases.
            dx -= 5 
            self.counter += 1
            self.direction = -1 
        if key[pygame.K_RIGHT]: #the same thing here but here it is going to increase 
            dx += 5 
            self.counter += 1
            self.direction = 1
        if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False: #resets the character animation after i stop press on keys
            self.counter = 0 
            self.index = 0
            if self.direction == 1: 
                 self.image = self.images_right[self.index]
            if self.direction == -1: 
                 self.image = self.images_left[self.index]
        
             
        #handle animation
        self.counter += 1 
        if self.counter > walk_cooldown:
            self.counter = 0 
            self.index += 1
            if self.index >= len(self.images_right):
                self.index = 0 
            if self.direction == 1: 
                 self.image = self.images_right[self.index]
            if self.direction == -1: 
                 self.image = self.images_left[self.index]
                 
             
       #add gravity
        self.vel_y += 1
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y

        #check for collision
        for tile in world.tile_list:
            if tile[1].colliderect(self.rect.x + self.rect.y, dy, self.width, self.height):
                dx = 0
            #check for collision in y direction
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                #check if below the ground i.e. jumping
                if self.vel_y < 0:
                    dy = tile[1].bottom - self.rect.top
                #check if above the ground  i.e. falling
                elif self.vel_y >= 0:
                    dy = tile[1].top - self.rect.bottom

        #update player coordinates
        self.rect.x += dx
        self.rect.y += dy

        if self.rect.bottom > screen_height:
            self.rect.bottom = screen_height
            dy = 0

        #draw player onto screen
        screen.blit(self.image, self.rect)
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2) #creates rectangle around the player
        
    
    
        

class World():
    def __init__(self, data): #as a normal class you start it up with an constructor which is ur init function
        self.tile_list = [] #Init takes the self argument and also the data argument, so this data is going to be the world data that i eventually supply to it

        #load images
        dirt_img = pygame.image.load('./dirt.png') 
        grass_img = pygame.image.load('./grass.png')
        #Essentially what I want to do is I wanted to be able to run through each of these rows one by one
        #and within each row I want to go through each of the tiles one by one or colums and just say 
        #if its a one then do this if its a two do that and if its a zero do nothing 
        #so for that I just need to run for loop 
        row_count = 0 #I need to make sure that theyre defined before I start. 
        for row in data: #so for row data in data is this list that im going to supplying into the class so for row meaning that iterate through each of the individual rows and then within each of those rows. 
            col_count = 0 #this is a counter that, call count which is my column count is zero and then as I iterate
            for tile in row: #for the tile in row we look at each individual column or each individual tile 
                if tile == 1: #so if that tile is one then that means that we have a block of dirt
                    img = pygame.transform.scale(dirt_img, (tile_size, tile_size)) #I need to make sure that each of these dirt blocks or in fact any block that I load in  corectly sized to it, so I need scale it up to that size and for that I use this command. 
                    img_rect = img.get_rect() #essentially it just takes the size of this image and it creates a rectangle from it
                    img_rect.x = col_count * tile_size #for this I need to use x and y coordinate because I need to know where I am within this grid where its going to show it on the main game window  
                    img_rect.y = row_count * tile_size 
                    tile = (img, img_rect) #so because I got two values I can just save in tile variable and I would save them as a tuple so the first value is going to be my image and the second value is going to be the rectangle.
                    self.tile_list.append(tile) #this is just a python list so I can you append function from python to add items to this list so I just add this tile
                if tile == 2: 
                    img = pygame.transform.scale(grass_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 3:    
                    blob = Enemy(col_count * tile_size, row_count * tile_size + 15)
                    blob_group.add(blob)
                col_count += 1 # essentially it means that as soon as ive gone through one of these tiles and ive moved to the next one increase that variable by one so now I know that im moving along within this row   
            row_count += 1 #this will make me be able to increase my  row counter as well, so we do this with this for loop 

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
            pygame.draw.rect(screen, (255, 255, 255), tile[1], 2) #draws a outline around the blocks


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('./blob.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        
    def update(self):
        self.rect.x += self.move_direction
        



world_data = [ #each of those rows essentially is a list on its own so what can I say is in the first row all bits of dirt.
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 1], 
[1, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 2, 2, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 7, 0, 5, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 1], 
[1, 7, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 7, 0, 0, 0, 0, 1], 
[1, 0, 2, 0, 0, 7, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 2, 0, 0, 4, 0, 0, 0, 0, 3, 0, 0, 3, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 7, 0, 0, 0, 0, 2, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 2, 2, 2, 2, 2, 1], 
[1, 0, 0, 0, 0, 0, 2, 2, 2, 6, 6, 6, 6, 6, 1, 1, 1, 1, 1, 1], 
[1, 0, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
[1, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
[1, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]



player = Player(100, screen_height - 130)

blob_group = pygame.sprite.Group()

world = World(world_data)



run = True #this varible tells the game to run (not to close after one 0.1)
while run: #this loop basically means that as long as this variable is set to true just keeps doing the code that is in here, so this is my game loop

    clock.tick(fps)
    
    screen.blit(bg_img, (0, 0)) #the function for putting an image onto the screen
    screen.blit(sun_img, (100, 100)) #the numbers show the position of where the image will be shown

    world.draw() #draws the world
    
    blob_group.update()
    blob_group.draw(screen)  
    
    player.update()
    
    #draw_grid() #draws the grids, that can help me find the right position of images.

    for event in pygame.event.get(): #this just cycles throught all the events 
        if event.type == pygame.QUIT: #this will make sure that you can close the game
            run = False

    pygame.display.update() #essentially what this means is that throughout the code you're going to be putting all these different blit functions and draw functions.
    #this one last line here essentially tells pygame okay, take all these things and now actually upadate the 
    #display window with those instructions. 

pygame.quit()