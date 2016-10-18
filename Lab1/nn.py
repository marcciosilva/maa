import datetime
import csv
import glob
import math
from DataTypes import SquareType, GameStatus
from Board import Board
from Move import Move
from sklearn.neural_network import MLPRegressor
from sklearn.externals import joblib
import numpy

# Genera una lista de listas, donde cada lista interna
# corresponde con los movimientos de una partida en particular.

def readLogs():
	filenames = glob.glob('./logs' + str(gameAmount) + '/*.csv')
	allMoves=[]
	for filename in filenames:
		file = open(filename, 'rb')
		reader = csv.reader(file)

		moves=[]
		for row in reader:
			if (len(row) == 4):
				moves.append(((int(row[0]), int(row[1])), row[2], row[3]))
		allMoves.append(moves)
		file.close
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
		matrix = board.get_as_matrix()
		if isMyMove(color, move):
			boardAsMatrix=board.get_as_matrix()
			if (color=='WHITE'):
				boardAsMatrix=invertBoard(boardAsMatrix)
			movem = numpy.zeros((8,8))
			movem[move[0][0]][move[0][1]]=1000
			data.append((boardAsMatrix, movem))
		excecuteMove(move, board)
	return data

def convert_matrix_board_to_nparray(board):
	lst = []
	for row in board:
		for element in row:
			lst.append(element)
	# print lst
	return numpy.array(lst)
	
gameAmount = 10000
hiddenLayerSize = int(math.ceil(gameAmount / (1.0 * (64 + 2))))

print str(hiddenLayerSize) + ' hidden layers.'

gameHistory = readLogs()
data=[]

for game in gameHistory:
	getData(game,data)
	# fit(data)

if (gameAmount >= 1000):
	clf = MLPRegressor(solver='adam', activation='identity', alpha=1e-4, 
	hidden_layer_sizes=(hiddenLayerSize), learning_rate_init=.01, max_iter=300)
else:
	clf = MLPRegressor(solver='lbfgs', activation='tanh', alpha=1e-4, 
	hidden_layer_sizes=(hiddenLayerSize), learning_rate_init=.1)
X=numpy.array([convert_matrix_board_to_nparray(x[0]) for x in data])
y=[z[0] for z in [numpy.array(x[1]).reshape(1,-1) for x in data]]

clf.fit(X,y)

print clf.predict(X[10])

joblib.dump(clf, 'red-neuronal-test-' + str(gameAmount) + '-partidas.pkl')

# 
# y=[[x[1] for x in y] for y in data]
# print '---'
# print X[0]
# print y
# print [[x[0], x[1]] for x in y]



		
		
