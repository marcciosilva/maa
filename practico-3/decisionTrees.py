import numpy as np
import math
import sys

'''
Retorna la entropia de un conjunto de datos para un determinado atributo objetivo.
'''
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

'''
Retorna el information gain para el atributo attr y el atributo objetivo targetAttr.
'''
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
 
'''
Obtiene el atributo que aporta mas information gain.
'''
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
    
'''
Retorna el valor mas comun del atributo objetivo.
'''
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

'''
Construye y retorna el arbol de decision.
'''
def genDecisionTree(data, attributes, target,maxHeight,currentHeight):
    data = np.array(data[:])
    #Obtengo un arreglo con todos los valores del atributo target
    #en cada instancia.
    targetValues = data[:,attributes.index(target)]
    mcv = mostCommonValue(targetValues)
    
    #Si todas las instancias tienen el mismo valor para el atributo,
    #etiquetar con ese valor.
    if len(set(targetValues)) == 1:
        return targetValues[0]
    
    #Si no quedan atributos, etiquetar con el valor mas comun.
    if (len(attributes) -1) == 0:
        return mcv

    #Si llego al largo maximo establecido para las ramas, etiquetar 
    #con el valor mas comun.
    if currentHeight == maxHeight:
        return mcv

    #Si no alcance el largo maximo, continua creciendo la rama.
    currentHeight = currentHeight + 1

    # Se elige el mejor atributo segun su information gain.
    bestAttr = getBestAttr(data, attributes, target)
    bestAttrIndex = attributes.index(bestAttr)

    bestAttrTargetValues = data[:,bestAttrIndex]
    bestAttrMostCommonValue = mostCommonValue(bestAttrTargetValues)


    #Genero una rama.
    #Cada nodo tendra su valor mas comun (de acuerdo a ejemplos de 
    #entrenamiento) asociado
    tree = {(bestAttr, bestAttrMostCommonValue):{}}

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
        tree[(bestAttr,bestAttrMostCommonValue)][val] = subtree
    
    return tree

'''
Clasifica una instancia de acuerdo a un arbol de decision.
'''
def evalInstance(instance, attributes, decisionTree):
    if (isinstance(decisionTree,dict)):
        #Obtengo nodo.
        node = decisionTree.keys()[0]
        #Obtengo indice del atributo en el arreglo de atributos posibles.
        index = attributes.index(node[0])
        #Si el valor del atributo de interes no es contemplado por el arbol,
        #se lo intercambia por el valor mas comun para ese atributo.

        attributeValue = instance[index]
        #Si no es una etiqueta soportada.
        if (not attributeValue in decisionTree[node].keys()):
            #Valor mas comun asociado en construccion.
            attributeValue = node[1]
        #De otra manera, simplemente sigo la rama que corresponda con
        #el valor original del atributo para la instancia.
        nextBranchOrValue = decisionTree[node][attributeValue]
        #Si estoy frente a una nueva rama, me sigo moviendo en ella
        if (isinstance(nextBranchOrValue,dict)):
            return evalInstance(instance, attributes, nextBranchOrValue)
        #De otra manera, devuelvo la clasificacion obtenida.
        else:
            return nextBranchOrValue
    else:
        return sys.maxint

'''
Obtiene un subconjunto a partir de un conjunto de datos.
'''
def getFold(i,data,fold_size):
    return data[(i-1)*fold_size:i*fold_size,:]

'''
Quita un subconjunto de un conjunto de datos.
'''
def getSampleWithoutFold(i,data,fold_size,k):
    return np.concatenate((data[0:(i-1)*fold_size,:],data[i*fold_size:k*fold_size,:]))

'''
Funcion que evalua el error cometido al intentar clasificar las instancias
del conjunto de validacion pasado por parametro, no tomado en cuenta para realizar 
el entrenamiento.
'''
def error(tree,attrs,targetAttr,validation_set):
    tmpAttrs = attrs[:-1]
    e_aux = 0
    for instance in validation_set:
        #Valor asignado por hipotesis obtenida mediante entrenamiento.
        h_x = float(evalInstance(instance, tmpAttrs, tree))
        #Valor asignado por funcion objetivo.
        f_x = float(instance[attrs.index(targetAttr)])
        if (h_x != f_x):
            e_x = 1.0
        else:
            e_x = 0.0
        e_aux += e_x

    return (1.0/len(validation_set)*e_aux)