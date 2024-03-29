import numpy as np
import math
import reader
import sys
import decisionTrees
import treePrinting
import atexit
from random import randint
from time import clock

def secondsToStr(t):
    return "%d:%02d:%02d.%03d" % \
        reduce(lambda ll,b : divmod(ll[0],b) + ll[1:],
            [(t*1000,),1000,60,60])

line = "="*40
def log(s, elapsed=None):
    print line
    print secondsToStr(clock()), '-', s
    if elapsed:
        print "Elapsed time:", elapsed
    print line
    print

def endlog():
    end = clock()
    elapsed = end-start
    log("End Program", secondsToStr(elapsed))

def now():
    return secondsToStr(clock())

start = clock()
atexit.register(endlog)
log("Start Program")
#Como las notas van de 0 a 20, tenemos 21 posibles notas.
cantNotasPosibles = 21

#Comparacion basada en seccion 5.6 del Mitchell.
def comparacionAlgoritmos():
    #Manejo de data.
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
    #Elimino columnas G1 y G2 para no tomarlos en cuenta
    #para la generacion del arbol de decision.
    attrs = np.delete(attrs, np.s_[30:32], axis=0).tolist()
    data = np.delete(data, np.s_[30:32], axis=1)
    iteraciones = 25
    #Listas para acumular estimacion de diferencia de errores
    #entre algoritmos.
    diff_NB_KNN1 = iteraciones * [0]
    diff_NB_KNN3 = iteraciones * [0]
    diff_NB_DT = iteraciones * [0]
    diff_KNN1_KNN3 = iteraciones * [0]
    diff_KNN1_DT = iteraciones * [0]
    diff_KNN3_DT = iteraciones * [0]
    k = 10
    training_set_size = data_size * 4/5
    print "Cantidad total de instancias en D : " + str(data_size)
    print "Size de muestra para entrenamiento con metodos de aprendizaje : " + str(training_set_size)
    #Tamanio de conjunto de validacion
    validation_set_size  = data_size - training_set_size
    print "Size de cada subconjunto de validacion : " + str(validation_set_size)
    for iteracion in range(iteraciones):
        print "##########################################################"
        print "Iteracion " + str(iteracion + 1)
        print "##########################################################"
        #Desordeno instancias
        data = np.random.permutation(data)
        #Listas para acumular sample errors.
        erroresSampleNB = k * [0]
        erroresSampleKNN1 = k * [0]
        erroresSampleKNN3 = k * [0]
        erroresSampleDT = k * [0]
        for i in range(1,k+1):
            #Se obtiene el conjunto (S_i-Ti), o sea toda la data sin el fold Ti.
            S_i = decisionTrees.getSampleWithoutFold(i,data,validation_set_size,k) 
            #Se entrena con el conjunto S_i
            # tree = genDecisionTree(S_i, attrs, 'G3',maxHeight,0)
            # #Se obtiene el subconjunto que no se uso para entrenar.
            validation_set = decisionTrees.getFold(i,data,validation_set_size)
            #Genero arbol de decision.
            maxHeight = 6
            tree = decisionTrees.genDecisionTree(S_i, attrs, 'G3',maxHeight,0)
            auxNB = 0
            auxKNN_1 = 0
            auxKNN_3 = 0
            auxDT = 0
            for validationInstance in validation_set:
                #Se suma 1 si fue un acierto, 0 en caso contrario.
                auxNB += clasificadorNB(validationInstance,attrs,S_i,targetAttr)
                auxKNN_1 += clasificadorKNN(validationInstance,attrs,S_i,targetAttr,1)
                auxKNN_3 += clasificadorKNN(validationInstance,attrs,S_i,targetAttr,3)
                auxDT += clasificadorDecisionTree(validationInstance,attrs,targetAttr,tree)
            #Calculo error de sample para cada algoritmo.
            #validation_set_size - auxX va a ser la cantidad de errores de cada algoritmo.
            erroresSampleNB[i-1] = (1.0/validation_set_size*(validation_set_size - auxNB))
            erroresSampleKNN1[i-1] = (1.0/validation_set_size*(validation_set_size - auxKNN_1))
            erroresSampleKNN3[i-1] = (1.0/validation_set_size*(validation_set_size - auxKNN_3))
            erroresSampleDT[i-1] = (1.0/validation_set_size*(validation_set_size - auxDT))
        #Ya tengo los sample errors para cada metodo, para todo set de validacion.
        #Error estimado entre NB y KNN1
        sum_aux = 0
        for i in range(k):
            sum_aux += erroresSampleNB[i] - erroresSampleKNN1[i]
        errorEstimado = (1.0/k) * sum_aux
        diff_NB_KNN1[iteracion] = errorEstimado
        print "Estimacion de diferencia en error entre NB y KNN1 = " + str(errorEstimado)
        #Error estimado entre NB y KNN3
        sum_aux = 0
        for i in range(k):
            sum_aux += erroresSampleNB[i] - erroresSampleKNN3[i]
        errorEstimado = (1.0/k) * sum_aux
        diff_NB_KNN3[iteracion] = errorEstimado
        print "Estimacion de diferencia en error entre NB y KNN3 = " + str(errorEstimado)    
        #Error estimado entre NB y DT
        sum_aux = 0
        for i in range(k):
            sum_aux += erroresSampleNB[i] - erroresSampleDT[i]
        errorEstimado = (1.0/k) * sum_aux
        diff_NB_DT[iteracion] = errorEstimado
        print "Estimacion de diferencia en error entre NB y DT = " + str(errorEstimado)    
        #Error estimado entre KNN1 y KNN3
        sum_aux = 0
        for i in range(k):
            sum_aux += erroresSampleKNN1[i] - erroresSampleKNN3[i]
        errorEstimado = (1.0/k) * sum_aux
        diff_KNN1_KNN3[iteracion] = errorEstimado
        print "Estimacion de diferencia en error entre KNN1 y KNN3 = " + str(errorEstimado)    
        #Error estimado entre KNN1 y DT
        sum_aux = 0
        for i in range(k):
            sum_aux += erroresSampleKNN1[i] - erroresSampleDT[i]
        errorEstimado = (1.0/k) * sum_aux
        diff_KNN1_DT[iteracion] = errorEstimado
        print "Estimacion de diferencia en error entre KNN1 y DT = " + str(errorEstimado)    
        #Error estimado entre KNN3 y DT
        sum_aux = 0
        for i in range(k):
            sum_aux += erroresSampleKNN3[i] - erroresSampleDT[i]
        errorEstimado = (1.0/k) * sum_aux
        diff_KNN3_DT[iteracion] = errorEstimado
        print "Estimacion de diferencia en error entre KNN3 y DT = " + str(errorEstimado)    
    print "diff_NB_KNN1: " + str(diff_NB_KNN1)
    print "diff_NB_KNN3: " + str(diff_NB_KNN3)
    print "diff_NB_DT: " + str(diff_NB_DT)
    print "diff_KNN1_KNN3: " + str(diff_KNN1_KNN3)
    print "diff_KNN1_DT: " + str(diff_KNN1_DT)
    print "diff_KNN3_DT: " + str(diff_KNN3_DT)

