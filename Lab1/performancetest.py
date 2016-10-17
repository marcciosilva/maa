import datetime
import csv
import glob
from DataTypes import SquareType, GameStatus
from Board import Board
from Move import Move
from sklearn.neural_network import MLPRegressor
from sklearn.externals import joblib
import numpy

# Genera una lista de listas, donde cada lista interna
# corresponde con los movimientos de una partida en particular.

def readLogs():
	filenames = glob.glob('./logs-performance-' + str(gameAmount) + '/*.csv')
	allMoves=[]
	for filename in filenames:
		file = open(filename, 'rb')
		reader = csv.reader(file)

		moves=[]
		for row in reader:
			if (len(row) == 4):
				moves.append(((int(row[0]), int(row[1])), row[2], row[3]))
		allMoves.append(moves)
	return allMoves

def getWinningColor(game):	
	return 'BLACK' if (game[0][2] == 'GameStatus.BLACK_WINS') else 'WHITE'

gameAmount = 3000
gameHistory = readLogs()
gamesWon = 0.0
for game in gameHistory:
	winningColor = getWinningColor(game)
	if (winningColor == 'BLACK'):
		gamesWon += 1
print gamesWon
print len(gameHistory)
print 'Porcentaje de partidas ganadas para una red entrenada con ' + str(gameAmount) + ' partidas: ' + str((gamesWon / len(gameHistory)) * 100) + '%'