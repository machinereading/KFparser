
# coding: utf-8

# In[161]:

import json
import etri
import kfn


# In[162]:

def load_kfn():
    with open('./resource/KFN_lus.json', 'r') as f:
        kolu = json.load(f)
    with open('./resource/KFN_annotations.json','r') as f:
        koanno = json.load(f)
    print('### load KFN ###')
    return kolu, koanno
kolu, koanno = load_kfn()


# In[4]:

def lu_rev():
    # annotation 오류가 없는 상태로 만들기
    new_kolu = []
    for i in kolu:
        s = i['surface_forms']
        if len(s) > 0:
            new_kolu.append(i)
    with open('./resource/KFN_lus.json','w') as f:
        json.dump(new_kolu, f, ensure_ascii=False, indent=4)    


# In[163]:

def get_eid(span, ori_text):
    text = ' '.join(ori_text.split())
    sent_list = text.split(' ')
    #print(sent_list)
    b,e = int(span['begin']), int(span['end'])
    n = 0
    k = 0
    ori_text_list = ori_text.split(' ')
    #print(ori_text_list)
    for i in ori_text_list:
        if i == '':
            k = k+1
    #print('k:',k)
    e_num = 0
    e_list = []
    for eojeol in sent_list:
        if eojeol == '':
            pass
        else:
            eojeol_begin_offset = n
            eojeol_end_offset = n+len(eojeol)
            n = eojeol_end_offset+1
            t = (eojeol_begin_offset, eojeol_end_offset, e_num, eojeol)
            e_list.append(t)
            e_num = e_num +1
    begin, end = 0,0
    for i in e_list:
        if b <= i[0]+k or (b >=i[0] and e <= i[1]+k):
            begin = i[2]
            break
    for i in e_list:
        if e <= i[1]+k:
            end = i[2]
            break
    #print(e_list)
    #print(b,e)
    #print(span)
    #print(begin,end)
    return begin, end

def get_eojeol(span, ori_text):
    text = ' '.join(ori_text.split())
    #text = ori_text
    begin, end = get_eid(span, ori_text)
    end = end+1
    text_list = text.split(' ')
    eojeol_list = text_list[begin:end]
    eojeol_list = [ e.replace('.', '') for e in eojeol_list ]
    eojeol_list = [ e.replace(',', '') for e in eojeol_list ]
    eojeol_list = [ e.replace('!', '') for e in eojeol_list ]
    eojeol_list = [ e.replace('?', '') for e in eojeol_list ]
    eojeol = ' '.join(eojeol_list)
    #print(eojeol)
    return eojeol


# training data 와 test data를 나누는 작업

# In[24]:

def gen_list_training_test():
    # training/test data 조건: FE annotation 에 오류가 없는 경우 (이건 그냥 믿고 진행)
    # test data 조건 1) ambiguity 가 있는 LU
    lexs = []
    for i in kolu:
        lex = i['lu'].split('.')[0]
        lexs.append(lex)
    ambi = []
    for i in lexs:
        count = lexs.count(i)
        if count >1:
            ambi.append(i)
    #ambi = list(set(ambi))
    print('전체 LU 개수:', len(lexs))
    print('모호성 있는 LU 개수:', len(ambi)) 
    ambi = list(set(ambi))
    # test data 조건 2) FE 가 있는 LU
    felus = []
    for i in kolu:
        lex = i['lu'].split('.')[0]
        luid = i['lu_id']
        if lex in ambi:
            print('### luid:',luid, 'added:', len(felus))
            anno = kfn.annotation(luid)
            for i in anno:
                for d in i['denotations']:
                    if d['obj'] != 'target':
                        aid = i['ko_annotation_id']
                        print('aid:', aid)
                        felus.append(aid)                 
            print('')
                        
    print(len(felus))
    felus = list(set(felus)) 
    print(len(felus))
    with open('./anno_ids_for_test_v1.json', 'w') as f:
        json.dump(felus, f, ensure_ascii=False, indent=4)
    # test data 조건 3) FE가 있으면서, 각 FE들이 다른 문장에서 등장한 경우
        #break
#gen_list_training_test()


# In[153]:

def gen_tt_data():
    with open('./anno_ids_for_test_v1.json', 'r') as f:
        aids = json.load(f)
    #print(len(aids))
    training_list = []
    test_list = []
    for i in kolu:

        luid = i['lu_id']
        print(luid)
