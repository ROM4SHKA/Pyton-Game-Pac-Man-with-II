import  pygame
class Level():
    def __init__(self,sc, img, rect_img, matrix):
        self.matrix = matrix
        self.sc = sc
        self.img = img
        self.rect_img = rect_img


    def draw_level(self):
            for x in range(0, 16):
                for y in range(0, 10):
                    if self.matrix[y][x] == '#':
                        self.sc.blit(self.img, self.rect_img.move(x * 50, y * 50))
    def draw_points(self):
        points_list = []
        for x in range(0, 16):
            for y in range(0, 10):
                if self.matrix[y][x] == '*' or self.matrix[y][x] == '&':
                    point = pygame.Surface((10, 10))
                    pygame.draw.circle(point, (255,255,255),(5, 5), 5)
                    rect = point.get_rect(center = (x*50+ 25,y*50+25))
                    self.sc.blit(point, rect)
                    points_list.append(rect)
        return  points_list