import pygame
import os
import time
import random

pygame.font.init()
myfont = pygame.font.SysFont(pygame.font.get_default_font(), 50)

class Object(): # parent class for both obstacles and player sprites
    def __init__(self,x,y,img):
        self.x=x
        self.y=y
        self.img=img
        #self.animationLength=len(img)
        #self.currentFrame=0
        
    def Draw(self,window):
        window.blit(self.img,(self.x,self.y))
        #window.blit(self.img[self.currentFrame],(self.x,self.y)) #draws the image at the correct x,y
        #if self.currentFrame < self.animationLength-1:
            #self.currentFrame+=1
        #else:
            #self.currentFrame=0
#the lines commented out above are for implementing animations

class EnemyEntity(Object): # specific class for Enemy because it doesnt move and includes health which is not required on other sprites
    def __init__(self,x,y,img,health):
        super().__init__(x,y,img)
        self.health=health
        self.mask= pygame.mask.from_surface(img)
        
    def DamageTaken(self):
        self.health=self.health - 1
    
class PlayerEntity(Object): # specific class for player because it includes health which is not required on other sprites
    def __init__(self,x,y,vel,img,health):
        super().__init__(x,y,img)
        self.vel=vel
        self.health=health
        self.mask= pygame.mask.from_surface(img)
        self.cooldown=0
        
    def DamageTaken(self):
        if self.cooldown <= 0:
            self.cooldown= 100
            self.health=self.health - 1
        
        
    def MovePlayer(self,width,height):
        keys = pygame.key.get_pressed() #returns a dict of keys:bool values that tell u if the key has been pressed
        if keys[pygame.K_a] and self.x - self.vel > 0: # left
            self.x -= self.vel
        if keys[pygame.K_d] and self.x + self.vel  < (width-50): # right
            self.x += self.vel
        if keys[pygame.K_w] and self.y - self.vel > 0: # up
            self.y -= self.vel
        if keys[pygame.K_s] and self.y + self.vel  < (height-30): # down
            self.y += self.vel
        
class ObstacleEntity(Object): 
    def __init__(self,x,y,vel,img):#add direction in prarameters when implementing
        super().__init__(x,y,img)
        self.vel=vel
        #self.direction=direction    #direction will be implemented later so just ignore this for now
        self.mask= pygame.mask.from_surface(img)
        
    def AutoMove(self): # the obstacle sprite doesnt depend on key presses to decide how to move therefore you can just make a function to do this automatically here
        self.x= self.x + self.vel
        #if self.direction == 'x':
            #self.x= self.x + self.vel
        #elif self.direction == '-x':
            #self.x= self.x - self.vel
        #elif self.direction == 'y':
            #self.y= self.y + self.vel
        #elif self.direction == '-y':
            #self.y= self.y - self.vel
            
def isCollide(obj1, obj2): #rectangular collision and then use masking to verify
    isCollision= False
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    if offset_y < 0 or offset_x < 0:  
        if obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None: # this returns the point of intersection or none if there is no point of intersection between the sprit
            isCollision= True
    return isCollision
            
def runGame():
    width, height = 1000, 350
    window = pygame.display.set_mode((width, height))
    pygame.display.set_caption("SPACE WAR")
    
    projectile = pygame.image.load(os.path.join("assets", "8.png"))

    projectile2 = pygame.image.load(os.path.join("assets", "7.png"))
    ORANGE_SPACE_SHIP =pygame.image.load(os.path.join("assets", "9B.png"))
    ORANGE_SPACE_SHIP_INV =pygame.image.load(os.path.join("assets", "9A.png"))

    PlayerBase= Object(width-150,(int((height-ORANGE_SPACE_SHIP.get_height())/2)),ORANGE_SPACE_SHIP_INV)
    EnemyObject=EnemyEntity(-150,(int((height-ORANGE_SPACE_SHIP.get_height())/2)),ORANGE_SPACE_SHIP,3)
    PlayerObject=PlayerEntity(width,(int((height-projectile2.get_height())/2)),3,projectile2,2)
    Obstacles=[]
    Clock=pygame.time.Clock()
    run = True
    win = False
    # initialisation and loading assets
    def updateWindow(Obstacles, PlayerObject, EnemyObject, PlayerBase, window, width):
        window.fill('black')
        
        EnemyHealth = myfont.render(f'Score {EnemyObject.health} Strikes to Win', 1, (0,255,0))
        PlayerHealth = myfont.render(f'You have {PlayerObject.health} lives left', 1, (0,255,0))
        window.blit(EnemyHealth, (10,10))#(40, int((height-70/2)))
        window.blit(PlayerHealth, (width-350,10))
        
        PlayerBase.Draw(window)
        EnemyObject.Draw(window)
        PlayerObject.Draw(window)
        
        for obstacle in Obstacles:
            obstacle.Draw(window)
            
        pygame.display.update()


    def ManageGameMechanics(Obstacles,PlayerObject,projectile,width, height):   
        if len(Obstacles) < 50:# this loop randomly initialises new obstacles
            NewObstacle= ObstacleEntity(random.randrange(-1500, -100),random.randrange(0, height - 30),random.randrange(2,5), projectile)
            #add rand choice state ment to allow the obstacles to start from different places and move in different directions
            Obstacles.append(NewObstacle)

        for Obstacle in reversed(Obstacles): # you need to reverse this so that it doesnt skip any indexes
            if Obstacle.x >width:
                Obstacles.remove(Obstacle)
            else:
                Obstacle.AutoMove()
                if isCollide(Obstacle,PlayerObject):
                    PlayerObject.DamageTaken()
    #start message ==========                
    StartMessage = myfont.render('The Space Force is testing a remote controlled bullet.', 1, (0,255,0))
    window.blit(StartMessage, (10, 10))
    pygame.display.update()
    time.sleep(3)
    window.fill('black')
    StartMessage = myfont.render('Since there are no Middle Eastern children left... ', 1, (0,255,0))
    window.blit(StartMessage, (10, 10))
    pygame.display.update()
    time.sleep(3)
    window.fill('black')
    StartMessage = myfont.render('They have to test it on themselves. ', 1, (0,255,0))
    window.blit(StartMessage, (10, 10))
    pygame.display.update()
    time.sleep(3)
    #========================
    while run:
        Clock.tick(60)
        
        PlayerObject.cooldown -=1

        PlayerObject.MovePlayer(width,height)

        ManageGameMechanics(Obstacles,PlayerObject,projectile,width,height)
        
        for event in pygame.event.get():#quit if x button in top right is pressed
            if event.type == pygame.QUIT:
                run = False
                

        if isCollide(EnemyObject,PlayerObject):#adjusts enemy health
            PlayerObject.x = width-70
            EnemyObject.DamageTaken()
            PlayerObject.cooldown=100


        updateWindow(Obstacles,PlayerObject,EnemyObject,PlayerBase,window,width)

        if PlayerObject.health <= 0:
            run = False

            
        if EnemyObject.health <= 0:
            run=False
            win=True

    # end message ===========
    time.sleep(1)        
    window.fill('black')
    if win:
        winMessage = myfont.render('YOU WON', 1, (0,255,0))
        window.blit(winMessage, (400, int((height/2))))
        pygame.display.update()
    else:
        winMessage = myfont.render('YOU LOST', 1, (0,255,0))
        window.blit(winMessage, (400, int((height/2))))
        pygame.display.update()
    # =======================

    time.sleep(3)
    quit()
    
runGame()
