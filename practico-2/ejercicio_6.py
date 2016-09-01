import numpy as np
import math
import reader

def main():
	#attrs=['a','b','target']
	#data=np.array([[1,2,1], [1,4,1], [1,6,1], [1,2,1], [1,4,1], [1,6,1], [1,3,0], [2,3,0]])
	fileName = "data/student-mat.csv"
	csvData = reader.getDataFromCsv(fileName)
	attrs, data = csvData[0], np.array(csvData[1])
	#Imprime la entropia del conjunto original con respecto a G3
	print entropy(attrs, data, 'G3')
	#Imprime el information gain del atributo 'Walc' respecto a G3.
	print informationGain(attrs, data, 'Walc', 'G3')
	
	print genDecisionTree(data, attrs, 'G3')

	
#Retorna la entropia de un conjunto de datos para un determinado atributo objetivo.
def entropy(attributes, data, targetAttr):

	i = attributes.index(targetAttr)
	targetValues = data[:,i]
	
	#Frecuencia de cada valor del atributo objetivo dentro del conjunto de datos.
	valFreq = {}
	entropy = 0.0

	for targetValue in targetValues:
		if (valFreq.has_key(targetValue)):
			valFreq[targetValue] += 1.0
		else:
			valFreq[targetValue]  = 1.0

	for freq in valFreq.values():
		proportion = freq/len(data)
		entropy += (-proportion) * math.log(proportion, 2) 
		
	return entropy

# Retorna el information gain para el atributo attr y el atributo objetivo targetAttr.
def informationGain(attributes, data, attr, targetAttr):	

	i = attributes.index(attr)
	attrValues = data[:,i]
	
	valFreq = {}
	for attrValue in attrValues:
		if (valFreq.has_key(attrValue)):
			valFreq[attrValue] += 1.0
		else:
			valFreq[attrValue]	= 1.0
	
	attrEntropy = 0.0
	dataLength = len(data)
	for val in valFreq.keys():
		valProb		   = valFreq[val] / dataLength
		attrData	 = np.array([entry for entry in data if entry[i] == val])
		attrEntropy += valProb * entropy(attributes, attrData, targetAttr)
 
	return (entropy(attributes, data, targetAttr) - attrEntropy)
 
def getBestAttr(data, attributes, target):
	best = attributes[0]
	maxGain = 0;
	nonTargetAttributes = attributes[:]
	nonTargetAttributes.remove(target)
	for attr in nonTargetAttributes:
		newGain = informationGain(attributes, data, attr, target) 
		if newGain>maxGain:
			maxGain = newGain
			best = attr
	return best
	
#Retorna el valor mas comun del atributo objetivo.
def mostCommonValue(targetValues):
	valFreq = {}	
	maxFreq = 0
	commonValue = 0
	
	for value in targetValues:
		if (valFreq.has_key(value)):
			valFreq[value] += 1 
		else:
			valFreq[value] = 1
		if valFreq[value] > maxFreq:
			maxFreq = valFreq[value]
			commonValue = value

	return commonValue

#Retorna el arbol de decision
def genDecisionTree(data, attributes, target):
	
	data = np.array(data[:])
	targetValues = data[:,attributes.index(target)]
	
	#Si todos los nodos tienen el mismo valor, etiquetar con ese valor
	if len(set(targetValues)) == 1:
		return targetValues[0]
	
	#Si no quedan atributos, etiquetar con el valor mas comun
	if (len(attributes) -1) == 0:
		return mostCommonValue(targetValues)	

	# Se elige el mejor atributo segun su information gain.
	bestAttr = getBestAttr(data, attributes, target)
	bestAttrIndex = attributes.index(bestAttr)
	#Genero una rama.
	tree = {bestAttr:{}}

	# Genero una rama para cada valor del atributo elegido
	for val in set(data[:,bestAttrIndex]):
		
		#Subconjunto de datos para cada valor del atributo
		valSubset = np.array([x for x in data if x[bestAttrIndex] == val])		
		valSubset = np.delete(valSubset, bestAttrIndex, 1)		
		
		#Remuevo el atributo de la lista de atributos
		newAttr = attributes[:]
		newAttr.remove(bestAttr)
		
		#Llamada recursiva
		subtree = genDecisionTree(valSubset, newAttr, target)
	
		tree[bestAttr][val] = subtree
	
	return tree
main()