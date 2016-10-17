import datetime
import csv
import glob
from DataTypes import SquareType, GameStatus
from Board import Board
from Move import Move
from sklearn.neural_network import MLPRegressor
import numpy

def readLogs():
	filenames = glob.glob('./logs/*.csv')
	allMoves=[]
	for filename in filenames:
		file = open(filename, 'rb')
		reader = csv.reader(file)
		
		firstRow = next(reader)
		moves=[((int(firstRow[0]), int(firstRow[1])), firstRow[2], firstRow[3])]
		for row in reader:
			if (len(row) == 4):
				moves.append(((int(row[0]), int(row[1])), row[2], row[3]))
			# else:
				# moves.append(((row[0]), row[1], row[2]))
		allMoves.append(moves)
	return allMoves

def getWinningColor(game):	
	return 'BLACK' if (game[0][2] == 'GameStatus.BLACK_WINS') else 'WHITE'

def isMyMove(myColor, row):
	return (row[1]==myColor)

def excecuteMove(move, board):
	if (move[0]=='pass'):
		return
	col = SquareType.BLACK if move[1]=='BLACK' else SquareType.WHITE
	for square in board.get_squares_to_mark(Move(move[0][0], move[0][1]), move[1]):
		board.set_position(square[0], square[1], col)
		
def invertBoard(board):
	return [[(-(x-1)) if (x<2) else x for x in y] for y in board]
	
def getData(game,data):
	board = []
	board = Board(8,8)
	color = getWinningColor(game)
	for move in game:
		if isMyMove(color, move):
			boardAsMatrix=board.get_as_matrix()
			if (color=='WHITE'):
				boardAsMatrix=invertBoard(boardAsMatrix)
			data.append((boardAsMatrix, move[0]))
		excecuteMove(move, board)
	return data

def convert_matrix_board_to_nparray(board):
    lst = []
    for row in board:
        for element in row:
            lst.append(element)
    # print lst
    return numpy.array(lst)
	
gameHistory = readLogs()
data=[]

for game in gameHistory:
	getData(game,data)
	# fit(data)

clf = MLPRegressor(solver='lbfgs', activation='tanh', alpha=1e-4, hidden_layer_sizes=(44), random_state=1, learning_rate_init=.1)
X=numpy.array([convert_matrix_board_to_nparray(x[0]) for x in data])
y=[z[0] for z in [numpy.array(x[1]).reshape(1,-1) for x in data]]

clf.fit(X,y)

print y[12]
print clf.predict(X[12])

# 
# y=[[x[1] for x in y] for y in data]
# print '---'
# print X[0]
# print y
# print [[x[0], x[1]] for x in y]



		
		
