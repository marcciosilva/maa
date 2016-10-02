import numpy as np
import math
from random import randint

izquierda = 0
derecha = 1
arriba = 2
abajo = 3
cantEstados = 33
EstadoObjetivo = 14
cantAcciones = 4

def main():
	# Se numeran los estados de la sigueinte manera

	# |0 |1 |2 |3 |4 |5 |
	# |6 |7 |8 |9 |10|11|
	# |12|13|  14 |15|16|
	# |17|18|     |19|20|
	# |21|22|23|24|25|26|
	# |27|28|29|30|31|32|

	# delta es una matriz, donde las filas representan a los posibles estados [0..32], 
	# y las columnas representan a las acciones (0 - izquierda, 1 - derecha, 2 - arriba, 3 - abajo).
	# Los posibles valores son [-1..32], representan los estados resultantes de aplicar la accion representada
	# por la columna, al estado dado por la fila, donde -1 representa que no existe transicion para ese estado.

	delta = np.matrix([[-1, 1,-1, 6],[ 0, 2,-1, 7],[ 1, 3,-1, 8],[ 2, 4,-1, 9],[ 3, 5,-1,10],[ 4,-1,-1,11],
		 	 [-1, 7, 0,12],[ 6, 8, 1,13],[ 7, 9, 2,14],[ 8,10, 3,14],[ 9,11, 4,15],[10,-1, 5,16],
		 	 [-1,13, 6,17],[12,14, 7,18],[-1,    -1,     -1,     -1],[14,16,10,19],[15,-1,11,20],
		 	 [-1,18,12,21],[17,14,13,22],                            [14,20,15,25],[19,-1,16,26],
		 	 [-1,22,17,27],[21,23,18,28],[22,24,14,29],[23,25,14,30],[24,26,19,31],[25,-1,20,32],
		 	 [-1,28,21,-1],[27,29,22,-1],[28,30,23,-1],[29,31,24,-1],[30,32,25,-1],[31,-1,26,-1]])
	
	# r es una matriz de las mismas dimensiones que delta, de la misma forma las filas representan los estados
	# y las columnas las acciones, pero los valores representan las "recompensas inmediatas" al ejecutar las accion para 
	# el estado.

	r = np.matrix([[  0,  0,  0,  0],[  0,  0,  0,  0],[  0,  0,  0,  0],[  0,  0,  0,  0],[  0,  0,  0,  0],[  0,  0,  0,  0],
		 [  0,  0,  0,  0],[  0,-20,  0,  0],[  0,  0,  0, 80],[  0,  0,  0, 80],[-20,  0,  0,  0],[  0,  0,  0,  0],
		 [  0,  0,  0,  0],[  0,  0,  0,  0],[0,        0,         0,         0],[  0,  0,  0,  0],[  0,  0,  0,  0],
		 [  0,  0,  0,  0],[  0,  0,  0,  0],                                    [  0,  0,  0,  0],[  0,  0,  0,  0],
		 [  0,  0,  0,  0],[  0,  0,  0,  0],[  0,  0, 20,  0],[  0,  0, 20,  0],[  0,  0,  0,  0],[  0,  0,  0,  0],
		 [  0,  0,  0,  0],[  0,  0,  0,  0],[  0,  0,  0,  0],[  0,  0,  0,  0],[  0,  0,  0,  0],[  0,  0,  0,  0]])

	y = 0.9
	episodios = 100
	Q = np.zeros((33, 4))
	Q_learning(r,delta,y,episodios,Q)

# funcion para determinar si es el estado Objetivo
def esEstadoObjetivo(s):
	return s == EstadoObjetivo

def elijoAccionParaEstado(s,delta):
	a = randint(0,cantAcciones-1)
	#print 'accion antes: ' + str(a)
	while delta[s,a] == -1:
		a = randint(0,cantAcciones-1)
	return a

def getAccionEntreEstados(ant, sig, delta):
	for a in range(cantAcciones):
		if delta[ant,a] == sig:
			return a

def Q_learning(r,delta,y,episodios,Q):
	# inicializo en cero los valores Q para cada estado-accion.
	for ep in range(episodios):
		# selecciono un estado de forma aleatoria
		s = randint(0,cantEstados-1)
		#estadoAnt = np.zeros(33)
		trayecto = []
		print 'Estado ' + str(s)
		# mientras no sea el Estado Objetivo
		sAux = s
		trayecto.append(sAux)
		while (not esEstadoObjetivo(sAux)):
			# elijo una de las posibles acciones para el estado actual
			a = elijoAccionParaEstado(sAux,delta)
			#print 'Accion: ' + str(a)
			rs = r[sAux,a]
			#print 'recompensa: ' + str(rs)
			s_sig = delta[sAux,a]
			#print 'Estado siguiente: ' + str(s_sig)
			#estadoAnt[s_sig] = sAux
			sAux = s_sig
			trayecto.append(sAux)
			#for aSig in range(cantAcciones):
			#	if delta[s_sig,aSig] != -1:
			#		s = s_sig
			#	else:
		#ant = estadoAnt[sAux]
		#print estadoAnt
		acum = 0
		cant = 0.0
		print trayecto
		#while ant != s:
		actual = trayecto[len(trayecto)-1]
		for i in range(len(trayecto)-2,-1,-1):
			anterior = trayecto[i]
			#print trayecto[i]
			#print '---------------'
			#print ant
			#print s
			#print '---------------'
			accion = getAccionEntreEstados(anterior, actual, delta)
			temp = r[anterior,accion] + math.pow(y,cant) * acum
			if temp > Q[anterior,accion]:
				Q[anterior,accion] = temp
			# print Q
			acum = Q[anterior,accion]
			cant += 1
			actual = anterior
			#ant = estadoAnt[sAux]
		print Q


main()