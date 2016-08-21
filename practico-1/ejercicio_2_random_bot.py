import numpy
import copy
import random
import sys
import math

# pesos de la funcion objetivo
w0 = 1.0
w1 = 1.0
w2 = 1.0
w3 = 1.0
w4 = 1.0
moderador = 0.0
randomBotIsBlack = True
won = 0
lost = 0
tie = 0

# booleano que indica si en el retorno se toma en cuenta o no
# la diferencia de fichas en el tablero final
consideringAmountDiff = True

# funcion objetivo siendo entrenada
def v(fichas_player, fichas_opponent, amenaza_player, amenaza_opponent):
	# amenaza_X es la cantidad de fichas X amenazadas por el contrario
	value = w0 + w1 * fichas_player + w2 * fichas_opponent + w3 * amenaza_player + w4 * amenaza_opponent
	return value

def printWeights():
	print "w0 = {}, w1 = {}, w2 = {}, w3 = {}, w4 = {}".format(w0, w1, w2, w3, w4)

# generacion de ejemplos de entrenamiento
def main():
	global w1, w2, w3, w4, won, lost, tie
	w1 = float(raw_input("Ingrese w1: "))
	w2 = float(raw_input("Ingrese w2: "))
	w3 = float(raw_input("Ingrese w3: "))
	w4 = float(raw_input("Ingrese w4: "))
	cantPartidas = int(raw_input("Ingrese la cantidad de partidas: "))
	for i in range(cantPartidas):
		# se obtiene un tablero inicial
		newBoard = getNewBoard()
		newBoard = playGame(newBoard)
		blackCheckerAmount = cantFichasColor(newBoard, True)
		whiteCheckerAmount = cantFichasColor(newBoard, False)
		if (blackCheckerAmount > whiteCheckerAmount):
			if (randomBotIsBlack):
				lost += 1
			else:
				won += 1
		elif (blackCheckerAmount < whiteCheckerAmount):
			if (randomBotIsBlack):
				won += 1
			else:
				lost += 1
		else:
			tie += 1
	printWeights()
	print "won = {}, lost = {}, tie = {}".format(won, lost, tie)


def printBoard(board):
    for i in range(len(board)):
        print board[i]
    print "##################"

# devuelve True si la ficha es amenazada por el contrario
#  sea que puede ser comida en el siguiente turno
def fichaAmenazada(position, board, isBlack):
    successors = getSuccessors(board, isBlack)
    if (isBlack):
        playerChecker = "B"
    else:
        playerChecker = "W"
    for s in successors:
        #si es comida en algun tablero sucesor
        if (s[position[0]][position[1]] != playerChecker):
            return True
    return False

# devuelve la cantidad de fichas de un color que se encuentran
# amenazadas por el contrario
def cantFichasAmenazadas(board, isBlack):
    cant = 0
    boardLength = len(board)
    if (isBlack):
        playerChecker = "B"
    else:
        playerChecker = "W"        
    for i in range(boardLength):
        for j in range(boardLength):
            if (board[i][j] == playerChecker and fichaAmenazada((i,j), board, isBlack)):
                cant += 1
    return cant
                
# devuelve la cantidad de fichas de un color
def cantFichasColor(board, isBlack):
    cant = 0
    boardLength = len(board)
    if (isBlack):
        playerChecker = "B"
    else:
        playerChecker = "W"    
    #assuming square board
    for i in range(boardLength):
        for j in range(boardLength):
            if (board[i][j] == playerChecker):
                cant += 1
    return cant

# devuelve True si la posicion pasada por parametro
# es legal para el tablero pasado por parametro
def checkLegalPosition(pos, board):
    #assuming square board
    return (pos[0] > -1 and pos[0] < len(board)) and (pos[1] > -1 and pos[1] < len(board))

