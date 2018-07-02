
# coding: utf-8

# In[12]:

import json
import re
from koreanframenet import kfn
import preprocessor
import random


# In[13]:

def load_data():
    training, test, training_fe = preprocessor.load_data()
    return training, test, training_fe

training_data, test_data, training_fe_data = load_data()


# In[11]:

def get_target(sent_list):
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
    return target, frame


# In[ ]:

def get_exams():
    mylist = []
    for i in test_data:
        target, frame = get_target(sent_list)
        lu_id = kfn.surface_to_lu_id(target, frame)
        #print(lu_id)
        lu = kfn.lu(lu_id)['lu']
        pos = lu.split('.')[1]
        if pos == 'v':
            mylist.append(lu)
            


# In[16]:

def get_lu_list(sent_list):
    target, frame = get_target(sent_list)
    lu_id = kfn.surface_to_lu_id(target, frame)
    
    return lu_id

def lu_statistic():
    mylist = []
    for sent_list in test_data:
        target, frame = get_target(sent_list)
        lu_id = kfn.surface_to_lu_id(target, frame)
        #print(lu_id)
        lu = kfn.lu(lu_id)['lu']
        mylist.append(lu)
    n,v,a=0,0,0
    for i in mylist:
        pos = i.split('.')[1]
        if pos == 'v':
            v = v+1
        elif pos == 'n':
            n = n+1
        else:
            a = a+1
    print(n,v,a)
#lu_statistic()


# (0) Baseline
# 
# 주어진 target 으로부터 random 으로 frame을 가져옴

# In[25]:

def load_kfn_data():
    with open('./koreanframenet/resource/KFN_lus.json','r') as f:
        kolus = json.load(f)
    return kolus
kolus = load_kfn_data()

def get_ramdom_frame(sent_list):
    target, frame = get_target(sent_list)
    lu_id = get_lu_list(sent_list)
    lu = kfn.lu(lu_id)['lu'].split('.')[0]
    frames = []
    for i in kolus:
        lex = i['lu'].split('.')[0]
        if lu == lex:
            frames.append(i['frameName'])
    frames = list(set(frames))
    frame = random.choice(frames)
    return frame


# (1) Baseline 2:
# 
# 각 LU의 dependency-based doc2vec embedding

# Evaluation method: accuracy

# In[ ]:

def test():
    c,e,n = 0,0,0
    for sent_list in test_data:
        target, answer_frame = get_target(sent_list)
        pred_frame = get_ramdom_frame(sent_list)
        if answer_frame == pred_frame:
            c = c+1
        else:
            print(target, answer_frame, pred_frame)
        n = n+1
    print('accuracy:', c/n)
        
test()

