import json
import argI_data_preprocessor
import re
import kfn

def load_data(file_name):
    result = argI_data_preprocessor.load_data(file_name)
    #result = training + test
    return result

def get_target(sent_list):
    token_list = []
    frame = 'None'
    for i in sent_list:
        #print(i)
        if len(i) <=3:
            print("error sentence ", sent_list)
        if i[-3] != '_':
            token_list.append(i[1])
            frame = i[-2]
    target = ' '.join(token_list)
    spc = [',','.','!','?']
    if len(target) >1:
        if target[-1] in spc:
            target = re.sub('[,.?!]', '', target)
    return target, frame

def get_lu_id(sent_list):
    target, frame = get_target(sent_list)
    lu_id = kfn.surface_to_lu_id(target, frame)
    return lu_id

def genData(data):
    result = []
    koreanFN = []
    for data_seg in data:
        koreanFN.append(data_seg['tokens'])
    # koreanFN = trainign data in CONLL format
    for sent_list in koreanFN:
        each_lu = {}
        lu_id = get_lu_id(sent_list)
        if lu_id == False:
            continue
        lu = kfn.lu(lu_id)
        each_lu['lu_id'] = lu['lu_id']
        # by this process, 'LU' is identified in training data
        isIn = False
        for i in result:
            if i['lu_id'] == lu_id:
                each_lu = i
#                 vp_list = each_lu['valencePatterns']
#                 # valence pattern 을 생성하는 함수 호출
#                 vp = getValencePattern(sent_list)
#                 vp_list = vp_list + vp
#                 each_lu['valencePatterns'] = vp_list
                i = each_lu
                isIn = True
                break
            else:
                pass
        if isIn == True:
            pass
            # result list 에 대해 중복 제거하기 위함
        else:
            each_lu['lu'] = lu['lu']
            each_lu['surface_forms'] = lu['surface_forms']
            each_lu['lexeme'] = lu['lexeme']
            each_lu['pattern'] = []        
            result.append(each_lu)
    return result