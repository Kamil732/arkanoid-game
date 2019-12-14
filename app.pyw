import pygame as pg
from math import pi, cos, sin

class Button(object):
    def __init__(self, x, y, width, height, button_color, text, text_color, font, font_size):
        self.x = x
        self.y = y
        self.stayX = x
        self.width = width
        self.height = height
        self.button_color = button_color
        self.text = text
        self.text_color = text_color
        self.font = font
        self.font_size = font_size

    def draw(self, surface, outline=False, outline_color=(0,0,0), outline_size=0):
        if outline:
            pg.draw.rect(surface, (outline_color), (self.x - outline_size, self.y - outline_size, self.width + outline_size*2, self.height + outline_size*2))

        pg.draw.rect(surface, (self.button_color), (self.x, self.y, self.width, self.height))
        font1 = pg.font.Font(self.font, self.font_size)
        text1 = font1.render(self.text, 1, (self.text_color))
        surface.blit(text1, (self.x + self.width//2 - text1.get_width()//2, self.y + self.height//2 - text1.get_height()//2))

    def isHover(self):
        pos = pg.mouse.get_pos()
        if pos[0] >= self.x and pos[0] <= self.x + self.width and pos[1] >= self.y and pos[1] <= self.y + self.height:
            return True
        return False

class Player(object):
    def __init__(self, x, y,  width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.lives = 3

    def draw(self, surface, outline=False, outline_color=(0,0,0), outline_size=0):
        if outline: # if outline == True, then draw outline
            pg.draw.rect(surface, (outline_color), (self.x - outline_size, self.y - outline_size, self.width + outline_size*2, self.height + outline_size*2))

        pg.draw.rect(surface, (self.color), (self.x, self.y, self.width, self.height)) # Draw player

    def move(self, win_width):
        keys = pg.key.get_pressed()
        if(keys[pg.K_LEFT] and self.x >= 0): self.x -= 4
        if(keys[pg.K_RIGHT] and self.x <= win_width - self.width): self.x += 4

class Brick(Player):
    def isCollision(self, ball): # Check the collsion beetwen ball and brick
        if ball.y - ball.radius <= self.y + self.height and ball.y + ball.radius >= self.y and ball.x - ball.radius < self.x + self.width and ball.x + ball.radius > self.x:
            return True
        return False

class Ball(object):
    def __init__(self, x, y, radius, color, speed):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.speed = speed
        self.dirX = speed *1
        self.dirY = speed *-1
        self.visibilty = True

    def draw(self, surface, outline=False, outline_color=(0,0,0), outline_size=0):
        if self.visibilty:
            if outline:
                pg.draw.circle(surface, (outline_color), (int(self.x), int(self.y)), self.radius + outline_size)

            pg.draw.circle(surface, (self.color), (int(self.x), int(self.y)), self.radius)

    def move(self, game_width, player):
        self.x += self.dirX # Ball speed X
        self.y += self.dirY # ball speed Y
        if (self.x >= game_width or self.x <= 0): self.x = game_width//2
        # Collsions
        if (self.x <= self.radius or self.x >= game_width - self.radius): self.dirX = -self.dirX # Bouncing ball when it hit left or right wall
        if (self.y <= self.radius): self.dirY = -self.dirY # Bouncing ball when it hit the celling
        if self.y >= player.y - self.radius and self.y <= player.y + player.height and self.x >= player.x - self.radius and self.x <= player.x + self.radius + player.width: # Bouncing ball when it hit the player
            collidePoint = self.x - (player.x + player.width/2)
            collidePoint = collidePoint / (player.width/2)

            angle = collidePoint * pi/3
            self.dirX = self.speed * sin(angle)
            self.dirY = - self.speed * cos(angle)

class Game:
    def __init__(self, width, height, player, ball, restartBtn):
        print('\n======================================================================\n============================= START GAME =============================\n======================================================================\n')
        pg.init()
        self.width = width
        self.height = height
        self.win = pg.display.set_mode((width, height))
        self.player = player
        self.ball = ball
        self.bricks = [Brick(10, 60, 60, 15, (0,0,255)), Brick(20 + 60, 60, 60, 15, (0,0,255)), Brick(30 + 120, 60, 60, 15, (0,0,255)), Brick(40 + 180, 60, 60, 15, (0,0,255)), Brick(50 + 240, 60, 60, 15, (0,0,255))]
        self.clock = pg.time.Clock()
        self.lvl = 1
        self.score = 0
        self.restartBtn = restartBtn
        self.restartBtn.x += 1000

    def __del__(self):
        print('\n======================================================================\n============================== END GAME ==============================\n======================================================================\n')

    def end_game(self):
        self.ball.visibilty = False
        self.player.y = 2000
        self.bricks = []
        self.restartBtn.x = self.restartBtn.stayX
        self.restartBtn.draw(self.win, True, (255,255,255), 2)

    def draw_texts(self, x, y, text, text_color, font, font_size):
        font1 = pg.font.Font(font, font_size)
        text1 = font1.render(text, 1, (text_color))
        self.win.blit(text1, (x, y))

    def restart(self):
        self.score = 0
        self.lvl = 1
        self.player.lives = 3
        self.player.x = self.width//2 - self.player.width//2
        self.player.y = self.height - 45
        self.ball.visibilty = True
        self.ball.x = self.width//2
        self.ball.y = self.height//2
        self.ball.speed = 4
        self.ball.dirY *= -1
        self.bricks = [Brick(10, 60, 60, 15, (0,0,255)), Brick(20 + 60, 60, 60, 15, (0,0,255)), Brick(30 + 120, 60, 60, 15, (0,0,255)), Brick(40 + 180, 60, 60, 15, (0,0,255)), Brick(50 + 240, 60, 60, 15, (0,0,255))]

    def checkFloorColision(self):
        if self.ball.y >= self.height + self.ball.radius*2: # minus one live when ball hit the floor and reset the ball
            if self.player.lives <= 1:
                self.player.lives = 0
                self.draw_texts(self.width//2 - 305//2, self.height//2 - 61//2, 'GAME OVER', (0,255,0), 'font.ttf', 50) # End game when lives == 0
                self.draw_texts(self.width//2 - 140//2, self.height//2 + 25, 'YOU LOST', (255,0,0), 'font.ttf', 28)
                self.end_game()
            else:
                self.ball.dirY = -self.ball.dirY
                self.player.lives -= 1
                self.ball.x = self.width//2
                self.ball.y = self.height//2

        if self.lvl == 5 and self.bricks == []: # Check win
            self.draw_texts(self.width//2 - 305//2, self.height//2 - 61//2, 'GAME OVER', (0,255,0), 'font.ttf', 50)
            self.draw_texts(self.width//2 - 123//2, self.height//2 + 25, 'YOU WON', (150,255,150), 'font.ttf', 28)
            self.end_game()

    def redrawWidnow(self):
        self.win.fill((20,20,20)) # Draw background
        self.draw_texts(8, 6, 'SCORE: ' + str(self.score), (255,255,255), 'font.ttf', 18) # Draw score textt
        self.draw_texts(300, 6, 'LVL: ' + str(self.lvl), (255,255,255), 'font.ttf', 18) # Draw lvl text
        self.draw_texts(8, self.height - 30, 'LIVES: ' + str(self.player.lives), (255,255,255), 'font.ttf', 18) # draw lives text
        self.player.draw(self.win, True, (100,100,255), 1) # Draw player
        self.ball.draw(self.win, True, (100,155,155), 1) # Draw ball
        self.ball.move(self.width, self.player) # Ball move
        self.player.move(self.width)
        self.checkFloorColision()
        for brick in self.bricks: # Draw bricks
            brick.draw(self.win, True, (255,255,255), 1)
        pg.display.update() # Show everything on the screen

    def run(self):
        while True:
            for ev in pg.event.get():
                if ev.type == pg.QUIT:
                    pg.quit()
                    quit()

                if ev.type == pg.MOUSEMOTION:
                    if self.restartBtn.isHover():
                        self.restartBtn.button_color = (170, 120, 15)
                    else:
                        self.restartBtn.button_color = (153, 102, 0)
                if ev.type == pg.MOUSEBUTTONDOWN:
                    if self.restartBtn.isHover():
                        self.restart()
                        self.restartBtn.x += 1000

            for brick in self.bricks:
                if brick.isCollision(self.ball):
                    self.bricks.pop(self.bricks.index(brick))
                    self.ball.dirY = -self.ball.dirY
                    self.score += 5

                    if self.bricks == []:
                        self.lvl += 1
                        self.ball.x = self.width//2
                        self.ball.y = self.height//2
                        self.ball.speed += 1
                        self.ball.dirY = -3

                        if self.lvl == 2:
                            self.bricks = [Brick(10, 60, 60, 15, (0,0,255)), Brick(20 + 60, 60, 60, 15, (0,0,255)), Brick(30 + 120, 60, 60, 15, (0,0,255)), Brick(40 + 180, 60, 60, 15, (0,0,255)), Brick(50 + 240, 60, 60, 15, (0,0,255)), Brick(10, 60 + 25, 60, 15, (0,0,255)), Brick(20 + 60, 60 + 25, 60, 15, (0,0,255)), Brick(30 + 120, 60 + 25, 60, 15, (0,0,255)), Brick(40 + 180, 60 + 25, 60, 15, (0,0,255)), Brick(50 + 240, 60 + 25, 60, 15, (0,0,255))]
                        if self.lvl == 3:
                            self.bricks = [Brick(10, 60, 60, 15, (0,0,255)), Brick(20 + 60, 60, 60, 15, (0,0,255)), Brick(30 + 120, 60, 60, 15, (0,0,255)), Brick(40 + 180, 60, 60, 15, (0,0,255)), Brick(50 + 240, 60, 60, 15, (0,0,255)), Brick(10, 60 + 25, 60, 15, (0,0,255)), Brick(20 + 60, 60 + 25, 60, 15, (0,0,255)), Brick(30 + 120, 60 + 25, 60, 15, (0,0,255)), Brick(40 + 180, 60 + 25, 60, 15, (0,0,255)), Brick(50 + 240, 60 + 25, 60, 15, (0,0,255)), Brick(10, 60 + 50, 60, 15, (0,0,255)), Brick(20 + 60, 60 + 50, 60, 15, (0,0,255)), Brick(30 + 120, 60 + 50, 60, 15, (0,0,255)), Brick(40 + 180, 60 + 50, 60, 15, (0,0,255)), Brick(50 + 240, 60 + 50, 60, 15, (0,0,255))]
                        if self.lvl == 4:
                            self.bricks = [Brick(10, 60, 60, 15, (0,0,255)), Brick(20 + 60, 60, 60, 15, (0,0,255)), Brick(30 + 120, 60, 60, 15, (0,0,255)), Brick(40 + 180, 60, 60, 15, (0,0,255)), Brick(50 + 240, 60, 60, 15, (0,0,255)), Brick(10, 60 + 25, 60, 15, (0,0,255)), Brick(20 + 60, 60 + 25, 60, 15, (0,0,255)), Brick(30 + 120, 60 + 25, 60, 15, (0,0,255)), Brick(40 + 180, 60 + 25, 60, 15, (0,0,255)), Brick(50 + 240, 60 + 25, 60, 15, (0,0,255)), Brick(10, 60 + 50, 60, 15, (0,0,255)), Brick(20 + 60, 60 + 50, 60, 15, (0,0,255)), Brick(30 + 120, 60 + 50, 60, 15, (0,0,255)), Brick(40 + 180, 60 + 50, 60, 15, (0,0,255)), Brick(50 + 240, 60 + 50, 60, 15, (0,0,255)), Brick(10, 60 + 75, 60, 15, (0,0,255)), Brick(20 + 60, 60 + 75, 60, 15, (0,0,255)), Brick(30 + 120, 60 + 75, 60, 15, (0,0,255)), Brick(40 + 180, 60 + 75, 60, 15, (0,0,255)), Brick(50 + 240, 60 + 75, 60, 15, (0,0,255))]

            self.clock.tick(55)
            self.redrawWidnow()

if __name__ == '__main__':
    arkanoid = Game(360, 500, Player(360/2 - 75/2, 500 - 45, 75, 12, (0,255,0)), Ball(360//2, 500//2, 8, (255,30,30), 4), Button(360//2 - 170//2, 500//2 + 360//3 - 40, 170, 55, (153, 102, 0), 'RESTART GAME', (0,0,0), 'font.ttf', 20))
    pg.display.set_caption('Arkanoid Game')
    run = True
    while run:
        for ev in pg.event.get():
            arkanoid.win.fill((100,100,100))
            arkanoid.draw_texts(arkanoid.width//2 - 325//2, arkanoid.height//2 - 26//2, 'PRESS ANY KEY TO PLAY', (255,255,255), 'font.ttf', 26)
            pg.display.update()
            if ev.type == pg.QUIT:
                run = False
                pg.quit()
                quit()

            if ev.type == pg.KEYDOWN:
                run = False
                arkanoid.run()