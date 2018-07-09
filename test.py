import targetid
import frameid
import argid
import etri

targetid_model = 'baseline'
frameid_model = 'frequent'
argid_model = 'rulebased'

sent = '나는 밥을 먹고 학교에 갔다'

conll = etri.getETRI_CoNLL2009(sent)
conll_target = targetid.target_identifier(conll, targetid_model)
conll_frame = frameid.frame_identifier(conll_target, frameid_model)
#conll_arg = argid.arg_identifier(conll_frame, argid_model)

for i in conll_frame:
    for j in i:
        print(j)

