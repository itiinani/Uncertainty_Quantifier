from sklearn.metrics import confusion_matrix, classification_report
from sklearn.preprocessing import StandardScaler
import pandas as pd
import csv
import statistics

def evaluateCI():
    trCIMap = dict()
    print("hello")
    with open('quant_bootstraps.tsv') as tsv:
        for column in zip(*[line for line in csv.reader(tsv, dialect="excel-tab")]):
            bootstrapData = list(column)
            trID = bootstrapData.pop(0)
            bootstrapData = [float(x) for x in bootstrapData]
            mean = statistics.mean(bootstrapData)
            sd = statistics.stdev(bootstrapData, xbar=mean)
            #print(trID)
            #print(mean)
            trCIMap[trID] = [mean,sd]
    return trCIMap

mean_sd = evaluateCI()
v = open("../input/quant.sf","r")
r = csv.reader(v,delimiter="\t")
write = open("../bin/quant_new.csv", "w")
writer = csv.writer(write,dialect='excel',delimiter='\t',quoting=csv.QUOTE_ALL)
for row in r:
    tr = row[0].split('\t')[0]
    if tr != "Name":
        if tr in mean_sd.keys():
            row.append(mean_sd[tr][0])
            row.append(mean_sd[tr][1])
        else:
            row.append("Mean")
            row.append("Std_deviation")
    print(row)