#        if luid == 2:
        anno = kfn.annotation(luid)
        test_1 = False
        for i in anno:
            aid = i['ko_annotation_id']
            if aid in aids:
                test_list.append(aid)
                break
        for i in anno:
            aid = i['ko_annotation_id']
            if aid not in aids:
                training_list.append(aid)
#             if test_1 == True:
#                 fetags = []
#                 for a in anno:
#                     for d in a['denotations']:
#                         if d['obj'] != 'target':
#                             fetag = d['obj']
#                             fetags.append(fetag)
#                 for a in anno:
#                     mytags = []
#                     for d in a['denotations']:
#                         if d['obj'] != 'target':
#                             mytag = d['obj']
#                             mytags.append(mytag)
#                     add = True
#                     print('mytags', mytags)
#                     for t in mytags:
#                         count = fetags.count(t)
#                         if count == 1:
#                             add = False
#                     #if len()
#                     if add == True:
#                         test_list.append(a['ko_annotation_id'])
#                         break
            print('test_data:',len(test_list))
            print('')
            #print(test_list)
    #total_aids = []
    #for i in kolu:
    #    luid = i['lu_id']
    #    anno = kfn.annotation(luid)
    #    for i in anno:
    #        aid = i['ko_annotation_id']
    #        total_aids.append(aid)
    #        if aid in test_list:
    #            pass
    #        else:
    #            training_list.append(aid)
            
    #print('total LU:',len(kolu))
    #print('total_aids:', len(total_aids))
    #print('test_list:')
    #print(len(test_list))
    #print(len(list(set(test_list))))
    #print('training_list:')
    #print(len(training_list))
    #print(len(list(set(training_list))))
    result = {}
    #training_list = []
    result['training'] = training_list
    result['test'] = test_list
    
    with open('./aids_list.json', 'w') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)
#gen_tt_data()


# In[164]:

def dummy():
    with open('./aids_list.json', 'r') as f:
        d = json.load(f)
    print(len(d['test']))
    print(len(d['training']))
dummy()


# In[107]:

def remove_annotation_error():
    with open('./resource/KFN_lus.json.bak2','r') as f:
        klu = json.load(f)
    for i in klu:
        surface_forms = []
        luid = i['lu_id']

        #if luid == 129:
        #if luid == 193:
        err = 0
        #if luid == 5:
        annos = kfn.annotation(luid)
        print('###', luid, i['lu'])
        for anno in annos:
            denos = anno['denotations']
            text = anno['text']
            #print(text)
            for deno in denos:
                #print(anno['ko_annotation_id'])

                if deno['obj'] == 'target' or deno['obj'] == 'Target':
                    #print(deno)
                    target_span = deno['span']
                    b,e = target_span['begin'], target_span['end']
                    #annotation error 제외
                    if type(b) == str:
                        err = anno['ko_annotation_id']
                        print(err)
                    else:
                        #e = e+1
                        pass
        #print(i['ko_annotation_id'])
        if err != 0:
            i['ko_annotation_id'].remove(err)
        print('')
    with open('./resource/KFN_lus.json','w') as f:
        json.dump(klu, f, ensure_ascii=False, indent=4)
#remove_annotation_error()
        


# In[172]:

def get_conll(anno, frame):
    #print(anno)
    denos = anno['denotations']
    ori_text = anno['text']
    #print(ori_text)
    #print(anno['ko_annotation_id'])
    text = ' '.join(ori_text.split())
    #ori_text_list 
    conll = etri.getETRI_CoNLL2006(ori_text)
    for deno in denos:
        span = deno['span']
        if deno['obj'] == 'target':
            begin, end = get_eid(span, ori_text)
            for token in conll:
                tid = token[0]
                if tid >= begin and tid <= end:
                    token.append('Y')
                    token.append(frame)
                else:
                    token.append('_')
                    token.append('_')
    #ori_text_list = text.split(' ')
    #print(ori_text_list)
    for deno in denos:
        fe = deno['obj']
        span = deno['span']
        if deno['obj'] != 'target':
            begin, end = get_eid(span, ori_text)
            #print(begin, end)
            for token in conll:
                #print(token)
                tid = token[0]
                if tid >= begin and tid <= end:
                    token.append(fe)
    for token in conll:
        if len(token) == 11:
            token.append('_')
        #print(token)
    #print('')
        
    return conll
            
