import csv
import re
import json
import argI_data_preprocessor

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
        if len(tokens[index]) < 14:
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

def test(file_seq=None, feature_seq = None, file_name=None, feature_name=None, output_file='./prediction.json',  save_mode=True, CoNLL=True, data_format=True):
    if data_format == True:
        answers = argI_data_preprocessor.load_data(file_name)

        with open(feature_name, "r", encoding="utf-8") as make_file:
            feature = json.load(make_file)
    else:
        answers = []
        
        for file in file_seq:
            temp = {}
            sentence = ""
            for token in file:
                sentence += token[1] + " "
            sentence = sentence[:-1]
            
            temp['text'] = sentence
            temp['sentid'] = 'UNK'
            temp['tokens'] = file
            answers.append(temp)
        feature = feature_seq
    
    feature_dic = make_dic(feature)
    to_frame_dic = feature_dic['to_frame_dic']
    from_frame_dic = feature_dic['from_frame_dic']
    to_parent_frame_dic = feature_dic['to_parent_frame_dic']
    from_parent_frame_dic = feature_dic['from_parent_frame_dic']
    to_suffix_dic = feature_dic['to_suffix_dic']
    from_suffix_dic = feature_dic['from_suffix_dic']
    other_suffix_dic = feature_dic['other_suffix_dic']
    
    datas = []
    for answer in answers:
        temp = {}
        temp['text'] = answer['text']
        temp['sentid'] = answer['sentid']
        temp['tokens'] = []
        for token in answer['tokens']:
            if CoNLL == True:
                temp['tokens'].append(token[0:-3]+['_', '_' , '_'])
            else:
                temp['tokens'].append(token[0:12]+['_' , '_' , 'O'])
        datas.append(temp)
    index = 0
    final_prediction = []
                            
                            
    if CoNLL == True:
        for data in datas:
            for i in range(0, len(data['tokens'])):
                data['tokens'][i][-1] = data['tokens'][i][-1].replace("B_", "")
                data['tokens'][i][-1] = data['tokens'][i][-1].replace("I_", "")
                data['tokens'][i][-1] = data['tokens'][i][-1].replace("O_", "")
                data['tokens'][i][-1] = data['tokens'][i][-1].replace("S_", "")
                
                
        for data in datas:
            if index % 100 == 1:
                print("Processing: ", index)
                
            prediction = []
            tokens = data['tokens']
            text = data['text']
            existance = 0
            frame_list = []

            for json_data in feature:
                ### find surface_form
                json_format = {}
                frame = []
                for surface_form in json_data['surface_forms'] :
                    if text.find(surface_form) != -1:
                        length = len(surface_form)
                        sp = text.find(surface_form)
                        inf = text[sp:sp+length].split(" ")
                        lu_seg = json_data['lu'].split(".")
                        for token in tokens:
                            for inf_seg in inf:
                                if token[1] == inf_seg:
                                    json_format = json_data
                                    frame.append(int(token[0]))
                                    final_pt = token[2]
                                    final_pt = final_pt.split("+")

                        if [frame, json_format] != [[],{}]:
                            frame_list.append([frame, json_format])
                        frame = []
                        json_format = {}



                for token in tokens:
                    leninf = token[2].split("+")
                    for leninf_seg in leninf:
                        inf = leninf_seg.split("/")
                        if len(inf) == 2:
                            if inf[1].find("N") != -1 or inf[1] == 'VV' or inf[1] == 'VA':
                                if json_data['lexeme'] == inf[0]:
                                    lu_seg = json_data['lu'].split(".")
                                    json_format = json_data
                                    frame.append(int(token[0]))
                                    if [frame, json_format] not in frame_list:
                                        frame_list.append([frame, json_format])
                                        frame = []
                                        json_format = {}


            if len(frame_list) >= 1:
                lu_id_list = []
                for x in range(0, len(frame_list)):
                    frame = frame_list[x][0][-1]
                    lu_id = frame_list[x][1]['lu_id']

                    predictions = {}
                    predictions['sentid'] = data['sentid']
                    predictions['text'] = data['text']
                    predictions['tokens'] = []
                    for token in tokens:
                        predictions['tokens'].append(token[:])

                    for y in range(0, len(frame_list[x][0])):
                        predictions['tokens'][frame_list[x][0][y]][-3] = 'Y'
                        predictions['tokens'][frame_list[x][0][y]][-2] = frame_list[x][1]['lu'].split(".")[2]

                    frame_pt = check_length(tokens, frame_list[x][0][-1], 6)
                    directed_list = []
                    #######################################################
                    # Calculate directed tokens
                    # First pass
                    #######################################################            
                    for token in tokens:
                        parent = int(check_length(tokens, int(token[0]), 5))
                        pt = check_length(tokens, int(token[0]), 6)
                        frame_pt = check_length(tokens, frame, 6)
                        frame_parent = int(check_length(tokens, frame, 5))
                        frame_parent_parent = int(check_length(tokens, frame_parent, 5))
                        pos = token[2]
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
                            predictions['tokens'][int(token[0])][-1] = FE
                            directed_list.append(int(token[0]))

                    #######################################################
                    # Calculate list to directed_list
                    # Second pass
                    #######################################################            
                    for token in tokens:
                        FE = None
                        if predictions['tokens'][int(token[0])][-1] == '_':
                            FE = find_path2(tokens, int(token[0]), predictions, directed_list)
                        if FE != None:
                            predictions['tokens'][int(token[0])][-1] = FE

                    #######################################################
                    # Consider exceptation rules
                    # Third pass
                    ########################################################
                    for token in tokens:
                        parent = int(check_length(tokens, int(token[0]), 5))
                        pt = check_length(tokens, int(token[0]), 6)
                        frame_pt = check_length(tokens, frame, 6)
                        frame_parent = int(check_length(tokens, frame, 5))
                        frame_parent_parent = int(check_length(tokens, frame_parent, 5))
                        pos = token[3]
                        info = pos.split("+")
                        suffix = None
                        for info_seg in info:
                            short_info_seg = info_seg.split("/")
                            if len(short_info_seg) >= 2:
                                if short_info_seg[1].find('J') != -1:
                                    suffix = short_info_seg[0]
                        FE = token[-1]
                        if FE == '_' and (pt == 'NP_MOD' or pt == 'VP_MOD' or pt == 'NP_AJT' or pt == 'VP_AJT'or pt =='VNP_MOD' or pt == 'VNP_AJT') and suffix != None:
                            FE = check_dictionary(other_suffix,dic, lu_id, frame_pt, suffix, pos)

                    prediction.append(predictions)
                    lu_id_list.append(lu_id)
            else:
                prediction = []
                
            final_prediction.append(prediction)
            index += 1
        
    else:
        for data in datas:
            for i in range(0, len(data['tokens'])):
                data['tokens'][i][-1] = data['tokens'][i][-1].replace("B_", "")
                data['tokens'][i][-1] = data['tokens'][i][-1].replace("I_", "")
                data['tokens'][i][-1] = data['tokens'][i][-1].replace("O_", "")
                data['tokens'][i][-1] = data['tokens'][i][-1].replace("S_", "")
                
        for data in datas:
            if index % 100 == 1:
                print("Evaluating: ", index)
            prediction = []
            tokens = data['tokens']
            text = data['text']
            existance = 0
            frame_list = []

            for json_data in feature:
                ### find surface_form
                json_format = {}
                frame = []
                for surface_form in json_data['surface_forms'] :
                    if text.find(surface_form) != -1:
                        length = len(surface_form)
                        sp = text.find(surface_form)
                        inf = text[sp:sp+length].split(" ")
                        for token in tokens:
                            for inf_seg in inf:
                                if token[1] == inf_seg:
                                    json_format = json_data
                                    frame.append(int(token[0]))
                                    break
                        if [frame, json_format] != [[],{}]:
                            frame_list.append([frame, json_format])
                        frame = []
                        json_format = {}



                for token in tokens:
                    leninf = token[2].split("+")
                    for leninf_seg in leninf:
                        inf = leninf_seg.split("/")
                        if len(inf) == 2:
                            if inf[1].find("N") != -1 or inf[1] == 'VV' or inf[1] == 'VA':
                                if json_data['lexeme'] == inf[0]:
                                    lu_seg = json_data['lu'].split(".")
                                    json_format = json_data
                                    frame.append(int(token[0]))
                                    if [frame, json_format] not in frame_list:
                                        frame_list.append([frame, json_format])
                                        frame = []
                                        json_format = {}


            if len(frame_list) >= 1:
                lu_id_list = []
                for x in range(0, len(frame_list)):
                    frame = frame_list[x][0][-1]
