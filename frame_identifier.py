
# coding: utf-8

# In[1]:

import json
import re
from koreanframenet import kfn
import preprocessor


# In[2]:

def load_data():
    training, test, training_fe = preprocessor.load_data()
    return training, test, training_fe

training, test, training_fe = load_data()


# In[16]:

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


# In[21]:

ok, no = 0,0
for i in training:
    #print(i)
    target, frame = get_target(i)
    lus = kfn.surface_to_lu_ids(target,frame)
    if len(lus) > 0:
        ok = ok+1
    else:
        print(target)
        no = no+1
    #break
print(len(training))
print(ok,no)

ok, no = 0,0
for i in test:
    #print(i)
    target, frame = get_target(i)
    lus = kfn.surface_to_lu_ids(target,frame)
    if len(lus) > 0:
        ok = ok+1
    else:
        print(target)
        no = no+1
    #break
#print(len(test))
#print(ok,no)

ok, no = 0,0
for i in training_fe:
    #print(i)
    target, frame = get_target(i)
    lus = kfn.surface_to_lu_ids(target,frame)
    if len(lus) > 0:
        ok = ok+1
    else:
        print(target)
        no = no+1
    #break
#print(len(training_fe))
#print(ok,no)

