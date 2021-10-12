import pygame
import networkx as nx
from random import randint
from random import choice
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
sc = pygame.display.set_mode((W, H))
pygame.display.set_caption("Pac-Man")
pygame.display.set_icon(pygame.image.load("Images/Pac_man.bmp"))
ticksCounter = pygame.time.Clock()

STATUS = 1

bloc = pygame.image.load("Images/stena.png").convert_alpha()

bloc = pygame.transform.scale(bloc, (50, 50))
bloc_rect = bloc.get_rect()
def level_creator():
    level_matrix = []
    X ,Y = W//50, (H-100)//50
    for y in range (0,Y):
        row = []
        for x in range(0,X):
            if y == 0 or y == Y-1:
                row.append('#')
            elif x == 0 or x == X-1:
                row.append('#')
            else:
                row.append('*')
        level_matrix.append(row)
    p_x, p_y = randint(1,X-2), randint(1,6)
    level_matrix[p_y][p_x] = '0'
    x_g, y_g = randint(2, X-2), randint(6,Y-2)
    level_matrix[y_g][x_g] = '+'
    level_matrix[y_g][x_g - 1] = '#'
    level_matrix[y_g][x_g + 1] = '#'
    level_matrix[y_g+1][x_g+1] = '#'
    level_matrix[y_g+1][x_g-1] = "#"
    level_matrix[y_g+1][x_g] = "#"
    G = nx.empty_graph()
    for y in range(1,Y-1):
        for x in range(1,X-1):
            if level_matrix[y][x] == '*':
                if level_matrix[y][x-1] =='*':
                    G.add_edge(y*X+x, y*X+x-1)
                if level_matrix[y][x + 1] == '*':
                    G.add_edge(y * X + x, y * X + x + 1)
                if level_matrix[y-1][x] == '*':
                    G.add_edge(y * X + x, (y-1) * X + x)
                if level_matrix[y + 1][x] == '*':
                    G.add_edge(y * X + x, (y + 1) * X + x)
    start_x = randint(2,12)
    start_y = randint(2,8)
    visited = []
    visited.append([start_x, start_y])
    while len(visited) > 0:
        if len(visited) > 0:
            current = visited[-1]
        nodes_for_check = []
        available_nodes = []
        if level_matrix[current[1]][current[0]] == '*' or level_matrix[current[1]][current[0]] == '#':
            if level_matrix[current[1]][current[0] - 1] == '*':
                available_nodes.append([current[0] - 1, current[1]])
                nodes_for_check.append([current[0] - 1, current[1]])
            elif level_matrix[current[1]][current[0] - 1] == '&':
                nodes_for_check.append([current[0] - 1, current[1]])
            if level_matrix[current[1]][current[0] + 1] == '*':
                available_nodes.append([current[0] + 1, current[1]])
                nodes_for_check.append([current[0] + 1, current[1]])
            elif level_matrix[current[1]][current[0] + 1] == '&':
                nodes_for_check.append([current[0] + 1, current[1]])
            if level_matrix[current[1] + 1][current[0]] == '*':
                available_nodes.append([current[0], current[1] + 1])
                nodes_for_check.append([current[0], current[1] + 1])
            elif level_matrix[current[1] + 1][current[0]] == '&':
                nodes_for_check.append([current[0], current[1] + 1])
            if level_matrix[current[1] - 1][current[0]] == '*':
                available_nodes.append([current[0], current[1] - 1])
                nodes_for_check.append([current[0], current[1] - 1])
            elif level_matrix[current[1]-1][current[0]] == '&':
                nodes_for_check.append([current[0], current[1] - 1])
            if level_matrix[current[1]][current[0]] == '*':
                has_pass = True
                if len(nodes_for_check) > 2:
                    Cur_graph = nx.Graph(G)
                    if Cur_graph.has_node(current[1]*X + current[0]):
                        Cur_graph.remove_node(current[1]*X+current[0])
                    for e1 in nodes_for_check:
                        for e2 in nodes_for_check:
                            if Cur_graph.has_node(e1[1] * X + e1[0]) and Cur_graph.has_node(e2[1]*X + e2[0]):
                                 if nx.has_path(Cur_graph, e1[1]*X + e1[0],e2[1]*X + e2[0]) == False:
                                    has_pass = False
                                    break
                else:
                    has_pass = False

                if has_pass:
                    if G.has_node(current[1] * X + current[0]):
                        G.remove_node(current[1] * X + current[0])
                    level_matrix[current[1]][current[0]] = '#'
                    if len(available_nodes)>0:
                        visited.append(choice(available_nodes))
                else:
                    if level_matrix[current[1]][current[0]] == '*':
                        level_matrix[current[1]][current[0]] = '&'
                    if len(visited) > 0:
                        visited.pop()
            else:
                if len(available_nodes) > 0:
                    visited.append(choice(available_nodes))
                elif  len(visited) > 0:
                 visited.pop()
        else:
            if len(visited) > 0:
                 visited.pop()

    return level_matrix

level1 = level_creator()

hero = PacMan(level1, "Images/MainHeroPac.png", sc)
ghost = Ghost(level1, "Images/ghost.png", sc)
level = Level(sc, bloc, bloc_rect, level1)

f = pygame.font.SysFont('calibri', 50)
f1 = pygame.font.SysFont('calibri', 100)
while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
            pygame.quit()
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_z:
                if ghost.algotitm == 1:
                    ghost.algotitm = 0
                    print("DFS")
                elif ghost.algotitm ==0:
                    ghost.algotitm = 1
                    print("BFS")
    if score ==65:
        STATUS =3

    if STATUS == 1:
        sc_text = f.render('SCORE:' + str(score), 1, WHITE, BLACK)
        t_rect = sc_text.get_rect(topleft = (20,520))
        STATUS = hero.dethTrigger(ghost.rect)

        sc.fill(BLACK)
        ghost.moveGhost(hero.rect.center[0], hero.rect.center[1])
        ghost.draw_pass()
        level.draw_level()
        points_rects = level.draw_points()
        score = hero.countPoints(level1, score, points_rects)
        ghost.draw_pass()
        hero.movePacmanAI()
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



