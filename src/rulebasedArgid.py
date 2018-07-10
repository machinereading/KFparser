import csv
import re
import json

def check_frame(file, frame_kind):
    dic = {}
    for json_file in file:
        for pattern in json_file['pattern']:
            for set_ in pattern['set']:
                if frame_kind in set_:
                    for segment in set_[frame_kind]:
                        if (json_file['lu_id'], pattern['pt'], segment['FE_pt']) not in dic:
                            dic[ (json_file['lu_id'], pattern['pt'], segment['FE_pt']) ] = [ [segment['FE_pos'], set_['FE'], segment['number']] ]
                        else:
                            existance = 0
                            for seg2 in dic[(json_file['lu_id'], pattern['pt'], segment['FE_pt'])]:
                                if seg2[0] == segment['FE_pos'] and seg2[1] == set_['FE']:
                                    seg2[2] += segment['number']
                            if existance == 0:
                                dic[ (json_file['lu_id'], pattern['pt'], segment['FE_pt']) ].append([segment['FE_pos'], set_['FE'], segment['number']])
                                
    return dic

def check_frame2(file, frame_kind):
    dic = {}
    for json_file in file:
        for pattern in json_file['pattern']:
            for set_ in pattern['set']:
                if frame_kind in set_:
                    for segment in set_[frame_kind]:
                        if (json_file['lu_id'], pattern['pt'], segment['suffix']) not in dic:
                            dic[ (json_file['lu_id'], pattern['pt'], segment['suffix']) ] = [ [segment['FE_pos'], set_['FE'], segment['number']] ]
                        else:
                            existance = 0
                            for seg2 in dic[(json_file['lu_id'], pattern['pt'], segment['suffix'])]:
                                if seg2[0] == segment['FE_pos'] and seg2[1] == set_['FE']:
                                    seg2[2] += segment['number']
                            if existance == 0:
                                dic[ (json_file['lu_id'], pattern['pt'], segment['suffix']) ].append([segment['FE_pos'], set_['FE'], segment['number']])
                                
    return dic
### file = feature_file (valencePattern)
def make_dic(file):
    dic = {}
    dic['to_frame_dic'] = check_frame(file, 'to_frame')
    dic['from_frame_dic'] = check_frame(file, 'from_frame')
    dic['to_parent_frame_dic'] = check_frame(file, 'to_parent_frame')
    dic['from_parent_frame_dic'] = check_frame(file, 'from_parent_frame')
    dic['to_suffix_dic'] = check_frame2(file, 'to_suffix')
    dic['from_suffix_dic'] = check_frame2(file, 'from_suffix')
    dic['other_suffix_dic'] = check_frame2(file, 'other_suffix')

    return dic

#CONLL 2006 = True, CoNLL 2009 = False
def check_length(tokens, index, number, CoNLL=True):
    if CoNLL == True:
        if len(tokens[index]) <= 11:
            return tokens[index][number-1]
        else:
            return tokens[index][number]
    else:
        if len(tokens[index]) < 13:
            return tokens[index][number-2]
        else:
            return tokens[index][number]
        
def find_path2(tokens, point, predictions, directed_list, CoNLL=True):
    if CoNLL == True:
        while point != -1:
            if point in directed_list:
                return predictions['tokens'][point][-1]
            point = int(check_length(tokens, point, 5))
        return None
    
    else:
        while point != -1:
            if point in directed_list:
                return predictions['tokens'][point][-1]
            point = int(check_length(tokens, point, 8))
        return None
    
def find_path(tokens, content, point, inf, num, value, CoNLL=True):
    if CoNLL == True:
        while point != -1:
            if point == content:
                inf[num] = value
                break
            point = int(check_length(tokens, point, 5)) 
        return inf
    else:
        while point != -1:
            if point == content:
                inf[num] = value
                break
            point = int(check_length(tokens, point, 8)) 
        return inf

def check_dictionary(dictionary, lu_id, frame_pt, value, pos):
    FE = None
    if (lu_id, frame_pt, value) in dictionary:
        existance = 0
        count = 0
        for dic_seg in dictionary[(lu_id, frame_pt, value)]:
            if dic_seg[0] == pos and dic_seg[2] > count:
                count = dic_seg[2]
                FE = dic_seg[1]
                existance = 1
        FE_dic = {}
        if existance == 0:
            for dic_seg in dictionary[(lu_id, frame_pt, value)]:
                if dic_seg[1] in FE_dic:
                    FE_dic[dic_seg[1]] += dic_seg[2]
                else:
                    FE_dic[dic_seg[1]] = dic_seg[2]
            count = 0
            for key in FE_dic:
                if FE_dic[key] > count:
                    count = FE_dic[key]
                    FE = key
    return FE


