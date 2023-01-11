import pygame
from battleship.player import player
from battleship.board import board
from battleship.constants import *

FPS = 60
WIN = pygame.display.set_mode((WIDTH, HEIGHT))  # creating the window
pygame.display.set_caption('Battleship')  # window title
btncolor = (211, 211, 211)


def set_design(players):
    for player in players:
        # 15 right guesses means they've won
        if len(player.guessboard.right) >= 15:
            WIN.fill(BLACK)
            if player == players[0]:  # player 1
                GAME_FONT.render_to(WIN, (350, 350), 'PLAYER 1 WINS!!!',
                                          (255, 255, 255))
            else:  # player 2
                GAME_FONT.render_to(WIN, (350, 350), 'PLAYER 2 WINS!!!',
                                    (255, 255, 255))
            break
        else:

            if player.turn:
                GAME_FONT.render_to(WIN, (player.gameboard.rect.x + 50, player.gameboard.rect.y - 55), 'YOUR BOARD', BLACK)
                player.gameboard.draw_square(WIN)  # drawing the gameboard
                GAME_FONT.render_to(WIN, (player.guessboard.rect.x + 2, player.guessboard.rect.y - 50), 'GUESSING BOARD', BLACK)
                player.guessboard.draw_square(WIN)  # drawing the guessingboard

                if not player.gameboard.set:  # if the board is not set
                    #player.gameboard.setBoard()
                    # instructions
                    INSTRUCTION_FONT.render_to(WIN, (player.gameboard.rect.x + 305.5, player.gameboard.rect.y - 28),
                                        'Place the Pieces onto Your Board', BLACK)
                    INSTRUCTION_FONT.render_to(WIN, (player.gameboard.rect.x + 305.5, player.gameboard.rect.y + 255),
                                          'Click to confirm placements', BLACK)

                    # box holding the pieces
                    pygame.draw.rect(WIN, (255, 255, 255),
                                     (player.gameboard.rect.x + 307.5, player.gameboard.rect.y - 15, 165, 235))
                    pygame.draw.rect(WIN, BLACK,
                                     (player.gameboard.rect.x + 307.5, player.gameboard.rect.y - 15, 165, 235), 1)
                    GAME_FONT.render_to(WIN, (player.gameboard.rect.x + 315, player.gameboard.rect.y - 5), 'PIECES',
                                        BLACK)

                    player.gameboard.createpieces(WIN)  # drawing the pieces

                    # drawing the confirmation button ('set position')
                    pygame.draw.rect(WIN, btncolor, player.gameboard.confirmbutton)
                    pygame.draw.rect(WIN, BLACK, player.gameboard.confirmbutton, 1)
                    BUTTON_FONT.render_to(WIN, (player.gameboard.confirmbutton.x + 5, player.gameboard.confirmbutton.y + 5),
                                          'SET POSITION', BLACK)
                else:
                    #instruction text once board is set
                    pygame.draw.rect(WIN, (255, 255, 255),
                                     (player.gameboard.rect.x + 270.5, player.gameboard.rect.y, 314, 150))
                    pygame.draw.rect(WIN, BLACK,
                                     (player.gameboard.rect.x + 270.5, player.gameboard.rect.y, 314, 150), 1)
                    INSTRUCTION_FONT.render_to(WIN, (player.gameboard.rect.x + 277.5, player.gameboard.rect.y + 25),
                                               'Click a coordinate on the Guessing Board', BLACK)
                    BUTTON_FONT.render_to(WIN,
                                          (player.gameboard.rect.x + 277.5, player.gameboard.rect.y + 5),
                                          'INSTRUCTIONS', BLACK)
                    INSTRUCTION_FONT.render_to(WIN, (player.gameboard.rect.x + 277.5, player.gameboard.rect.y + 40),
                                               'to guess the location of enemy pieces', BLACK)
                    pygame.draw.line(WIN, (255, 0, 0), (player.gameboard.rect.x + 277.5, player.gameboard.rect.y + 60), (player.gameboard.rect.x + 287.5, player.gameboard.rect.y + 70))
                    pygame.draw.line(WIN, (255, 0, 0), (player.gameboard.rect.x + 277.5, player.gameboard.rect.y + 70), (player.gameboard.rect.x + 287.5, player.gameboard.rect.y + 60))
                    INSTRUCTION_FONT.render_to(WIN, (player.gameboard.rect.x + 292.5, player.gameboard.rect.y + 60),
                                               'represents a correct guess (another ', BLACK)
                    INSTRUCTION_FONT.render_to(WIN, (player.gameboard.rect.x + 292.5, player.gameboard.rect.y + 75),
                                               'guess is granted)', BLACK)
                    pygame.draw.ellipse(WIN, BLACK, (player.gameboard.rect.x + 277.5, player.gameboard.rect.y + 95, 10, 10))
                    INSTRUCTION_FONT.render_to(WIN, (player.gameboard.rect.x + 292.5, player.gameboard.rect.y + 95),
                                               'represents an incorrect guess (turn ends)', BLACK)
                    INSTRUCTION_FONT.render_to(WIN, (player.gameboard.rect.x + 277.5, player.gameboard.rect.y + 115),
                                               'First player to hit all 15 piece-containing', BLACK)
                    INSTRUCTION_FONT.render_to(WIN, (player.gameboard.rect.x + 277.5, player.gameboard.rect.y + 130),
                                               'coordinates wins!', BLACK)


            else:
                # covering the other side
                pygame.draw.rect(WIN, BLACK, (player.gameboard.rect.x - 30, player.gameboard.rect.y - 80, 900, 400))


