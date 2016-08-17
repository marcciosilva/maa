import numpy
import copy

'''
Este modulo es una utilidad para manejar tableros de damas y obtener
tableros sucesores a partir de un tablero actual.
Se asume que los tableros son cuadrados (el tablero estandar de damas
es de 8 x 8).
'''

def printBoard(board):
    for i in range(len(board)):
        print board[i]
    print "##################"

#B for black
#W for white
#O for empty

#tablero inicial
# board = [
#     ["O", "W", "O", "W", "O", "W", "O", "W"],
#     ["W", "O", "W", "O", "W", "O", "W", "O"],
#     ["O", "W", "O", "W", "O", "W", "O", "W"],
#     ["O", "O", "O", "O", "O", "O", "O", "O"],
#     ["O", "O", "O", "O", "O", "O", "O", "O"],
#     ["B", "O", "B", "O", "B", "O", "B", "O"],
#     ["O", "B", "O", "B", "O", "B", "O", "B"],
#     ["B", "O", "B", "O", "B", "O", "B", "O"]
#     ]

#juego corto
board = [
    ["O", "O", "O", "O", "O", "O", "O", "O"],
    ["O", "O", "O", "O", "O", "O", "O", "O"],    
    ["O", "O", "O", "O", "O", "O", "O", "O"],
    ["O", "O", "O", "O", "O", "O", "O", "O"],
    ["O", "O", "O", "W", "O", "O", "O", "O"],
    ["O", "O", "B", "O", "O", "O", "O", "O"],
    ["O", "O", "O", "O", "O", "O", "O", "O"],
    ["O", "O", "O", "O", "O", "O", "O", "O"]
    ]

#tablero en donde las negras pueden comer una blanca
# board = [
#     ["O", "W", "O", "W", "O", "W", "O", "W"],
#     ["W", "O", "W", "O", "W", "O", "W", "O"],
#     ["O", "W", "O", "O", "O", "O", "O", "W"],
#     ["O", "O", "O", "O", "W", "O", "W", "O"],
#     ["O", "B", "O", "B", "O", "O", "O", "O"],
#     ["O", "O", "B", "O", "O", "O", "B", "O"],
#     ["O", "B", "O", "B", "O", "B", "O", "B"],
#     ["B", "O", "B", "O", "B", "O", "B", "O"]
#     ]

#comida simple
# board = [
#     ["O", "O", "O", "O", "O", "O", "O", "O"],
#     ["O", "O", "O", "O", "O", "O", "O", "O"],
#     ["O", "O", "O", "O", "O", "O", "O", "O"],
#     ["O", "O", "O", "O", "W", "O", "O", "O"],
#     ["O", "O", "O", "B", "O", "O", "O", "O"],
#     ["O", "O", "O", "O", "O", "O", "O", "O"],
#     ["O", "O", "O", "O", "O", "O", "O", "O"],
#     ["O", "O", "O", "O", "O", "O", "O", "O"]
#     ]

#comida doble
# board = [
#     ["O", "O", "O", "O", "O", "O", "O", "O"],
#     ["O", "O", "O", "O", "O", "O", "W", "O"],
#     ["O", "O", "O", "O", "O", "O", "O", "O"],
#     ["O", "O", "O", "O", "W", "O", "W", "O"],
#     ["O", "O", "O", "O", "O", "O", "O", "O"],
#     ["O", "O", "O", "O", "W", "O", "O", "O"],
#     ["O", "O", "O", "B", "O", "O", "O", "O"],
#     ["O", "O", "O", "O", "O", "O", "O", "O"]
#     ]

#white action
# board = [
#     ["O", "O", "O", "O", "O", "O", "O", "O"],
#     ["O", "O", "O", "O", "O", "O", "O", "O"],
#     ["O", "O", "O", "O", "O", "O", "O", "O"],
#     ["O", "O", "O", "O", "W", "O", "O", "O"],
#     ["O", "O", "O", "B", "O", "O", "O", "O"],
#     ["O", "O", "O", "O", "O", "O", "O", "O"],
#     ["O", "O", "O", "O", "O", "O", "O", "O"],
#     ["O", "O", "O", "O", "O", "O", "O", "O"]
#     ]

#white double
# board = [
#     ["O", "O", "O", "O", "O", "O", "O", "O"],
#     ["O", "O", "O", "O", "O", "O", "O", "O"],
#     ["O", "O", "O", "O", "O", "O", "O", "O"],
#     ["O", "O", "O", "O", "W", "O", "O", "O"],
#     ["O", "O", "O", "B", "O", "B", "O", "O"],
#     ["O", "O", "O", "O", "O", "O", "O", "O"],
#     ["O", "O", "O", "B", "O", "O", "O", "O"],
#     ["O", "O", "O", "O", "O", "O", "O", "O"]
#     ]

#devuelve True si la ficha es amenazada por el contrario
#o sea que puede ser comida en el siguiente turno
def fichaAmenazada(position, board, isBlack):
    successors = getSuccessors(board, isBlack)
    if (isBlack):
        playerChecker = "B"
    else:
        playerChecker = "W"
    for s in successors:
        #si es comida en algun sucesor
        if (s[position[0]][position[1]] != playerChecker):
            return True
    return False

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

