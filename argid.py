
# coding: utf-8

# In[1]:

import json


# In[2]:

def arg_identifier_rulebased(token_list):
    result = []
    return result


# In[ ]:

def arg_identifier(sent_list, model):
    for n in range(len(sent_list)):
        if model == 'rulebased':
            arg = arg_identifier_rulebased(sent_list[n])
            
    return sent_list