#                     print(index, frame_list[x][0][-1])
                    lu_id = frame_list[x][1]['lu_id']

                    predictions = {}
                    predictions['sentid'] = data['sentid']
                    predictions['text'] = data['text']
                    predictions['tokens'] = []
                    for token in tokens:
                        predictions['tokens'].append(token[:14])
                     

                    for y in range(0, len(frame_list[x][0])):
                        predictions['tokens'][frame_list[x][0][y]][12] = frame_list[x][1]['lu'].split(".")[0] + '.' + frame_list[x][1]['lu'].split(".")[1]
                        predictions['tokens'][frame_list[x][0][y]][13] = frame_list[x][1]['lu'].split(".")[2]

                    frame_pt = check_length(tokens, frame_list[x][0][-1], 11, False)
                    directed_list = []
                    #######################################################
                    # Calculate directed tokens
                    # First pass
                    #######################################################            
                    for token in tokens:
                        parent = int(check_length(tokens, int(token[0]), 9, False))
                        pt = check_length(tokens, int(token[0]), 11, False)
                        frame_pt = check_length(tokens, frame, 11, False)
                        frame_parent = int(check_length(tokens, frame, 9, False))
                        frame_parent_parent = int(check_length(tokens, frame_parent, 9, False))
                        pos = token[2]
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
                        if FE != None and len(predictions['tokens'][int(token[0])])<=14:
                            predictions['tokens'][int(token[0])].append(FE)
                            directed_list.append(int(token[0]))

                    #######################################################
                    # Calculate list to directed_list
                    # Second pass
                    #######################################################            
                    for token in tokens:
                        FE = None
                        if len(predictions['tokens'][int(token[0])])<=14:
                            FE = find_path2(tokens, int(token[0]), predictions, directed_list, False)
                        if FE != None:
                            predictions['tokens'][int(token[0])].append(FE)

                    #######################################################
                    # Consider exceptation rules
                    # Third pass
                    ########################################################
                    for token in tokens:
                        if len(predictions['tokens'][int(token[0])]) >= 15:
                            continue
                        parent = int(check_length(tokens, int(token[0]), 9 ,False))
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
                        if FE == None and (pt == 'NP_MOD' or pt == 'VP_MOD' or pt == 'NP_AJT' or pt == 'VP_AJT'or pt =='VNP_MOD' or pt == 'VNP_AJT') and suffix != None:
                            FE = check_dictionary(other_suffix,dic, lu_id, frame_pt, suffix, pos)
                        if FE != None:
                            predictions['tokens'][int(token[0])].append(FE)
                        
                    for token in tokens:
                        if len(predictions['tokens'][int(token[0])]) <= 14:
                            while len(predictions['tokens'][int(token[0])]) < 15:
                                predictions['tokens'][int(token[0])].append('O')
                        
                        
                    prediction.append(predictions)
                    lu_id_list.append(lu_id)
            else:
                prediction = []
            final_prediction.append(prediction)
            index += 1    
                            
                            
    if save_mode == True:
        with open(output_file, "w", encoding="utf-8") as make_file:
            json.dump(final_prediction, make_file, ensure_ascii=False, indent = 4)
                            
    return final_prediction
#                             , covered_final_prediction                        
   
        
