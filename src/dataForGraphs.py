from src import FaultyTranscriptFilter
import pandas as pd

def getErrorCSV():
    faultyList = FaultyTranscriptFilter.filterFaultyTranscripts()
    lineCount = 0
    truthMap = dict()
    quantMap = dict()
    for line in open('../input/poly_truth.tsv'):
        lineCount += 1
        if lineCount == 1:
            continue
        data = line.split('\t')
        if data[0] in faultyList:
            truthMap[data[0]] = int(data[1])
    for line in open('../input/quant.tsv'):
        lineCount += 1
        if lineCount == 1:
            continue
        data1 = line.split('\t')
        if data1[0] in faultyList:
            quantMap[data1[0]] = int(data1[1])

    resultMap = dict()
    for x in truthMap.keys():
        truthValue = truthMap.get(x)
        quantValue = quantMap.get(x)
        errorFraction = (truthValue - quantValue)/truthValue
        resultMap[x] = errorFraction
    df = pd.DataFrame(resultMap.items(), columns=['TranscriptID', 'ErrorFraction'])
    df.to_csv("errorFraction.csv", encoding='utf-8')

getErrorCSV()