# intercambia los contenidos de las celdas pasadas por parametro
# sobre el tablero pasado por parametro
def swapCellContents(initPos, endPos, board):
    board[initPos[0]][initPos[1]], board[endPos[0]][endPos[1]] = board[endPos[0]][endPos[1]], board[initPos[0]][initPos[1]]

# agrega un tablero a una lista de tableros, ambos pasados por parametro
def insertBoardInBoardList(board, boardList):
    if (not (board in boardList)):
        boardList.append(board)

# devuelve una lista de posibles tableros sucesores
# para un jugador en particular, dado un tablero
def getSuccessors(board, isBlack):
    boardList = []
    boardLength = len(board)
    if (isBlack):
        opponentChecker, playerChecker = "W", "B"
    else:
        opponentChecker, playerChecker = "B", "W"
    # se asume tablero cuadrado
    for i in range(boardLength):
        for j in range(boardLength):
            if (isBlack):
                # casilla superior izquierda
                # i indica la fila en la matriz y j la columna
                topLeft, topRight = (i-1, j-1), (i-1, j+1)
            else:
                topLeft, topRight = (i+1, j+1), (i+1, j-1)
            if (board[i][j] == playerChecker):
                if (checkLegalPosition(topLeft, board)):
                    # celda vacia
                    if (board[topLeft[0]][topLeft[1]] == "O"):
                        # se genera una nueva copia del tablero
                        newSuccessor = copy.deepcopy(board)
                        # se realiza el movimiento
                        swapCellContents((i,j), topLeft, newSuccessor)
                        insertBoardInBoardList(newSuccessor, boardList)
                    elif (board[topLeft[0]][topLeft[1]] == opponentChecker):
                        boardList = boardList + jumpEnemyChecker((i,j), topLeft, opponentChecker, board)
                # casilla superior derecha
                if (checkLegalPosition(topRight, board)):
                    # celda vacia
                    if (board[topRight[0]][topRight[1]] == "O"):
                        # se genera una nueva copia del tablero
                        newSuccessor = copy.deepcopy(board)
                        # se realiza el movimiento
                        swapCellContents((i,j), topRight, newSuccessor)
                        insertBoardInBoardList(newSuccessor, boardList)
                    elif (board[topRight[0]][topRight[1]] == opponentChecker):
                        boardList = boardList + jumpEnemyChecker((i,j), topRight, opponentChecker, board)
    return boardList

# asume que la siguiente celda (para la direccion determinada por
# las posiciones pasadas por parametro) es legal y tiene una ficha contraria
def jumpEnemyChecker(position, enemyCheckerPos, opponentChecker, board):
    # position es la posicion de la ficha del jugador
    # enemyCheckerPos la de la ficha enemiga
    # direccion vertical (filas)
    vDir = enemyCheckerPos[0] - position[0]
    # direccion horizontal (columnas)
    hDir = enemyCheckerPos[1] - position[1]
    boardList = []
    # posicion siguiente a la ficha enemiga, en misma direccion
    nextPos = (enemyCheckerPos[0] + vDir, enemyCheckerPos[1] + hDir)
    # aca ya se que en la siguiente celda hay una ficha enemiga
    # si la posicion siguiente a la ficha enemiga es legal y esta vacia
    if (checkLegalPosition(nextPos, board) 
        and board[nextPos[0]][nextPos[1]] == "O"):
        newBoard = copy.deepcopy(board)
        # muevo mi ficha comiendo a la otra
        swapCellContents(position, nextPos, newBoard)
        # vacio celda enemiga
        newBoard[enemyCheckerPos[0]][enemyCheckerPos[1]] = "O"
        # si es legal continuar moviendome hacia el lado contrario
        if (checkLegalPosition((nextPos[0] + vDir, nextPos[1]), newBoard)):
            # recursion para la direccion determinada por parametros
            leftPos = (nextPos[0] + vDir, nextPos[1] + hDir)
            if (checkLegalPosition(leftPos, newBoard)
                and newBoard[leftPos[0]][leftPos[1]] == opponentChecker):
                boardList = boardList + jumpEnemyChecker(nextPos, leftPos, opponentChecker, newBoard)
            # recursion para el otro
            rightPos = (nextPos[0] + vDir, nextPos[1] - hDir)
            if (checkLegalPosition(rightPos, newBoard)
                and newBoard[rightPos[0]][rightPos[1]] == opponentChecker):
                boardList = boardList + jumpEnemyChecker(nextPos, rightPos, opponentChecker, newBoard)
        # si resulta que no pude encadenar saltos (solo pude comer una ficha contraria)
        if (len(boardList) == 0):
            insertBoardInBoardList(newBoard, boardList)
    return boardList

