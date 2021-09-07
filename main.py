import pygame
import random
from pacman import PacMan
from levelvis import Level
from ghost import Ghost
running = True
FPS = 30
W, H = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
score = 0
pygame.init()
print(pygame.font.get_fonts())
sc = pygame.display.set_mode((W, H))
pygame.display.set_caption("Pac-Man")
pygame.display.set_icon(pygame.image.load("Images/Pac_man.bmp"))
ticksCounter = pygame.time.Clock()

STATUS = 1

bloc = pygame.image.load("Images/stena.png").convert_alpha()

bloc = pygame.transform.scale(bloc, (50, 50))
bloc_rect = bloc.get_rect()
level1 = [['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#'],
          ['#', '*', '*', '*', '#', '0', '*', '*', '*', '*', '*', '*', '*', '*', '*', '#'],
          ['#', '*', '#', '*', '#', '*', '#', '#', '#', '#', '*', '#', '#', '#', '*', '#'],
          ['#', '*', '#', '*', '#', '*', '*', '*', '*', '#', '*', '*', '*', '*', '*', '#'],
          ['#', '*', '#', '*', '*', '*', '#', '#', '*', '*', '#', '*', '#', '*', '#', '#'],
          ['#', '*', '#', '#', '#', '*', '#', '#', '#', '*', '#', '*', '#', '*', '#', '#'],
          ['#', '*', '*', '*', '#', '*', '*', '*', '#', '*', '#', '*', '#', '', '#', '#'],
          ['#', '*', '#', '*', '#', '#', '#', '*', '#', '*', '#', '*', '#', '+', '#', '#'],
          ['#', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '#', '#', '#', '#'],
          ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#']
          ]
hero = PacMan(level1, "Images/MainHeroPac.png")
ghost = Ghost(level1, "Images/ghost.png")
level = Level(sc, bloc, bloc_rect, level1)

f = pygame.font.SysFont('calibri', 50)
f1 = pygame.font.SysFont('calibri', 100)
while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
            pygame.quit()
    if score ==65:
        STATUS =3

    if STATUS == 1:
        sc_text = f.render('SCORE:' + str(score), 1, WHITE, BLACK)
        t_rect = sc_text.get_rect(topleft = (20,520))
        STATUS = hero.dethTrigger(ghost.rect)
        hero.MovePac()
        ghost.moveGhost()
        sc.fill(BLACK)
        level.draw_level()
        points_rects = level.draw_points()
        score = hero.countPoints(level1,score,points_rects)
        sc.blit(ghost.cur_img, ghost.rect)
        sc.blit(hero.cur_img, hero.rect)
        sc.blit(sc_text, t_rect)
    if STATUS == 2:
        sc.fill(BLACK)
        sc_text= f1.render('YOU LOSE!', 1, WHITE, BLACK)
        t_rect = sc_text.get_rect(center=(W/2, H/2))
        sc.blit(sc_text, t_rect)
    if STATUS == 3:
        sc.fill(BLACK)
        sc_text = f1.render('YOU WIN!', 1, WHITE, BLACK)
        t_rect = sc_text.get_rect(center=(W / 2, H / 2))
        sc.blit(sc_text, t_rect)
    pygame.display.update()
    ticksCounter.tick(FPS)  # set FPS



