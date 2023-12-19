import pygame.time

from PPlay.window import *
from PPlay.sprite import *

class Game:
    def __init__(self):
        # Window commands
        self.window = Window(1920,1080)
        self.window.set_title("Jujutsu Pong")
        self.background = Sprite('background.png')
        self.key = self.window.get_keyboard()
        self.mouse = self.window.get_mouse()
        self.clock = pygame.time.Clock()

        # Multiplayer or Ia
        self.multiplayer = False

        # Pontos
        self.left = 0
        self.right = 0

        # Ball commands
        self.ball = Sprite("ballJ.png")
        self.ball.x = self.window.width/2 - self.ball.width/2
        self.ball.y = self.window.height/2 - self.ball.height/2

        # Pads commands
        self.pad1 = Sprite("padG.png")
        self.pad2 = Sprite("padS.png")
        self.pad1.x = self.window.width/90
        self.pad1.y = self.window.height/2 - self.pad1.height/2
        self.pad2.x = self.window.width - self.window.width/90 - self.pad2.width
        self.pad2.y = self.window.height/2 - self.pad2.height/2

        # Speed commands
        self.pad_p = 600
        self.pad_ia = 350
        self.bx = 500
        self.by = 500

    def pad1(self):
        if self.key.key_pressed("w") and self.pad1.y > 0:
            self.pad1.y -= self.pad_p * self.window.delta_time()
        if self.key.key_pressed("s") and self.pad1.y < self.window.height - self.pad1.height:
            self.pad1.y += self.pad_p * self.window.delta_time()

    def pad2(self):
        if self.key.key_pressed("UP") and self.pad2.y > 0:
            self.pad2.y -= 600 * self.window.delta_time()
        if self.key.key_pressed("DOWN") and self.pad2.y < self.window.height - self.pad1.height:
            self.pad2.y += 600 * self.window.delta_time()

    def ia(self):
        if self.ball.y > self.pad2.y and self.ball.x >= self.window.width / 2 and self.pad2.y <= self.window.height - self.pad2.height:
            self.pad2.y += self.pad_ia * self.window.delta_time()
        if self.ball.y < self.pad2.y and self.ball.x >= self.window.width / 2 and self.pad2.y >= 0:
            self.pad2.y -= self.pad_ia * self.window.delta_time()
    def att_ball(self):
        self.ball.x += self.bx * self.window.delta_time()
        self.ball.y += self.by * self.window.delta_time()

    def check_collision(self):
        if self.pad1.collided(self.ball):
            self.bx *= -1
            self.ball.x = self.pad1.x + self.ball.width
        if self.pad2.collided(self.ball):
            self.bx *= -1
            self.ball.x = self.pad2.x - self.ball.width
        if self.ball.y + self.ball.height >= self.window.height:
            self.ball.y = self.window.height - self.ball.height
            self.by *= -1
        if self.ball.y <= 0:
            self.ball.y = 0
            self.by *= -1

    def scores(self):
        if self.ball.x + self.ball.width >= self.window.width:
            self.left += 1
            self.ball.x = self.window.width / 2 - self.ball.width / 2
            self.ball.y = self.window.height / 2 - self.ball.height / 2
            self.bx *= -1
        if self.ball.x <= 0:
            self.right += 1
            self.ball.x = self.window.width / 2 - self.ball.width / 2
            self.ball.y = self.window.height / 2 - self.ball.height / 2
            self.bx *= -1

    def menu(self):
        self.img_menu = Sprite('menu.png')
        self.img_menu_solo = Sprite('menu_solo.png')
        self.img_menu_sair = Sprite('menu_sair.png')
        self.img_menu_multi = Sprite('menu_multi.png')
        while True:
            x, y = pygame.mouse.get_pos()
            self.img_menu.draw()
            if x>= self.window.width*0.45 and x<= self.window.width*0.55 and y>= self.window.height*0.5 and y<=self.window.height*0.6:
                self.img_menu_solo.draw()
                if self.mouse.is_button_pressed(1):
                    self.multiplayer = False
                    Game.run(self, self.multiplayer)
            if x>= self.window.width*0.36 and x<= self.window.width*0.64 and y>= self.window.height*0.65 and y<=self.window.height*0.75:
                self.img_menu_multi.draw()
                if self.mouse.is_button_pressed(1):
                    self.multiplayer = True
                    Game.run(self,self.multiplayer)
            if x>= self.window.width*0.45 and x<= self.window.width*0.55 and y>= self.window.height*0.8 and y<=self.window.height*0.88:
                self.img_menu_sair.draw()
                if self.mouse.is_button_pressed(1):
                    break
            self.window.update()

    def initial_position(self):
        self.pad1.x = self.window.width / 90
        self.pad1.y = self.window.height / 2 - self.pad1.height / 2
        self.pad2.x = self.window.width - self.window.width / 90 - self.pad2.width
        self.pad2.y = self.window.height / 2 - self.pad2.height / 2
        self.ball.x = self.window.width / 2 - self.ball.width / 2
        self.ball.y = self.window.height / 2 - self.ball.height / 2

    def run(self, multiplayer):
        Game.initial_position(self)
        self.left = 0
        self.right = 0
        # Game Looping
        while True:
            self.background.draw()
            Game.pad1(self)
            if multiplayer:
                Game.pad2(self)
            else:
                Game.ia(self)
            Game.scores(self)
            Game.att_ball(self)
            Game.check_collision(self)
            if self.key.key_pressed('esc'):
                break
            self.window.draw_text(f"{self.left}", self.window.width/90, 10, 50, (255,255,0))
            self.window.draw_text(f"{self.right}", self.window.width - self.window.width/90 - 30, 10, 50, (255, 255, 0))
            self.ball.draw()
            self.pad1.draw()
            self.pad2.draw()
            self.clock.tick()
            self.window.update()

Game().menu()