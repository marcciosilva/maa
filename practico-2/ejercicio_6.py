import numpy as np
import math

def main():
	attrs=['a','b','target']
	data=np.array([[1,2,1], [1,4,1], [1,6,1], [1,2,1], [1,4,1], [1,6,1], [1,3,0], [1,3,0]])
	print entropy(attrs, data, 'target')

#Retorna la entropia de un conjunto de datos para un determinado atributo objetivo.
def entropy(attributes, data, targetAttr):

    i = attributes.index(targetAttr)
    targetValues = data[:,i]
	
    valFreq = {} #Frecuencia de cada valor del target atributo objetivo dentro del conjunto de datos.
    entropy = 0.0

    for targetValue in targetValues:
        if (valFreq.has_key(targetValue)):
            valFreq[targetValue] += 1.0
        else:
            valFreq[targetValue]  = 1.0
   
    for freq in valFreq.values():
        entropy += (-freq/len(data)) * math.log(freq/len(data), 2) 
        
    return entropy
	
main()