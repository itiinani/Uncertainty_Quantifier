from src import FaultyTranscriptFilter
import csv

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
                eq_tuple[0] = val1
                eq_tuple[1] = val2
                eq_tuple[2] = val3
            else:
                eq_tuple.append(int(val[len(val) - 1][:-1]))
                eq_tuple.append(1)
                eq_tuple.append(int(val[0]))
            trEqMap[trMap[int(tr_id)]] = eq_tuple
    return trEqMap


def getUniqueAndAmbiguousMaps():
    unique_map = dict()
    uni_uni_map = dict()
    ambiguous_map = dict()
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

    print("EQ list length: ", len(trEQMap))
    print("Faulty list length: ", len(faultyList))
    print("Uni uni mapped faulty list length: ", len(uni_uni_map))
    print("Uniquely mapped faulty list length: ", len(unique_map))
    print("Ambiguously mapped faulty list length: ", len(ambiguous_map))
    print("Non-mapped faulty list length: ", len(notInEq))

    v = open('../input/quant.csv')
    r = csv.reader(v)
    print "done reading"
    row = r.next()
    while row:
        if row[0] in faultyList:
            row.append(1)
        else:
            row.append(0)
        if row[0] in uni_uni_map.keys():
            row.append(1)
        else:
            row.append(0)
        row = r.next()
    print "Done"

getUniqueAndAmbiguousMaps()
