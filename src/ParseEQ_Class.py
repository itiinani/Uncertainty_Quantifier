from sklearn.cross_validation import train_test_split
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.preprocessing import StandardScaler

from src import FaultyTranscriptFilter
from src import dataForGraphs
import csv
import pandas as pd
from sklearn import svm

def parseEQClass():
    trCount = 0
    lineCount = 0
    trMap = dict()
    trEqMap = dict()
    i = 0
    j = 0
    for line in open('../input/eq_classes.txt'):
        lineCount += 1
        if(lineCount == 1):
            trCount = int(line)
            continue
        if(lineCount == 2):
            continue
        if(i < trCount):
            trMap[i] = line[:-1]
            i += 1
            continue
        val = line.split("\t")
        for tr_id in val[1:-1]:
            eq_tuple = []
            if trMap[int(tr_id)] in trEqMap.keys():
                eq_tuple = trEqMap[trMap[int(tr_id)]]
                val1 = eq_tuple[0] + int(val[len(val) - 1][:-1])
                val2 = eq_tuple[1] + 1
                val3 = eq_tuple[2] + int(val[0])
                val4 = 0
                if int(val[0]) == 1:
                    val4 = eq_tuple[3] + 10000
                else:
                    val4 = eq_tuple[3] - (int(val[0])*100)
                eq_tuple[0] = val1
                eq_tuple[1] = val2
                eq_tuple[2] = val3
                eq_tuple[3] = val4
            else:
                eq_tuple.append(int(val[len(val) - 1][:-1]))
                eq_tuple.append(1)
                eq_tuple.append(int(val[0]))
                if int(val[0]) == 1:
                    eq_tuple.append(10000)
                else:
                    eq_tuple.append(-int(val[0])*100)
            trEqMap[trMap[int(tr_id)]] = eq_tuple
    return trEqMap


def getUniqueAndAmbiguousMaps():
    uniquely_mapped_tr_list = []
    weight_map = dict()
    faultyList = FaultyTranscriptFilter.filterFaultyTranscripts()
    errorMap = dataForGraphs.get_AllTrancriptsError_CSV()

    trEQMap = parseEQClass()
    for tr in faultyList:
        if tr in trEQMap.keys():
            eq_tuple = trEQMap[tr]
            if eq_tuple[1] == 1:
                if eq_tuple[2] == 1:
                    uniquely_mapped_tr_list.append(tr)
    for tr in trEQMap.keys():
        weight_map[tr] = trEQMap[tr][3]

    print("EQ list length: ", len(trEQMap))
    print("Faulty list length: ", len(faultyList))
    print("Uniquely mapped faulty list length: ", len(uniquely_mapped_tr_list))

    v = open("../input/quant.sf","r")
    r = csv.reader(v,delimiter="\t")
    write = open("../bin/quant_new.csv", "w")
    writer = csv.writer(write,dialect='excel',delimiter='\t',quoting=csv.QUOTE_ALL)
    for row in r:
        tr = row[0].split('\t')[0]
        if tr != "Name":
            if tr in uniquely_mapped_tr_list:
                row.append(True)
            else:
                row.append(False)
            if tr in weight_map.keys():
                row.append(weight_map[tr])
            else:
                row.append(0)
            if tr in errorMap.keys():
                row.append(errorMap[tr])
            else:
                row.append(0)
            if tr in faultyList:
                row.append(True)
            else:
                row.append(False)
        else:
            row.append("UniqueMap")
            row.append("Weight")
            row.append("ErrorFraction")
            row.append("Faulty")
        writer.writerow(row)
    v.close()
    write.close()

    train_dataframe = pd.read_csv("../bin/quant_new.csv",sep="\t")
    train_dataframe["Length"] = train_dataframe["Length"].astype(int)
    train_dataframe["EffectiveLength"] = train_dataframe["EffectiveLength"].astype(int)
    train_dataframe["TPM"] = train_dataframe["TPM"].astype(int)
    train_dataframe["NumReads"] = train_dataframe["NumReads"].astype(int)
    train_dataframe["ErrorFraction"] = train_dataframe["NumReads"].astype(int)

    print("Classification started")
    train_dataframe.drop('Length',axis=1)
    train_dataframe.drop('EffectiveLength',axis=1)
    train_dataframe.drop('TPM', axis=1)
    train_dataframe.drop('NumReads',axis=1)
    train_dataframe.drop('Weight', axis=1)
    train_dataframe.drop('UniqueMap', axis=1)
    train_dataframe.drop('ErrorFraction', axis=1)

    train_dataframe = train_dataframe.drop('Name',axis=1)
    X = train_dataframe.drop('Faulty',axis=1)
    y = train_dataframe['Faulty']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1)
    scaler = StandardScaler()
    scaler.fit(X_train)
    print("Training data fitted")
    X_train = scaler.transform(X_train)
    X_test = scaler.transform(X_test)

    clf = svm.SVC(gamma=0.001, C=100)
    clf.fit(X_train, y_train)

    print("Training done")

    predictions = clf.predict(X_test)

    print(confusion_matrix(y_test, predictions))
    print(classification_report(y_test, predictions))
    print("Classification done")


getUniqueAndAmbiguousMaps()
