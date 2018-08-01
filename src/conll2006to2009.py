
# coding: utf-8

# In[ ]:

import json
import etri
from koreanframenet import kfn
import re


f1 = './koreanframenet/data/conll2006/test.tsv'
f2 = './koreanframenet/data/conll2006/training.tsv'
f3 = './koreanframenet/data/conll2006/training_fe.tsv'
files = [f1, f2, f3]

def getBIO_list(sent_list):
    result = []
    fe_list = []
    for i in range(len(sent_list)):
        fe = sent_list[i][14]
        fe_list.append(fe)
    for i in range(len(sent_list)):
        fe = sent_list[i][14]
        if i == 0:
            if fe == '_':
                fe = 'O'
            else:
                try:
                    if fe == fe_list[i+1]:
                        fe = 'B_'+fe
                    else:
                        fe = 'S_'+fe
                except KeyboardInterrupt:
                    raise
                except:
                    fe = 'S_'+fe
        else:
            if fe == '_':
                fe = 'O'
            else:
                if fe != fe_list[i-1]:
                    try:
                        if fe == fe_list[i+1]:
                            fe = 'B_'+fe
                        else:
                            fe = 'S_'+fe
                    except KeyboardInterrupt:
                        raise
                    except:
                        fe = 'S_'+fe
                else:
                    fe = 'I_'+fe
        result.append(fe)               
    return result

def get_lu(sent_list):
    token_list = []
    frame = 'None'
    for i in sent_list:
        #print(i)
        if i[9] == 'Y':
            token_list.append(i[1])
            frame = i[10]
    target = ' '.join(token_list)
    spc = [',','.','!','?']
    if len(target) >1:
        if target[-1] in spc:
            target = re.sub('[,.?!]', '', target)
    lu_id = kfn.surface_to_lu_id(target, frame)
    lemma = kfn.lu(lu_id)['lu'].split('.')[0]
    pos = kfn.lu(lu_id)['lu'].split('.')[1]
    lu = lemma+'.'+pos
    return lu

def getCoNLL(lines, filename):
    filetype = filename.split('/')[-1]
    target_file = './koreanframenet/data/'+filetype
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
            etri_result = etri.getETRI_CoNLL2009(ori_text)
            morp = []
            lu = get_lu(conll)
            for i in range(len(etri_result)):
                fillpred = lu
                pred = conll[i][10]
                arg = conll[i][11]
                if conll[i][9] != '_':
                    etri_result[i].append(fillpred)
                else:
                    etri_result[i].append('_')
                etri_result[i].append(pred)
                etri_result[i].append(arg)
            
            fe_list = getBIO_list(etri_result)
            for i in range(len(etri_result)):
                etri_result[i][14] = fe_list[i]
                
            for token in etri_result:
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
        


# In[19]:

f1 = './koreanframenet/data/conll2009/test.tsv'
#f2 = './koreanframenet/data/conll2006/training.tsv'
#f3 = './koreanframenet/data/conll2006/training_fe.tsv'

import preprocessor
import pprint

def getBIO(sent_list):
    result = []
    fe_list = []
    for i in range(len(sent_list)):
        fe = sent_list[i][14]
        fe_list.append(fe)
    for i in range(len(sent_list)):
        fe = sent_list[i][14]
        if i == 0:
            if fe == '_':
                fe = 'O'
            else:
                try:
                    if fe == fe_list[i+1]:
                        fe = 'B_'+fe
                    else:
                        fe = 'S_'+fe
                except KeyboardInterrupt:
                    raise
                except:
                    fe = 'S_'+fe
        else:
            if fe == '_':
                fe = 'O'
            else:
                if fe != fe_list[i-1]:
                    try:
                        if fe == fe_list[i+1]:
                            fe = 'B_'+fe
                        else:
                            fe = 'S_'+fe
                    except KeyboardInterrupt:
                        raise
                    except:
                        fe = 'S_'+fe
                else:
                    fe = 'I_'+fe
        result.append(fe)               
    return result

def test():
    with open(f1,'r') as f:
        d = f.readlines()
        conll, _ = preprocessor.load_tsv(d)
        #getBIO(conll[1])
        #for i in conll[12]:
        #    print(i)
        #d = getBIO(conll[12])
        #print('fes')
        for i in conll:
            d = getBIO(i)
            print(d)
        