def testAciertos(startRange, endRange):
    #Acumuladores de aciertos.
    porcentajeAciertosNB = []
    porcentajeAciertosKNN1 = []
    porcentajeAciertosKNN3 = []
    porcentajeAciertosDT = []
    porcentajeAciertosRandom = []
    #Manejo de data.
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
    #Elimino columnas G1 y G2 para no tomarlos en cuenta
    #para la generacion del arbol de decision.
    attrs = np.delete(attrs, np.s_[30:32], axis=0).tolist()
    data = np.delete(data, np.s_[30:32], axis=1)

    for iteracion in range(startRange,endRange):
        #Desordeno instancias
        dataTmp = np.random.permutation(data)
        s_size = data_size * 4/5
        # print "Cantidad total de instancias en D : " + str(data_size)
        # print "Size de muestra para entrenar NB : " + str(s_size)
        sample = dataTmp[:s_size,:]
        #Genero arbol de decision.
        maxHeight = 2
        tree = decisionTrees.genDecisionTree(sample, attrs, 'G3',maxHeight,0)
        auxNB = 0
        auxKNN1 = 0
        auxKNN3 = 0
        auxDT = 0
        auxRandom = 0
        for x in range(s_size,data_size):
            instancia = dataTmp[x,:]
            #Se suma 1 si fue un acierto, 0 en caso contrario.
            auxNB += clasificadorNB(instancia,attrs,sample,targetAttr)
            auxKNN1 += clasificadorKNN(instancia,attrs,sample,targetAttr,1)
            auxKNN3 += clasificadorKNN(instancia,attrs,sample,targetAttr,3)
            auxDT += clasificadorDecisionTree(instancia,attrs,targetAttr,tree)
            #Clasifico aleatoriamente.
            if (int(instancia[attrs.index(targetAttr)]) == randint(0,20)):
                auxRandom += 1
            # print "----------------------------------------------------------------"
        porcentajeAciertosNB.append(round(100.00 * auxNB / (data_size - s_size),2))
        porcentajeAciertosKNN1.append(round(100.00 * auxKNN1 / (data_size - s_size),2))
        porcentajeAciertosKNN3.append(round(100.00 * auxKNN3 / (data_size - s_size),2))
        porcentajeAciertosDT.append(round(100.00 * auxDT / (data_size - s_size),2))
        porcentajeAciertosRandom.append(round(100.00 * auxRandom / (data_size - s_size),2))
    lstSize = len(porcentajeAciertosNB)
    print "Aciertos NB: "
    for i in range(lstSize):
        print "(" + str(i + startRange) + "," + str(porcentajeAciertosNB[i]) + ") "
    print ""
    print "Aciertos KNN1: "
    for i in range(lstSize):
        print "(" + str(i + startRange) + "," + str(porcentajeAciertosKNN1[i]) + ") "    
    print ""
    print "Aciertos KNN3: "
    for i in range(lstSize):
        print "(" + str(i + startRange) + "," + str(porcentajeAciertosKNN3[i]) + ") "    
    print ""    
    print "Aciertos DT: "
    for i in range(lstSize):
        print "(" + str(i + startRange) + "," + str(porcentajeAciertosDT[i]) + ") "
    print ""
    print "Aciertos Random: "
    for i in range(lstSize):
        print "(" + str(i + startRange) + "," + str(porcentajeAciertosRandom[i]) + ") "    

