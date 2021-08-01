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
    def __init__(self):
        print("Player initialized...")
        self.size = witdh, height = 10,10

        self.grapics = PlayerGraphics()

    def draw(self):
        pass

    def update(self):
        pass

class PlayerGraphics(Graphics):
    def __init__(self):
        print("Player Graphics initilized...")

    def draw(self):
        pygame.draw.rect()

class Enemy(Entity):
    def __init__(self):
        print("Enemy initialized...")
        self.size = witdh, height = 10,10

        self.graphics = EnemyGraphics()

    def draw(self):
        pass

    def update(self):
        pass

class EnemyGraphics(Graphics):
    def __init__(self):
        print("Enemy Graphics intialized...")

    def draw(self):
        pygame.draw.rect()

class World(Entity):
    def __init__(self):
        print ("World initialized...")
        self.size = width, height = 640, 480
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption('Pong')

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
        self.screen.fill(self.bg_color)
        pygame.display.flip()

    def update(self, delta_time):
            pass

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