# performance system

# la idea de esta funcion es pasarle a playGame un tablero inicial.
# dicha funcion devuelve un historial de las jugadas hechas por los dos jugadores.
def playGame(board):
	# contadores de partidas ganadas, perdidas y empatadas
	global won, lost, tied
	history = []
	blackCanMove = True
	whiteCanMove = True
	history.append(board)
	# printBoard(board)
	while True:
		# mueve el jugador de fichas negras
		if (randomBotIsBlack):
			successors = getSuccessors(board, True)
			succLength = len(successors)
			if (succLength > 0):
				pickRandom = int(math.floor(random.uniform(0, succLength)))
				nextBoard = successors[pickRandom]
			else:
				nextBoard = []
		else:
			nextBoard = move(True, board)
		if (whiteCanMove):
			if (len(nextBoard) != 0):
				board = nextBoard
				#guardar tablero previo en un historial
				history.append(board)
			else:
				blackCanMove = False
		else:# no hay mas movimientos para las fichas blancas (gana black)
			break
		# mueve el jugador de fichas negras
		if (blackCanMove):
			if (not randomBotIsBlack):
				successors = getSuccessors(board, False)
				succLength = len(successors)
				if (succLength > 0):
					pickRandom = int(math.floor(random.uniform(0, succLength)))
					nextBoard = successors[pickRandom]
				else:
					nextBoard = []				
			else:
				nextBoard = move(False, board)
			if (len(nextBoard) != 0):
				board = nextBoard
				# guardar board previa en un historial
				history.append(board)
			else:
				whiteCanMove = False
		else:# no hay mas movimientos para las fichas negras (gana white)
			break
		# printBoard(board)
	return board

def move(isBlack, board):
	if (isBlack):
		value = -sys.maxint - 1
	else:
		value = sys.maxint
	successors = getSuccessors(board, isBlack)
	nextBoard = []
	for s in successors:
		# uso funcion v refinada por generalizer
		sValue = v(cantFichasColor(s, True), 
			cantFichasColor(s, False),
			cantFichasAmenazadas(s, True),
			cantFichasAmenazadas(s, False))
		if (not isBlack): # juega en contra
			# elijo el tablero que menor valor aporte
			if (sValue < value):
				value = sValue
				nextBoard = s
			elif (sValue == value): # elige de manera aleatoria
				if (random.random() < 0.5):
					value = sValue
				# else se queda igual					
		else:
			if (sValue > value):
				value = sValue
				nextBoard = s
			elif (sValue == value): # elige de manera aleatoria
				if (random.random() < 0.5):
					value = sValue
				# else se queda igual
	return nextBoard

# experiment generator

def getNewBoard():
		#tablero inicial
	board = [
	    ["O", "W", "O", "W", "O", "W", "O", "W"],
	    ["W", "O", "W", "O", "W", "O", "W", "O"],
	    ["O", "W", "O", "W", "O", "W", "O", "W"],
	    ["O", "O", "O", "O", "O", "O", "O", "O"],
	    ["O", "O", "O", "O", "O", "O", "O", "O"],
	    ["B", "O", "B", "O", "B", "O", "B", "O"],
	    ["O", "B", "O", "B", "O", "B", "O", "B"],
	    ["B", "O", "B", "O", "B", "O", "B", "O"]
	    ]
	return board

main()