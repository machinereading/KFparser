import csv
import re
import json
import argI_Load_KFN
import argI_data_preprocessor


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
       
    
def make_dictionary(json_data, tree_structure, tree_structure_name, make_dic):
    for to_frame_seg in tree_structure:
        if to_frame_seg[0] == json_data['lu_id']:
            is_in = 0
            for pattern in make_dic['pattern']:
                if pattern['pt'] == to_frame_seg[1]:
                    is_in = 1
                    is_in2 = 0
                    for in_set in pattern['set']:
                        if to_frame_seg[2] == in_set['FE']:
                            is_in2 = 1
                            is_in3 = 0
                            if tree_structure_name in in_set:
                                for to_frame_set in in_set[tree_structure_name]:
                                    if to_frame_set['FE_pt'] == to_frame_seg[3] and to_frame_set['FE_pos'] == to_frame_seg[4]:
                                        is_in3 = 1
                                        to_frame_set['number'] += 1
                            else:
                                in_set[tree_structure_name] = []
                            
                            if is_in3 == 0:
                                temp_dic3 = {}
                                temp_dic3['FE_pt'] = to_frame_seg[3]
                                temp_dic3['FE_pos'] = to_frame_seg[4]
                                temp_dic3['number'] = 1
                                in_set[tree_structure_name].append(temp_dic3)
                    if is_in2 == 0:
                        temp_dic3 = {}
                        temp_dic3['FE_pt'] = to_frame_seg[3]
                        temp_dic3['FE_pos'] = to_frame_seg[4]
                        temp_dic3['number'] = 1
                        
                        temp_dic2 = {}
                        temp_dic2['FE'] = to_frame_seg[2]
                        temp_dic2[tree_structure_name] = [temp_dic3]
                        pattern['set'].append(temp_dic2)
            if is_in == 0:
                temp_dic3 = {}
                temp_dic3['FE_pt'] = to_frame_seg[3]
                temp_dic3['FE_pos'] = to_frame_seg[4]
                temp_dic3['number'] = 1

                temp_dic2 = {}
                temp_dic2['FE'] = to_frame_seg[2]
                temp_dic2[tree_structure_name] = [temp_dic3]
                temp_dic = {}
                
                temp_dic['set'] = [temp_dic2]
                temp_dic['pt'] = to_frame_seg[1]
                make_dic['pattern'].append(temp_dic)
    return make_dic


def make_dictionary2(json_data, tree_structure, tree_structure_name, make_dic):
    for to_frame_seg in tree_structure:
        if to_frame_seg[0] == json_data['lu_id']:
            is_in = 0
            for pattern in make_dic['pattern']:
                if pattern['pt'] == to_frame_seg[1]:
                    is_in = 1
                    is_in2 = 0
                    for in_set in pattern['set']:
                        if to_frame_seg[2] == in_set['FE']:
                            is_in2 = 1
                            is_in3 = 0
                            if tree_structure_name in in_set:
                                for to_frame_set in in_set[tree_structure_name]:
                                    if to_frame_set['suffix'] == to_frame_seg[3] and to_frame_set['FE_pos'] == to_frame_seg[4]:
                                        is_in3 = 1
                                        to_frame_set['number'] += 1
                            else:
                                in_set[tree_structure_name] = []
                            if is_in3 == 0:
                                temp_dic3 = {}
                                temp_dic3['suffix'] = to_frame_seg[3]
                                temp_dic3['FE_pos'] = to_frame_seg[4]
                                temp_dic3['number'] = 1
                                in_set[tree_structure_name].append(temp_dic3)
                    if is_in2 == 0:
                        temp_dic3 = {}
                        temp_dic3['suffix'] = to_frame_seg[3]
                        temp_dic3['FE_pos'] = to_frame_seg[4]
                        temp_dic3['number'] = 1
                        
                        temp_dic2 = {}
                        temp_dic2['FE'] = to_frame_seg[2]
                        temp_dic2[tree_structure_name] = [temp_dic3]
                        pattern['set'].append(temp_dic2)
            if is_in == 0:
                temp_dic3 = {}
                temp_dic3['suffix'] = to_frame_seg[3]
                temp_dic3['FE_pos'] = to_frame_seg[4]
                temp_dic3['number'] = 1

                temp_dic2 = {}
                temp_dic2['FE'] = to_frame_seg[2]
                temp_dic2[tree_structure_name] = [temp_dic3]
                temp_dic = {}
                
                temp_dic['set'] = [temp_dic2]
                temp_dic['pt'] = to_frame_seg[1]
                make_dic['pattern'].append(temp_dic)
    return make_dic


