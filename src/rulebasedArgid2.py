import csv
import re
import json

def arg_id(datasc, feature_list):
    datas=[]
    for data in datasc:
        temp = []
        for token in data:
            temp.append(token[:14])
        datas.append(temp)
    
    for data in datas:
        for token in data:
            token = token[:14]
            
        for token in data:
            if token[12] != '_':
                frame_lu = token[12] + '.' + token[13]
                frame_usage = token[11]
        
        for feature in feature_list:
            if feature['lu'] == frame_lu:
                frame_form = feature
        
        for token in data:
            word_tokens = token[2].split("+")
            for word_token in word_tokens:
                info = word_token.split("/")
                count = 0
                FE = None
                if len(info) >= 2:
                    if info[1].find("J") != -1:
                        for pattern in frame_form['pattern']:
                            if pattern['pt'] == frame_usage:
                                for set_ in pattern['set']:
                                    if set_ == info[0] and pattern['set'][set_] > count:
                                        count = pattern['set'][set_]
                                        FE = pattern['FE']
            if FE != None:
                token.append(FE)
        for token in data:
            if len(token) == 14:
                token.append('O')
    
    return datas