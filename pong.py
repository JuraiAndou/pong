import pygame, sys, random
from pygame import draw
from pygame.locals import *

class Entity:
    def draw():
        pass

    def update():
        pass

class Physics:
    def update():
        pass

class Graphics:
    def draw():
        pass

class Player(Entity):
    def __init__(self, world, x , y, width, height):
        print("Player initialized...")
        self.body = self.x, self.y, self.width, self.height = x, y, width, height

        self.world = world
        self.graphics = PlayerGraphics()

    def draw(self):
        self.graphics.draw(self.body, self.world)

    def update(self):
        self.draw()

class PlayerGraphics(Graphics):
    def __init__(self):
        print("Player Graphics initilized...")

    def draw(self, body, world):
        pygame.draw.rect(world.screen, (255, 255, 255), body)

class Enemy(Entity):
    def __init__(self, world, x, y, width, height):
        print("Enemy initialized...")
        self.body = self.x, self.y, self.width, self.height = x, y, width, height
        self.world = world
        self.graphics = EnemyGraphics()

    def draw(self):
        self.graphics.draw(self.world, self.body)

    def update(self):
        pass

class EnemyGraphics(Graphics):
    def __init__(self):
        print("Enemy Graphics intialized...")

    def draw(self, world, body):
        pygame.draw.rect(world.screen, (255,255,255), body)

class World(Entity):
    game_state = 'GAME'
    def __init__(self):
        print ("World initialized...")
        self.size = self.width, self.height = 640, 480
        self.screen = pygame.display.set_mode(self.size)
        self.graphics = WorldGraphics(self)
        pygame.display.set_caption('Pong')
        #initializing entities
        self.entities = []

        #player
        self.player = Player(self, 10, (self.height / 2) - 50, 12, 100)
        self.entities.append(self.player)

        #enemy
        self.player = Enemy(self, self.width - 22, (self.height / 2) - 50, 12, 100)
        self.entities.append(self.player)

        self.bg_color = (0, 0, 0)
        
        self.inputs = Inputs(self)

        print("Initializing Game Loop...")
        self.game_loop()

    def game_loop(self):
        previous_tick = pygame.time.get_ticks()
        FPS = 60
        MS_PER_UPDATE = 1000/FPS
        delta_time = 0
        frame_lag = 0

        while 42:
            current_tick = pygame.time.get_ticks()
            delta_time = current_tick - previous_tick
            previous_tick = current_tick
            frame_lag += delta_time
            
            #Check for user input
            self.inputs.input()
            while frame_lag >= MS_PER_UPDATE:
                #updates the game
                self.update(MS_PER_UPDATE)
                frame_lag -= MS_PER_UPDATE

            #draws the frames
            self.draw()


    def draw(self):
        #self.screen.fill(self.bg_color)
        ##pygame.draw.rect(self.screen, (255, 255, 255), (10, 10, 40,40))
        #
        #for i in self.entities:
        #    i.draw()

        #pygame.display.flip()

        self.graphics.draw()

    def update(self, delta_time):
            pass

class WorldGraphics(Graphics):
    def __init__(self, world):
        print("world graphics initialized...")
        self.world = world

    def draw(self):
        self.world.screen.fill(self.world.bg_color)
        
        if self.world.game_state == 'GAME':
            self.game()

        pygame.display.flip()
    
    def game(self):
        for i in self.world.entities:
            i.draw()

class Inputs():
    def __init__(self, world):
        print("Inputs initialized...")
        self.world = world

    def input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT :
                sys.exit()


def main():
    pygame.init()
    print("Initialazing game...")
    World()


if __name__ == "__main__":
    main()