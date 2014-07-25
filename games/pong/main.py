import pygame
import sys
from pygame.locals import *
import numpy


class GameText(object):
    def __init__(self, font_obj, pos):
        self.font = font_obj
        self.text = ""
        self.visible = True
        self.color = BLACK
        self.position = pos
        self.id = len(game_text)
        game_text.append(self)

    def create_render(self):
        print self.text
        return self.font.render(self.text, True, self.color)


class GameObject(object):
    def __init__(self, pos):
        self.position = pos
        self.speed = [0, 0]
        self.rect = Rect((0, 0), (0, 0))
        game_objects.append(self)

    def move(self):
        self.position = update_pos(self.position, self.speed)
        self.rect = Rect(self.position, self.rect.size)
        if self.rect.colliderect(bound_area_top):
            print("Debug")

    def update_speed(self, new_speed):
        self.speed[0] = new_speed[0]
        self.speed[1] = new_speed[1]

    def collides(self, obj2):
        return abs(self.position[0] - obj2.position[0]) < 50 or abs(self.position[1] - obj2.position[1]) < 100


class Player(GameObject):
    def __init__(self, elem, pos):
        super(Player, self).__init__(pos)
        self.elem = elem
        self.speed = [0, 0]
        self.rect = elem.get_rect()

    def move(self):
        newpos = update_pos(self.position, self.speed)
        newrect = Rect(newpos, self.rect.size)
        if newrect.colliderect(bound_area_top):
            newpos[1] = bound_area_top.bottom
        if newrect.colliderect(bound_area_bottom):
            newpos[1] = bound_area_bottom.top - newrect.height
        self.position = newpos
        self.rect = Rect(self.position, self.rect.size)


class Ball(GameObject):
    def __init__(self, elem, pos):
        super(Ball, self).__init__(pos)
        self.elem = elem
        self.speed = 100 * numpy.random.random(2) - 45
        #self.speed = [TILE_SIZE*2, TILE_SIZE*1]
        self.rect = elem.get_rect()
        self.maxspeed = [TILE_SIZE*15, TILE_SIZE*15]

    def move(self):
        global score_text
        newpos = update_pos(self.position, self.speed)
        newrect = Rect(newpos, self.rect.size)
        if newrect.colliderect(bound_area_left) or newrect.colliderect(bound_area_right):
            if newrect.colliderect(bound_area_left):
                score[1] += 1
            elif newrect.colliderect(bound_area_right):
                score[0] += 1
            score_text.text = str(score[0]) + " - " + str(score[1])
            clock.tick(10)
            self.position = [TILE_SIZE*15, TILE_SIZE*20]
            self.speed = [TILE_SIZE*2, TILE_SIZE*2]
        else:
            if newrect.colliderect(bound_area_top) or newrect.colliderect(bound_area_bottom):
                self.speed = [self.speed[0], -(self.speed[1])]
            if newrect.colliderect(player1.rect):
                if newrect.top > player1.rect.bottom or newrect.bottom < player1.rect.top:
                    self.speed = [self.speed[0], -self.speed[1]]
                else:
                    #self.speed = [-(self.speed[0]), self.speed[1]]
                    self.speed = [-(self.speed[0]), self.speed[1] + 0.25*player1.speed[1]]
            if newrect.colliderect(player2.rect):
                if newrect.top > player2.rect.bottom or newrect.bottom < player2.rect.top:
                    self.speed = [self.speed[0], -self.speed[1]]
                else:
                    #self.speed = [-(self.speed[0]), self.speed[1]]
                    self.speed = [-(self.speed[0]), self.speed[1] + 0.25*player2.speed[1]]
            self.position = update_pos(self.position, self.speed)
        self.speed = [min(self.speed[0], self.maxspeed[0]), min(self.speed[1], self.maxspeed[1])]
        self.rect = Rect(tuple(self.position), self.rect.size)

    def bounce(self):
        if self.collides(player1) or self.collides(player2):
            self.speed = [-self.speed[0], self.speed[1]]
        print("Bounce!")


class Window:
    def __init__(self, w, h):
        self.width = w
        self.height = h
        self.rect = (self.width, self.height)

    def change_size(self, new_size):
        self.width = new_size[0]
        self.height = new_size[1]
        self.rect = (self.width, self.height)


def update_pos(original, speed):
    result = [0, 0]
    result[0] = original[0] + speed[0]
    result[1] = original[1] + speed[1]
    return result


