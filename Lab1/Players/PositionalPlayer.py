# -*- coding:utf-8 -*-

from Player import Player
import numpy as np
import sys

class PositionalPlayer(Player):
    """Jugador posicional."""
    
    name = 'PositionalPlayer'

    def __init__(self, color):
        super(PositionalPlayer, self).__init__(self.name, color)

    def move(self, board, opponent_move):
        """
        :param board: Board
        :param opponent_move: Move
        :return: Move
        """
        positionalValues = np.matrix([  [150,-20, 10,  5,  5, 10,-20,150],
                                        [-20,-50, -2, -2, -2, -2,-50,-20],
                                        [ 10, -2, -1, -1, -1, -1, -2, 10],
                                        [  5, -2, -1, -1, -1, -1, -2,  5],
                                        [  5, -2, -1, -1, -1, -1, -2,  5],
                                        [ 10, -2, -1, -1, -1, -1, -2, 10],
                                        [-20,-50, -2, -2, -2, -2,-50,-20],
                                        [150,-20, 10,  5,  5, 10,-20,150],])
        chosen_move = None
        maximo = -sys.maxint
        opponent_color = board._get_opposite(self.color).value
        b = board.get_as_matrix()
        cant_fichas = 0.0
        for i in xrange(8):
            for j in xrange(8):
                if b[i][j] == self.color.value or b[i][j] == opponent_color:
                    cant_fichas += 1
        if (cant_fichas / 64) > 0.8:
            parteFinal = 1
        else:
            parteFinal = 0
        for move in board.get_possible_moves(self.color):
            b = board.get_as_matrix()
            tmp = 0
            for (c,f) in board.get_squares_to_mark(move=move, color=self.color):
                b[c][f] = self.color.value
            for i in xrange(8):
                for j in xrange(8):
                    if b[i][j] == self.color.value:
                        if parteFinal == 0:
                            tmp += positionalValues[j,i]
                        else:
                            tmp += 1
                    elif b[i][j] == opponent_color:
                        if parteFinal == 0:
                            tmp -= positionalValues[j,i]
                        else:
                            tmp -= 1
            if tmp > maximo:
                maximo = tmp
                chosen_move = move
        return chosen_move

    def on_win(self, board):
        print 'Gané y soy el color:' + self.color.name

    def on_defeat(self, board):
        print 'Perdí y soy el color:' + self.color.name

    def on_draw(self, board):
        print 'Empaté y soy el color:' + self.color.name

    def on_error(self, board):
        raise Exception('Hubo un error.')