def load_sejong():
    with open('./resource/KFN_annotations_from_sejong.json','r') as f:
        sejong = json.load(f)
    return sejong
sejong = load_sejong()

def get_sejong_anno(sejong_id):
    result = []
    for i in sejong:
        for j in i['annotations']:
            if sejong_id == j['ko_annotation_id']:
                result = j
                break
    return result

def write_training_for_all(conll, sent_id, sent):
    #print(conll)
    with open('./training_for_all.tsv', 'a') as f:
        f.write("#sentid:"+sent_id+"\n")
        f.write("#text:"+sent+"\n")
        for token in conll:
            #print(token)
            line = '\t'.join(map(str,token))
            f.write(line+"\n")
        f.write("\n")
        
def write_training(conll, sent_id, sent):
    #print(conll)
    with open('./training.tsv', 'a') as f:
        f.write("#sentid:"+sent_id+"\n")
        f.write("#text:"+sent+"\n")
        for token in conll:
            #print(token)
            line = '\t'.join(map(str,token))
            f.write(line+"\n")
        f.write("\n")
        
def write_test(conll, sent_id, sent):
    #print(conll)
    with open('./test.tsv', 'a') as f:
        f.write("#sentid:"+sent_id+"\n")
        f.write("#text:"+sent+"\n")
        for token in conll:
            #print(token)
            line = '\t'.join(map(str,token))
            f.write(line+"\n")
        f.write("\n")

def gen_data():
    with open('./resource/KFN_annotations_from_sejong.json','r') as f:
        sejong = json.load(f)
    with open('./aids_list.json', 'r') as f:
        aids_list = json.load(f)
    training_list = aids_list['training']
    test_list = aids_list['test']
    
    #training_for_all = []
    for i in kolu:
        frame = i['lu'].split('.')[2]
        aids = i['ko_annotation_id']
        luid = i['lu_id']
        
        #if luid == 1:
        #if luid == 193:
        #if luid == 129:
        
        #for all
        
        #if luid == 5:
        #if luid == 6795:
        print('training', i['lu'])
        print(i['lu'])
        annos = kfn.annotation(luid)
        for aid in aids:
            if aid in test_list:
                for anno in annos:
                    if aid == anno['ko_annotation_id']:
                        try:
                            conll = get_conll(anno, frame)
                            sent_id = str(anno['sent_id'])
                            sent = anno['text']
                            write_test(conll, sent_id, sent)
                            print(str(aid)+': success')
                        except KeyboardInterrupt:
                            raise
                        except Exception as e:
                            print(str(aid)+': error')
                            pass

            else:
                for anno in annos:
                    if aid == anno['ko_annotation_id']:
                        try:
                            conll = get_conll(anno, frame)
                            sent_id = str(anno['sent_id'])
                            sent = anno['text']
                            write_training_for_all(conll, sent_id, sent)
                            print(str(aid)+': success')
                        except KeyboardInterrupt:
                            raise
                        except Exception as e:
                            print(str(aid)+': error')
                            pass

        sejong_ids = i['sejong_annotation_id']

        if len(sejong_ids) >0:
            for sid in sejong_ids:
                try:
                    sejong_anno = get_sejong_anno(sid)
                    sent = sejong_anno['text']
                    conll = get_conll(sejong_anno, frame)        
                    sent_id = str(sejong_anno['ko_annotation_id'])
                    write_training_for_all(conll, sent_id, sent)
                    print(str(sid)+': success')
                except KeyboardInterrupt:
                    raise
                except Exception as e:
                    print(str(sid)+': error')
                    pass
            #break

    for i in kolu:
        frame = i['lu'].split('.')[2]
        aids = i['ko_annotation_id']
        luid = i['lu_id']
        print('test', i['lu'])
        annos = kfn.annotation(luid)
        for aid in aids:
            if aid in test_list:
                pass

            else:
                for anno in annos:
                    if aid == anno['ko_annotation_id']:
                        try:
                            conll = get_conll(anno, frame)
                            sent_id = str(anno['sent_id'])
                            sent = anno['text']
                            write_training(conll, sent_id, sent)
                        except KeyboardInterrupt:
                            raise
                        except Exception as e:
                            print(str(aid)+': error')
                            pass

gen_data()

