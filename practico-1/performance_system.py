import checkers
import sys

# checkers.printBoard(checkers.board)
# checkers.main()

w0 = 0
w1 = 2
w2 = -2
w3 = -1
w4 = 1

'''
La idea de este modulo es pasarle a playGame un tablero inicial.
Dicha funcion devuelve un historial de las jugadas hechas por los dos player.
'''

def v(fichas_B, fichas_W, amenaza_B, amenaza_W, isBlack):
	#amenaza_X es la cantidad de fichas X amenazadas por el contrario
	value = w0 + w1 * fichas_B + w2 * fichas_W + w3 * amenaza_B + w4 * amenaza_W
	if (isBlack):
		print "value = {} + {} * {} + {} * {} + {} * {} + {} * {} = {} ".format(w0, w1, fichas_B, w2, fichas_W, w3, amenaza_B, w4, amenaza_W, value)
		return value
	else:
		print "value = {} + {} * {} + {} * {} + {} * {} + {} * {} = {} ".format(w0, w1, fichas_B, w2, fichas_W, w3, amenaza_B, w4, amenaza_W, -value)
		return -value

def playGame(): #la idea es pasarle un board a este main
	history = []
	#TODO pasar esto por parametro
	blackCanMove = True
	whiteCanMove = True
	board = checkers.board
	history.append(board)
	print "Initial board"
	checkers.printBoard(board)
	while True:
		#black moves
		nextBoard = move(True, board)
		if (len(nextBoard) != 0):
			board = nextBoard
			#guardar board previa en un historial
			history.append(board)
		else:
			blackCanMove = False
		#white moves
		nextBoard = move(False, board)
		if (len(nextBoard) != 0):
			board = nextBoard
			#guardar board previa en un historial
			history.append(board)
		else:
			whiteCanMove = False
		# newBoard = []
		if (not blackCanMove and not whiteCanMove): #no hay mas movimientos
			break
	return history

def move(isBlack, board):
	#min int
	value = -sys.maxint - 1
	successors = checkers.getSuccessors(board, isBlack)
	nextBoard = []
	print "gonna pick between"
	for s in successors:
		sValue = v(checkers.cantFichasColor(s, True), 
			checkers.cantFichasColor(s, False),
			checkers.cantFichasAmenazadas(s, True),
			checkers.cantFichasAmenazadas(s, False),
			isBlack)
		print "or"
		if (sValue > value):
			value = sValue
			nextBoard = s	
	return nextBoard

history = playGame()
print "Historial"
for board in history:
	checkers.printBoard(board)