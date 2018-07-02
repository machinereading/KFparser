
# coding: utf-8

# In[2]:

import json
import etri

f1 = './koreanframenet/data/bak/test.tsv'
f2 = './koreanframenet/data/bak/training.tsv'
f3 = './koreanframenet/data/bak/training_fe.tsv'
files = [f1, f2, f3]

def getCoNLL(lines, filename):
    filetype = filename.split('/')[-1]
    target_file = './'+filetype
    result = []
    sent = []
    sent_ids = []
    each_sent = {}
    for line in lines:
        line = line.rstrip('\n')
        if line.startswith('#'):
            if line[1] == 's':
                #sent_id = line.split(':')[1]
                each_sent['sent_id'] = line
            else:
                #text = line[6:]
                each_sent['text'] = line
        else:
            if line != '':
                token = line.split('\t')
                sent.append(token)
            else:
                each_sent['conll'] = sent
                result.append(each_sent)
                each_sent = {}
                sent = []
    with open(target_file, 'a') as f:
        for i in result:
            sent_id = i['sent_id']
            text = i['text']
            ori_text = text[6:]
            f.write(sent_id+'\n')
            f.write(text+'\n')
            conll = i['conll']
            etri_result = etri.getETRI_CoNLL2006(ori_text)
            morp = []
            for i in range(len(conll)):
                conll[i][2] = etri_result[i][2]
                if conll[i][11] != '_':
                    conll[i][11] = conll[i][11].lower()
            for token in conll:
                line = '\t'.join(map(str,token))
                f.write(line+'\n')
            f.write('\n')
    print('write:', target_file)

def genData():
    for i in files:
        with open(i, 'r') as f:
            d = f.readlines()
            conll = getCoNLL(d, i)
            
genData()
        