def draw_background():
    pygame.Surface.fill(screen, WHITE)
    if drawGrid:
        for f in range(1, 720/TILE_SIZE):
            pygame.draw.line(screen, GRAY, [0, f*TILE_SIZE], [1280, f*TILE_SIZE])
        for c in range(1, 1280/TILE_SIZE):
            pygame.draw.line(screen, GRAY, [c*TILE_SIZE, 0], [c*TILE_SIZE, 720])
    for bound in bounds.values():
        pygame.draw.rect(screen, BLACK, bound)


def draw_game_objects():
    for obj in game_objects:
        screen.blit(obj.elem, obj.position)
        if drawRects:
            #print obj.elem.get_rect()
            pygame.draw.rect(screen, BLACK, Rect(obj.position, obj.rect.size), 1)


def draw_player(player):
    screen.blit(player.elem, player.position)


def draw_text():
    for obj in game_text:
        if obj.visible:
            screen.blit(obj.create_render(), obj.position)

pygame.init()
game_objects = []
game_text = []
drawGrid = False
drawRects = True
window = Window(1280, 720)

screen = pygame.display.set_mode(window.rect)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (150, 150, 150)

K_P1_UP = K_w
K_P1_DOWN = K_s

K_P2_UP = K_i
K_P2_DOWN = K_k

TILE_SIZE = 8

clock = pygame.time.Clock()
FPS = 24
score = [0, 0]

background = pygame.image.load('imgs/background.png').convert_alpha()
background = pygame.transform.scale(background, window.rect)

paddle_img = pygame.image.load('imgs/paddle2x4.png').convert()
paddle_img = pygame.transform.scale(paddle_img, (TILE_SIZE*5, TILE_SIZE*20))

ball_img = pygame.image.load('imgs/awesome.png').convert_alpha()
ball_img = pygame.transform.scale(ball_img, (TILE_SIZE*5, TILE_SIZE*5))

font_score = pygame.font.Font(pygame.font.match_font(pygame.font.get_fonts()[0]), 36)

score_text = GameText(font_score, [1280/2, TILE_SIZE*12])
score_text.text = "0 - 0"

player1 = Player(paddle_img, [TILE_SIZE*4, TILE_SIZE*16])
player2 = Player(paddle_img, [TILE_SIZE*150, TILE_SIZE*16])
ball = Ball(ball_img, [TILE_SIZE*10, TILE_SIZE*15])

bound_area_left = Rect((0, 0), (TILE_SIZE*2, 720))
bound_area_right = Rect((1280 - TILE_SIZE*2, TILE_SIZE*2), (1280 - TILE_SIZE*1, 720 - TILE_SIZE*1))
bound_area_top = Rect((0, 0), (1280, TILE_SIZE*2))
bound_area_bottom = Rect((TILE_SIZE*2, 720-TILE_SIZE*2), (1280 - TILE_SIZE*2, 720 - TILE_SIZE*1))

bounds = dict(left=bound_area_left, right=bound_area_right, top=bound_area_top, bottom=bound_area_bottom)


def main():
    global drawGrid, drawRects, FPS
    esta_pausado = False
    draw_background()
    draw_game_objects()
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and event.key == K_SPACE:
                esta_pausado = not esta_pausado
            else:
                if not esta_pausado:
                    if event.type == KEYDOWN:
                        if event.key == K_P2_UP:
                            player2.update_speed([0, -TILE_SIZE*8])
                        if event.key == K_P2_DOWN:
                            player2.update_speed([0, TILE_SIZE*8])
                    if event.type == KEYUP:
                        if event.key == K_P2_UP:
                            player2.update_speed([0, 0])
                        if event.key == K_P2_DOWN:
                            player2.update_speed([0, 0])
        if not esta_pausado:
            pressed = pygame.key.get_pressed()
            if pressed[K_P1_UP]:
                player1.update_speed([0, -TILE_SIZE*8])
            elif pressed[K_P1_DOWN]:
                player1.update_speed([0, TILE_SIZE*8])
            else:
                player1.update_speed([0, 0])
            if pressed[K_P2_UP]:
                player2.update_speed([0, -TILE_SIZE*5])
            elif pressed[K_P2_DOWN]:
                player2.update_speed([0, TILE_SIZE*5])
            else:
                player2.update_speed([0, 0])
            if pressed[K_g]:
                drawGrid = True
                drawRects = True
            if pressed[K_f]:
                drawGrid = False
                drawRects = False
            if pressed[K_o]:
                FPS = 5
            if pressed[K_p]:
                FPS = 24
            player1.move()
            player2.move()
            ball.move()
        draw_background()
        draw_game_objects()
        draw_text()
        pygame.display.update()
        clock.tick(FPS)

if __name__ == "__main__":
    main()