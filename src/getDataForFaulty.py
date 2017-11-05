import pandas as pd

def getErrorFractionAll():
    lineCount = 0
    errorMap = dict()
    for line in open('../input/errorFraction_all.csv'):
        lineCount += 1
        if lineCount == 1:
            continue
        data = line.split(',')
        print(len(data))
        errorMap[data[1]] = data[2]
    return errorMap

def getErrorFractionFaulty():
    lineCount=0
    errorMap = dict()
    for line in open('../input/errorFraction_faulty.csv'):
        lineCount+=1
        if lineCount ==1:
            continue
        data = line.split(',')
        print(len(data))
        errorMap[data[1]] = data[2]
    return errorMap

def createFaultyTranscriptCSV():
    lineCount =0
    faultyMap = dict()
    download_dir = "../input/faultyTrData.csv"
    csv = open(download_dir, "w")
    columnTitleRow = "ID,Length,EffectiveLength,TPM,NumReads,Weight\n"
    csv.write(columnTitleRow)
    for line in open('../input/quant_new.csv'):
        lineCount += 1
        if lineCount == 1:
            continue
        if lineCount%2 ==0:
            continue
        print(line)
        data = line.split('\t')
        print(len(data))
        if data[7]=='"1"\n':
            ID = data[0]
            length = data[1]
            effectiveLength = data[2]
            tpm = data[3]
            numReads = data[4]
            weight = data[6]
            row = ID + "," + length + ","+effectiveLength+","+tpm+","+numReads+","+weight+"\n"
            csv.write(row)

def createPCData():
    lineCount = 0
    faultyMap = dict()
    download_dir = "../input/PCData.csv"
    csv = open(download_dir, "w")
    columnTitleRow = "NumReads,TPM,ErrorFraction,Weight\n"
    csv.write(columnTitleRow)
    errorMap = getErrorFractionFaulty()
    for line in open('../input/quant_new.csv'):
        lineCount += 1
        if lineCount == 1:
            continue
        if lineCount % 2 == 0:
            continue
        print(line)
        data = line.split('\t')
        print(len(data))

        if data[7] == '"1"\n':
            tpm = data[3]
            numReads = data[4]
            weight = data[6]
            if data[0].replace('"','') in errorMap.keys():
                errorFraction = errorMap[data[0].replace('"','')]
                row = numReads + "," + tpm + "," + errorFraction + "," + weight + "\n"
                csv.write(row)


def createDataForForceDirected():
    trCount = 0
    lineCount = 0
    trMap = dict()
    trEqMap = dict()
    i = 0
    j = 0
    classID =0;
    download_dir = "../input/ForceDirectedData.csv"
    csv = open(download_dir, "w")
    columnTitleRow = "source,target\n"
    csv.write(columnTitleRow)
    for line in open('../input/eq_classes.txt'):
        lineCount += 1
        if (lineCount == 1):
            trCount = int(line)
            continue
        if (lineCount == 2):
            continue
        if (i < trCount):
            trMap[i] = line[:-1]
            i += 1
            continue
        val = line.split("\t")
        for tr_id in val[1:-1]:
            transcript = trMap[int(tr_id)]
            classNumber = str(classID)
            row = transcript+","+classNumber+"\n"
            csv.write(row)
        classID = classID+1

createDataForForceDirected()
createFaultyTranscriptCSV()
createPCData()


