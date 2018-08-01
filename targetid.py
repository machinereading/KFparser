
# coding: utf-8

# In[28]:


# input: CoNLL2009-based list (output of preprocessor.py)

from koreanframenet import kfn
import preprocessor
import re
from src import etri
import posChanger


# In[36]:


def target_identification_surfaceform(sent_list):
    result = []
    frame = 'None'
    for i in sent_list:
        #print(i[0], i[2], i[3])
        lu1, lu2 = [],[]
        #print(i)
        lus =[]
        lex = i[2].split('+')[0].split('/')[0]
        pos = i[2].split('+')[0].split('/')[1]
        pos = posChanger.posChanger(pos)
        lemma = lex+'.'+pos
        lu1 = kfn.lus_by_lemma(lemma)
        #print(lu1)
        
        surfaceform = i[1]
        spc = [',','.','!','?']
        if len(surfaceform) > 1:
            if surfaceform[-1] in spc:
                surfaceform = re.sub('[,.?!]', '', surfaceform)
        lu2 = kfn.lus_by_surfaceform(surfaceform)
        lus = lu1+lu2
        lus = list(set(lus))
        
        pos = i[4].split('+')[0]
        pos = posChanger.posChanger(pos)
        lu_candis = []
        if len(lus) > 0:
            for lc in lus:
                lu_pos = lc.split('.')[1]
                #print('pos', pos, lu_pos)
                if pos == lu_pos:
                    lu_candi_list = lc.split('.')[:-1]
                    lu_candi = '.'.join(lu_candi_list)
                    lu_candis.append(lu_candi)
                    #print(lu_candi)
                    #if surfaceform[0] == lu_candi[0]:
                        #lu_candis.append(lu_candi)
        lu_candis = list(set(lu_candis))
#         print(lu_candis)
        if len(lu_candis) > 0:
            lu = False
            max = 0
            for j in lu_candis:
                lexu_list = kfn.lus_by_lu(j)
                for k in lexu_list:
                    count = len(k['ko_annotation_id'])
                    if count > max:
                        lu = j
                        max = count                
            lu_dict = {}
            lu_dict['token_id'] = i[0]
            lu_dict['lu'] = lu
            lu_with_frame = []
            for j in lus:
                lexu = j.split('.')[0] + '.' + j.split('.')[1]
                if lexu == lu:
                    lu_with_frame.append(j)
            lu_dict['lu_with_frame'] = lu_with_frame
            if lu != False:
                result.append(lu_dict)
    return result


# In[25]:


def dummy():
    st = '선언서를'
    d = kfn.lus_by_surfaceform(st)
    print(d)
#dummy()    


# In[67]:


def target_identifier(sent_list, model):
    if model == 'baseline':
        targets = target_identification_surfaceform(sent_list)
    else:
        targets = target_identification_surfaceform(sent_list)
    result = []
    token_list = sent_list
    for i in range(len(targets)):
        new_token_list = []
        for token in token_list:
            new_token = token
            if len(new_token) > 12:
                new_token = token[:12]
            tokid = token[0]
            if tokid == targets[i]['token_id']:
                new_token.append(targets[i]['lu'])
            else:
                new_token.append('_')
            new_token_list.append(new_token)
        result.append(new_token_list)
    if len(result) == 0:
        new_token_list = []
        for token in token_list:
            new_token = token[:12]
            new_token.append('_')
            new_token_list.append(new_token)
        result.append(new_token_list)
                    
    return result


# In[69]:


def test():
    sent = '나는 밥을 먹고 학교에 갔다'
    conll = etri.getETRI_CoNLL2009(sent)
    #targets = target_identifier(conll)
#    for i in sent_list:
#        print(i[0], i[2])

    #targets = target_identification_surfaceform(sent_list)
    result = target_identifier(conll, 'baseline')
    for i in result:
        for j in i:
            print(j)
        print('')
#test()

