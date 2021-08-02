import pygame, sys, random

from pygame import draw, init
from pygame.display import update
from pygame.locals import *
from pygame.constants import MOUSEBUTTONUP

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

#Player Stuff
class Player(Entity):
    def __init__(self, world):
        print("Player initialized...")
        self.world = world
        self.body = pygame.Rect(self.world.width - 20, self.world.height / 2 - 70, 10, 140)
        self.score = 0

        self.graphics = PlayerGraphics()
        self.physics = PlayerPhysics(self.world)

    def draw(self):
        self.graphics.draw(self.body, self.world)

    def update(self, dt):
        self.physics.update(self)

class PlayerGraphics(Graphics):
    def __init__(self):
        print("Player Graphics initilized...")

    def draw(self, body, world):
        pygame.draw.rect(world.screen, (255, 255, 255), body)

class PlayerPhysics(Physics):
    def __init__(self, world):
        print("Player Physics initialized...")
        self.world = world

    def update(self, player):
        player.body[1] = self.world.inputs.mouseY()

#Enemy Stuff
class Enemy(Entity):
    def __init__(self, world):
        print("Enemy initialized...")
        self.world = world
        self.body = pygame.Rect(10, self.world.height / 2 - 70, 10, 140)
        self.speed = 10
        self.score = 0
        
        self.graphics = EnemyGraphics()
        self.physics = EnemyPhysics(self.world, self.body)

    def draw(self):
        self.graphics.draw(self.world, self.body)

    def update(self, dt):
        self.physics.update(self.speed)

class EnemyGraphics(Graphics):
    def __init__(self):
        print("Enemy Graphics intialized...")

    def draw(self, world, body):
        pygame.draw.rect(world.screen, (255,255,255), body)

class EnemyPhysics(Physics):
    def __init__(self, world, body):
        print("Enemy Physics initialized...")
        self.world = world
        self.body = body

    def update(self, speed):
        if self.body.bottom < self.world.ball.body.y:
            self.body.bottom += speed
        if self.body.top > self.world.ball.body.y:
            self.body.top -= speed

#Ball Stuff
class Ball(Entity):
    def __init__(self, world):
        print("Ball initialized...")
        self.world = world
        self.body = pygame.Rect(self.world.width / 2 - 15, self.world.height / 2 - 15, 30, 30)
        self.speedX = 0.5
        self.speedY = 0.2
        
        self.graphics = BallGraphics()
        self.physics = BallPhysics(self.world, self.body)

    def draw(self):
        self.graphics.draw(self.world, self.body)

    def update(self, dt):
        self.physics.update(self, dt)

class BallGraphics(Graphics):
    def __init__(self):
        print("Ball Graphics intialized...")

    def draw(self, world, body):
        pygame.draw.rect(world.screen, (255,255,255), body)

class BallPhysics(Physics):
    def __init__(self, world, body):
        print("Ball Physics initialized...")
        self.world = world
        self.body = body

    def update(self, ball, dt):
        #movimment 
        self.body.x = self.body.x + self.world.ball.speedX * dt
        self.body.y = self.body.y + self.world.ball.speedY * dt

        #border collisions
        if self.body.bottom >= self.world.height:
            if self.world.ball.speedY >= 0:
                self.world.ball.speedY = self.world.ball.speedY * -1

        elif self.body.top <= 0:
            if self.world.ball.speedY <= 0:
                self.world.ball.speedY = self.world.ball.speedY * -1

        #collision with player
        if self.body.bottom >= self.world.player.body.top and self.world.ball.body.top <= self.world.player.body.bottom and self.world.ball.body.right >= self.world.player.body.left:
            if self.world.ball.speedX >= 0:
                delta = self.world.ball.body.centery - self.world.enemy.body.centery
                self.world.ball.speedY = delta * 0.008
                self.world.ball.speedX = self.world.ball.speedX * -1
                self.world.ball.speedX = self.world.ball.speedX - 0.01

        #collision with enemy
        if self.world.ball.body.bottom >= self.world.enemy.body.top and self.world.ball.body.top <= self.world.enemy.body.bottom and self.world.ball.body.left <= self.world.enemy.body.right:
            if self.world.ball.speedX <=0:
                delta = self.world.ball.body.centery - self.world.enemy.body.centery
                self.world.ball.speedY = delta * 0.005
                self.world.ball.speedX = self.world.ball.speedX * -1.000
                self.world.ball.speedX = self.world.ball.speedX - 0.01

        if self.world.enemy.body.bottom < self.world.ball.body.y:
            self.world.enemy.body.bottom += self.world.enemy.speed
        if self.world.enemy.body.top > self.world.ball.body.y:
            self.world.enemy.body.top -= self.world.enemy.speed

        if (self.world.ball.body.right >= self.world.width):
            self.world.enemy.score += 1
            self.reset_ball()
        elif self.world.ball.body.left <= 0:
            self.world.player.score += 1
            self.reset_ball()

    def reset_ball(self):
        self.body.center = (self.world.width / 2, self.world.height / 2)
        self.world.ball.speedX = random.choice((-0.5,0.5))


