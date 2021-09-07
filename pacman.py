import  pygame

class PacMan(pygame.sprite.Sprite):
    def __init__(self, matrix, filename):
        pygame.sprite.Sprite.__init__(self)
        self._image = pygame.image.load(filename).convert_alpha()
        self._image = pygame.transform.scale(self._image, (40, 40))
        self.rect = self._image.get_rect()
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

    def MovePac(self):
        coordX , coordY = self.rect.x, self.rect.y
        bt = pygame.key.get_pressed()
        if bt[pygame.K_LEFT]:
            self.rect.x -= self._speed
            if self._matrix[self.rect.y // 50][(self.rect.x - self._speed)//50] == '#' or self._matrix[self.rect.bottomright[1]//50][(self.rect.x - self._speed)//50] == '#':
               self.rect.x = coordX
               self.rect.y = coordY
            else:
                self.cur_img = self._left_image

        elif bt[pygame.K_RIGHT]:
            self.rect.x += self._speed
            if self._matrix[self.rect.y//50][(self.rect.topright[0])//50] == '#' or self._matrix[self.rect.bottomright[1]//50][(self.rect.bottomright[0])//50] == '#':
                self.rect.x = coordX
                self.rect.y = coordY
            else:
                self.cur_img = self._right_image

        elif bt[pygame.K_UP]:
            self.rect.y -= self._speed
            if self._matrix[(self.rect.y - self._speed)//50][self.rect.x//50] == '#' or self._matrix[(self.rect.y- self._speed)//50][self.rect.topright[0]//50]=='#':
                self.rect.x = coordX
                self.rect.y = coordY
            else:
                self.cur_img = self._up_image
        elif bt[pygame.K_DOWN]:
            self.rect.y += self._speed
            if self._matrix[(self.rect.bottomleft[1] + self._speed)//50][self.rect.x//50] == '#' or self._matrix[(self.rect.bottomright[1] + self._speed)//50][self.rect.bottomright[0]//50] == '#':
                self.rect.x = coordX
                self.rect.y = coordY
            else:
                self.cur_img = self._down_image

    def countPoints(self,matrix, score, point_rects):
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




