import pygame
from battleship.constants import*
from battleship.piece import piece

class board:
    def __init__(self, x, y, width, height, SQUARE_SIZE):
        self.board = {}
        self.x = x
        self.y = y
        self.SQUARE_SIZE = SQUARE_SIZE
        self.image = pygame.Surface((width + 1, height + 1))
        self.image.fill(LIGHT_BLUE)
        self.rect = self.image.get_rect(x=self.x,y=self.y)
        self.pieces = []
        self.square = pygame.Surface((self.SQUARE_SIZE, self.SQUARE_SIZE))
        self.restrictedsquares = []
        self.confirmbutton = pygame.Rect(self.rect.x + self.image.get_width() + 35, self.rect.y + 225, 135, 25)
        self.set = False
        self.wrong = []
        self.right = []
        self.full = []

    def draw_square (self, win):
        # drawing board square on screen
        win.blit(self.image, (self.x, self.y))
        for col in range(COLS):
            for row in range(ROWS):
                if col == 0 and row == 0:
                    # don't need to draw top left
                    continue

                # drawing labeled coordinate box
                elif col == 0 or row == 0:
                    pygame.draw.rect(win, (240, 248, 255), ((col * self.SQUARE_SIZE) + (self.x-self.SQUARE_SIZE), (row * self.SQUARE_SIZE) + (self.y-self.SQUARE_SIZE), self.SQUARE_SIZE, self.SQUARE_SIZE))
                    pygame.draw.rect(win, BLACK, ((col * self.SQUARE_SIZE) + (self.x - self.SQUARE_SIZE), (row * self.SQUARE_SIZE) + (self.y - self.SQUARE_SIZE), self.SQUARE_SIZE, self.SQUARE_SIZE), 3)

                    pygame.font.init()  # initializing font module
                    BOX_FONT = pygame.font.SysFont('ITC Machine Bold', int(self.SQUARE_SIZE/2))

                    if row == 0:  # 1st row
                        text = BOX_FONT.render(str(chr(col + 64)), True, BLACK)
                        text_rect = text.get_rect(center=(((col * self.SQUARE_SIZE) + (self.x - self.SQUARE_SIZE)) + self.SQUARE_SIZE/2, ((row * self.SQUARE_SIZE) + (self.y - self.SQUARE_SIZE)) + self.SQUARE_SIZE/2))
                        win.blit(text, text_rect)

                    if col == 0:
                        text = BOX_FONT.render(str(row), True, BLACK)
                        text_rect = text.get_rect(center=(((col * self.SQUARE_SIZE) + (self.x - self.SQUARE_SIZE)) + self.SQUARE_SIZE / 2, ((row * self.SQUARE_SIZE) + (self.y - self.SQUARE_SIZE)) + self.SQUARE_SIZE / 2))
                        win.blit(text, text_rect)

                # drawing coordinates
                else:
                    coordinate = str(chr(col + 64)) + str(row) # creating the coordinate name (ex. A1)
                    squarerect = self.square.get_rect(x=self.x + (col-1)*self.SQUARE_SIZE, y=self.y + (row-1) * self.SQUARE_SIZE)
                    self.square.fill((173, 216, 230))
                    if len(self.restrictedsquares) > 0:
                        for q in range(len(self.restrictedsquares)):
                            # if its a restricted square, fill grey
                            if self.restrictedsquares[q] == coordinate:
                                self.square.fill((211,211,211))

                    elif self.set:
                        # if it contains a piece, fill green
                        if coordinate in self.full:
                            self.square.fill((47,79,79))

                    # if its a correctly guessed coordinate, draw an X
                    if coordinate in self.right:
                        pygame.draw.line(win, (255, 0, 0), (squarerect.topleft), (squarerect.bottomright))
                        pygame.draw.line(win, (255, 0, 0), (squarerect.topright), (squarerect.bottomleft))

                    # if its an incorrectly guessed coordinate, draw a circle
                    if coordinate in self.wrong:
                        pygame.draw.ellipse(win, BLACK, squarerect)

                    pygame.draw.rect(self.square, BLACK, (0, 0, self.SQUARE_SIZE, self.SQUARE_SIZE), 1)
                    self.board[coordinate] = squarerect # adding to dictionary of coordinates
                    self.image.blit(self.square, ((col-1)*self.SQUARE_SIZE, (row-1) * self.SQUARE_SIZE)) # drawing on screen

    def setBoard(self):
        del self.restrictedsquares[:] # remaking the list everytime
        if len(self.pieces) > 0:
            for i in self.board:
                for boat in self.pieces:
                    if boat.rect.colliderect(self.rect) and not boat.click:
                        for square in range (boat.squares):
                            # if piece is lined up with the center of the coordinate
                            if ((boat.rect.x + self.SQUARE_SIZE/2) + (square*self.SQUARE_SIZE), boat.rect.y + (self.SQUARE_SIZE/2)) == self.board[i].center:
                                # denotes coordinate contains a piece
                                self.board[i] = 'full'
            if not self.set:
                self.createrestrictedlist(boat)

    def createpieces(self, win):
        for i in range(5):
            verticalShift = i*40

            # drawing the piece holders
            pygame.draw.rect(win, (211, 211, 211),(self.x + self.image.get_width() + 45, (self.y + 20) + verticalShift,self.SQUARE_SIZE*(5-i), self.SQUARE_SIZE))

            # drawing the pieces
            boat = piece(5 - i,self.x + self.image.get_width() + 45, (self.y + 20) + verticalShift, self.SQUARE_SIZE)
            boat.drawpiece()
            self.pieces.append(boat)
            self.pieces[i].update(win)

    def adjustboard(self, boat):
        for i in self.board:
            # if the top left corner of the piece lies in between a coordinate
            if self.board[i] != 'full' and \
                (self.board[i].x <= boat.rect.x <= self.board[i].x + self.SQUARE_SIZE) and \
                (self.board[i].y <= boat.rect.y <= self.board[i].y + self.SQUARE_SIZE) and \
                boat.rect.topleft != self.board[i].topleft:

                # if it lies in the bottom left quadrant, move it to the bottom left corner
                if boat.rect.x <= self.board[i].centerx and boat.rect.y <= self.board[i].centery:
                    boat.rect.move_ip(self.board[i].x - boat.rect.x, self.board[i].y - boat.rect.y)

                # if it lies in the bottom right quadrant, move it to the bottom right corner
                elif boat.rect.x >= self.board[i].centerx and boat.rect.y <= self.board[i].centery:
                    boat.rect.move_ip((self.board[i].x + self.SQUARE_SIZE) - boat.rect.x, self.board[i].y - boat.rect.y)

                # if it lies in the top left quadrant, move it to the top left corner
                elif boat.rect.x <= self.board[i].centerx and boat.rect.y >= self.board[i].centery:
                    boat.rect.move_ip(self.board[i].x - boat.rect.x, (self.board[i].y + self.SQUARE_SIZE) - boat.rect.y)

                # if it lies in the top right quadrant, move it to the top right corner
                elif boat.rect.x >= self.board[i].centerx and boat.rect.y >= self.board[i].centery:
                    boat.rect.move_ip((self.board[i].x + self.SQUARE_SIZE) - boat.rect.x, (self.board[i].y + self.SQUARE_SIZE) - boat.rect.y)

                for num in range(len(self.restrictedsquares)):
                    coordinate = self.restrictedsquares[num]
                    # if piece is on a restricted square, move it to the starting position
                    if boat.rect.colliderect(self.board[coordinate]):
                        boat.rect.move_ip(boat.x - boat.rect.x, boat.y - boat.rect.y)
                        boat.click = False

    def createrestrictedlist(self, boat):
            for n in range(len(self.board)):
                values = list(self.board.values()) # list of value of coordinates ('full' or rect object)
                keys = list(self.board.keys()) # list of coordinates
                # checks if the coordinate is 'full'
                if values[n] != 'full':
                    coordinate = keys[n]
                    above = n - 1
                    below = n + 1
                    right = n + 9
                    left = n - 9
                    topleft = n - 10
                    topright = n + 8
                    bottomleft = n - 8
                    bottomright = n + 10

                    if (boat.squares == 1 and
                        # if coordinate is I8
                        ((n < 80 and isinstance(values[below], str) and keys[below] == 'I9') or
                        # if coordinate is H8
                        (n < 71 and isinstance(values[bottomright], str) and keys[bottomright] == 'I9') or
                        # if coordinate is H9
                        (n < 72 and isinstance(values[right], str) and keys[right] == "I9"))) or\
                        \
                        \
                        (# if coordinate above is not a bottom row coordinate and is full
                        (n > 0 and isinstance(values[above], str) and (above) % 9 != 8) or

                        # if coordinate below is not a top row coordinate and is full
                        (n < len(self.board) - 2 and isinstance(values[below], str) and (below) % 9 != 0)) or \
                        \
                        \
                        (# if coordinate to the left is full (n > 8 to avoid index out of bounds)
                        (n > 8 and isinstance(values[left], str)) or

                        # if coordinate to the right is full (n < len(self.board) - 10 avoids index out of bounds)
                        (n < len(self.board) - 10 and isinstance(values[right], str)) or

                        # if coordinate to the top left is full (n > 9 avoids index out of bounds)
                        (n > 9 and isinstance(values[topleft], str) and (topleft) % 9 != 8) or

                        # if coordinate to the bottom right is full (n < len(self.board) - 11 avoids index out of bounds)
                        (n < len(self.board) - 11 and isinstance(values[bottomright], str) and (bottomright) % 9 != 0) or

                        # if coordinate to the top left is full (n > 7 avoids index out of bounds)
                        (n > 7 and isinstance(values[bottomleft], str) and (bottomleft) % 9 != 0) or

                        # if coordinate to the bottom right is full (n < len(self.board) - 9 avoids index out of bounds)
                        (n < len(self.board) - 9 and isinstance(values[topright], str) and (topright) % 9 != 8)):

                        # add square to restricted list
                        self.restrictedsquares.append(coordinate)

    def isFull(self):
        onBoard = 0
        for boat in self.pieces:
            if not boat.click and boat.rect.colliderect(self.rect):
                onBoard +=1
        if onBoard == 5:
            return True
        else:
            return False

