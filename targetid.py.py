
# coding: utf-8

# In[1]:

# input: CoNLL2009-based list (output of preprocessor.py)

from koreanframenet import kfn
import preprocessor
import re


# In[31]:

def target_identification_surfaceform(sent_list):
    result = []
    frame = 'None'
    for i in sent_list:
        #print(i[0], i[2], i[3])
        lu1, lu2 = [],[]
        #print(i)
        lus =[]
        lemma = i[2].split('+')[0]
        #lu1 = kfn.lus_by_lemma(lemma)
        
        surfaceform = i[1]
        spc = [',','.','!','?']
        if len(surfaceform) > 1:
            if surfaceform[-1] in spc:
                surfaceform = re.sub('[,.?!]', '', surfaceform)
        lu2 = kfn.lus_by_surfaceform(surfaceform)
        lus = lu1+lu2
        lus = list(set(lus))
        #print(lus)
        
        pos = i[4].split('+')[0]
        if pos.startswith('N'):
            pos = 'n'
        elif pos == 'VV':
            pos = 'v'
        elif pos == 'VA':
            pos = 'a'
        else:
            pass
        lu_candis = []
        if len(lus) > 0:
            for lc in lus:
                lu_pos = lc.split('.')[1]
                #print('pos', pos, lu_pos)
                if pos == lu_pos:
                    lu_candi_list = lc.split('.')[:-1]
                    lu_candi = '.'.join(lu_candi_list)
                    #print(lu_candi)
                    if surfaceform[0] == lu_candi[0]:
                        lu_candis.append(lu_candi)
        lu_candis = list(set(lu_candis))
        if len(lu_candis) > 0:
            lu_dict = {}
            lu_dict['token_id'] = i[0]
            lu_dict['lu'] = lu_candis
            lu_dict['lu_with_frame'] = lus
            result.append(lu_dict)
    return result


# In[16]:

def dummy():
    st = '선언서를'
    d = kfn.lus_by_surfaceform(st)
    print(d)
dummy()
    


# In[32]:

def test():
    data, _, _ = preprocessor.load_data()
    sent_list = data[0]
    for i in sent_list:
        print(i[0], i[2])
    print('')
    targets = target_identification_surfaceform(sent_list)
    print(targets)
test()

