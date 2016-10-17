# -*- coding: utf-8 -*-

from Player import Player
import random
import numpy
import sys
import math
from Move import Move
from sklearn.neural_network import MLPClassifier
from sklearn.externals import joblib
from DataTypes import SquareType
import warnings

class JugadorGrupo13(Player):
    """Jugador que elige una jugada al azar dentro de las posibles."""
    name = 'JugadorGrupo13'

    def __init__(self, color):
        super(JugadorGrupo13, self).__init__(self.name, color=color)
        self.neuralNetwork = joblib.load('red-neuronal-test.pkl') 
        print "Red neuronal cargada."
        # newBoard = numpy.random.randint(3, size=64)
        # newBoard = newBoard.reshape(1,-1)
        # print self.neuralNetwork.predict(newBoard)

    def move(self, board, opponent_move):
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        possible_moves = board.get_possible_moves(self.color)
        # Lista con tuplas, donde cada tupla tiene las coordenadas (x,y)
        # de un movimiento posible.
        moveTuples = []
        for move in possible_moves:
            moveTuples.append((move.get_row(), move.get_col()))

        X = convert_matrix_board_to_nparray(board)
        X.reshape(1,-1)
        predictedMove = self.neuralNetwork.predict(X)
        predictedMoveTuple = (predictedMove[0][0], predictedMove[0][1])

        # Encuentro movimiento posible mas cercano.
        nearest = min(moveTuples, key=lambda x: math.hypot(predictedMoveTuple[0] - x[0], predictedMoveTuple[1] - x[1]))

        # print "#######################################"
        # print "Possible moves are: " + str(moveTuples)
        # print "Predicted move is: " + str((predictedMove[0][0], predictedMove[0][1]))
        # print "Closest move is: " + str((nearest[0], nearest[1]))
        # print "#######################################"

        return Move(nearest[0], nearest[1])

        # print "#########MOVES#########"
        # print possible_moves_array_format
        # # Obtengo al tablero como una lista.
        # boardAsList = convert_matrix_board_to_nparray(board)
        # # La ANN precisa reshape.
        # boardAsList = boardAsList.reshape(1,-1)
        # print "#########BOARD#########"
        # print boardAsList
        # print "#########PASADO POR ANN#########"
        # # Evaluo el tablero con mi ANN.

        # # Puede ser que todavía no esté entrenada, por lo que contemplo 
        # # la excepción NotFittedError.
        # try:
        #     annEval = self.neuralNetwork.predict(boardAsList)
        #     # # Se obtiene el mejor movimiento
        #     # print "ANN suggests to move: " + str(annEval[0].argmax(axis=0))
        #     qOutputIndex = get_best_move_id(annEval[0], possible_moves_array_format)
        # except:
        #     print(sys.exc_info()[0],"occured.")
        #     annEval = [[0] * 64]
        #     qOutputIndex = get_best_move_id(annEval[0], possible_moves_array_format)


        # # Si hay movimientos posibles.
        # if (qOutputIndex != -1): 
        #     # Simulo siguiente movimiento.
        #     for square in board.get_squares_to_mark(possible_moves[qOutputIndex], self.color):
        #         board.set_position(square[0], square[1], self.color)

        #     # Obtengo recompensa por siguiente tablero.
        #     reward = getReward(board, self.color)

        #     try:
        #         annEvalNext = self.neuralNetwork.predict(boardAsList)
        #         # # Se obtiene el mejor movimiento
        #         # print "ANN suggests to move: " + str(annEval[0].argmax(axis=0))
        #         qMaxIndex = get_best_move_id(annEvalNext[0], possible_moves_array_format)
        #     except:
        #         print(sys.exc_info()[0],"occured.")
        #         annEvalNext = [[0] * 64]
        #         qMaxIndex = get_best_move_id(annEvalNext[0], possible_moves_array_format)

        #     alpha = 0.1
        #     gamma = 1.0
        #     qTarget = (1.0-alpha) * annEval[0][qOutputIndex] + alpha * (reward + gamma * annEvalNext[0][qMaxIndex])

        #     annEval[0][qOutputIndex] = qTarget

        #     # Se entrena la red neuronal.
        #     self.neuralNetwork.fit(boardAsList, annEval)

        #     return possible_moves[qOutputIndex]
        # else:
        #     i = random.randint(0, len(possible_moves) - 1)
        #     return possible_moves[qOutputIndex]


    def on_win(self, board):
        # joblib.dump(neuralNetwork, 'red-neuronal-test.pkl')
        print 'Gané y soy el color:' + self.color.name

    def on_defeat(self, board):
        # joblib.dump(neuralNetwork, 'red-neuronal-test.pkl')
        print 'Perdí y soy el color:' + self.color.name

    def on_draw(self, board):
        # joblib.dump(neuralNetwork, 'red-neuronal-test.pkl')
        print 'Empaté y soy el color:' + self.color.name

    def on_error(self, board):
        raise Exception('Hubo un error.')

# def convert_matrix_board_to_nparray(board):
#     lst = []
#     for row in board:
#         for element in row:
#             lst.append(element)
#     # print lst
#     return numpy.array(lst)

def convert_matrix_board_to_nparray(board):
    lst = []
    for row in board.get_as_matrix():
        for element in row:
            lst.append(element)
    # print lst
    return numpy.array(lst)

def convert_moves_to_list(moves):
    lst = []
    for move in moves:
        lst.append(8 * move.get_row() + move.get_col())
    return lst

def get_best_move_id(annEvalList, movesList):
    maxGain = -1
    maxGainIndex = -1
    for move in movesList:
        if (annEvalList[move] > maxGain):
            maxGain = annEvalList[move]
            maxGainIndex = movesList.index(move)
    print "Max gain is " + str(maxGain)
    return maxGainIndex

def getReward(board, playerColor):
    if (len(board.get_possible_moves(playerColor)) > 0):
        # No se termina el juego.
        reward = 0
    else:
        if ((playerColor == SquareType.BLACK) and (len(board.get_possible_moves(SquareType.WHITE)) > 0)):
            # El player va a tener que "pasar", reward es 0
            reward = 0
        elif ((playerColor == SquareType.WHITE) and (len(board.get_possible_moves(SquareType.BLACK)) > 0)):
            reward = 0
        else:
            # Ninguno tiene mas movimientos para hacer.
            blackAmount = getBlackAmount(board)
            whiteAmount = getWhiteAmount(board)
            if (playerColor == SquareType.BLACK):
                if (blackAmount > whiteAmount):
                    reward = 1
                elif (blackAmount == whiteAmount):
                    reward = 0
                else:
                    reward = -1
            else:
                if (blackAmount > whiteAmount):
                    reward = -1
                elif (blackAmount == whiteAmount):
                    reward = 0
                else:
                    reward = 1
    return reward

def getBlackAmount(board):
    count = 0
    boardAsList = convert_matrix_board_to_nparray(board)
    for element in boardAsList:
        if (element == 1):
            count += 1
    return count

def getWhiteAmount(board):
    count = 0
    boardAsList = convert_matrix_board_to_nparray(board)
    for element in boardAsList:
        if (element == 0):
            count += 1
    return count