def clasificadorNB(instancia,attrs,sample,targetAttr):
    # print "### clasificador NB ###"
    # print "Clasificando instancia: " + str(instancia)
    #Genero arreglos de 21 ceros.
    p = cantNotasPosibles * [0]
    #Arreglo que almacena la cantidad de ocurrencias para cada nota,
    #segun el sample (atributo G3).
    cantNota = cantNotasPosibles * [0]
    #Quito tres ultimos atributos porque no se utilizan al clasificar.
    attrsSinNotas = attrs[:-1]
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
                m[i,x] = m[i,x] / float(cantNota[i])
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

    # print "maximo = " + str(maximo) + ", total = " + str(total)
    porcentaje = round((maximo / total * 100.0),2)
    # print "Con un " + str(porcentaje) + "%" + " de seguridad puedo afirmar que la nota final es: " + str(notaRes) + "."
    if (int(instancia[attrs.index(targetAttr)]) == notaRes):
        return 1
    else:
        return 0

binaryAttrs = ["school", "sex", "address", "famsize", "Pstatus", "schoolsup", 
    "famsup", "paid", "activities", "nursery", "higher", "internet", "romantic"]
nominalAttrs = ["Mjob", "Fjob", "reason", "guardian"]

def isAttrBinary(attr):
    return attr in binaryAttrs

def isAttrNominal(attr):
    return attr in nominalAttrs

#Equivalencias de atributos nominales a numericos.
equivalenceXjob = {"other" : 0, "services" : 1, "health" : 2, "teacher" : 3, "at_home" : 4}
equivalenceReason = {"reputation" : 0, "course" : 1, "home" : 2, "other" : 3}
equivalenceGuardian = {"father" : 0, "mother" : 1, "other" : 2}
#Limites en los valores de atributos de interes (no binarios).
maxAttrValue = {"age" : 22, "Medu" : 4, "Fedu" : 4, "Mjob" : 4, "Fjob" : 4, "reason" : 3, 
    "guardian" : 2, "traveltime" : 4, "studytime" : 4, "failures" : 4, "famrel" : 5, 
    "freetime" : 5, "goout" : 5, "Dalc" : 5, "Walc" : 5, "health" : 5, "absences" : 93}
minAttrValue = {"age" : 15, "Medu" : 0, "Fedu" : 0, "Mjob" : 0, "Fjob" : 0, "reason" : 0, 
    "guardian" : 0, "traveltime" : 1, "studytime" : 1, "failures" : 0, "famrel" : 1, 
    "freetime" : 1, "goout" : 1, "Dalc" : 1, "Walc" : 1, "health" : 1, "absences" : 0}

#Recibe a cada valor de atributo con el tipo compartido por ambos.
#Se asume que se pasan atributos del mismo tipo por parametro.
def distAttrValues(attrsType, fstAttr, sndAttr):
    if (isAttrBinary(attrsType)):
        #Distancia de Hamming para atributos binarios.
        if (fstAttr == sndAttr):
            return 0.0
        else:
            return 1.0
    elif (isAttrNominal(attrsType)):
        #Distancias asignadas para atributos nominales.
        if (attrsType == "Mjob" or attrsType == "Fjob"):
            distance = abs(equivalenceXjob[fstAttr] - equivalenceXjob[sndAttr])
        elif (attrsType == "reason"):
            distance = abs(equivalenceReason[fstAttr] - equivalenceReason[sndAttr])
        #Si es guardian por descarte.
        else:
            distance = abs(equivalenceGuardian[fstAttr] - equivalenceGuardian[sndAttr])
        #Normalizo distancia de acuerdo al rango de valores 
        #que toma el atributo.            
        return float(distance) / (maxAttrValue[attrsType] - minAttrValue[attrsType])
    #Atributos numericos por descarte.
    else:
        # print "fstAttr: " + str(fstAttr) + ", sndAttr: " + str(sndAttr)
        distance = abs(int(fstAttr) - int(sndAttr))
        #Normalizo distancia de acuerdo al rango de valores 
        #que toma el atributo.        
        return float(distance) / (maxAttrValue[attrsType] - minAttrValue[attrsType])

