import math
import random
import string
import numpy

# Devuelve un nro random entre a y b
def rand(a, b):
	return (b-a)*random.random() + a

# Sigmoid
def sigmoid(x):
	return 1 / (1 + math.exp(-x))

# Derivada de sigmoid
def dsigmoid(x):
	return x*(1-x)
	
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
				self.wi[i][j] = rand(-0.2, 0.2)
		for j in range(self.hidden):
			for k in range(self.output):
				self.wo[j][k] = rand(-2.0, 2.0)
				
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
				
		# Recalculo pesos de salida usando el factor de aprendizaje N
		for j in range(self.hidden):
			for k in range(self.output):
				self.wo[j][k] = self.wo[j][k] + N * outputError[k] * self.xh[j]				

		# update pesos de nodos de entrada
		for i in range(self.input):
			for j in range(self.hidden):
				self.wi[i][j] = self.wi[i][j] + N* hiddenError[j] * self.xi[i]
			
		return error

	def test(self, patterns):
		for p in patterns:
			print(p[0], '->', self.update(p[0]))
	
	# Entrena a la red neuronal
	# N=factor de aprendizaje
	# targetError = error objetivo hasta el cual seguira entrenando.
	def train(self, examples, N=0.5, maxIters=1000):
		i=0
		while (i<maxIters):
			error = 0.0
			for p in examples:
				inputs = p[0]
				targets = p[1]
				self.update(inputs)				
				error = error + self.backPropagation(targets, N)				
			i=i+1
		print('error %-.5f' % error)

def main():
	random.seed(0)
	
	#x^2
	cuadr = [
		 [[0,0,0], [0,0,0,0,0]],
		 [[0,0,1], [0,0,0,0,1]],
		 [[0,1,0], [0,0,0,1,1]],
		 [[1,0,0], [1,0,0,0,0]],
		 [[1,0,1], [1,1,0,0,1]],		 
		 ]
	
	n = Network(3, 8, 5)
	n.train(cuadr)
	n.test(cuadr)

main()


