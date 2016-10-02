import numpy as np
import math
from random import randint

izquierda = 0
derecha = 1
arriba = 2
abajo = 3

def main():
	# Se numeran los estados de la realidad planteada de la sigueinte manera:
	# |0 |1 |2 |3 |4 |5 |
	# |6 |7 |8 |9 |10|11|
	# |12|13|  14 |15|16|
	# |17|18|     |19|20|
	# |21|22|23|24|25|26|
	# |27|28|29|30|31|32|

	# delta es una matriz, donde las filas representan a los posibles estados [0..32], 
	# y las columnas representan a las acciones (0 - izquierda, 1 - derecha, 2 - arriba, 3 - abajo).
	# Los posibles valores son [-1..32], representan los estados resultantes de aplicar la accion representada
	# por el numero de columna, al estado representado por el numero de fila, donde -1 representa que no existe transicion 
	# para ese estado y acion.
	delta = np.matrix([ [-1, 1,-1, 6],[ 0, 2,-1, 7],[ 1, 3,-1, 8],[ 2, 4,-1, 9],[ 3, 5,-1,10],[ 4,-1,-1,11],
		 	 			[-1, 7, 0,12],[ 6, 8, 1,13],[ 7, 9, 2,14],[ 8,10, 3,14],[ 9,11, 4,15],[10,-1, 5,16],
		 				[-1,13, 6,17],[12,14, 7,18],[-1,    -1,     -1,     -1],[14,16,10,19],[15,-1,11,20],
		 				[-1,18,12,21],[17,14,13,22],                            [14,20,15,25],[19,-1,16,26],
		 				[-1,22,17,27],[21,23,18,28],[22,24,14,29],[23,25,14,30],[24,26,19,31],[25,-1,20,32],
		 				[-1,28,21,-1],[27,29,22,-1],[28,30,23,-1],[29,31,24,-1],[30,32,25,-1],[31,-1,26,-1]])
	
	# r es una matriz de las mismas dimensiones que delta, de la misma forma las filas representan los estados
	# y las columnas las acciones, pero los valores representan las "recompensas inmediatas" al ejecutar las accion para 
	# el estado.
	r = np.matrix([	[  0,  0,  0,  0],[  0,  0,  0,  0],[  0,  0,  0,  0],[  0,  0,  0,  0],[  0,  0,  0,  0],[  0,  0,  0,  0],
		 			[  0,  0,  0,  0],[  0,-20,  0,  0],[  0,  0,  0, 80],[  0,  0,  0, 80],[-20,  0,  0,  0],[  0,  0,  0,  0],
		 			[  0,  0,  0,  0],[  0,  0,  0,  0],[0,        0,         0,         0],[  0,  0,  0,  0],[  0,  0,  0,  0],
		 			[  0,  0,  0,  0],[  0,  0,  0,  0],                                    [  0,  0,  0,  0],[  0,  0,  0,  0],
		 			[  0,  0,  0,  0],[  0,  0,  0,  0],[  0,  0, 20,  0],[  0,  0, 20,  0],[  0,  0,  0,  0],[  0,  0,  0,  0],
		 			[  0,  0,  0,  0],[  0,  0,  0,  0],[  0,  0,  0,  0],[  0,  0,  0,  0],[  0,  0,  0,  0],[  0,  0,  0,  0]])

	# El estado objetivo de la realidad planteada.
	estadoObjetivo = 14

	# La Constante de aprendizaje. 
	y = 0.9

	# Cantidad de Episodios.
	episodios = 200

	Q_learning(r,delta,estadoObjetivo,y,episodios)

# Funcion que retorna una accion valida para el estado s, de forma aleatoria.
def elijoAccionParaEstado(s,delta):

	cantAcciones = delta.shape[1]
	a = randint(0,cantAcciones-1)
	while delta[s,a] == -1:
		a = randint(0,cantAcciones-1)
	return a

# Funcion que retorna la accion de la cual se llega a el estado sig desde el estado ant
# en un solo movimiento.
def getAccionEntreEstados(ant, sig, delta):

	cantAcciones = delta.shape[1]
	for a in range(cantAcciones):
		if delta[ant,a] == sig:
			return a

def Q_learning(r,delta,estadoObjetivo,y,episodios):

	cantEstados = len(delta)
	cantAcciones = delta.shape[1]

	# inicializo en cero los valores Q para cada estado-accion.
	Q = np.zeros((cantEstados, cantAcciones))

	# Itero cantidad episodios veces
	for ep in range(episodios):

		# selecciono un estado de forma aleatoria.
		s = randint(0,cantEstados-1)
		print 'Estado origen: ' + str(s)

		# inicializo trayecto, una lista que guarda la secuencia de estados desde
		# el origen s, hasta el estado objetivo.
		trayecto = []
		
		# agrego el estado inicial a trayecto.
		trayecto.append(s)

		# mientras no sea el Estado Objetivo, se ejecutan acciones.
		while (not s == estadoObjetivo):

			# elijo una de las posibles acciones para el estado actual.
			a = elijoAccionParaEstado(s,delta)

			# obtengo la recompensa inmediata de ejecutar la accion a al estado s.
			rs = r[s,a]

			# obtengo el estado resultante de ejecutar la accion a al estado s.
			s_sig = delta[s,a]

			# cambio de estado.
			s = s_sig

			# agrego el estado actual al final de trayecto.
			trayecto.append(s)

		# llegue al estado objetivo.

		# inicializo variable que acumula el retorno de los siguientes estados.
		acum = 0

		# inicializo variable que se utiliza como exponente de la constante y, para
		# descontar la recompensa por retraso.
		cant = 0.0

		print 'Trayecto desde el estado origen ' + str(trayecto[0]) + ' al estado objetivo ' + str(trayecto[len(trayecto)-1]) + ':'
		print trayecto

		# A continuacion recorro el trayecto en orden inverso, para lo cual
		# primero obtengo el ultimo estado de trayecto, el estado objetivo.
		actual = trayecto[len(trayecto)-1]

		# recorro el trayecto en orden inverso sin tener en cuenta al estado objetivo (si es que hay estados).
		for i in range(len(trayecto)-2,-1,-1):

			# obtengo estado anterior.
			anterior = trayecto[i]

			# obtengo accion de la transicion anterior -> actual.
			accion = getAccionEntreEstados(anterior, actual, delta)

			# aplico la formula Q para el estado anterior.
			temp = r[anterior,accion] + math.pow(y,cant) * acum

			# Si el calculo supera al valor registrado anteriormente, lo remplaza.
			if temp > Q[anterior,accion]:
				Q[anterior,accion] = temp

			# actualizo variable que acumula el retorno de los siguientes estados.
			acum = Q[anterior,accion]

			# actualizo variable que se utiliza como exponente de la constante y, para
			# descontar la recompensa por retraso.
			cant += 1

			# me muevo hacia atras en el trayecto.
			actual = anterior

		# Fin del algoritmo para Q.

		print 'La matriz con los retornos para cada estado y accion aprendidos en el episodio ' + str(ep) + ' es:'
		print Q
		print '------------------------------------------------------------------------------------------------------'

main()
