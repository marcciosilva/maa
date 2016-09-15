import numpy as np
import math
import reader
import sys
#import treePrinting

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
	s_size = data_size * 4/5
	print "Cantidad total de instancias en D : " + str(data_size)
	print "Size de muestra para entrenar NB : " + str(s_size)
	sample = data[:s_size,:]
	aux = 0
	for x in range(s_size,data_size):
		instancia = data[x,:]
		aux += clasificadorNB(instancia,attrs,sample,targetAttr)
		print "----------------------------------------------------------------   " + str(aux)
	print data_size - s_size
	acierto = round(100.00 * aux / (data_size - s_size),2)
	print acierto
	print "Se acierta en un: " + str(acierto) + "%"

def clasificadorNB(instancia,attrs,sample,targetAttr):
	print "### clasificador NB ###"
	print "Clasificando instancia: " + str(instancia)
	i = 0
	j = 0
	p = 21 * [0]
	cantNota = 21 * [0]
	attrsSinNotas = attrs[:-3]
	m = np.zeros((21, len(attrsSinNotas)))
	result = 21 * [0]
	aux = 21 * [1]
	#print aux
	#for i in range(21):
	for j in range(len(sample)):
	#if (sample[j,attrs.index(targetAttr)] == str(i)):
	#p[i] += 1
		nota = int(sample[j,attrs.index(targetAttr)])
		cantNota[nota] += 1
		a = 0
		for a in range(len(attrsSinNotas)):
			if (instancia[a] == sample[j,a]):
				m[nota,a] += 1
	#print m
	maximo = 0
	notaRes = 0
	for i in range(21):
		p[i] = cantNota[i] / float(len(sample))
		x = 0
		for x in range(len(attrsSinNotas)):
			if cantNota[i] > 0:
				m[i,x] = m[i,x] / cantNota[i]
			aux[i] = aux[i] * m[i,x]
		result[i] = aux[i] * p[i]
		if (result[i] > maximo):
			maximo = result[i]
			notaRes = i

	total = sum(result)
	porcent = round((maximo / total * 100),2)
	#print m
	#print "-------------------------"
	#print result
	#print "-------------------------"
	#print maximo
	#print "-------------------------"
	#print total
	#print "-------------------------"
	#print notaRes
	#print "-------------------------"
	#print round((maximo / total * 100),2)

	print "Con un " + str(porcent) + "%" + " de seguridad puedo afirmar que la nota final es: " + str(notaRes) + "."
	if (int(instancia[attrs.index(targetAttr)]) == notaRes):
		print 111111111111111
		return 1
	else:
		return 0
	#print str(p)
	#aux = 0
	#for pi in p:
	#	aux += pi
	#print aux

main()
