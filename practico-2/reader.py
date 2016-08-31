from csv import reader

def getDataFromCsv(fileName):
	csv_reader = reader(open(fileName,"rb"), delimiter=";", quotechar="\"")
	rawData = []
	for row in csv_reader:
	    rawData.append(row)
	attrs = rawData[0] #head
	data = rawData[1:] #tail
	# print "attributes : " + str(attrs)
	# print "data : " + str(data)
	return (attrs, data)