import battleship.board
from battleship.constants import BLACK
import pygame

class piece():

    def __init__(self, pieceNumber, x, y, SQUARE_SIZE):
        self.image = pygame.Surface((SQUARE_SIZE*pieceNumber, SQUARE_SIZE))
        self.image.fill((47,79,79))
        self.x = x
        self.y = y
        self.SQUARE_SIZE = SQUARE_SIZE
        self.squares = pieceNumber
        self.rect = self.image.get_rect(x=x, y=y)
        self.shadow = pygame.Rect(x, y, SQUARE_SIZE*pieceNumber, SQUARE_SIZE)
        self.click = False

    def drawpiece(self):
        for squares in range(self.squares):
            pygame.draw.rect(self.image, BLACK, (squares*(self.SQUARE_SIZE), 0, self.SQUARE_SIZE, self.SQUARE_SIZE), 1)

    def update(self, surface):
        if self.click:
            # center of piece is attached to mouse
            self.rect.center = pygame.mouse.get_pos()

        surface.blit(self.image, self.rect)






