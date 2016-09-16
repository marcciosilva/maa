import numpy as np
import math
import reader
import sys

def main():

	fileName = "data/student-mat.csv"
	csvData = reader.getDataFromCsv(fileName)
	attrs, data = csvData[0], np.array(csvData[1])
	#Obtengo el resto de los datos.
	fileName = "data/student-por.csv"
	csvData = reader.getDataFromCsv(fileName)
	#Agrego nueva data a la anterior.
	data = np.concatenate((data, csvData[1]))
	targetAttr = 'G3'
	data_size = len(data)
	#Desordeno instancias
	data = np.random.permutation(data)
	s_size = data_size * 4/5
	print "Cantidad total de instancias en D : " + str(data_size)
	print "Size de muestra para entrenar NB : " + str(s_size)
	sample = data[:s_size,:]
	#Acumulador de aciertos.
	aux = 0
	for x in range(s_size,data_size):
		instancia = data[x,:]
		#Se suma 1 si fue un acierto, 0 en caso contrario.
		aux += clasificadorNB(instancia,attrs,sample,targetAttr)
		print "----------------------------------------------------------------"
	acierto = round(100.00 * aux / (data_size - s_size),2)
	print "Aciertos = " + str(aux) + " de " + str(data_size - s_size) + " (" + str(acierto) + "%)"

def clasificadorNB(instancia,attrs,sample,targetAttr):
	print "### clasificador NB ###"
	print "Clasificando instancia: " + str(instancia)
	#Como las notas van de 0 a 20, tenemos 21 posibles notas.
	cantNotasPosibles = 21
	#Genero arreglos de 21 ceros.
	p = cantNotasPosibles * [0]
	#Arreglo que almacena la cantidad de ocurrencias para cada nota,
	#segun el sample (atributo G3).
	cantNota = cantNotasPosibles * [0]
	#Quito tres ultimos atributos porque no se utilizan al clasificar.
	attrsSinNotas = attrs[:-3]
	#Genero matriz de ceros de cantNotasPosibles * len(attrsSinNotas).
	#Cada fila es una nota posible, cada columna un atributo posible.
	#La idea es almacenar las ocurrencias de cada atributo para una
	#clasificacion en particular.
	m = np.zeros((cantNotasPosibles, len(attrsSinNotas)))
	result = cantNotasPosibles * [0]
	aux = cantNotasPosibles * [1]
	for j in range(len(sample)):
		#Recabo cantidad de apariciones de cada nota segun la sample.
		nota = int(sample[j,attrs.index(targetAttr)])
		cantNota[nota] += 1
		for a in range(len(attrsSinNotas)):
			if (instancia[a] == sample[j,a]):
				m[nota,a] += 1
	print "###################################"
	print "cantNota = " + str(cantNota)
	print "###################################"
	maximo = -sys.maxint - 1
	#Clasificacion obtenida.
	notaRes = 0
	for i in range(cantNotasPosibles):
		#Proporcion del valor de atributo i en el total de la muestra.
		p[i] = cantNota[i] / float(len(sample))
		for x in range(len(attrsSinNotas)):
			if cantNota[i] > 0:
				#La celda que contenia la cantidad de ocurrencias del valor
				#de atributo x con clasificacion i pasa a ser 
				#la proporcion entre ese valor y la cantidad de veces que
				#ocurre la nota i.
				m[i,x] = m[i,x] / cantNota[i]
				aux[i] = aux[i] * m[i,x]
			#En caso contrario el producto permanece incambiado porque
			#no hay ocurrencias de esa nota en la muestra.
			#Ademas, en dicho caso, p[i] ya es 0, por lo que de todas
			#maneras el resultado se anula en la siguiente linea.
		result[i] = aux[i] * p[i]
		if (result[i] > maximo):
			maximo = result[i]
			notaRes = i
	total = sum(result)
	porcentaje = round((maximo / total * 100),2)
	print "Con un " + str(porcentaje) + "%" + " de seguridad puedo afirmar que la nota final es: " + str(notaRes) + "."
	if (int(instancia[attrs.index(targetAttr)]) == notaRes):
		return 1
	else:
		return 0


main()
