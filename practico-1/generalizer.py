import performance_system
import experiment_generator
import checkers
import random
'''
La idea de este modulo es recibir ejemplos de entrenamiento y refinar la hipotesis
'''

w0 = -1.0
w1 = -1.0
w2 = -1.0
w3 = -1.0
w4 = -1.0
moderador = 0.0

def v(fichas_player, fichas_opponent, amenaza_player, amenaza_opponent):
	#amenaza_X es la cantidad de fichas X amenazadas por el contrario
	value = w0 + w1 * fichas_player + w2 * fichas_opponent 
	+ w3 * amenaza_player + w4 * amenaza_opponent
	return value
	# if (isBlack):
	# 	print "value = {} + {} * {} + {} * {} + {} * {} + {} * {} = {} ".format(w0, w1, fichas_B, w2, fichas_W, w3, amenaza_B, w4, amenaza_W, value)
	# 	return value
	# else:
	# 	print "value = {} + {} * {} + {} * {} + {} * {} + {} * {} = {} ".format(w0, w1, fichas_B, w2, fichas_W, w3, amenaza_B, w4, amenaza_W, -value)
	# 	return -value

def lms(trainingExamples): #ajusta coeficientes
	#el entrenamiento lo hago solo desde el punto de vista del jugador
	#de fichas negras
	#aunque despues esa misma funcion se usa para simular los movimientos
	#del jugador de fichas blancas
	global w1, w2, w3, w4
	for example in trainingExamples:
		vtrain = example[1]
		board = example[0]
		x1 = checkers.cantFichasColor(board, True)
		x2 = checkers.cantFichasColor(board, False)
		x3 = checkers.cantFichasAmenazadas(board, True)
		x4 = checkers.cantFichasAmenazadas(board, False)
		vcurrent = v(x1, x2, x3, x4)
		# print "vtrain = {}".format(vtrain)
		# print "vcurrent = {}".format(vcurrent)
		# print "w0 = {}, w1 = {}, w2 = {}, w3 = {}, w4 = {}".format(w0, w1, w2, w3, w4)
		# print "x1 = {}".format(x1)
		# print "x2 = {}".format(x2)
		# print "x3 = {}".format(x3)
		# print "x4 = {}".format(x4)
		w1 += moderador * (vtrain - vcurrent) * x1
		w2 += moderador * (vtrain - vcurrent) * x2
		w3 += moderador * (vtrain - vcurrent) * x3
		w4 += moderador * (vtrain - vcurrent) * x4

def updateHypothesis():
	pass


#esto es lo que va a hacer critic en realidad
def main():
	import critic
	# moderador = 0.5
	# print "w0 = {}, w1 = {}, w2 = {}, w3 = {}, w4 = {}".format(w0, w1, w2, w3, w4)
	for i in range(15):
		trainingExamples = critic.generateTrainingExamples()
		#ajustar coeficientes con lms
		lms(trainingExamples)
		print "w0 = {}, w1 = {}, w2 = {}, w3 = {}, w4 = {}".format(w0, w1, w2, w3, w4)
	# w0 = random.random()
	# w1 = random.random()
	# w2 = -random.random()
	# w3 = -random.random()
	# w4 = random.random()