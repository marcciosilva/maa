import datetime
import csv
import glob
from DataTypes import SquareType, GameStatus
from Board import Board
from Move import Move

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
			else:
				moves.append(((row[0]), row[1]))
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

def getData(game):
	board = []
	board = Board(8,8)
	data=[]
	color = getWinningColor(game)
	print color
	for move in game:
		if isMyMove(color, move):
			data.append((board.get_as_matrix(), move[0]))
		excecuteMove(move, board)
	return data
	
myColor='BLACK'
gameHistory = readLogs()
data=[]
for game in gameHistory:
	data.append(getData(game))
	# fit(data)
print data
		
		