def game_event_loop(players):
    global btncolor
    for event in pygame.event.get():
        pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)  # default cursor image
        if event.type == pygame.QUIT:
            pygame.quit()
            # bypasses python error
            raise SystemExit

        for index in range(len(players)):
            if players[index].turn:
                board = players[index].gameboard
                guessboard = players[index].guessboard
                if board.set:
                    start(players)
                    # deletes the solid pieces (to allow me to draw over the full squares)
                    del board.pieces[:]
                    for coord in guessboard.board:
                        # if user hovers over a coordinate on the guessing board
                        if guessboard.board[coord].collidepoint(pygame.mouse.get_pos()):
                            # checks if coord has already been guessed
                            if coord in guessboard.right or coord in guessboard.wrong:
                                pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_NO)
                                continue
                            else:
                                pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)
                                if event.type == pygame.MOUSEBUTTONDOWN:
                                    otherplayer = players[switchplayer(index)]
                                    # checking if guess is correct
                                    players[index].checkguess(coord, otherplayer)

                else:
                    btncolor = (211, 211, 211)  # setting original color
                    # if users hovers over set position button
                    if board.confirmbutton.collidepoint(pygame.mouse.get_pos()):
                        if not board.isFull():  # checks if board contains all 5 pieces
                            pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_NO)
                        else:
                            pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)
                            btncolor = (224, 224, 224)  # change color when users hovers over
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                board.set = True 
                                players[switchplayer(index)].turn = True
                                del board.confirmbutton  # remove the button once clicked
                                del board.restrictedsquares[:]  # deleting the gray restricted squares
                                players[index].turn = False 
                    else:
                        for boat in board.pieces:
                            # if user hovers over a piece
                            if boat.rect.collidepoint(pygame.mouse.get_pos()):
                                pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)
                                if event.type == pygame.MOUSEBUTTONDOWN:
                                    if boat.rect.colliderect(boat.shadow):
                                        if not boat.click:
                                            boat.click = True
                                        else:
                                            boat.click = False
                                            boat.rect.move_ip(boat.x - boat.rect.x, boat.y - boat.rect.y)
                                    # checks if whole piece is making contact with board
                                    elif board.rect.collidepoint(boat.rect.topleft) and board.rect.collidepoint(boat.rect.bottomright):
                                        #if piece is being held
                                        if boat.click:
                                            for otherboat in board.pieces:
                                                if otherboat != boat:
                                                    # if it is dropped on another piece
                                                    if boat.rect.colliderect(otherboat.rect):
                                                        boat.rect.move_ip(boat.x - boat.rect.x, boat.y - boat.rect.y)
                                                    else:
                                                        boat.click = False

                                        else:
                                            boat.click = True

                                        board.adjustboard(boat)
                                        board.setBoard()


def switchplayer(index):  # returns index of opposite player
    if index == 0:  # player1
        index += 1  # switches to player 2

    else:  # player2
        index -= 1  # switches to player 1

    return index


def start(players):
    for player in players:
        player.gameboard.setBoard()  # final time setting piece locations
        for coord in player.gameboard.board:
            if isinstance(player.gameboard.board[coord], str):  # if 'full' (aka square contains piece)
                player.gameboard.full.append(coord)  # adds to list of coords containing a piece



def main():
    run = True
    clock = pygame.time.Clock()

    # creating board and player objects
    p1refboard = board(640, 80, 225, 225, 25)
    p2refboard = board(640, 480, 225, 225, 25)

    p1gameboard = board(30, 80, 270, 270, 30)
    p2gameboard = board(30, 480, 270, 270, 30)

    player1 = player(p1gameboard, p1refboard)
    player1.turn = True  # player 1 starts

    player2 = player(p2gameboard, p2refboard)

    players = [player1, player2]
    while run:
        clock.tick(FPS)
        WIN.fill(LIGHT_BLUE)

        game_event_loop(players)
        set_design(players)

        pygame.display.update()  # updating display


main()