class World(Entity):
    def __init__(self):
        print ("World initialized...")
        self.size = self.width, self.height = 640, 480
        self.screen = pygame.display.set_mode(self.size)
        self.graphics = WorldGraphics(self)
        self.game_state = "START"
        pygame.display.set_caption('Pong')
        #initializing entities
        self.entities = []

        #player
        self.player = Player(self)
        self.entities.append(self.player)

        #enemy
        self.enemy = Enemy(self)
        self.entities.append(self.enemy)

        #Ball
        self.ball = Ball(self)
        self.entities.append(self.ball)

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
                if self.enemy.score > 2:
                    self.game_state = "LOST"
                    self.restart_game()
                elif self.player.score > 2:
                    self.game_state = "WIN"
                    self.restart_game()

            #draws the frames
            self.draw()

    def restart_game(self):
        self.ball.physics.reset_ball()
        self.ball.speedX = 0.5
        self.player.centery = self.height /2
        self.enemy.centery = self.height / 2
        self.enemy.score = 0
        self.player.score = 0 

    def draw(self):
        self.graphics.draw()

    def update(self, delta_time):
            if self.game_state == "GAME":
                for i in self.entities:
                    i.update(delta_time)

class WorldGraphics(Graphics):
    def __init__(self, world):
        print("world graphics initialized...")
        self.world = world
        self.gui = GUI(self.world)

    def draw(self):
        self.world.screen.fill(self.world.bg_color)
        print(self.world.game_state)
        if self.world.game_state == "GAME":
            self.game()
        elif self.world.game_state == "START":
            self.gui.gui_start()
        elif self.world.game_state == "WIN":
            self.gui.gui_win()
        elif self.world.game_state == "LOST":
            self.gui.gui_lost()

        pygame.display.flip()
    
    def game(self):
        self.gui.gui_game()
        for i in self.world.entities:
            i.draw()

class GUI:
    def __init__(self, world):
        print("GUI intialized...")
        self.world = world

        self.font1 = pygame.font.SysFont(None, 150)
        self.font2 = pygame.font.SysFont(None, 75)
        self.font3 = pygame.font.SysFont(None, 40)

        self.textStart = self.font2.render("Clique para começar", True, (255,255,255))
        self.textPerdeu = self.font2.render("perdeu", True, (255,255,255))
        self.textComecar = self.font3.render("Clique para começar", True, (255,255,255))
        self.textGanhou = self.font2.render("Ganhou", True, (255,255,255))

    def gui_game(self):
        #player score
        textScore = self.font1.render(str(self.world.player.score), True, (255,255,255))
        self.world.screen.blit(textScore, ((self.world.width/2) - 120, 20))

        #enemy score
        textScore = self.font1.render(str(self.world.enemy.score), True, (255,255,255))
        self.world.screen.blit(textScore, ((self.world.width/2) + 50, 20))
        
        #line
        pygame.draw.aaline(self.world.screen, (255, 255, 255), (self.world.width / 2, 0), (self.world.width / 2, self.world.height))

    def gui_start(self):
        self.world.screen.blit(self.textStart, ((self.world.width/2) - 250, 250))

    def gui_win(self):
        self.world.screen.blit(self.textGanhou, ((self.world.width/2) - 90, 250))
        self.world.screen.blit(self.textComecar, ((self.world.width/2) - 150, 310))
    
    def gui_lost(self):
        self.world.screen.blit(self.textPerdeu, ((self.world.width/2) - 90, 250))
        self.world.screen.blit(self.textComecar, ((self.world.width/2) - 150, 310))

class Inputs():
    def __init__(self, world):
        print("Inputs initialized...")
        self.world = world

    def input(self):
        for event in pygame.event.get():
            if self.world.game_state == "GAME":
                pass

            elif self.world.game_state == "START":
                if event.type == MOUSEBUTTONUP:
                    self.world.game_state = "GAME"

            elif self.world.game_state == "WIN" or "LOST":
                if event.type == MOUSEBUTTONUP:
                    self.world.game_state = "GAME"

            #closing the game
            if event.type == pygame.QUIT :
                sys.exit()

    def mouseY(self):
        mousex, mousey = pygame.mouse.get_pos()
        return mousey

class Input:
    def __init__(self):
        print("input initialized...")
    def mouseY(self):
        mousex, mousey = pygame.mouse.get_pos()
        return mousey

def main():
    pygame.init()
    print("Initialazing game...")
    World()


if __name__ == "__main__":
    main()