def train(file_seq=None, output_file = './feature_file.json', file_name = None, save_mode=True , CoNLL=True, data_format=True):
    if data_format == True:
        datas = argI_data_preprocessor.load_data(file_name)
    else:
        datas = []
        for file in file_seq:
            temp = {}
            temp['tokens'] = file
            datas.append(temp)
    
    feature_list = argI_Load_KFN.genData(datas, CoNLL)
    with open("temp_feature.json", "w", encoding="utf-8") as make_file:
        json.dump(feature_list, make_file, ensure_ascii=False, indent = 4)
    
    index = 0
    to_frame = []
    from_frame = []
    to_suffix = []
    from_suffix = []
    other_suffix = []
    to_parent_frame = []
    from_parent_frame = []
    phrases = ['NP', 'VP', 'VNP']
    
    if CoNLL == True:
        for data in datas:
            for i in range(0, len(data['tokens'])):
                data['tokens'][i][-1] = data['tokens'][i][-1].replace("B_", "")
                data['tokens'][i][-1] = data['tokens'][i][-1].replace("I_", "")
                data['tokens'][i][-1] = data['tokens'][i][-1].replace("O_", "")
                data['tokens'][i][-1] = data['tokens'][i][-1].replace("S_", "")
        
        
        
        for data in datas:
            if index % 100 == 0:
                print(index)
            index += 1
            tokens = data['tokens']
            frame_list = []
            FE_tokens = []


            for token in tokens:
                if token[-1] != '_':
                    if token[2] != 'SS':
                        FE_tokens.append(int(token[0]))

                if token[9] == 'Y' and token[2] != 'SS':
                    frame_list.append(int(token[0]))

            if len(frame_list) >= 2:
                temp_frame = []
                for frame in frame_list:
                    standard_frame = frame
                    point = frame
                    while tokens[point][9] == 'Y' and point != -1:
                        point = int(tokens[point][5])
                        if tokens[point][9] == 'Y' and point != -1:
                            standard_frame = point
                    temp_frame.append(standard_frame)
                standard_frame = temp_frame[0]
            else:
                standard_frame = frame_list[0]
            surface_form = ""
            for frame in frame_list:
                surface_form += tokens[frame][1] + ' '
            surface_form = surface_form[:-1]

            usage = check_length(tokens, standard_frame, 6)        

            lexeme_candidate = []
            leninf = tokens[standard_frame][2].split('+')
            for inf in leninf:
                info = inf.split("/")
                if info[1].find('N')!=-1 or info[1] == 'VV' or info[1] == 'VA':
                    lexeme_candidate.append(info[0])

            for feature in feature_list:
                if surface_form in feature['surface_forms'] or feature['lexeme'] in lexeme_candidate:
                    if feature['lu'].split('.')[2] == tokens[standard_frame][-2]:
                        lu_id = feature['lu_id']


            to_frame_index = []
            from_frame_index = []

            for FE_token in FE_tokens:
                parent = int(check_length(tokens, FE_token, 5))
                if parent in frame_list:
                    usage = check_length(tokens, parent, 6)
                    pt = check_length(tokens, FE_token, 6)
                    function = pt.split("_")
                    if len(function) == 1:
                        to_frame.append((lu_id, usage, tokens[FE_token][-1], pt, tokens[FE_token][3]))

                    elif len(function)==2 and (function[1]!='AJT' and function[1] != 'MOD'):
                        for phrase in phrases:
                            to_frame.append((lu_id, usage, tokens[FE_token][-1], phrase+"_"+function[1], tokens[FE_token][3]))
                            to_frame_index.append(FE_token)

                    else:
                        word_tokens = tokens[FE_token][2].split("+")
                        suffix_word = ""
                        for word in word_tokens:
                            info = word.split("/")
                            if len(info) >= 2:
                                if info[1].find("J") != -1:
                                    suffix_word += info[0]
                        if suffix_word == "":
                            for phrase in phrases:
                                to_frame.append((lu_id, usage, tokens[FE_token][-1], phrase+"_"+function[1], tokens[FE_token][3]))
                        else:
                            to_suffix.append((lu_id, usage, tokens[FE_token][-1], suffix_word, tokens[FE_token][3]))
                        to_frame_index.append(FE_token)

            for frame in frame_list:
                parent = int(check_length(tokens, frame, 5))
                usage = check_length(tokens, frame, 6)
                if parent == -1:
                    continue
                if tokens[parent][-1] != '_':
                    pt = check_length(tokens, parent, 6)
                    function = pt.split("_")

                    if len(function) == 1:
                        from_frame.append((lu_id, usage, tokens[parent][-1], pt, tokens[parent][3]))

                    elif len(function) == 2 and (function[1]!='AJT' and function[1] != 'MOD'):
                        for phrase in phrases:
                            from_frame.append((lu_id, usage, tokens[parent][-1], phrase+"_"+function[1], tokens[parent][3]))
                            from_frame_index.append(parent)
                    else:
                        word_tokens = tokens[parent][2].split("+")
                        suffix_word = ""
                        for word in word_tokens:
                            info = word.split("/")
                            if len(info) >= 2:
                                if info[1].find("J") != -1:
                                    suffix_word += info[0]
                        if suffix_word == "":
                            for phrase in phrases:
                                from_frame.append((lu_id, usage, tokens[parent][-1], phrase+"_"+function[1], tokens[parent][3]))
                        else:
                            from_suffix.append((lu_id, usage, tokens[parent][-1], suffix_word, tokens[FE_token][3]))
                        from_frame_index.append(parent)

            other_suffix_index = []
            for FE_token in FE_tokens:
                if FE_token not in to_frame_index and FE_token not in from_frame_index:
                    point = int(check_length(tokens, FE_token, 5))
                    usage = check_length(tokens, standard_frame, 6) 
                    existance = 0
                    while point != -1:
                        if point in to_frame_index or \
                        point in from_frame_index:
                            existance = 1
                            break
                        point = int(check_length(tokens, point, 5))

                    if existance == 0:
                        pt = check_length(tokens, FE_token, 6)
                        function = pt.split("_")

                        if len(function) == 2:
                            if function[1] == 'AJT' or function[1] == 'MOD':
                                word_tokens = tokens[FE_token][2].split("+")
                                suffix_word = ""
                                for word in word_tokens:
                                    info = word.split("/")
                                    if len(info) >= 2:
                                        if info[1].find("J") != -1:
                                            suffix_word += info[0]
                                if suffix_word != "":
                                    other_suffix.append((lu_id, usage, tokens[FE_token][-1], suffix_word, tokens[FE_token][3]))
                                    other_suffix_index.append(FE_token)

            parent_frame_index = []
            for frame in frame_list:
                parent = int(check_length(tokens, frame, 5))
                usage = check_length(tokens, frame, 6)
                function = usage.split("_")
                if len(function) == 2:
