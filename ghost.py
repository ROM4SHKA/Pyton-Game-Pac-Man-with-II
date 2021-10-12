import pygame
import random
class Ghost(pygame.sprite.Sprite):
    def __init__(self, matrix, filename, sc):
        pygame.sprite.Sprite.__init__(self)
        self._image = pygame.image.load(filename).convert_alpha()
        self._image = pygame.transform.scale(self._image, (45, 45))
        self.rect = self._image.get_rect()
        self._sc = sc
        self._right_image = self._image
        self._left_image = pygame.transform.flip(self._image, 1, 0)
        self._speed = 3.5
        self.cur_img = self._right_image
        self._matrix = matrix
        for x in range(0, 15):
            for y in range(0, 9):
                if matrix[y][x] == '+':
                    self.rect = self.rect.move(x * 50, y * 50)
                    break
        self._isMove= False
        self._curWay = None
        self.algotitm = 0
        self._movematrix = self._matrix
    def _moveTop(self):
        self.rect.y -= self._speed
    def _moveBottom(self):
        self.rect.y += self._speed
    def _moveLeft(self):
        self.rect.x -= self._speed
        self.cur_img = self._left_image
    def _moveRight(self):
        self.rect.x += self._speed
        self.cur_img = self._right_image

    def _BFS(self, P_x, P_y):
        X, Y = 800 // 50, (600 - 100) // 50
        pacman_X = P_x // 50
        pacman_Y = P_y // 50

        G_X = self.rect.center[0] // 50
        G_Y = self.rect.center[1] // 50
        start_x, start_y = G_X, G_Y
        visited = []
        visited.append([start_x, start_y])
        ghost_pass = []
        values = []
        values.append([start_y * X + start_x,start_y * X + start_x])
        nodes_value = dict(values)
        s = self._movematrix

        while len(visited) > 0:
            if len(visited) > 0:
                current = visited[0]
                if current[0] == pacman_X and current[1] == pacman_Y:
                    c_x, c_y = current[0], current[1]
                    ghost_pass.append([c_x, c_y])
                    while  nodes_value.get(c_y*X + c_x) != c_y*X + c_x:
                            res = nodes_value[c_y*X + c_x]
                            c_x = res - (res//X)*X
                            c_y = res // X
                            ghost_pass.append([c_x, c_y])
                    break


                if self._movematrix[current[1]][current[0] + 1] != '#':
                    if nodes_value.get(current[1] * X + current[0] + 1) == None:
                        visited.append([current[0] + 1, current[1]])
                        nodes_value[current[1] * X + current[0] + 1] = current[1] * X + current[0]


                if self._movematrix[current[1]][current[0] - 1] != '#':
                    if nodes_value.get(current[1] * X + current[0] - 1) == None:
                        visited.append([current[0] - 1, current[1]])
                        nodes_value[current[1] * X + current[0] - 1] = current[1] * X + current[0]


                if self._movematrix[current[1] + 1][current[0]] != '#':
                    if nodes_value.get(current[1] * X + X + current[0]) == None:
                        visited.append([current[0], current[1] + 1])
                        nodes_value[current[1] * X + X + current[0]] = current[1] * X + current[0]


                if self._movematrix[current[1] - 1][current[0]] != '#':
                    if nodes_value.get(current[1] * X - X + current[0]) == None:
                        visited.append([current[0], current[1] - 1])
                        nodes_value[current[1] * X - X + current[0]] = current[1] * X + current[0]

                visited.pop(0)
        res_matrix = []
        for i in range(0, 10):
            row = []
            for j in range(0, 16):
                row.append('#')
            res_matrix.append(row)
        for g in ghost_pass:
            res_matrix[g[1]][g[0]] = ''
        self._matrix = res_matrix

    def _DFS(self, P_x, P_y):
        X, Y = 800// 50, (600 - 100) // 50
        pacman_X = P_x // 50
        pacman_Y = P_y // 50

        G_X = self.rect.center[0] // 50
        G_Y = self.rect.center[1] // 50
        start_x, start_y = G_X, G_Y
        visited = []
        visited.append([start_x, start_y])
        ghost_pass = []
        values = []
        values.append([start_y * X + start_x, 0])
        nodes_value = dict(values)
        s = self._movematrix
        while len(visited) > 0:
            if len(visited) > 0:
                current = visited[-1]
                if current[0] == pacman_X and current[1] == pacman_Y:
                    if len(ghost_pass) > len(visited) or len(ghost_pass) == 0:
                        ghost_pass.clear()
                        for i in visited:
                            ghost_pass.append(i)
                        continue

                if self._movematrix[current[1]][current[0]+1]!= '#':
                    if nodes_value.get(current[1]* X + current[0]+1) == None or nodes_value[current[1]* X + current[0]+1] > nodes_value[current[1]* X + current[0]] + 1:
                        visited.append([current[0] + 1,current[1]])
                        nodes_value[current[1] * X + current[0]+1] = nodes_value[current[1] * X + current[0]] + 1

                        continue
                if self._movematrix[current[1]][current[0] - 1]!= '#':
                    if nodes_value.get(current[1]* X + current[0]-1) == None or nodes_value[current[1]* X + current[0]-1] > nodes_value[current[1]* X + current[0]]  + 1:
                        visited.append([current[0] - 1, current[1]])
                        nodes_value[current[1] * X + current[0] - 1] = nodes_value[current[1] * X + current[0]] + 1

                        continue
                if self._movematrix[current[1]+1][current[0]] != '#':
                    if nodes_value.get(current[1]* X + X + current[0]) == None or nodes_value[current[1]* X + X + current[0]] > nodes_value[current[1]* X + current[0]]  + 1:
                        visited.append([current[0],current[1] + 1])
                        nodes_value[current[1] * X + X + current[0]] = nodes_value[current[1] * X + current[0]] + 1

                        continue
                if self._movematrix[current[1] - 1][current[0]] != '#':
                    if nodes_value.get(current[1] * X - X + current[0]) == None or nodes_value[current[1] * X - X + current[0]] > nodes_value[current[1]* X + current[0]]  + 1:
                        visited.append([current[0],current[1] - 1])
                        nodes_value[current[1] * X - X + current[0]] = nodes_value[current[1] * X + current[0]] + 1

                        continue
                visited.pop()

        res_matrix = []
        for i in range (0,10):
            row = []
            for j in range(0, 16):
                row.append('#')
            res_matrix.append(row)
        for g in ghost_pass:
            res_matrix[g[1]][g[0]] = ''

        self._matrix = res_matrix

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
    def moveGhost(self, P_x, P_y):

        func = self._DFS
        if self.algotitm ==0:
            func = self._DFS
        elif self.algotitm ==1:
            func = self._BFS
        func(P_x, P_y)
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

    def draw_pass(self):
        for x in range(0, 16):
            for y in range(0, 10):
                if self._matrix[y][x] == '':
                        point = pygame.Surface((10, 10))
                        pygame.draw.circle(point, (0, 255, 0), (5, 5), 5)
                        rect = point.get_rect(center=(x * 50 + 25, y * 50 + 25))
                        self._sc.blit(point, rect)
