
# coding: utf-8

# In[3]:


import json
from src import rulebasedArgid
from src import rulebasedArgid2


# In[10]:


def load_data():
    with open('./src/data/rulebased_argid_features.json','r') as f:
        rulebasedFeature = json.load(f)
    with open('./src/data/rulebased2_argid_features.json','r') as f:
        suffixFeature = json.load(f)
        
    return rulebasedFeature, suffixFeature
rulebasedFeature, suffixFeature = load_data()


# In[19]:


def check_target(sent_list):
    target = False
    for sent in sent_list:
        for token in sent:
            if token[12] != '_':
                target = True
            else:
                pass
    return target


# In[20]:


def null_arg(sent_list):
    for sent in sent_list:
        for token in sent:
            token.append('_')
    return sent_list


# In[17]:


def arg_identifier_rulebased(sent_list):
    result = rulebasedArgid.argid(sent_list, rulebasedFeature)
    return result

def arg_identifier_suffix_only(sent_list):
    result = rulebasedArgid2.arg_id(sent_list, suffixFeature)
    return result


# In[23]:


def arg_identifier(sent_list, model):
    result = []
    check = check_target(sent_list)
    if check:
        if model == 'rulebased':
            result = arg_identifier_rulebased(sent_list)
        if model == 'suffix_only':
            result = arg_identifier_suffix_only(sent_list)
    else:
        pass     
    return result


# In[18]:


def test():
    sent_list = [[[0, '나는', '나/NP+는/JX', '나는', 'NP+JX', 'NP+JX', '_', '_', 2, 2, 'NP_SBJ', 'NP_SBJ', '_', '_'], [1, '밥을', '밥/NNG+을/JKO', '밥을', 'NNG+JKO', 'NNG+JKO', '_', '_', 2, 2, 'NP_OBJ', 'NP_OBJ', '_', '_'], [2, '먹고', '먹/VV+고/EC', '먹고', 'VV+EC', 'VV+EC', '_', '_', 4, 4, 'VP', 'VP', '먹다.v', 'Ingestion'], [3, '학교에', '학교/NNG+에/JKB', '학교에', 'NNG+JKB', 'NNG+JKB', '_', '_', 4, 4, 'NP_AJT', 'NP_AJT', '_', '_'], [4, '갔다', '가/VV+었/EP+다/EF', '갔다', 'VV+EP+EF', 'VV+EP+EF', '_', '_', -1, -1, 'VP', 'VP', '_', '_']], [[0, '나는', '나/NP+는/JX', '나는', 'NP+JX', 'NP+JX', '_', '_', 2, 2, 'NP_SBJ', 'NP_SBJ', '_', '_'], [1, '밥을', '밥/NNG+을/JKO', '밥을', 'NNG+JKO', 'NNG+JKO', '_', '_', 2, 2, 'NP_OBJ', 'NP_OBJ', '_', '_'], [2, '먹고', '먹/VV+고/EC', '먹고', 'VV+EC', 'VV+EC', '_', '_', 4, 4, 'VP', 'VP', '_', '_'], [3, '학교에', '학교/NNG+에/JKB', '학교에', 'NNG+JKB', 'NNG+JKB', '_', '_', 4, 4, 'NP_AJT', 'NP_AJT', '학교.n', 'Locale_by_use'], [4, '갔다', '가/VV+었/EP+다/EF', '갔다', 'VV+EP+EF', 'VV+EP+EF', '_', '_', -1, -1, 'VP', 'VP', '_', '_']], [[0, '나는', '나/NP+는/JX', '나는', 'NP+JX', 'NP+JX', '_', '_', 2, 2, 'NP_SBJ', 'NP_SBJ', '_', '_'], [1, '밥을', '밥/NNG+을/JKO', '밥을', 'NNG+JKO', 'NNG+JKO', '_', '_', 2, 2, 'NP_OBJ', 'NP_OBJ', '_', '_'], [2, '먹고', '먹/VV+고/EC', '먹고', 'VV+EC', 'VV+EC', '_', '_', 4, 4, 'VP', 'VP', '_', '_'], [3, '학교에', '학교/NNG+에/JKB', '학교에', 'NNG+JKB', 'NNG+JKB', '_', '_', 4, 4, 'NP_AJT', 'NP_AJT', '_', '_'], [4, '갔다', '가/VV+었/EP+다/EF', '갔다', 'VV+EP+EF', 'VV+EP+EF', '_', '_', -1, -1, 'VP', 'VP', '가다.v', 'Motion']]]
    pred = arg_identifier(sent_list, 'suffix_only')
    for i in pred:
        for j in i:
            print(j, len(j))
#test()

