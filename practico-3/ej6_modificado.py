import numpy as np
import math
import reader
import sys
import treePrinting

def main():
    maxHeight = 6
    parteA(maxHeight)
    # parteB(maxHeight)
    # parteC(maxHeight)

def overfittingTest():
    erroresB = []
    erroresC = []
    for i in range(40):
        erroresB.append(parteB(i))
        erroresC.append(parteC(i))
    print "Errores de parte B segun altura:"
    for i in range(40):
        print str((i, erroresB[i])) + " "
    print "Errores de parte C segun altura:"
    for i in range(40):
        print str((i, erroresC[i])) + " "


def parteA(maxHeight):
    print "### Parte A ###"
    #Obtengo el conjunto completo de datos de prueba.
    fileName = "data/student-mat.csv"
    csvData = reader.getDataFromCsv(fileName)
    attrs, data = csvData[0], np.array(csvData[1])
    #Obtengo el resto de los datos.
    fileName = "data/student-por.csv"
    csvData = reader.getDataFromCsv(fileName)
    #Agrego nueva data a la anterior variable.
    data = np.concatenate((data, csvData[1]))
    #Elimino columnas G1 y G2 para no tomarlos en cuenta
    #para la generacion del arbol de decision.
    attrs = np.delete(attrs, np.s_[30:32], axis=0).tolist()
    data = np.delete(data, np.s_[30:32], axis=1)
    #Se determina altura maxima.
    tree = genDecisionTree(data, attrs, 'G3',maxHeight,0)
    # #Se imprime arbol a archivo de texto
    # f = open('out/arbol-parte-a.txt', 'w')
    # f.write(str(tree))
    # f.close()
    # print "Arbol exportado a out/arbol-parte-a.txt"
    #Imprime arbol exportable a pdf.
    treePrinting.printTree(tree)

def parteB(maxHeight):
    print "### Parte B ###"
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
    print "Cantidad total de instancias en D : " + str(data_size)
    print "Size de muestra para validacion cruzada : " + str(s_size)
    fold_size  = s_size / k
    print "Size de cada subconjunto T_i : " + str(fold_size)
    s = data[:s_size,:]
    targetAttr = 'G3'
    i = 1
    e_aux = 0.0
    for i in range(1,k+1):
        #Se obtiene el conjunto (S_i-Ti), o sea toda la data sin el fold Ti.
        S_i = getSampleWithoutFold(i,s,fold_size,k) 
        #Se entrena con el conjunto S_i
        tree = genDecisionTree(S_i, attrs, 'G3',maxHeight,0)
        #Se obtiene el subconjunto que no se uso para entrenar.
        T_i = getFold(i,s,fold_size)
        e_i = error(tree,attrs,targetAttr,T_i)
        print "Error del arbol generado, validando con el subconjunto T_" + str(i) + " = " + str(e_i)
        e_aux += e_i
    #Promedio de errores estimados para cada subconjunto.
    e = (1.0/k) * e_aux
    print "El error obtenido mediante validacion cruzada es "  + str(e) + " en promedio"
    #Constante de intervalo de confianza para un 95% de confianza.
    constanteIntervaloConfianza = 1.96
    diferencia = constanteIntervaloConfianza * math.sqrt((e * (1.0 - e)) / fold_size)
    print "Un intervalo de confianza del 95% para el error calculado es " + str((e - diferencia, e + diferencia))
    return e

def parteC(maxHeight):
    print "### Parte C ###"
    fileName = "data/student-mat.csv"
    csvData = reader.getDataFromCsv(fileName)
    attrs, data = csvData[0], np.array(csvData[1])
    #Obtengo el resto de los datos.
    fileName = "data/student-por.csv"
    csvData = reader.getDataFromCsv(fileName)
    #Agrego nueva data a la anterior.
    data = np.concatenate((data, csvData[1]))
    data_size = len(data)
    training_set_size = data_size * 4/5
    print "Cantidad total de instancias en D : " + str(data_size)
    validation_set_size = -(data_size - training_set_size)
    print "Size de muestra para validacion : " + str(abs(validation_set_size))
    #Ultimo quinto de la data.
    validation_set = data[validation_set_size:,:]
    training_set = data[:training_set_size,:]
    #Se limita altura maxima.
    # maxHeight = 31
    tree = genDecisionTree(training_set, attrs, 'G3',maxHeight,0)
    #Se imprime arbol a archivo de texto
    f = open('out/arbol-parte-c.txt', 'w')
    f.write(str(tree))
    f.close()
    print "Arbol exportado a out/arbol-parte-c.txt"
    #Imprime arbol exportable a pdf.
    treePrinting.printTree(tree)
    #Evaluo el validation_set con este arbol generado.
    targetAttr = 'G3'
    e = error(tree, attrs, targetAttr, validation_set)
    print "El error estimado obtenido es " + str(e)
    #Constante de intervalo de confianza para un 95% de confianza.
    constanteIntervaloConfianza = 1.96
    diferencia = constanteIntervaloConfianza * math.sqrt((e * (1.0 - e)) / (-validation_set_size))
    print "Un intervalo de confianza del 95% para el error calculado es " + str((e - diferencia, e + diferencia))
    return e

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
    # tree = {bestAttr:{}}
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
            # print decisionTree[node].keys()
            # print "Tree node is " + str(node)
            #Valor mas comun asociado en construccion.
            # print "Unknown value " + "(" + attributeValue + ")" + " at node " + node[0]
            attributeValue = node[1]
            # print "Just assigned " + attributeValue + " to it"
        #De otra manera, simplemente sigo la rama que corresponda con
        #el valor original del atributo para la instancia.
        nextBranchOrValue = decisionTree[node][attributeValue]
        #Si estoy frente a una nueva rama, me sigo moviendo en ella
        if (isinstance(nextBranchOrValue,dict)):
            return evalInstance(instance, attributes, nextBranchOrValue)
        #De otra manera, devuelvo la clasificacion obtenida.
        else:
            # print str(instance) + " classifies as " + nextBranchOrValue
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

main()