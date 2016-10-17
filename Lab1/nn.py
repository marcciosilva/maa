import datetime
import csv
import glob
from DataTypes import SquareType, GameStatus
from Board import Board
from Move import Move
def readLogs(color):
	filenames = glob.glob('./logs/*.csv')
	allMoves=[]
	for filename in filenames:
		file = open(filename, 'rb')
		reader = csv.reader(file)
		
		firstRow = next(reader)
		if IWon(color, firstRow):
			moves=[((int(firstRow[0]), int(firstRow[1])), firstRow[2])]
			for row in reader:
				if (len(row) == 4):
					moves.append(((int(row[0]), int(row[1])), row[2]))
				else:
					moves.append(((row[0]), row[1]))
		allMoves.append(moves)
	return allMoves


def IWon(myColor, row):
	winStatus = 'GameStatus.BLACK_WINS' if (myColor=='BLACK') else 'GameStatus.WHITE_WINS'
	return row[3]==winStatus

def isMyMove(myColor, row):
	return (row[1]==myColor)

def excecuteMove(move, board):
	if (move[0]=='pass'):
		return
	col = SquareType.BLACK if move[1]=='BLACK' else SquareType.WHITE
	for square in board.get_squares_to_mark(Move(move[0][0], move[0][1]), move[1]):
		board.set_position(square[0], square[1], col)

def getData(game, myColor):
	board = []
	board = Board(8,8)
	data=[]
	for move in game:
		if isMyMove(myColor, move):
			data.append((board.get_as_matrix(), move[0]))
		excecuteMove(move, board)
	return data
	
myColor='BLACK'
gameHistory = readLogs(myColor)
for game in gameHistory:
	data=getData(game, myColor)
	# fit(data)
print data	
		
		
