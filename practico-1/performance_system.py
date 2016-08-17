import checkers
import experiment_generator
import sys
import random

'''
La idea de este modulo es pasarle a playGame un tablero inicial.
Dicha funcion devuelve un historial de las jugadas hechas por los dos player.
'''

def playGame(board): #la idea es pasarle un board a este main
	history = []
	#TODO pasar esto por parametro
	blackCanMove = True
	whiteCanMove = True
	history.append(board)
	# print "Initial board"
	# checkers.printBoard(board)
	while True:
		#black moves
		nextBoard = move(True, board)
		if (whiteCanMove):
			if (len(nextBoard) != 0):
				board = nextBoard
				#guardar board previa en un historial
				history.append(board)
			else:
				blackCanMove = False
		else:#no hay mas movimientos para las fichas blancas (gana black)
			break
		#white moves
		if (blackCanMove):
			nextBoard = move(False, board)
			if (len(nextBoard) != 0):
				board = nextBoard
				#guardar board previa en un historial
				history.append(board)
			else:
				whiteCanMove = False
		else:#no hay mas movimientos para las fichas negras (gana white)
			break
	return history

def move(isBlack, board):
	#min int
	value = -sys.maxint - 1
	successors = checkers.getSuccessors(board, isBlack)
	nextBoard = []
	for s in successors:
		#uso funcion v refinada por generalizer
		import generalizer
		sValue = generalizer.v(checkers.cantFichasColor(s, True), 
			checkers.cantFichasColor(s, False),
			checkers.cantFichasAmenazadas(s, True),
			checkers.cantFichasAmenazadas(s, False))
		if (not isBlack): #juega en contra obviamente
			if (sValue < value):
				value = sValue
				nextBoard = s
			elif (sValue == value): #choose randomly
				if (random.random() < 0.5):
					value = sValue
				#else se queda igual					
		else:
			if (sValue > value):
				value = sValue
				nextBoard = s
			elif (sValue == value): #choose randomly
				if (random.random() < 0.5):
					value = sValue
				#else se queda igual

	return nextBoard

# history = playGame(experiment_generator.getNewBoard())
# print "Historial"
# for board in history:
# 	checkers.printBoard(board)