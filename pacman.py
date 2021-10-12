import  pygame
import random
import math
class PacMan(pygame.sprite.Sprite):
    def __init__(self, matrix, filename, sc):
        pygame.sprite.Sprite.__init__(self)
        self._image = pygame.image.load(filename).convert_alpha()
        self._image = pygame.transform.scale(self._image, (45, 45))
        self.rect = self._image.get_rect()
        self._sc = sc
        self._right_image = self._image
        self._left_image = pygame.transform.flip(self._image, 1, 0)
        self._up_image = pygame.transform.rotate(self._image, 90)
        self._down_image = pygame.transform.rotate(self._image, -90)
        self._speed = 5
        self.cur_img = self._right_image
        self._matrix = matrix
        for x in range(0,15):
            for y in range(0,9):
              if matrix[y][x] == '0':
                self.rect = self.rect.move(x*50,y*50)
                break
        self._movematrix = self._matrix
        self._isMove = False
        self._curWay = None
        self._hasPass = False
        self._curPass = None
        
    def MovePac(self):
        coordX , coordY = self.rect.x, self.rect.y
        bt = pygame.key.get_pressed()
        if bt[pygame.K_LEFT]:
            self.rect.x -= self._speed
            if self._movematrix[self.rect.y // 50][(self.rect.x - self._speed)//50] == '#' or self._movematrix[self.rect.bottomright[1]//50][(self.rect.x - self._speed)//50] == '#':
               self.rect.x = coordX
               self.rect.y = coordY
            else:
                self.cur_img = self._left_image

        elif bt[pygame.K_RIGHT]:
            self.rect.x += self._speed
            if self._movematrix[self.rect.y//50][(self.rect.topright[0])//50] == '#' or self._movematrix[self.rect.bottomright[1]//50][(self.rect.bottomright[0])//50] == '#':
                self.rect.x = coordX
                self.rect.y = coordY
            else:
                self.cur_img = self._right_image

        elif bt[pygame.K_UP]:
            self.rect.y -= self._speed
            if self._movematrix[(self.rect.y - self._speed)//50][self.rect.x//50] == '#' or self._movematrix[(self.rect.y- self._speed)//50][self.rect.topright[0]//50]=='#':
                self.rect.x = coordX
                self.rect.y = coordY
            else:
                self.cur_img = self._up_image
        elif bt[pygame.K_DOWN]:
            self.rect.y += self._speed
            if self._movematrix[(self.rect.bottomleft[1] + self._speed)//50][self.rect.x//50] == '#' or self._movematrix[(self.rect.bottomright[1] + self._speed)//50][self.rect.bottomright[0]//50] == '#':
                self.rect.x = coordX
                self.rect.y = coordY
            else:
                self.cur_img = self._down_image
    def countPoints(self, matrix, score, point_rects):
        for p in point_rects:
            if self.rect.collidepoint(p.center):
                score += 1
                matrix[p.y//50][p.x//50] = ''
        return score
    def dethTrigger(self, ghost_rect):
        if self.rect.collidepoint(ghost_rect.center):
            self.kill()
            return 2
        else:
            return 1

    def _moveTop(self):
        self.rect.y -= self._speed
        self.cur_img = self._up_image
    def _moveBottom(self):
        self.rect.y += self._speed
        self.cur_img = self._down_image
    def _moveLeft(self):
        self.rect.x -= self._speed
        self.cur_img = self._left_image

    def _moveRight(self):
        self.rect.x += self._speed
        self.cur_img = self._right_image
    def _findWays(self):
        availableWays = []
        #left
        if self._matrix[self.rect.y//50][(self.rect.x-5)//50] != '#' and self._matrix[(self.rect.bottomleft[1])//50][(self.rect.x-5)//50] != '#':
            availableWays.append([self._moveLeft,'LEFT'])
        if self._matrix[self.rect.y//50][(self.rect.topright[0]+5)//50] != '#' and self._matrix[(self.rect.bottomright[1])//50][(self.rect.bottomright[0]+5)//50] != '#':
            availableWays.append([self._moveRight,'RIGHT'])
        if self._matrix[(self.rect.y - 5)//50][self.rect.x//50]!= '#' and self._matrix[(self.rect.y-5)//50][(self.rect.topright[0])//50]!='#':
            availableWays.append([self._moveTop,'TOP'])
        if self._matrix[(self.rect.bottomleft[1]+5)//50][self.rect.x // 50] != '#' and self._matrix[(self.rect.bottomright[1]+5)//50][self.rect.bottomright[0] // 50] != '#':
            availableWays.append([self._moveBottom,'BOT'])
        return availableWays
    def movePacmanAI(self):

        func = self._Astar

        func()
        ways = self._findWays()
        if self._isMove == False:
            if len(ways) > 0:
                self._curWay = random.choice(ways)
                self._isMove = True
        else:
            have = False
            for e in ways:
                if self._curWay[1] == e[1]:
                    have = True
                    break
            if have == False:
                self._isMove = False
                self._curWay = None
            else:
                self._curWay[0]()
    def _Astar(self):
        X, Y = 800// 50, (600 - 100) // 50

        ways_for_pacman = []
        P_X = self.rect.center[0] // 50
        P_Y = self.rect.center[1] // 50

        if self._hasPass == False:
            for x in range(0, 16):
                for y in range(0, 10):
                    if self._matrix[y][x]!= '#' and x!= P_X and y!= P_Y:
                        ways_for_pacman.append([x, y])
            self._curPass = random.choice(ways_for_pacman)
            self._hasPass = True
            print(self._curPass)

        self._drawCircle(self._curPass[0], self._curPass[1], (0,0,255))
        if P_X == self._curPass[0] and P_Y == self._curPass[1]:
            self._hasPass = False
            self._matrix = self._movematrix
            return
        start_x, start_y = P_X, P_Y
        p = self._curPass
        result_way = []
        result_way.append([start_x, start_y])

        close_list = {}
        close_list[start_y*X + start_x] = [(0, 0), math.fabs(start_x - self._curPass[0]) + math.fabs(start_y - self._curPass[1]), True]
        final_way = []
        lenth = 1000
        while len(result_way) > 0:
            current = result_way[-1]
            if current == self._curPass and len(result_way) < lenth:
                lenth = len(result_way)
                for el in result_way:
                    final_way.append(el)
            min_way = ()
            min = 100
            if self._matrix[current[1]][current[0] + 1] != '#':
                if close_list.get(current[1] * X + current[0] + 1) == None:
                    close_list[current[1] * X + current[0] + 1] = [tuple(current), 1 + math.fabs(current[0] + 1 - self._curPass[0]) + math.fabs(current[1] - self._curPass[1]), False]
                elif close_list[current[1] * X + current[0] + 1][1] > 1 + math.fabs(current[0] + 1 - self._curPass[0]) + math.fabs(current[1] - self._curPass[1])  and close_list[current[1] * X + current[0] + 1][2] == False:
                    close_list[current[1] * X + current[0] + 1] = [tuple(current), 1 + math.fabs(current[0] + 1 - self._curPass[0]) + math.fabs(current[1] - self._curPass[1]), False]

                if close_list[current[1] * X + current[0] + 1][1] < min and close_list[current[1] * X + current[0] + 1][2] == False:
                    min = close_list[current[1] * X + current[0] + 1][1]
                    min_way = (current[0] + 1, current[1])
            if self._matrix[current[1]][current[0] - 1] != '#':
                if close_list.get(current[1] * X + current[0] - 1) == None:
                    close_list[current[1] * X + current[0] - 1] = [tuple(current), 1 + math.fabs(
                        current[0] - 1 - self._curPass[0]) + math.fabs(current[1] - self._curPass[1]), False]
                elif close_list[current[1] * X + current[0] - 1][1] > 1 + math.fabs(
                        current[0] - 1 - self._curPass[0]) + math.fabs(current[1] - self._curPass[1]) and \
                        close_list[current[1] * X + current[0] + 1][2] == False:
                    close_list[current[1] * X + current[0] - 1] = [tuple(current), 1 + math.fabs(
                        current[0] - 1 - self._curPass[0]) + math.fabs(current[1] - self._curPass[1]), False]

                if close_list[current[1] * X + current[0] - 1][1] < min and close_list[current[1] * X + current[0] - 1][2] == False:
                    min = close_list[current[1] * X + current[0] - 1][1]
                    min_way = (current[0] - 1, current[1])
            if self._matrix[current[1] - 1][current[0]] != '#':
                if close_list.get((current[1] - 1) * X + current[0]) == None:
                    close_list[(current[1] - 1)* X + current[0]] = [tuple(current), 1 + math.fabs(
                        current[0] - self._curPass[0]) + math.fabs(current[1]  - 1 - self._curPass[1]), False]
                elif close_list[(current[1] - 1) * X + current[0]][1] > 1 + math.fabs(
                        current[0] - self._curPass[0]) + math.fabs(current[1] - 1 - self._curPass[1]) and \
                        close_list[(current[1] - 1) * X + current[0]][2] == False:
                    close_list[(current[1] - 1) * X + current[0]] = [tuple(current), 1 + math.fabs(
                        current[0] - self._curPass[0]) + math.fabs(current[1] - 1 - self._curPass[1]), False]
                if close_list[(current[1] - 1) * X + current[0]][1] < min and close_list[(current[1] - 1) * X + current[0]][2] == False:
                    min = close_list[(current[1] - 1) * X + current[0]][1]
                    min_way = (current[0], current[1] - 1)
            if self._matrix[current[1] + 1][current[0]] != '#':
                if close_list.get((current[1] + 1) * X + current[0]) == None:
                    close_list[(current[1] + 1)* X + current[0]] = [tuple(current), 1 + math.fabs(
                        current[0] - self._curPass[0]) + math.fabs(current[1]  + 1 - self._curPass[1]), False]
                elif close_list[(current[1] + 1) * X + current[0]][1] > 1 + math.fabs(
                        current[0] - self._curPass[0]) + math.fabs(current[1] + 1 - self._curPass[1]) and \
                        close_list[(current[1] + 1) * X + current[0]][2] == False:
                    close_list[(current[1] + 1) * X + current[0]] = [tuple(current), 1 + math.fabs(
                        current[0] - self._curPass[0]) + math.fabs(current[1] + 1 - self._curPass[1]), False]
                if close_list[(current[1] + 1) * X + current[0]][1] < min and close_list[(current[1] + 1) * X + current[0]][2] == False:
                    min = close_list[(current[1] + 1) * X + current[0]][1]
                    min_way = (current[0], current[1] + 1)
            if len(min_way) != 0:
                result_way.append([min_way[0], min_way[1]])
                close_list[min_way[1]*X + min_way[0]][2] = True
            else:
                result_way.pop(-1)

        #print(close_list)

        res_matrix = []
        for i in range(0, 10):
            row = []
            for j in range(0, 16):
                row.append('#')
            res_matrix.append(row)
        for g in final_way:
            res_matrix[g[1]][g[0]] = ''
        self._matrix = res_matrix



    def _drawCircle(self,x, y , color):
        point = pygame.Surface((10, 10))
        pygame.draw.circle(point, color, (5, 5), 5)
        rect = point.get_rect(center=(x * 50 + 25, y * 50 + 25))
        self._sc.blit(point, rect)


