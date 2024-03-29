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

# contadores de partidas ganadas, perdidas y empatadas
won = 0
lost = 0
tied = 0

# historial de pesos de funcion objetivo
listaWeights = []

# booleano que indica si en el retorno se toma en cuenta o no
# la diferencia de fichas en el tablero final
consideringAmountDiff = True

# funcion objetivo siendo entrenada
def v(fichas_player, fichas_opponent, amenaza_player, amenaza_opponent):
	# amenaza_X es la cantidad de fichas X amenazadas por el contrario
	value = w0 + w1 * fichas_player + w2 * fichas_opponent + w3 * amenaza_player + w4 * amenaza_opponent
	return value

def lms(trainingExamples): #ajusta coeficientes
	# el entrenamiento se hace solo desde el punto de vista del jugador
	# de fichas negras
	# aunque despues esa misma funcion se usa para simular los movimientos
	# del jugador de fichas blancas
	global w1, w2, w3, w4
	for example in trainingExamples:
		vtrain = example[1]
		board = example[0]
		x1 = cantFichasColor(board, True)
		x2 = cantFichasColor(board, False)
		x3 = cantFichasAmenazadas(board, True)
		x4 = cantFichasAmenazadas(board, False)
		vcurrent = v(x1, x2, x3, x4)
		w1 += moderador * (vtrain - vcurrent) * x1
		w2 += moderador * (vtrain - vcurrent) * x2
		w3 += moderador * (vtrain - vcurrent) * x3
		w4 += moderador * (vtrain - vcurrent) * x4

def printWeights():
	print "w0 = {}, w1 = {}, w2 = {}, w3 = {}, w4 = {}".format(w0, w1, w2, w3, w4)

def main():
	# inicializacion de pesos
	randomrange = raw_input("Ingrese el valor absoluto de uno de los extremos del intervalo del cual se tomaran wi aleatorios: ")
	global w1, w2, w3, w4, moderador, won, lost, tied
	# se inicializan los pesos en base a la entrada del usuario
	w1 = random.uniform(-float(randomrange), float(randomrange))
	w2 = random.uniform(-float(randomrange), float(randomrange))
	w3 = random.uniform(-float(randomrange), float(randomrange))
	w4 = random.uniform(-float(randomrange), float(randomrange))
	# se agrega el valor inicial de los pesos a una estructura
	# encargada de mantener un historial de los mismos
	listaWeights.append((w1, w2, w3, w4))
	moderador = float(raw_input("Ingrese el valor del moderador (ej.: 0.001): "))
	gameAmount = int(raw_input("Ingrese la cantidad de partidas a jugar: "))
	for i in range(gameAmount):
		# se generan ejemplos de entrenamiento
		trainingExamples = generateTrainingExamples()
		# se ajustan los pesos utilizando LMS
		lms(trainingExamples)
		listaWeights.append((w1, w2, w3, w4))
	# impresion de historial de pesos a un formato graficable en latex
	# w1
	print "won = {}, lost = {}, tied = {}".format(won, lost, tied)
	print "###### w1 ######"
	print "coordinates {"
	for index, tupla in enumerate(listaWeights):
		print (index, tupla[0]),
	print
	print "};"
	print
	# w2
	print "###### w2 ######"
	print "coordinates {"
	for index, tupla in enumerate(listaWeights):
		print (index, tupla[1]),
	print
	print "};"
	print
	# w3
	print "###### w3 ######"
	print "coordinates {"
	for index, tupla in enumerate(listaWeights):
		print (index, tupla[2]),
	print
	print "};"
	print
	# w4
	print "###### w4 ######"
	print "coordinates {"
	for index, tupla in enumerate(listaWeights):
		print (index, tupla[3]),
	print
	print "};"

# generacion de ejemplos de entrenamiento
def generateTrainingExamples():
	# se obtiene un tablero inicial
	newBoard = getNewBoard()
	# se simula la realizacion de la partida
	history = playGame(newBoard)
	# aqui se guardaran los ejemplos de entrenamiento (tablero, valoracion)
	trainingExamples = []
	for board in history:
		# printBoard(board)
		index = history.index(board)
		next_board = history[index+1] if index + 1 < len(history) else None
		if (next_board == None): #tablero final
			blackCheckerAmount = cantFichasColor(board, True)
			whiteCheckerAmount = cantFichasColor(board, False)
			if (consideringAmountDiff):
				diff = blackCheckerAmount - whiteCheckerAmount
				# coeficiente de la funcion interpolada en base a los puntos de la forma
				# (diff, value): {(-12,-100),(-6,-50),(0,0),(6,50),(12,100)}
				# Se asigna un puntaje en base a la diferencia de fichas
				coefficient = 25.0 / 3
				trainingExamples.append((board, diff * coefficient))
			else:
				# Aqui se asigna puntaje en base a si se gano, perdio o empato
				if (blackCheckerAmount > whiteCheckerAmount):
					trainingExamples.append((board, 100))
				elif (whiteCheckerAmount > blackCheckerAmount):
					trainingExamples.append((board, -100))
				else:
					trainingExamples.append((board, 0))
		else:
			# si el tablero no es final, se le asigna como valor
			# el valor del siguiente tablero
			x1 = cantFichasColor(next_board, True)
			x2 = cantFichasColor(next_board, False)
			x3 = cantFichasAmenazadas(next_board, True)
			x4 = cantFichasAmenazadas(next_board, False)
			value = v(x1, x2, x3, x4)
			trainingExamples.append((board, value))
	return trainingExamples

