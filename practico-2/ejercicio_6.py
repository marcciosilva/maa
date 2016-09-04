import numpy as np
import math
import reader
import treePrinting

def main():
    attrs=['a','b','target']
    fileName = "data/student-mat.csv"
    csvData = reader.getDataFromCsv(fileName)
    attrs, data = csvData[0], np.array(csvData[1])

    #Obtengo el resto de los datos.
    fileName = "data/student-por.csv"
    csvData = reader.getDataFromCsv(fileName)
    #Agrego nueva data a la anterior.
    data = np.concatenate((data, csvData[1]))


    #Imprime la entropia del conjunto original con respecto a G3
    print entropy(attrs, data, 'G3')
    #Imprime el information gain del atributo 'Walc' respecto a G3.
    print informationGain(attrs, data, 'Walc', 'G3')

    #Calcular de alguna forma el maxHeight optimo
    #Le asigno un valor adecuado
    maxHeight = 7
    tree = genDecisionTree(data, attrs, 'G3',maxHeight,0)
    print tree
    #Imprime arbol exportable a pdf.
    treePrinting.printTree(tree)
    # testExample()

def testExample():
	#Prueba utilizando ejemplo del capitulo 3 del Mitchell.
    attrs = ['Outlook', 'Temperature', 'Humidity', 'Wind', 'PlayTennis']
    data = np.array([
        ["Sunny", "Hot", "High", "Weak", "No"], 
        ["Sunny", "Hot", "High", "Strong", "No"],
        ["Overcast", "Hot", "High", "Weak", "Yes"],
        ["Rain", "Mild", "High", "Weak", "Yes"],
        ["Rain", "Cool", "Normal", "Weak", "Yes"],
        ["Rain", "Cool", "Normal", "Strong", "No"],
        ["Overcast", "Cool", "Normal", "Strong", "Yes"],
        ["Sunny", "Mild", "High", "Weak", "No"],
        ["Sunny", "Cool", "Normal", "Weak", "Yes"],
        ["Rain", "Mild", "Normal", "Weak", "Yes"],
        ["Sunny", "Mild", "Normal", "Strong", "Yes"],
        ["Overcast", "Mild", "High", "Strong", "Yes"],
        ["Overcast", "Hot", "Normal", "Weak", "Yes"],
        ["Rain", "Mild", "High", "Strong", "No"]
        ])
    # print entropy(attrs, data, 'PlayTennis')
    # print "Outlook information gain: " + str(informationGain(attrs, data, 'Outlook', 'PlayTennis'))
    # print "Humidity information gain: " + str(informationGain(attrs, data, 'Humidity', 'PlayTennis'))
    # print "Wind information gain: " + str(informationGain(attrs, data, 'Wind', 'PlayTennis'))
    # print "Temperature information gain: " + str(informationGain(attrs, data, 'Temperature', 'PlayTennis'))
    tree = genDecisionTree(data, attrs, 'PlayTennis',3,0)
    print tree
    tmpAttrs = attrs[:-1]
    for instance in data:
    	tmpInstance = instance[:-1]
    	evalInstance(tmpInstance, tmpAttrs, tree)
    treePrinting.printTree(tree)
    
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
            valFreq[attrValue]    = 1.0
    
    attrEntropy = 0.0
    dataLength = len(data)
    for val in valFreq.keys():
        valProb           = valFreq[val] / dataLength
        attrData     = np.array([entry for entry in data if entry[i] == val])
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

#Retorna el arbol de decision.
def genDecisionTree(data, attributes, target,maxHeight,currentHeight):
    
    data = np.array(data[:])

    #Obtengo un arreglo con todos los valores del atributo target
    #en cada instancia.
    targetValues = data[:,attributes.index(target)]
    
    #Si todos los nodos tienen el mismo valor, etiquetar con ese valor.
    if len(set(targetValues)) == 1:
        return targetValues[0]
    
    #Si no quedan atributos, etiquetar con el valor mas comun.
    if (len(attributes) -1) == 0:
        return mostCommonValue(targetValues)    

    #Si llego al largo maximo establecido para las ramas, etiquetar con el valor mas comun.
    if currentHeight == maxHeight:
        return mostCommonValue(targetValues)

    #Si no alcance el largo maximo, continua creciendo la rama.
    currentHeight = currentHeight + 1

    # Se elige el mejor atributo segun su information gain.
    bestAttr = getBestAttr(data, attributes, target)
    bestAttrIndex = attributes.index(bestAttr)

    #Genero una rama.
    tree = {bestAttr:{}}

    # Genero una rama para cada valor del atributo elegido.
    for val in set(data[:,bestAttrIndex]):
        
        #Subconjunto de datos para cada valor del atributo.
        #Obtengo los ejemplos que comparten el mismo valor del atributo.
        valSubset = np.array([x for x in data if x[bestAttrIndex] == val])
        #A cada ejemplo le quito la coordenada correspondiente al atributo
        #elegido, porque no interesa para las proximas iteraciones.
        valSubset = np.delete(valSubset, bestAttrIndex, 1)        
        
        #Remuevo el atributo de la lista de atributos.
        newAttr = attributes[:]
        newAttr.remove(bestAttr)
        
        #Llamada recursiva.
        subtree = genDecisionTree(valSubset, newAttr, target, maxHeight, currentHeight)
    
    	#Agrego el subarbol al nodo actual.
        tree[bestAttr][val] = subtree
    
    return tree

#Clasifica una instancia de acuerdo a un arbol de decision.
def evalInstance(instance, attributes, decisionTree):
	#Obtengo nodo.
	node = decisionTree.keys()[0]
	#Obtengo indice del atributo en el arreglo de atributos posibles.
	index = attributes.index(node)
	#Asumiendo que el valor del atributo esta entre las claves,
	#determino el indice de la rama por la que tiene que seguir la instancia.
	#Valor del atributo en la instance.
	instanceAttrValue = decisionTree[node][instance[index]]
	#Si estoy frente a una nueva rama, me sigo moviendo en ella
	if (isinstance(instanceAttrValue,dict)):
		return evalInstance(instance, attributes, instanceAttrValue)
	#De otra manera, devuelvo la clasificacion obtenida.
	else:
		print str(instance) + " classifies as " + instanceAttrValue
		return instanceAttrValue

#def crossValidation(data, attributes,k):
   

def getFold(i,data,fold_size):
    return data[(i-1)*fold_size:i*fold_size,:]

def getSampleWithoutFold(i,data,fold_size,k):
    return np.concatenate((data[0:(i-1)*fold_size,:],data[i*fold_size:k*fold_size,:]))

def crossValidation():
    attrs=['a','b','target']
    fileName = "data/student-mat.csv"
    csvData = reader.getDataFromCsv(fileName)
    attrs, data = csvData[0], np.array(csvData[1])

    #Obtengo el resto de los datos.
    fileName = "data/student-por.csv"
    csvData = reader.getDataFromCsv(fileName)
    #Agrego nueva data a la anterior.
    data = np.concatenate((data, csvData[1]))

    k = 10
    data_size = len(data)
    s_size = data_size * 4/5
    print s_size
    fold_size  = s_size / k
    print fold_size
    s = data[:s_size,:]
    #print s
    #T1
    fold = getFold(1,s,fold_size)
    #fold = data[1*fold_size:2*fold_size,:]
    print 'T1'
    print fold
    #D-T1
    s_fold = getSampleWithoutFold(1,s,fold_size,k)
    #s_fold = np.concatenate((data[0*fold_size:1*fold_size,:],data[2*fold_size:k*fold_size,:]))
    print 'D-T1'
    print s_fold
    
#main()
#testExample()
crossValidation()