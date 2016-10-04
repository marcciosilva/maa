import math
import random
import string
import numpy

# Devuelve un nro random entre a y b
def rand(a, b):
	return (b-a)*random.random() + a

# Sigmoid
def sigmoid(x):
	try:
		return 1 / (1 + numpy.exp(-x))
	except OverflowError:
		print 'overflow'
		return 1

# Derivada de sigmoid
def dsigmoid(x):
	sig = sigmoid(x)
	return sig*(1-sig)
	
#input: nodos de entrada
#hidden: nodos ocultos
#output: nodos de salida
class Network:
	def __init__(self, input, hidden, output):
		self.input = input + 1 # +1 for bias node
		self.hidden = hidden
		self.output = output

		# Inicializacion de pesos
		self.wi = numpy.zeros((self.input, self.hidden),)
		self.wo = numpy.zeros((self.hidden, self.output),)		
		
		for i in range(self.input):
			for j in range(self.hidden):
				self.wi[i][j] = rand(-1.0, 1.0)
		for j in range(self.hidden):
			for k in range(self.output):
				self.wo[j][k] = rand(-1.0, 1.0)
				
		# activations for nodes
		self.xi = [1.0]*self.input
		self.xh = [1.0]*self.hidden
		self.xo = [1.0]*self.output

	#Actualiza los pesos de los nodos con las entradas dadas en input.
	def update(self, inputs):
		
		# Activa los nodos de entrada.	
		for i in range(self.input-1):
			self.xi[i] = inputs[i]

		# Calcula la salida de los nodos ocultos
		for j in range(self.hidden):
			sum = 0.0
			for i in range(self.input):
				sum = sum + self.xi[i] * self.wi[i][j]				
			self.xh[j] = sigmoid(sum)

		# Calcula la salida de los nodos de salida
		for k in range(self.output):
			sum = 0.0
			for j in range(self.hidden):
				sum = sum + self.xh[j] * self.wo[j][k]
			self.xo[k] = sigmoid(sum)

		return self.xo[:]
	
	def backPropagation(self, targets, N):	

		# Delta para los nodos de salida
		# Genero lista para los errores de la salida de la capa de output.
		outputError = [0.0] * self.output
		for k in range(self.output):
			outputError[k] = dsigmoid(self.xo[k]) * (targets[k]-self.xo[k])
		
		# Delta para los nodos ocultos
		hiddenError = [0.0] * self.hidden
		for j in range(self.hidden):
			error = 0.0
			for k in range(self.output):
				error = error + outputError[k]*self.wo[j][k]
			hiddenError[j] = dsigmoid(self.xh[j]) * error
		
		# Error
		error = 0.0
		for k in range(len(targets)):
			error = error + 0.5*(targets[k]-self.xo[k])**2
				
		# Recalculo pesos de salida usando el factor de aprendizaje N.
		for j in range(self.hidden):
			for k in range(self.output):
				self.wo[j][k] = self.wo[j][k] + N * outputError[k] * self.xh[j]				

		# Recalculo pesos de nodos de capa oculta usando el factor de aprendizaje N.
		for i in range(self.input):
			for j in range(self.hidden):
				self.wi[i][j] = self.wi[i][j] + N* hiddenError[j] * self.xi[i]
		
		return error

	def test(self, patterns):
		for p in patterns:
			print( p[0], self.update(p[0])[0])
			#print(p[0], '->', self.update(p[0]))
	
	# Entrena a la red neuronal	
	# N=factor de aprendizaje
	def train(self, examples, N, maxIters):
		i=0
		while (i<maxIters):
			error = 0.0
			for p in examples:
				inputs = p[0]
				targets = p[1]
				# Evalua inputs en la red actual (forward propagation)
				self.update(inputs)				
				error = error + self.backPropagation(targets, N)				
			i=i+1
		print('error %-.5f' % error)

def sen():
	# return [[[x/20.0], [round(math.sin(x*math.pi*1.5),3)]] for x in range(-20,19)]
	# 40 valores equiespaciados entre -1.0 y 1.0
	lst = []
	domain = numpy.arange(-1, 1, 0.05)
	for number in domain:
		lst.append([[number],[round(math.sin(number*math.pi*1.5),3)]])
	return lst
	
# def senTest():
# 	return [[[x/100.0], [round(math.sin(x*math.pi*1.5),3)]] for x in range(-10,10)]
	
# def qtest():
# 	return [[[x/100.0], [round((x/100.0)**2,3)]] for x in range(-100, 101)]

def quadr():
	lst = []
	#40
	domain = numpy.arange(-1, 1, 0.05)
	for number in domain:
		lst.append([[number],[number**2]])
	return lst

def h(begin, end, step):
	# Numeros equiespaciados entre begin y end, separados por step
	x = numpy.arange(begin, end, step)
	X, Y = numpy.meshgrid(x, x)
	# Se obtienen len(x)**2 numeros equiespaciados entre (-1.0,-1.0) y (1.0,1.0)
	puntosEquiespaciados = [numpy.array(thing) for thing in zip(X.flatten(), Y.flatten())]
	# print puntosEquiespaciados
	setSize = len(puntosEquiespaciados)
	# Genero el set de entrenamiento
	trainingValues = []
	for i in range(setSize):
	# for punto in puntosEquiespaciados:
		x = puntosEquiespaciados[i][0]
		y = puntosEquiespaciados[i][1]
		imagen = 0.0
		# Aplico funcion h(x)
		if (x**2 + y**2 < 0.5):
			imagen = 1.0
		trainingValues.append([[x, y],[imagen]])
	return trainingValues

def main():
	random.seed(0)
	setIteraciones = [10**2, 10**3, 10**4, 10**5]
	N = 0.5
	print "#############Test funcion seno#############"
	print "#############Funcion original#############"
	for element in sen():
		print (element[0][0], element[1][0])
	for iteraciones in setIteraciones:
		print "#############Test con " + str(iteraciones) + " iteraciones#############"
		n = Network(1, 20, 1)
		n.train(sen(), N, iteraciones)
		# Se testea contra los datos de entrada a ver que tanto llega a asimilarse a la funcion
		# original para esos puntos.		
		n.test(sen())
		# n.test(senTest())
	print "#############Funcion original#############"
	for element in quadr():
		print (element[0][0], element[1][0])	
	print "#############Test funcion cuadratica#############"
	for iteraciones in setIteraciones:
		print "#############Test con " + str(iteraciones) + " iteraciones#############"
		n = Network(1,20,1)
		n.train(quadr(), N, iteraciones)
		# Se testea contra los datos de entrada a ver que tanto llega a asimilarse a la funcion
		# original para esos puntos.
		n.test(quadr())
		# n.test(qtest())
	print "#############Test funcion h(x)#############"
	print "#############Funcion original#############"
	print h(-1.0,1.1,0.4)	
	for element in h(-1.0,1.1,0.4):
		print ((element[0][0], element[0][1]), element[1][0])
	for iteraciones in setIteraciones:
		print "#############Test con " + str(iteraciones) + " iteraciones#############"
		n = Network(1,20,1)
		n.train(h(-1.0,1.1,0.4), N, iteraciones)
		# Se testea contra los datos de entrada a ver que tanto llega a asimilarse a la funcion
		# original para esos puntos.
		n.test(h(-1.0,1.1,0.4))

main()


