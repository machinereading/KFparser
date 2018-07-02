
# coding: utf-8

# In[11]:

import json
import preprocessor
import re
from koreanframenet import kfn

# loading DATA
def load_data():
    training, test, training_fe = preprocessor.load_data()
    #result = training + test
    result = training
    return result

koreanFN = load_data()


# In[14]:

def dummy():
    for i in koreanFN[0]:
        print(i)
dummy()


# In[15]:

# for a given sentence list, it identifies 'target' and 'its frame'
def get_target(sent_list):
    token_list = []
    frame = 'None'
    for i in sent_list:
        #print(i)
        if i[12] != '_':
            token_list.append(i[1])
            frame = i[13]
    target = ' '.join(token_list)
    spc = [',','.','!','?']
    if len(target) >1:
        if target[-1] in spc:
            target = re.sub('[,.?!]', '', target)
    return target, frame


# In[16]:

# for a given sentence list, it identifies an ID of 'LU'
def get_lu_id(sent_list):
    target, frame = get_target(sent_list)
    print('target:', target, 'frame:', frame)
    lu_id = kfn.surface_to_lu_id(target, frame)
    
    return lu_id


# In[17]:

# CoNLL format의 문장 리스트에 대해, valence pattern을 생성하는 함수
def getValencePattern(sent_list):
    result = []
    fes = []
    for token in sent_list:
        if token[14] != 'O':
            fe = token[14].split('_')[1]
            fes.append(fe)
    fes = list(set(fes))
    for fe in fes:
        pos_seq = []
        pt_seq = []
        for token in sent_list:
            if token[14] != 'O':
                fe_in_sent = token[14].split('_')[1]
            else:
                fe_in_sent = token[14]
            if fe == fe_in_sent:
                # 각 argument 에 대해서 패턴 생성
                pos_seq.append(token[4])
                pt_seq.append(token[9])
                pt = token[9]
                pos = token[4]
                if 'J' in pos:
                    suffix = token[2].split('+')[-1]
                    suffix_pos = token[4].split('+')[-1]
                elif 'NN' in pos:
                    suffix = ''
                    suffix_pos = ''
                else:
                    suffix = token[1]+'/'+token[4]
                    suffix_pos = token[4]                    
        valenceUnit = {}
        valenceUnit['FE'] = fe
        valenceUnit['PT'] = pt
        valenceUnit['suffix'] = suffix
        valenceUnit['suffix_pos'] = suffix_pos
        valenceUnit['pos_sequence'] = pos_seq
        valenceUnit['pt_sequence'] = pt_seq
        result.append(valenceUnit)
    return result


# In[10]:

def genData():
    result = []
    # koreanFN = trainign data in CONLL format
    for sent_list in koreanFN:
        each_lu = {}
        lu_id = get_lu_id(sent_list)
        lu = kfn.lu(lu_id)
        each_lu['lu_id'] = lu['lu_id']
        # by this process, 'LU' is identified in training data
        isIn = False
        for i in result:
            if i['lu_id'] == lu_id:
                each_lu = i
                vp_list = each_lu['valencePatterns']
                # valence pattern 을 생성하는 함수 호출
                vp = getValencePattern(sent_list)
                vp_list = vp_list + vp
                each_lu['valencePatterns'] = vp_list
                i = each_lu
                isIn = True
                break
            else:
                pass
        if isIn == True:
            pass
            # result list 에 대해 중복 제거하기 위함
        else:
            each_lu['lu'] = lu['lu']
            each_lu['surface_forms'] = lu['surface_forms']
            each_lu['lexeme'] = lu['lexeme']
            vp_list = []
            # valence pattern 을 생성하는 함수 호출
            vp = getValencePattern(sent_list)
            vp_list = vp_list + vp
            each_lu['valencePatterns'] = vp_list        
            result.append(each_lu)
        
        print(lu['lu'])
        print(each_lu)
    # SAVE Valence Pattern to FILE
    with open('./valencePattern_0702.json','w') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)
genData()

