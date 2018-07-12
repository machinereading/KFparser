
# coding: utf-8

# In[1]:


import json
import re
from koreanframenet import kfn
import preprocessor
import random


# In[2]:


def get_frame_candidates(token_list):
    lu_list = []
    frame_candis = []
    for token in token_list:
        if token[12] != '_':
            target = token[12]
            lu_list = kfn.lus_by_lu(target)
            break
#     for lu_item in lu_list:
#         frame_candi = lu_item['frameName']
#         frame_candis.append(frame_candi)
#     frame_candis = list(set(frame_candis))
    return lu_list


# In[3]:


def frame_identification_frequent(token_list):
    lu_list = get_frame_candidates(token_list)
    max_num = 0
    frame = None
    for lu_item in lu_list:
        count = len(lu_item['ko_annotation_id'])
        if count > max_num:
            frame = lu_item['frameName']
            max_num = count
    return frame


# In[4]:


def frame_identification_random(token_list):
    lu_list = get_frame_candidates(token_list)
    frame_candis = []
    for lu_item in lu_list:
        frame_candi = lu_item['frameName']
        frame_candis.append(frame_candi)
    frame_candis = list(set(frame_candis))
    if len(frame_candis) > 0:
        frame = random.choice(frame_candis)
    else:
        frame = None
    return frame


# In[23]:


def frame_identifier(sent_list, model):
    for n in range(len(sent_list)):
        if model == 'random':
            frame  = frame_identification_random(sent_list[n])
        elif model == 'frequent':
            frame = frame_identification_frequent(sent_list[n])
        else:
            print('no model')
        if frame != None:
            for token in sent_list[n]:
                if token[12] != '_':
                    token.append(frame)
                else:
                    token.append('_')
        else:
            for token in sent_list[n]:
                token.append('_')
    return sent_list


# In[13]:


def eval_model(test_data, model):    
    answer, wrong = 0,0    
    fid_result = frame_identifier(test_data, model)
    result = []
    for sent_num in range(len(test_data)):
        for token in test_data[sent_num]:
            if token[13] != '_':
                gold = token[13]
                break
        for token in fid_result[sent_num]:
            if token[-1] != '_':
                pred = token[-1]
                break
        if gold == pred:
            answer += 1
        else:
            wrong += 1
        new_sent_list = []
        for token in test_data[sent_num]:
            token = token[:14]
            if token[12] == '_':
                token.append('_')
            else:
                token.append(pred)
            new_sent_list.append(token)
        result.append(new_sent_list)
    fname = './tmp/frameid.result.'+model
    with open(fname, 'w') as f:
        for i in result:
            for token in i:
                line = '\t'.join(map(str,token))
                f.write(line+'\n')
            f.write('\n')
    perform = round(answer / (answer+wrong), 4)
    return perform, fname
        

def evaluation():
    _, test_data, _, _ = preprocessor.load_data()
    models = ['random', 'frequent']
    for model in models:
        _, test_data, _, _ = preprocessor.load_data()
        perform, fname = eval_model(test_data, model)
        print('MODEL:', model, ', accuracy:',perform)
        print('Result is save at', fname)
        print('')
#evaluation()


# In[22]:


def test():
    import targetid
    import etri
    
    _, test_data, _, _ = preprocessor.load_data()
    test = test_data
    testing = [  test[1] ]
    fid_result = frame_identifier(testing, 'random')
    print(fid_result)
    _, test_data, _, _ = preprocessor.load_data()
    test = test_data
    testing = [  test[1] ]
    fid_result = frame_identifier(testing, 'frequent')
    print(fid_result)
#test()

