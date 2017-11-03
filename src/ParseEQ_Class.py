from src import FaultyTranscriptFilter

def parseEQClass():
    trCount = 0
    eqCount = 0
    lineCount = 0
    trMap = dict()
    trEqMap = dict()
    i = 0
    j = 0
    unique_list = []
    amb_map = dict()
    for line in open('../input/eq_classes.txt'):
        lineCount += 1
        if(lineCount == 1):
            trCount = int(line)
            continue
        if(lineCount == 2):
            eqCount = int(line)
            continue
        if(i < trCount):
            trMap[i] = line[:-1]
            i += 1
            continue
        val = line.split("\t")
        if val[0] == '1':
            unique_list.append((trMap[int(val[1])],int(val[2][:-1])))
        else:
            for tr_id in val[1:-1]:
                if trMap[int(tr_id)] in amb_map.keys():
                    amb_map[trMap[int(tr_id)]] += int(val[len(val)-1][:-1])
                else:
                    amb_map[trMap[int(tr_id)]] = int(val[len(val)-1][:-1])

    return [unique_list, amb_map]


faulty = FaultyTranscriptFilter.filterFaultyTranscripts()
print(len(faulty))

eq_output = parseEQClass()

def compareUniqueTrWithFaulty():
    unique_list = eq_output[0]
    uni_common_list = []
    print(len(unique_list))
    for tr in unique_list:
        if tr[0] in faulty:
            uni_common_list.append(tr)
    return uni_common_list


def compareAmbTrWithFaulty():
    amb_map = eq_output[1]
    amb_common_list = []
    print(len(amb_map))
    for tr in faulty:
        if tr in amb_map.keys():
            amb_common_list.append((tr, amb_map[tr]))
    return amb_common_list


uni_common_list = compareUniqueTrWithFaulty()
amb_common_list = compareAmbTrWithFaulty()

print(len(uni_common_list))
print(uni_common_list)

print(len(amb_common_list))
print(amb_common_list)
