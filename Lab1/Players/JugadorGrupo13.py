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
		print 'Gané y soy el color:' + self.color.name

	def on_defeat(self, board):
		# joblib.dump(neuralNetwork, 'red-neuronal-test.pkl')
		print 'Perdí y soy el color:' + self.color.name

	def on_draw(self, board):
		# joblib.dump(neuralNetwork, 'red-neuronal-test.pkl')
		print 'Empaté y soy el color:' + self.color.name

	def on_error(self, board):
		raise Exception('Hubo un error.')

def convert_matrix_board_to_nparray(board):
	lst = []
	for row in board:
		for element in row:
			lst.append(element)
	# print lst
	return numpy.array(lst)