# utilidades de manejo de tablero

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
	while True:
		# mueve el jugador de fichas negras
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
			nextBoard = move(False, board)
			if (len(nextBoard) != 0):
				board = nextBoard
				# guardar board previa en un historial
				history.append(board)
			else:
				whiteCanMove = False
		else:# no hay mas movimientos para las fichas negras (gana white)
			break
	if (len(history) > 0):
		# se actualizan contadores de partidas jugadas
		blackAmount = cantFichasColor(history[-1], True)
		whiteAmount = cantFichasColor(history[-1], False)
		if (blackAmount > whiteAmount):
			won += 1
		elif (blackAmount < whiteAmount):
			lost += 1
		else:
			tied += 1
	return history

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


	# amountOfBoards = 4
	# boardChoice = math.floor(random.random() * amountOfBoards)
	# if (boardChoice == 0):
	# 	#tablero inicial
	# 	board = [
	# 	    ["O", "W", "O", "W", "O", "W", "O", "W"],
	# 	    ["W", "O", "W", "O", "W", "O", "W", "O"],
	# 	    ["O", "W", "O", "W", "O", "W", "O", "W"],
	# 	    ["O", "O", "O", "O", "O", "O", "O", "O"],
	# 	    ["O", "O", "O", "O", "O", "O", "O", "O"],
	# 	    ["B", "O", "B", "O", "B", "O", "B", "O"],
	# 	    ["O", "B", "O", "B", "O", "B", "O", "B"],
	# 	    ["B", "O", "B", "O", "B", "O", "B", "O"]
	# 	    ]
	# elif (boardChoice == 1):
	# 	#comida doble
	# 	board = [
	# 	    ["O", "O", "O", "O", "O", "O", "O", "O"],
	# 	    ["O", "O", "O", "O", "O", "O", "W", "O"],
	# 	    ["O", "O", "O", "O", "O", "O", "O", "O"],
	# 	    ["O", "O", "O", "O", "W", "O", "W", "O"],
	# 	    ["O", "O", "O", "O", "O", "O", "O", "O"],
	# 	    ["O", "O", "O", "O", "W", "O", "O", "O"],
	# 	    ["O", "O", "O", "B", "O", "O", "O", "O"],
	# 	    ["O", "O", "O", "O", "O", "O", "O", "O"]
	# 	    ]
	# elif (boardChoice == 2):
	# 	#tablero en donde las negras pueden comer una blanca
	# 	board = [
	# 	    ["O", "W", "O", "W", "O", "W", "O", "W"],
	# 	    ["W", "O", "W", "O", "W", "O", "W", "O"],
	# 	    ["O", "W", "O", "O", "O", "O", "O", "W"],
	# 	    ["O", "O", "O", "O", "W", "O", "W", "O"],
	# 	    ["O", "B", "O", "B", "O", "O", "O", "O"],
	# 	    ["O", "O", "B", "O", "O", "O", "B", "O"],
	# 	    ["O", "B", "O", "B", "O", "B", "O", "B"],
	# 	    ["B", "O", "B", "O", "B", "O", "B", "O"]
	# 	    ]
	# elif (boardChoice == 3):
	# 	board = [
	# 	    ["O", "W", "O", "W", "O", "W", "O", "W"],
	# 	    ["W", "O", "W", "O", "W", "O", "W", "O"],
	# 	    ["O", "W", "O", "O", "O", "W", "O", "W"],
	# 	    ["O", "O", "O", "O", "O", "O", "O", "O"],
	# 	    ["O", "B", "O", "B", "O", "O", "O", "O"],
	# 	    ["O", "O", "B", "O", "O", "O", "W", "O"],
	# 	    ["O", "B", "O", "B", "O", "B", "O", "B"],
	# 	    ["B", "O", "B", "O", "B", "O", "B", "O"]
	# 	    ]	    
	return board

main()