def argid(file_seq = None, feature = None):
    datas = []
    for file in file_seq:
        temp = {}
        sentence = ""
        for token in file:
            sentence += token[1] + " "
        sentence = sentence[:-1]
        
        temp['text'] = sentence
        temp['sentid'] = 'UNK'
        temp['tokens'] = file
        datas.append(temp)
    
    feature_dic = make_dic(feature)
    to_frame_dic = feature_dic['to_frame_dic']
    from_frame_dic = feature_dic['from_frame_dic']
    to_parent_frame_dic = feature_dic['to_parent_frame_dic']
    from_parent_frame_dic = feature_dic['from_parent_frame_dic']
    to_suffix_dic = feature_dic['to_suffix_dic']
    from_suffix_dic = feature_dic['from_suffix_dic']
    other_suffix_dic = feature_dic['other_suffix_dic']
    
    index = 0
    final_prediction = []

    for data in datas:
        if index % 100 == 1:
            #print("Evaluating: ", index)
        tokens = data['tokens']
        text = data['text']
        
        frame = None
        for token in tokens:
            if token[-1] != '_':
                lu = token[-2] + '.' + token[-1]
                frame = int(token[0])
        
        predictions = {}
        predictions['sentid'] = data['sentid']
        predictions['text'] = data['text']
        predictions['tokens'] = []
        for token in tokens:
            predictions['tokens'].append(token[:])

        
        frame_format = None
        for json_data in feature:
            if json_data['lu'] == lu:
                lu_id = json_data['lu_id']
                frame_format = json_data

        if frame != None:
            
            frame_pt = check_length(tokens, frame, 11, False)
            directed_list = []
            #######################################################
            # Calculate directed tokens
            # First pass
            #######################################################            
            for token in tokens:
                if len(token) == 15:
                    token.pop(-1)
                
                parent = int(check_length(tokens, int(token[0]), 9, False))
                pt = check_length(tokens, int(token[0]), 11, False)
                frame_pt = check_length(tokens, frame, 11, False)
                frame_parent = int(check_length(tokens, frame, 9, False))
                frame_parent_parent = int(check_length(tokens, frame_parent, 9, False))
                pos = token[4]
                info = pos.split("+")
                suffix = None
                for info_seg in info:
                    short_info_seg = info_seg.split("/")
                    if len(short_info_seg) >= 2:
                        if short_info_seg[1].find('J') != -1:
                            suffix = short_info_seg[0]
                FE = None
                if (pt == 'NP_MOD' or pt == 'VP_MOD' or pt == 'NP_AJT' or pt == 'VP_AJT' or pt =='VNP_MOD' or pt == 'VNP_AJT')\
                and suffix != None and parent == frame:
                    FE = check_dictionary(to_suffix_dic, lu_id, frame_pt, suffix, pos)
                if FE == None and parent == frame:
                    FE = check_dictionary(to_frame_dic, lu_id, frame_pt, pt, pos)
                if (pt == 'NP_MOD' or pt == 'VP_MOD' or pt == 'NP_AJT' or pt == 'VP_AJT'or pt =='VNP_MOD' or pt == 'VNP_AJT')\
                and FE == None and suffix != None and frame_parent == int(token[0]):
                    FE = check_dictionary(from_suffix_dic, lu_id, frame_pt, suffix, pos)
                if FE == None and frame_parent == int(token[0]):
                    FE = check_dictionary(from_frame_dic, lu_id, frame_pt, pt, pos)
                pt_check = frame_pt.split("_")
                if len(pt_check) >= 2:
                    if FE == None and (pt_check[1] == 'CMP' or pt_check[1] == 'OBJ' or pt_check[1] == 'SBJ') and (parent == frame_parent):
                        FE = check_dictionary(to_parent_frame_dic, lu_id, frame_pt, pt, pos)
                    if FE == None and (pt_check[1] == 'CMP' or pt_check[1] == 'OBJ' or pt_check[1] == 'SBJ') and (frame_parent_parent == int(token[0])):
                        FE = check_dictionary(from_parent_frame_dic, lu_id, frame_pt, pt, pos)
                if FE != None:
                    predictions['tokens'][int(token[0])].append(FE)
                    directed_list.append(int(token[0]))

            #######################################################
            # Calculate list to directed_list
            # Second pass
            #######################################################            
            for token in tokens:
                FE = None
                if len(predictions['tokens'][int(token[0])]) <= 14:
                    FE = find_path2(tokens, int(token[0]), predictions, directed_list, False)
                if FE != None:
                    predictions['tokens'][int(token[0])].append(FE)
                    
            for token in tokens:
                if len(predictions['tokens'][int(token[0])]) <= 14:
                    while len(predictions['tokens'][int(token[0])]) < 15:
                        predictions['tokens'][int(token[0])].append('O')

            final_prediction.append(predictions['tokens'])
        else:
            final_prediction.append(data['tokens'])
        index += 1    

    
                            
    return final_prediction
    
