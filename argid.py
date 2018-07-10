
# coding: utf-8

# In[1]:

import json
from src import rulebasedArgid


# In[2]:

def load_data():
    with open('./src/data/rulebased_argid_features.json','r') as f:
        rulebasedFeature = json.load(f)
    return rulebasedFeature
rulebasedFeature = load_data()


# In[3]:

def arg_identifier_rulebased(sent_list):
    result = rulebasedArgid.argid(sent_list, rulebasedFeature)
    return result


# In[4]:

def arg_identifier(sent_list, model):
    if model == 'rulebased':
        result = arg_identifier_rulebased(sent_list)
    
        
            
    return result


# In[9]:

def test():
    sent_list = [[[0, '나는', '나/NP+는/JX', '나는', 'NP+JX', 'NP+JX', '_', '_', 2, 2, 'NP_SBJ', 'NP_SBJ', '_', '_'], [1, '밥을', '밥/NNG+을/JKO', '밥을', 'NNG+JKO', 'NNG+JKO', '_', '_', 2, 2, 'NP_OBJ', 'NP_OBJ', '_', '_'], [2, '먹고', '먹/VV+고/EC', '먹고', 'VV+EC', 'VV+EC', '_', '_', 4, 4, 'VP', 'VP', '먹다.v', 'Ingestion'], [3, '학교에', '학교/NNG+에/JKB', '학교에', 'NNG+JKB', 'NNG+JKB', '_', '_', 4, 4, 'NP_AJT', 'NP_AJT', '_', '_'], [4, '갔다', '가/VV+었/EP+다/EF', '갔다', 'VV+EP+EF', 'VV+EP+EF', '_', '_', -1, -1, 'VP', 'VP', '_', '_']], [[0, '나는', '나/NP+는/JX', '나는', 'NP+JX', 'NP+JX', '_', '_', 2, 2, 'NP_SBJ', 'NP_SBJ', '_', '_'], [1, '밥을', '밥/NNG+을/JKO', '밥을', 'NNG+JKO', 'NNG+JKO', '_', '_', 2, 2, 'NP_OBJ', 'NP_OBJ', '_', '_'], [2, '먹고', '먹/VV+고/EC', '먹고', 'VV+EC', 'VV+EC', '_', '_', 4, 4, 'VP', 'VP', '_', '_'], [3, '학교에', '학교/NNG+에/JKB', '학교에', 'NNG+JKB', 'NNG+JKB', '_', '_', 4, 4, 'NP_AJT', 'NP_AJT', '학교.n', 'Locale_by_use'], [4, '갔다', '가/VV+었/EP+다/EF', '갔다', 'VV+EP+EF', 'VV+EP+EF', '_', '_', -1, -1, 'VP', 'VP', '_', '_']], [[0, '나는', '나/NP+는/JX', '나는', 'NP+JX', 'NP+JX', '_', '_', 2, 2, 'NP_SBJ', 'NP_SBJ', '_', '_'], [1, '밥을', '밥/NNG+을/JKO', '밥을', 'NNG+JKO', 'NNG+JKO', '_', '_', 2, 2, 'NP_OBJ', 'NP_OBJ', '_', '_'], [2, '먹고', '먹/VV+고/EC', '먹고', 'VV+EC', 'VV+EC', '_', '_', 4, 4, 'VP', 'VP', '_', '_'], [3, '학교에', '학교/NNG+에/JKB', '학교에', 'NNG+JKB', 'NNG+JKB', '_', '_', 4, 4, 'NP_AJT', 'NP_AJT', '_', '_'], [4, '갔다', '가/VV+었/EP+다/EF', '갔다', 'VV+EP+EF', 'VV+EP+EF', '_', '_', -1, -1, 'VP', 'VP', '가다.v', 'Motion']]]
    pred = rulebasedArgid.argid(sent_list, rulebasedFeature)
    for i in pred:
        for j in i:
            print(j, len(j))
#test()