#                     if function[1] == 'CMP' or function[1] == 'SBJ' or function == 'OBJ':
                    for FE_token in FE_tokens:
                        pt = check_length(tokens, FE_token, 6)
                        point = int(check_length(tokens, FE_token, 5))
                        if point == parent:
                            for phrase in phrases:
                                to_parent_frame.append((lu_id, phrase+"_"+function[1], tokens[FE_token][-1], pt, tokens[FE_token][3]))
                            parent_frame_index.append(FE_token)

                        parent_parent = int(check_length(tokens, parent, 5))
                        if FE_token == parent_parent:
                            for phrase in phrases:
                                from_parent_frame.append((lu_id, phrase+"_",function[1], tokens[FE_token][-1], pt, tokens[FE_token][3]))
                            parent_frame_index.append(FE_token)

                else:
                    for FE_token in FE_tokens:
                        pt = check_length(tokens, FE_token, 6, False)
                        point = int(check_length(tokens, FE_token, 5, False))
                        if point == parent:
                            to_parent_frame.append((lu_id, usage, tokens[FE_token][-1], pt, tokens[FE_token][3]))
                            parent_frame_index.append(FE_token)

                        parent_parent = int(check_length(tokens, parent, 5, False))
                        if FE_token == parent_parent:
                            from_parent_frame.append((lu_id, usage, tokens[FE_token][-1], pt, tokens[FE_token][3]))
                            parent_frame_index.append(FE_token)                    
                                                
                             
    else:
        for data in datas:
            for i in range(0, len(data['tokens'])):
                data['tokens'][i][-1] = data['tokens'][i][-1].replace("B_", "")
                data['tokens'][i][-1] = data['tokens'][i][-1].replace("I_", "")
                data['tokens'][i][-1] = data['tokens'][i][-1].replace("O_", "")
                data['tokens'][i][-1] = data['tokens'][i][-1].replace("S_", "")
                
                
        for data in datas:
            if index % 100 == 0:
                print(index)
            index += 1
            tokens = data['tokens']
            frame_list = []
            FE_tokens = []

            for token in tokens:
                if token[14] != 'O':
                    FE_tokens.append(int(token[0]))

                if token[12] != '_':
                    frame_list.append(int(token[0]))
            if frame_list == []:
                print(tokens)

            if len(frame_list) >= 2:
                temp_frame = []
                for frame in frame_list:
                    standard_frame = frame
                    point = frame
                    while tokens[point][12] != '_' and point != -1:
                        point = int(tokens[point][9])
                        if tokens[point][12] != '_' and point != -1:
                            standard_frame = point
                    temp_frame.append(standard_frame)
                standard_frame = temp_frame[0]
            else:
                standard_frame = frame_list[0]
                
            surface_form = ""
            for frame in frame_list:
                surface_form += tokens[frame][1] + ' '
            surface_form = surface_form[:-1]

            usage = check_length(tokens, standard_frame, 11, False)        

            
            lu_id = None
            for feature in feature_list:
                if feature['lu'] == tokens[standard_frame][12] + '.' + tokens[standard_frame][13]:
                    lu_id = feature['lu_id']
                    
            if lu_id == None:
                print("standard_frame: ", standard_frame)
                for token in tokens:
                    print(token)
                print(tokens[standard_frame][12] + '.' + tokens[standard_frame][13])

            to_frame_index = []
            from_frame_index = []

            for FE_token in FE_tokens:
                parent = int(check_length(tokens, FE_token, 9, False))
                if parent in frame_list:
                    usage = check_length(tokens, parent, 11, False)
                    pt = check_length(tokens, FE_token, 11, False)
                    function = pt.split("_")
                    if len(function) == 1:
                        to_frame.append((lu_id, usage, tokens[FE_token][-1], pt, tokens[FE_token][5]))

                    elif len(function)==2 and (function[1]!='AJT' and function[1] != 'MOD'):
                        for phrase in phrases:
                            to_frame.append((lu_id, usage, tokens[FE_token][-1], phrase+"_"+function[1], tokens[FE_token][5]))
                            to_frame_index.append(FE_token)

                    else:
                        word_tokens = tokens[FE_token][2].split("+")
                        suffix_word = ""
                        for word in word_tokens:
                            info = word.split("/")
                            if len(info) >= 2:
                                if info[1].find("J") != -1:
                                    suffix_word += info[0]
                        if suffix_word == "":
                            for phrase in phrases:
                                to_frame.append((lu_id, usage, tokens[FE_token][-1], phrase+"_"+function[1], tokens[FE_token][5]))
                        else:
                            to_suffix.append((lu_id, usage, tokens[FE_token][-1], suffix_word, tokens[FE_token][5]))
                        to_frame_index.append(FE_token)

            for frame in frame_list:
                parent = int(check_length(tokens, frame, 9, False))
                usage = check_length(tokens, frame, 11, False)
                if parent == -1:
                    continue
                if tokens[parent][-1] != 'O':
                    pt = check_length(tokens, parent, 11, False)
                    function = pt.split("_")

                    if len(function) == 1:
                        from_frame.append((lu_id, usage, tokens[parent][-1], pt, tokens[parent][5]))

                    elif len(function) == 2 and (function[1]!='AJT' and function[1] != 'MOD'):
                        for phrase in phrases:
                            from_frame.append((lu_id, usage, tokens[parent][-1], phrase+"_"+function[1], tokens[parent][5]))
                            from_frame_index.append(parent)
                    else:
                        word_tokens = tokens[parent][2].split("+")
                        suffix_word = ""
                        for word in word_tokens:
                            info = word.split("/")
                            if len(info) >= 2:
                                if info[1].find("J") != -1:
                                    suffix_word += info[0]
                        if suffix_word == "":
                            for phrase in phrases:
                                from_frame.append((lu_id, usage, tokens[parent][-1], phrase+"_"+function[1], tokens[parent][5]))
                        else:
                            from_suffix.append((lu_id, usage, tokens[parent][-1], suffix_word, tokens[FE_token][5]))
                        from_frame_index.append(parent)

            other_suffix_index = []
            for FE_token in FE_tokens:
                if FE_token not in to_frame_index and FE_token not in from_frame_index:
                    point = int(check_length(tokens, FE_token, 9, False))
                    usage = check_length(tokens, standard_frame, 11, False) 
                    existance = 0
                    while point != -1:
                        if point in to_frame_index or \
                        point in from_frame_index:
                            existance = 1
                            break
                        point = int(check_length(tokens, point, 9, False))

                    if existance == 0:
                        pt = check_length(tokens, FE_token, 11, False)
                        function = pt.split("_")

                        if len(function) == 2:
                            if function[1] == 'AJT' or function[1] == 'MOD':
                                word_tokens = tokens[FE_token][2].split("+")
                                suffix_word = ""
                                for word in word_tokens:
                                    info = word.split("/")
                                    if len(info) >= 2:
                                        if info[1].find("J") != -1:
                                            suffix_word += info[0]
                                if suffix_word != "":
                                    other_suffix.append((lu_id, usage, tokens[FE_token][-1], suffix_word, tokens[FE_token][5]))
                                    other_suffix_index.append(FE_token)

            parent_frame_index = []
            for frame in frame_list:
                parent = int(check_length(tokens, frame, 9, False))
                usage = check_length(tokens, frame, 11, False)
                function = usage.split("_")
                if len(function) == 2:
