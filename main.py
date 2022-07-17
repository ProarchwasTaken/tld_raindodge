import pygame, sys, random, json, os

# General Stuff
pygame.init()
clock = pygame.time.Clock()

screenWidth, screenHeight = 800, 600
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Rain Drop Dodging")

# Fonts 
font_small = pygame.font.Font(None, 32)
font_medium = pygame.font.Font(None, 64)
font_large = pygame.font.Font(None, 128)

# Colors - (r, g, b)
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
dark_green = pygame.Color(0, 128, 0)
dark_blue = pygame.Color(0, 0, 128)

# Variables
game_scene = "title"

total_raindrops = [] # This will be used later to create an infinite amount of raindrops.

# Two things needed to make dir path getting work.
dir_name = os.path.dirname(__file__)

file_dir = os.path.join(dir_name, "high_score.json") # Stores dir to json that stores highscore.


save = open(file_dir, "r+") # Prepares high_score.json

score = 0 # Score increases each time a raindrop hits the ground.

highscore = json.load(save)# Makes values in high_score.json useable

# Spawn delays
last = pygame.time.get_ticks()
spawn_delay = 1.5 # How much seconds between raindrop spawns.
lowest_delay = 0.1

# Static Text - For text that doesn't have any special properties

# -Title Text
title_text = font_large.render("Rain Dodge", True, white)
title_rect = title_text.get_rect(center=(screenWidth/2, 100))
# -Credits Text
cred_text = font_small.render("Game made by: Tyler Dillard, 2022", True, white)
cred_rect = cred_text.get_rect()
cred_rect.bottomleft = 0, 600
# -Play button Text
pb_text = font_medium.render("   Play   ", True, black, white)

# Simple Rects
# (x, y, width, Height)
ground = pygame.Rect(0, 500, 800, 100)

# Classes

class Player:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x - (width/2), y - height, width, height) # (x, y, width, height)
        self.speed = 0
        self.max_speed = 4
        
    
    def Update(self, color):
        self.rect.x += self.speed
        
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > screenWidth:
            self.rect.right = screenWidth
        
        pygame.draw.rect(screen, color, self)
    
    def inputCheck(self):
        if event.type == pygame.KEYDOWN:
            # Moves the player left or right when a key is pressed
            if event.key == pygame.K_RIGHT:
                self.speed += self.max_speed
            if event.key == pygame.K_LEFT:
                self.speed -= self.max_speed

        if event.type == pygame.KEYUP:
            # Stops the player when a key is released
            if event.key == pygame.K_RIGHT:
                self.speed -= self.max_speed
            if event.key == pygame.K_LEFT:
                self.speed += self.max_speed
        
class RainDrop:
    objs = [] #This list to used to keep track of all created RainDrop instances.
    
    def __init__(self, x, width, height, f_speed):
        self.rect = pygame.Rect(x - (width/2), -100, width, height)
        RainDrop.objs.append(self)
        
        self.falling_speed = f_speed
    
    @classmethod
    def Update(cls, color):
        global score, spawn_delay
        # Updates every instance of a class.
        for obj in cls.objs:
            # Automatically moves instance down. speed is dictation by it's own falling_speed variable
            obj.rect.y += obj.falling_speed
            
            # This removes the rain down instance if it collides with the ground.
            if ground.colliderect(obj):
                # This also removes the instance from the objs and total_raindrops list
                cls.objs.remove(obj)
                total_raindrops.remove(obj)
                
                score += 10 # Increases the score
                if spawn_delay > lowest_delay:
                    # Decreases the spawn delay. The amount decreased is based on the length on total_raindrops
                    spawn_delay -= 0.01 - ((len(total_raindrops) / 2) / 1000)
            
            # Game is over when the player touches a raindrop
            if player.rect.colliderect(obj):
                end_game()
            
            pygame.draw.rect(screen, color, obj)

# Game Scenes
def Title_Screen(): # This scene will drawn when the program is opened.
    global pb_text, game_scene
    mouse_pos = pygame.mouse.get_pos()
    
    
    # High Score Text
    hs_text = font_small.render(f"High Score: {highscore['Value']}", True, white)
    hs_rect = hs_text.get_rect()
    hs_rect.center = 400, 150
    
    # Play Button Rect
    pb_rect = pb_text.get_rect()
    pb_rect.center = 400, 300
    
    if pb_rect.collidepoint(mouse_pos):
        # Changes the play button color to red if mouse is hovering over it
        pb_text = font_medium.render("   Play   ", True, black, red)
        if pygame.mouse.get_pressed()[0] == 1:
            # Switches game scene when button is clicked.
            game_scene = "game"
            player.speed = 0
            print("Starting the game...")
    else:
        # Change the color back if mouse is not hovering over it.
        pb_text = font_medium.render("   Play   ", True, black, white)
    
    # Draws the stuff needed for the Title Screen
    screen.blit(pb_text, pb_rect)
    screen.blit(title_text, title_rect)
    screen.blit(cred_text, cred_rect)
    screen.blit(hs_text, hs_rect)
    
def Game_Screen():
    
    score_text = font_small.render(f"{score}", True, white, black)
    score_rect = score_text.get_rect()
    score_rect.center = 400, 550
    
    player.Update(red)
    
    RainDrop.Update(dark_blue)
    
    spawnDrop()
    
    # This draws the ground.
    pygame.draw.rect(screen, dark_green, ground)
    # Draws the Score text
    screen.blit(score_text, score_rect)

def spawnDrop():
    global last
    now = pygame.time.get_ticks()
    
    if now - last >= spawn_delay * 1000:
        last = now
        # This creates a new instance of the RainDrop class - (x, width, height, f_speed)
        total_raindrops.append(RainDrop(random.randrange(25, 775), 8, 32, random.randrange(2,10)))
        
        
# Class Instances
# (x, y, width, height)
player = Player(400, 500, 32, 64)

# This function resets everything and takes the player back to the title screen
def end_game():
    global total_raindrops, player, spawn_delay, score, game_scene
    print("Game Over")
    
    game_scene = "title"
    # Changes highscore value to score if score is higher than highscore
    if score > highscore["Value"]:
        highscore["Value"] = score
        
        # Saves highscore to .json
        save.seek(0)
        json.dump(highscore, save)
        save.truncate()
        
        print("You got a new highscore!")
    
    score = 0
    
    RainDrop.objs = []
    total_raindrops = []
    
    player = Player(400, 500, 32, 64)
    spawn_delay = 1.5
    

# Game Loop
while True:
    for event in pygame.event.get():
        #Allows player to quit the game.
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # This class funtion checks for player input.
        player.inputCheck()
    
    # Draws stuff
    screen.fill(black)
    
    if game_scene == "title":
        Title_Screen()
    
    if game_scene == "game":
        Game_Screen()
    
    # Updates the screen.
    pygame.display.update()
    clock.tick(60)