#Calcula distancia entre dos instancias.
def distInstances(fstInstance, sndInstance, attrTypes):
    # print "###############################"
    # print "Instance 1: " + str(fstInstance)
    # print "Instance 2: " + str(sndInstance)
    # print "###############################"
    result = 0
    #Para cada atributo.
    for i in range(len(attrTypes[:-1])):
        #Sumo distancia al cuadrado entre valores de atributo.
        result += math.pow(distAttrValues(attrTypes[i], fstInstance[i], sndInstance[i]), 2)
    result = math.sqrt(result)
    return result

def clasificadorKNN(instancia,attrs,sample,targetAttr,k):
    # print "### clasificador KNN ###"
    # print "Clasificando instancia: " + str(instancia)
    #Copia local de sample.
    sampleCopy = np.empty_like(sample)
    sampleCopy[:] = sample
    #for toda instancia de sampleCopy
        #si la distancia a la instancia actual es menor que l
    #Clave: instancia, valor: distancia
    distances = {}
    for row in sampleCopy:
        instance = tuple(row)
        distance = distInstances(instancia, instance, attrs)
        if (instance in distances.keys()):
            #En caso de que haya una instancia igual, se utiliza la distancia mas corta.
            if (distance < distances[instance]):
                distances[instance] = distance
        else:
            #Convierto a tupla porque un tipo mutable no puede ser
            #clave de un diccionario.
            distances[instance] = distance
    #Ahora en distances tengo a todas las sample instances cargadas
    #con su respectiva distancia desde/hacia "instancia".

    #Obtengo k instancias mas cercanas (super ineficiente).
    instanciasCercanas = []
    for i in range(k):
        minDist = sys.maxint
        chosenInstance = []
        for instance in distances.keys():
            tmp = distances[instance]
            if (tmp < minDist and not (instance in instanciasCercanas)):
                minDist = tmp
                chosenInstance = instance
        #Instancia encontrada.
        if (len(chosenInstance) > 0):
            # print "dist for k:" + str(i) + " = " + str(minDist)
            # print "clasificacion para instancia cercana: " + str(chosenInstance[-1])
            instanciasCercanas.append(chosenInstance)
            # del distances[chosenInstance]

    #Clasificacion a determinar.
    clasificacion = -1
    sumatoria = -sys.maxint - 1
    exactMatch = False
    #Algoritmo de clasificacion. P.232 Mitchell.
    clasificacionPosible = 0
    while (clasificacionPosible < cantNotasPosibles and not exactMatch):
    # for clasificacionPosible in (range(cantNotasPosibles)):
        #Para toda instancia cercana.
        #Asumiendo que se consiguieron k instancias.
        tmpSumatoria = 0
        i = 0
        while (i < k and not exactMatch):
        # for i in range(k):
            # print "Clasificacion posible = " + str(clasificacionPosible) + ", instanciasCercanas[i][attrs.index(targetAttr)] = " + str(instanciasCercanas[i][attrs.index(targetAttr)])
            if (clasificacionPosible == int(instanciasCercanas[i][attrs.index(targetAttr)])):
                divisor = math.pow(distances[instanciasCercanas[i]], 2.0)
                #Si la distancia resulta 0 se asume que la distancia entre instancias
                #es 0, y por lo tanto se asigna directamente esa clasificacion
                if (divisor == 0.0):
                    exactMatch = True
                    clasificacion = clasificacionPosible
                else:
                    tmpSumatoria += 1.0 / divisor
            i += 1

        if (not exactMatch and tmpSumatoria > sumatoria and tmpSumatoria != 0):
            sumatoria = tmpSumatoria
            clasificacion = clasificacionPosible
        clasificacionPosible += 1
    # print "La clasificacion asignada es " + str(clasificacion) + "."
    if (int(instancia[attrs.index(targetAttr)]) == clasificacion):
        return 1
    else:
        return 0

def clasificadorDecisionTree(instancia,attrs,targetAttr,tree):
    clasificacion = decisionTrees.evalInstance(instancia, attrs, tree)
    # print "La clasificacion asignada es " + str(clasificacion) + "."
    if (int(instancia[attrs.index(targetAttr)]) == int(clasificacion)):
        return 1
    else:
        return 0    

# comparacionAlgoritmos()
# testAciertos(0,100)