def printNotLegal():
    print "Movement is not legal"

def checkLegalPosition(pos, board):
    #assuming square board
    return (pos[0] > -1 and pos[0] < len(board)) and (pos[1] > -1 and pos[1] < len(board))

def swapCellContents(initPos, endPos, board):
    board[initPos[0]][initPos[1]], board[endPos[0]][endPos[1]] = board[endPos[0]][endPos[1]], board[initPos[0]][initPos[1]]

def printMovement(initPos, endPos):
    print "Moved {} to {}".format(initPos, endPos)

def insertBoardInBoardList(board, boardList):
    if (not (board in boardList)):
        boardList.append(board)

#returns list of possible outcome boards
def getSuccessors(board, isBlack):
    boardList = []
    boardLength = len(board)
    if (isBlack):
        opponentChecker, playerChecker = "W", "B"
    else:
        opponentChecker, playerChecker = "B", "W"
    #assuming square board
    for i in range(boardLength):
        for j in range(boardLength):
            if (isBlack):
                #top left
                #i indica la fila en la matriz y j la columna
                topLeft, topRight = (i-1, j-1), (i-1, j+1)
            else:
                topLeft, topRight = (i+1, j+1), (i+1, j-1)
            if (board[i][j] == playerChecker):
                if (checkLegalPosition(topLeft, board)):
                    #empty cell
                    if (board[topLeft[0]][topLeft[1]] == "O"):
                        #make new copy of board
                        newSuccessor = copy.deepcopy(board)
                        #make the move
                        swapCellContents((i,j), topLeft, newSuccessor)
                        insertBoardInBoardList(newSuccessor, boardList)
                    elif (board[topLeft[0]][topLeft[1]] == opponentChecker):
                        boardList = boardList + jumpEnemyChecker((i,j), topLeft, opponentChecker, board)
                #top right
                if (checkLegalPosition(topRight, board)):
                    #empty cell
                    if (board[topRight[0]][topRight[1]] == "O"):
                        #make new copy of board
                        newSuccessor = copy.deepcopy(board)
                        #make the move
                        swapCellContents((i,j), topRight, newSuccessor)
                        insertBoardInBoardList(newSuccessor, boardList)
                    elif (board[topRight[0]][topRight[1]] == opponentChecker):
                        boardList = boardList + jumpEnemyChecker((i,j), topRight, opponentChecker, board)
    return boardList

#asume que la siguiente celda (para el lado que se ponga por parametro) es legal
#y tiene una ficha contraria
def jumpEnemyChecker(position, enemyCheckerPos, opponentChecker, board):
    #position es la posicion de la ficha del jugador
    #enemyCheckerPos la de la ficha enemiga
    #vertical direction (rows)
    vDir = enemyCheckerPos[0] - position[0]
    #horizontal direction (columns)
    hDir = enemyCheckerPos[1] - position[1]
    boardList = []
    #posicion siguiente a la ficha enemiga, en misma direccion
    nextPos = (enemyCheckerPos[0] + vDir, enemyCheckerPos[1] + hDir)
    #aca ya se que en la siguiente celda hay una ficha enemiga
    #si la posicion siguiente a la ficha enemiga es legal y esta vacia
    if (checkLegalPosition(nextPos, board) 
        and board[nextPos[0]][nextPos[1]] == "O"):
        newBoard = copy.deepcopy(board)
        #muevo mi ficha comiendo a la otra
        swapCellContents(position, nextPos, newBoard)
        #vacio celda enemiga
        newBoard[enemyCheckerPos[0]][enemyCheckerPos[1]] = "O"
        #si es legal continuar moviendome hacia el lado contrario
        if (checkLegalPosition((nextPos[0] + vDir, nextPos[1]), newBoard)):
            #recursion para el lado que vino (le pongo left because fuck you)
            leftPos = (nextPos[0] + vDir, nextPos[1] + hDir)
            if (checkLegalPosition(leftPos, newBoard)
                and newBoard[leftPos[0]][leftPos[1]] == opponentChecker):
                boardList = boardList + jumpEnemyChecker(nextPos, leftPos, opponentChecker, newBoard)
            #recursion para el otro
            rightPos = (nextPos[0] + vDir, nextPos[1] - hDir)
            if (checkLegalPosition(rightPos, newBoard)
                and newBoard[rightPos[0]][rightPos[1]] == opponentChecker):
                boardList = boardList + jumpEnemyChecker(nextPos, rightPos, opponentChecker, newBoard)
        #si resulta que no pude encadenar saltos (solo pude comer una ficha contraria)
        if (len(boardList) == 0):
            insertBoardInBoardList(newBoard, boardList)
    return boardList

def main():
    print "Initial board"
    printBoard(board)
    print "Getting successors for white player..."
    print("####################################")
    boardList = getSuccessors(board, False)
    for member in boardList:
        printBoard(member)
        print("####################################")