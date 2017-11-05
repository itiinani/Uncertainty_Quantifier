from sklearn.cross_validation import train_test_split
from sklearn.tree import DecisionTreeClassifier

from src import FaultyTranscriptFilter
import csv
import pandas as pd
import numpy as np
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
                    val4 = eq_tuple[3] - int(val[0])
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
                    eq_tuple.append(-int(val[0]))
            trEqMap[trMap[int(tr_id)]] = eq_tuple
    return trEqMap


def getUniqueAndAmbiguousMaps():
    unique_map = dict()
    uni_uni_map = dict()
    ambiguous_map = dict()
    weight_map = dict()
    notInEq = []
    faultyList = FaultyTranscriptFilter.filterFaultyTranscripts()


    trEQMap = parseEQClass()
    for tr in faultyList:
        if tr in trEQMap.keys():
            eq_tuple = trEQMap[tr]
            if eq_tuple[1] == 1:
                if eq_tuple[2] == 1:
                    uni_uni_map[tr] = eq_tuple[0]
                else:
                    unique_map[tr] = eq_tuple[0]
            else:
                ambiguous_map[tr] = eq_tuple[0]
        else:
            notInEq.append(tr)
    for tr in trEQMap.keys():
        weight_map[tr] = trEQMap[tr][3]

    print("EQ list length: ", len(trEQMap))
    print("Faulty list length: ", len(faultyList))
    print("Uni uni mapped faulty list length: ", len(uni_uni_map))
    print("Uniquely mapped faulty list length: ", len(unique_map))
    print("Ambiguously mapped faulty list length: ", len(ambiguous_map))
    print("Non-mapped faulty list length: ", len(notInEq))

    # df = pd.read_csv("../input/quant.csv")
    # print(df)

    v = open("../input/quant.csv","r")
    r = csv.reader(v,delimiter="\t")
    write = open("quant_new.csv", "w")
    writer = csv.writer(write,dialect='excel',delimiter='\t',quoting=csv.QUOTE_ALL)
    for row in r:
        tr = row[0].split('\t')[0]
        if tr != "Name":
            if tr in uni_uni_map.keys():
                row.append("1")
            else:
                row.append("0")
            if tr in weight_map.keys():
                row.append(str(weight_map[tr]))
            else:
                row.append("0")
            if tr in faultyList:
                row.append("1")
            else:
                row.append("0")
        else:
            row.append("uniquemap")
            row.append("weight")
            row.append("faulty")
        # print(row)
        writer.writerow(row)
    v.close()
    write.close()

    train_dataframe = pd.read_csv("quant_new.csv",sep="\t")
    # print(df)
    # print(df["Name"])
    print("Classification started")
    X = train_dataframe.values[:,1:7]
    Y = train_dataframe.values[:,7]
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.3, random_state=100)
    clf_gini = DecisionTreeClassifier(criterion="gini", random_state=100,
                                      max_depth=3, min_samples_leaf=5)
    clf_gini.fit(X_train, y_train)
    print("Classification done")


getUniqueAndAmbiguousMaps()
