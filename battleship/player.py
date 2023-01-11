class player:

    def __init__(self, gameboard, guessboard):
        self.gameboard = gameboard
        self.guessboard = guessboard
        self.turn = False

    def checkguess(self, coord, player):
        if coord in player.gameboard.full:
            self.guessboard.right.append(coord)
            player.gameboard.right.append(coord)
        else:
            self.guessboard.wrong.append(coord)
            player.gameboard.wrong.append(coord)

            # switching turns
            self.turn = False
            player.turn = True


