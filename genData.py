
# coding: utf-8

# In[1]:

from koreanframenet import kfn
import json
import etri
import random


# In[2]:

def load_kfn():
    with open('./koreanframenet/resource/KFN_lus.json', 'r') as f:
        kolu = json.load(f)
    with open('./koreanframenet/resource/KFN_annotations.json','r') as f:
        koanno = json.load(f)
    print('### load KFN ###')
    return kolu, koanno
kolu, koanno = load_kfn()


# # Step 1. Generate Sentence List of TRN, TST, and DEV

# In[41]:

def gen_list():
    sent_ids = []
    for i in koanno:
        sent_id = i['text']['sent_id']
        sent_ids.append(sent_id)
    random.shuffle(sent_ids)
    
    tst = sent_ids[:3500]
    trn = sent_ids[3500:]

    result = {}
    result['trn'] = trn
    result['tst'] = tst
    #result['dev'] = dev
    print(len(trn), len(tst))
    return result
sent_list = gen_list()


# In[42]:

def get_luid(anno_id):
    luid = False
    for lu in kolu:
        if anno_id in lu['ko_annotation_id']:
            luid = lu['lu_id']
            #print(luid)
            break
    return luid

def get_fes(deno):
    fes = []
    for d in deno:
        if d['obj'] != 'target':
            fe = d['obj'].lower()
            fes.append(fe)
    fes = list(set(fes))
    return fes 

def get_lus(data):
    result = []
    for i in koanno:
        sent_id = i['text']['sent_id']
        lu_list = []
        if sent_id in data:
            annos = i['frameAnnotation']['ko_annotations']
            for a in annos:
                anno_id = a['ko_annotation_id']
                lu = get_luid(anno_id)
                deno = a['denotations']
                lu_fes = get_fes(deno)
                if lu != False:
                    lu_dic = {}
                    lu_dic['luid'] = lu
                    lu_dic['fes'] = lu_fes
                    lu_list.append(lu_dic)
                    
            d = {}
            d['sent_id'] = sent_id
            d['lus'] = lu_list
            result.append(d)
    #lus = list(set(lus))
    return result

def gen_lus():
    trn, tst= sent_list['trn'], sent_list['tst']
    d = {}
    d['trn'] = get_lus(trn)
    print('trn is done')
    d['tst'] = get_lus(tst)
    print('tst is done')
#     d['dev'] = get_lus(dev)
#     print('dev is done')
    
    with open('./data/data_lus.json','w') as f:
        json.dump(d, f, ensure_ascii=False, indent=4)

#gen_lus()


# In[51]:

with open('./data/data_lus.json','r') as f:
    data_lus = json.load(f)

def check_lus():
    lus_in_trn = []
    for trn_sent in data_lus['trn']:
        for i in trn_sent['lus']:
            luid, fes = i['luid'], i['fes']
            tu = (luid, fes)
            lus_in_trn.append(tu)        

    sent_list = []
    sent_count, anno_count = 0,0 
    for tst_sent in data_lus['tst']:
        count = 0
        sent_id = tst_sent['sent_id']
        for i in tst_sent['lus']:
            luid, fes = i['luid'], i['fes']
            check = False
            for j in lus_in_trn:
                if luid == j[0]:
                    check_list = []
                    for fe in fes:
                        if fe in j[1]:
                            check_list.append('t')
                    if len(check_list) == len(fes):
                        check = True
                        #anno_count += 1
                        break
            if check == True:
                anno_count += 1
                count += 1
            
        if count == len(tst_sent['lus']):
            sent_count += 1
            sent_list.append(sent_id)
    
    random.shuffle(sent_list)
    
    dev = sent_list[:50]
    tst = sent_list[50:]
    trn = []
    for i in koanno:
        sent_id = i['text']['sent_id']
        if sent_id not in tst:
            if sent_id not in dev:
                trn.append(sent_id)
    dev = dev + trn[:50]
    trn = trn[50:]
    print(len(trn), len(tst), len(dev))
    
    d = {}
    d['trn'] = trn
    d['tst'] = tst
    d['dev'] = dev
    
        
    print(sent_count, anno_count, len(data_lus['tst']))
    with open('./data/data_sent_list.json','w') as f:
        json.dump(d, f, ensure_ascii=False, indent=4)
            
#check_lus()


# # Step 2. Generate CoNLL for dataset

# In[52]:

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
    return begin, end

def get_lu_frame(anno_id):
    for i in kolu:
        if type(anno_id) == str:
            if anno_id in i['sejong_annotation_id']:
                lu_name = i['lu']
                break
        else:
            if anno_id in i['ko_annotation_id']:
                lu_name = i['lu']
                break
    lu_list = lu_name.split('.')
    lu = lu_list[0]+'.'+lu_list[1]
    frame = lu_list[2]
    return lu, frame

def getBIO_list(sent_list):
    result = []
    fe_list = []
    for i in range(len(sent_list)):
        fe = sent_list[i][14].lower()
        fe_list.append(fe)
    for i in range(len(sent_list)):
        fe = sent_list[i][14]
        if i == 0:
            if fe == '_':
                fe = 'O'
            else:
                try:
                    if fe == fe_list[i+1]:
                        fe = 'B_'+fe
                    else:
                        fe = 'S_'+fe
                except KeyboardInterrupt:
                    raise
                except:
                    fe = 'S_'+fe
        else:
            if fe == '_':
                fe = 'O'
            else:
                if fe != fe_list[i-1]:
                    try:
                        if fe == fe_list[i+1]:
                            fe = 'B_'+fe
                        else:
                            fe = 'S_'+fe
                    except KeyboardInterrupt:
                        raise
                    except:
                        fe = 'S_'+fe
                else:
                    fe = 'I_'+fe
        result.append(fe)
    for i in range(len(sent_list)):
        sent_list[i][14] = result[i]
    return sent_list


