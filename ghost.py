import pygame
import random
class Ghost(pygame.sprite.Sprite):
    def __init__(self, matrix, filename):
        pygame.sprite.Sprite.__init__(self)
        self._image = pygame.image.load(filename).convert_alpha()
        self._image = pygame.transform.scale(self._image, (45, 45))
        self.rect = self._image.get_rect()
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
    def moveGhost(self):
        ways = self._findWays()
        if self._isMove == False:
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
