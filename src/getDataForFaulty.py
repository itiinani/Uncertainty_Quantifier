import pandas as pd

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
    columnTitleRow = "Length,EffectiveLength,TPM,NumReads,Weight\n"
    csv.write(columnTitleRow)
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
            length = data[1]
            effectiveLength = data[2]
            tpm = data[3]
            numReads = data[4]
            weight = data[6]
            row = length + "," + effectiveLength + "," + tpm + "," + numReads + "," + weight + "\n"
            csv.write(row)

createFaultyTranscriptCSV()
createPCData()


