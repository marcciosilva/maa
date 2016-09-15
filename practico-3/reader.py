from csv import reader

def getDataFromCsv(fileName):
	csv_reader = reader(open(fileName,"rb"), delimiter=";", quotechar="\"")
	rawData = []
	for row in csv_reader:
	    rawData.append(row)
	attrs = rawData[0]
	data = rawData[1:]
	return (attrs, data)