#                     if function[1] == 'CMP' or function[1] == 'SBJ' or function == 'OBJ':
                    for FE_token in FE_tokens:
                        pt = check_length(tokens, FE_token, 11, False)
                        point = int(check_length(tokens, FE_token, 9, False))
                        if point == parent:
                            for phrase in phrases:
                                to_parent_frame.append((lu_id, phrase+"_"+function[1], tokens[FE_token][-1], pt, tokens[FE_token][5]))
                            parent_frame_index.append(FE_token)

                        parent_parent = int(check_length(tokens, parent, 9, False))
                        if FE_token == parent_parent:
                            for phrase in phrases:
                                from_parent_frame.append((lu_id, phrase+"_",function[1], tokens[FE_token][-1], pt, tokens[FE_token][5]))
                            parent_frame_index.append(FE_token)
                else:
                    for FE_token in FE_tokens:
                        pt = check_length(tokens, FE_token, 11, False)
                        point = int(check_length(tokens, FE_token, 9, False))
                        if point == parent:
                            to_parent_frame.append((lu_id, usage, tokens[FE_token][-1], pt, tokens[FE_token][5]))
                            parent_frame_index.append(FE_token)

                        parent_parent = int(check_length(tokens, parent, 9, False))
                        if FE_token == parent_parent:
                            from_parent_frame.append((lu_id, usage, tokens[FE_token][-1], pt, tokens[FE_token][5]))
                            parent_frame_index.append(FE_token)                    
                                
    
#     print(to_frame)
#     print(from_frame)
#     print(to_parent_frame)
#     print(from_parent_frame)
#     print(to_suffix)
#     print(from_suffix)
#     print(other_suffix)
    make_json = []
    for json_data in feature_list:
        make_dic = json_data
        make_dic = make_dictionary(json_data, to_frame, 'to_frame', make_dic)
        make_dic = make_dictionary(json_data, from_frame, 'from_frame', make_dic)
        make_dic = make_dictionary(json_data, to_parent_frame, 'to_parent_frame', make_dic)
        make_dic = make_dictionary(json_data, from_parent_frame, 'from_parent_frame', make_dic)
        make_dic = make_dictionary2(json_data, to_suffix, 'to_suffix', make_dic)
        make_dic = make_dictionary2(json_data, from_suffix, 'from_suffix', make_dic)
        make_dic = make_dictionary2(json_data, other_suffix, 'other_suffix', make_dic)

        make_json.append(make_dic)
        
    if save_mode == True:
        with open(output_file, "w", encoding="utf-8") as make_file:
            json.dump(make_json, make_file, ensure_ascii=False, indent = 4)
    
    return make_json

