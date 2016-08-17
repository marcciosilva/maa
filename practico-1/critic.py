import experiment_generator
import performance_system
import generalizer
import checkers
import random

def generateTrainingExamples():
	#init wi
	if (generalizer.w0 == -1.0):
		generalizer.w0 = random.random()
	if (generalizer.w1 == -1.0):
		generalizer.w1 = random.random()
	if (generalizer.w2 == -1.0):
		generalizer.w2 = random.random()
	if (generalizer.w3 == -1.0):
		generalizer.w3 = random.random()
	if (generalizer.w4 == -1.0):
		generalizer.w4 = random.random()
	if (generalizer.moderador == 0.0):
		generalizer.moderador = 0.01
	newBoard = experiment_generator.getNewBoard()
	history = performance_system.playGame(newBoard)
	# for board in history:
	# 	checkers.printBoard(board)
	trainingExamples = []
	for board in history:
		index = history.index(board)
		next_board = history[index+1] if index + 1 < len(history) else None
		if (next_board == None): #tablero final
			blackCheckerAmount = checkers.cantFichasColor(board, True)
			whiteCheckerAmount = checkers.cantFichasColor(board, False)
			diff = blackCheckerAmount - whiteCheckerAmount
			#mas fichas negras que blancas
			if (blackCheckerAmount > whiteCheckerAmount):
				trainingExamples.append((board, diff * 100))
			#mas fichas blancas que negras
			elif (whiteCheckerAmount > blackCheckerAmount):
				trainingExamples.append((board, diff * 100))
			#empate
			else:
				trainingExamples.append((board, 0))
		else:
			x1 = checkers.cantFichasColor(next_board, True)
			x2 = checkers.cantFichasColor(next_board, False)
			x3 = checkers.cantFichasAmenazadas(next_board, True)
			x4 = checkers.cantFichasAmenazadas(next_board, False)
			trainingExamples.append((board, generalizer.v(x1, x2, x3, x4)))
	return trainingExamples