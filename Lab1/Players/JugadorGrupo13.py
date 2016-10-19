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

def invertBoard(board):
	return [[(-(x-1)) if (x<2) else x for x in y] for y in board]
	
class JugadorGrupo13(Player):
	name = 'JugadorGrupo13'

	def __init__(self, color):
		super(JugadorGrupo13, self).__init__(self.name, color=color)
		self.neuralNetwork = joblib.load('red-neuronal.pkl') 
		print "Red neuronal cargada."

	def move(self, board, opponent_move):
		warnings.filterwarnings("ignore", category=DeprecationWarning)
		possible_moves = board.get_possible_moves(self.color)
		# Lista con tuplas, donde cada tupla tiene las coordenadas (x,y)
		# de un movimiento posible.
		moveTuples = []
		for move in possible_moves:
			moveTuples.append((move.get_row(), move.get_col()))

		X = board.get_as_matrix()

		if (self.color==SquareType.WHITE):
			# print 'Tablero invertido'
			X = invertBoard(X)
		X= convert_matrix_board_to_nparray(X)
		prediction = self.neuralNetwork.predict(X)		
		#Ordeno el tablero de mayor a menor y paso a tuplas de movimientos
		sortedMoves = [(divmod(prediction[0].tolist().index(x),8)[0], divmod(prediction[0].tolist().index(x),8)[1]) for x in sorted(prediction[0], reverse=True)]
		i=0
		#Agarro el mejor movimiento dentro de los posibles
		for p in sortedMoves:
			i=i+1
			if (p in moveTuples):
				m=p
				break
				
		#Que tan lejos nos tuvimos que ir en la lista de movimientos "sugeridos" para encontrar uno legal.
		#print "Posición del mejor movimiento"
		#print i
		return Move(m[0], m[1])


	def on_win(self, board):
		# joblib.dump(neuralNetwork, 'red-neuronal-test.pkl')
		print 'Ganéppp y soy el color:' + self.color.name

	def on_defeat(self, board):
		# joblib.dump(neuralNetwork, 'red-neuronal-test.pkl')
		print 'Perdíppp y soy el color:' + self.color.name

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
	for row in board:
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