# In[53]:

def genCoNLLdata(anno):
    result = []
    sent_id = anno['sent_id'] 
    ori_text = anno['ko_text']
    denos = anno['annotations']
    text = ' '.join(ori_text.split())

    for deno in denos:
        try:
            conll = etri.getETRI_CoNLL2009(ori_text)
            anno_id = deno['ko_annotation_id']            
            try:
                lu, frame = get_lu_frame(anno_id)
                for d in deno['denotations']:
                    span = d['span']
                    if d['obj'] == 'target':
                        begin, end = get_eid(span, ori_text)
                        for token in conll:
                            tid = token[0]
                            if tid >= begin and tid <= end:
                                token.append(lu)
                                token.append(frame)
                            else:
                                token.append('_')
                                token.append('_')
                for d in deno['denotations']:
                    fe = d['obj']
                    span = d['span']
                    if fe != 'target':
                        begin, end = get_eid(span, ori_text)
                        for token in conll:
                            tid = token[0]
                            if tid >= begin and tid <= end:
                                token.append(fe)
                for token in conll:
                    if len(token) == 14:
                        token.append('_')
                conll = getBIO_list(conll)
                result.append(conll)
            except KeyboardInterrupt:
                raise
            except:
                print('err2',anno_id)
                pass
        except KeyboardInterrupt:
            raise
        except:
            print('err1',sent_id)
    return result


# # Step 3. Write Data Files

# In[ ]:

# def load_sejong():
#     with open('./koreanframenet/resource/KFN_annotations_from_sejong.json','r') as f:
#         sejong = json.load(f)
#     return sejong
# sejong = load_sejong()


# In[57]:

def write_data():
    with open('./data/data_sent_list.json', 'r') as f:
        d = json.load(f)
    dev = d['dev']
    tst = d['tst']
    trn = d['trn']

#     for s in sejong:
#         for a in s['annotations']:
#             anno = {}
#             anno['sent_id'] = a['ko_annotation_id']
#             anno['ko_text'] = a['text']
#             anno['annotations'] = [a]

#             conlls = genCoNLLdata(anno)
#             for conll in conlls:
#                 add = False
#                 for t in conll:
#                     if t[12] != '_':
#                         add = True
#                 if add == True:
#                     with open('./koreanframenet/data/exemplar.tsv', 'a') as f:
#                         sent_id = str(anno['sent_id'])
#                         sent = anno['ko_text']
#                         f.write("#sentid:"+sent_id+"\n")
#                         f.write("#text:"+sent+"\n")
#                         for token in conll:
#                             line = '\t'.join(map(str,token))
#                             f.write(line+"\n")
#                         f.write('\n')
        
    for i in koanno:
        s_id = i['text']['sent_id']
        print(s_id)
        if s_id in tst:
            anno = {}
            anno['sent_id'] = i['text']['sent_id']
            anno['ko_text'] = i['text']['ko_text']
            anno['annotations'] = i['frameAnnotation']['ko_annotations']
            conlls = genCoNLLdata(anno)
            for conll in conlls:
                add = False
                for t in conll:
                    if t[12] != '_':
                        add = True
                if add == True:
                    with open('./koreanframenet/data/test.tsv', 'a') as f:
                        sent_id = str(anno['sent_id'])
                        sent = anno['ko_text']
                        f.write("#sentid:"+sent_id+"\n")
                        f.write("#text:"+sent+"\n")
                        for token in conll:
                            line = '\t'.join(map(str,token))
                            f.write(line+"\n")
                        f.write('\n')
        elif s_id in dev:
            anno = {}
            anno['sent_id'] = i['text']['sent_id']
            anno['ko_text'] = i['text']['ko_text']
            anno['annotations'] = i['frameAnnotation']['ko_annotations']
            conlls = genCoNLLdata(anno)
            for conll in conlls:
                add = False
                for t in conll:
                    if t[12] != '_':
                        add = True
                if add == True:
                    with open('./koreanframenet/data/dev.tsv', 'a') as f:
                        sent_id = str(anno['sent_id'])
                        sent = anno['ko_text']
                        f.write("#sentid:"+sent_id+"\n")
                        f.write("#text:"+sent+"\n")
                        for token in conll:
                            line = '\t'.join(map(str,token))
                            f.write(line+"\n")
                        f.write('\n')
        else:
            anno = {}
            anno['sent_id'] = i['text']['sent_id']
            anno['ko_text'] = i['text']['ko_text']
            anno['annotations'] = i['frameAnnotation']['ko_annotations']

            conlls = genCoNLLdata(anno)
            for conll in conlls:
                add = False
                for t in conll:
                    if t[12] != '_':
                        add = True
                if add == True:
                    with open('./koreanframenet/data/training.tsv', 'a') as f:
                        sent_id = str(anno['sent_id'])
                        sent = anno['ko_text']
                        f.write("#sentid:"+sent_id+"\n")
                        f.write("#text:"+sent+"\n")
                        for token in conll:
                            line = '\t'.join(map(str,token))
                            f.write(line+"\n")
                        f.write('\n')
    print('done')
write_data()

