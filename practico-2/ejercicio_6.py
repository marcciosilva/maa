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
            valFreq[attrValue]  = 1.0
	
    attrEntropy = 0.0
    dataLength = len(data)
    for val in valFreq.keys():
        valProb        = valFreq[val] / dataLength
        attrData     = np.array([entry for entry in data if entry[i] == val])
        attrEntropy += valProb * entropy(attributes, attrData, targetAttr)
 
    return (entropy(attributes, data, targetAttr) - attrEntropy)
	
main()