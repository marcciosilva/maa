import numpy
import copy

def printBoard(board):
    for i in range(len(board)):
        print board[i]

#B for black
#W for white
#O for empty
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

# def moveTo(initPos, endPos, board, black):
#     if (checkLegalPosition(initPos, board) and checkLegalPosition(endPos, board)):
#         horizontalDistance = abs(initPos[0] - endPos[0])
#         verticalDistance = initPos[1] - endPos[1]
#         endSymbol = board[endPos[0]][endPos[1]]
#         initSymbol = board[initPos[0]][initPos[1]]
#         if (black):
#             #move to empty cell
#             if (initSymbol == "B" and endSymbol == "O"):
#                 #movement is in correct sense
#                 if (horizontalDistance == 1 and verticalDistance == -1):
#                     swapCellContents(initPos, endPos, board)
#                     printMovement(initPos, endPos)
#                 else:
#                     printNotLegal()
#             #move to occupied cell
#             elif (initSymbol == "B" and endSymbol == "W"):
#                 #check if checker can be conquered

#                 if (checkLegalPosition())
#             else:
#                 printNotLegal()
#         elif (not black):
#             #move to empty cell
#             if (initSymbol == "W" and endSymbol == "O"):
#                 #movement is in correct sense
#                 if (horizontalDistance == 1 and verticalDistance == 1):
#                     #swap cell contents
#                     swapCellContents(initPos, endPos, board)
#                     printMovement(initPos, endPos)                    
#                 else:
#                     printNotLegal()
#                         #move to occupied cell
#             elif (initSymbol == "B" and endSymbol == "W"):
#                 #check if checker can be conquered
#                 if (checkLegalPosition())
#             else:
#                 printNotLegal()
#     return board

#returns list of possible outcome boards
#empty if equal (?)
def getSuccessors(board, isBlack):
    boardList = []
    boardLength = len(board)
    #assuming square board
    for i in range(boardLength):
        for j in range(boardLength):
            #if black checker
            if (board[i][j] == "B"):
                #top left
                #i indica la fila en la matriz y j la columna
                topLeft = (i-1, j-1)
                topRight = (i-1, j+1)
                if (checkLegalPosition(topLeft, board)):
                    #empty cell
                    if (board[topLeft[0]][topLeft[1]] == "O"):
                        #make new copy of board
                        newSuccessor = copy.deepcopy(board)
                        #make the move
                        swapCellContents((i,j), topLeft, newSuccessor)
                        insertBoardInBoardList(newSuccessor, boardList)
                    # elif (board[topLeft[0]][topLeft[1]] == "W"):
                    #     #check if next in line is empty
                    #     pass
                    # else:
                    #     pass
                #top right
                if (checkLegalPosition(topRight, board)):
                    #empty cell
                    if (board[topRight[0]][topRight[1]] == "O"):
                        #make new copy of board
                        newSuccessor = copy.deepcopy(board)
                        #make the move
                        swapCellContents((i,j), topRight, newSuccessor)
                        insertBoardInBoardList(newSuccessor, boardList)
                    # elif (board[topRight[0]][topRight[1]] == "W"):
                    #     #check if next in line is empty
                    #     pass
    return boardList


#(en un while capaz rinde, onda 
#while checkLegalPosition(posicion siguiente en el sentido que se viene) 
#and hayFichaContraria o algo asi)

"""
pseudocodigo para comer fichas
me pasas una ficha y el tipo y yo intento comer

para cada lado
    si la posicion de desp de la siguiente ficha es legal y ademas esta vacia Y
    si hay una ficha contraria para el lado que miro
        hago los swaps y bla y dejo la ficha en el nuevo lugar
    sino
        agrego esa board a la boardList de resultado
retorno la boardList de resultado (que perfectamente puede ser vacia)


"""

#deberia usar un set para las boards posibles, en caso de que alguna se repita


print board == copy.deepcopy(board)


printBoard(board)
print "Getting successors for black player..."
print("####################################")
boardList = getSuccessors(board, True)
for member in boardList:
    printBoard(member)
    print("####################################")