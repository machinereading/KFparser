
# coding: utf-8

# In[17]:


from koreanframenet import kfn
import json
from src import etri
import random
import os
import sys
import preprocessor


# In[2]:


def load_kfn():
    dir_path = os.getcwd()
    with open(dir_path+'/koreanframenet/resource/KFN_lus.json', 'r') as f:
        kolu = json.load(f)
    with open(dir_path+'/koreanframenet/resource/KFN_annotations.json','r') as f:
        koanno = json.load(f)
    print('### load KFN ###')
    return kolu, koanno
kolu, koanno = load_kfn()


# # Step 1. Generate Sentence List of TRN, TST, and DEV

# In[23]:


def gen_list():
    sent_ids = []
    for i in koanno:
        sent_id = i['text']['sent_id']
        sent_ids.append(sent_id)
    random.shuffle(sent_ids)
    
    tst = sent_ids[:1250]
    dev = sent_ids[1250:1450]
    trn = sent_ids[1400:]

    result = {}
    result['trn'] = trn
    result['tst'] = tst
    result['dev'] = dev
    #result['dev'] = dev
    sys.stderr.write("\nKOREAN FRAMENET DATA (CoNLL format) GENERATION\n_____________________\n")
    sys.stderr.write("\n...shuffle Korean FrameNet full-text annotation sentences...\n")
    sys.stderr.write("training data: \t" + str(len(trn)) + ' sents\n')
    sys.stderr.write("dev data:      \t" + str(len(dev)) + '  sents\n')
    sys.stderr.write("test data:     \t" + str(len(tst)) + ' sents\n')
    return result
sent_list = gen_list()


# # Step 2. Generate CoNLL for dataset

# In[4]:


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
        fe = sent_list[i][14].lower()
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


# In[12]:


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
                #print('err2',anno_id)
                pass
        except KeyboardInterrupt:
            raise
        except:
            pass
            #print('err1',sent_id)
    return result


# # Step 3. Write Data Files

# In[ ]:


# def load_sejong():
#     with open('./koreanframenet/resource/KFN_annotations_from_sejong.json','r') as f:
#         sejong = json.load(f)
#     return sejong
# sejong = load_sejong()


# In[24]:


def write_data():
    sys.stderr.write("\n...converting data to CoNLL 2009 format...\n")
    dir_path = os.getcwd()
    dev = sent_list['dev']
    tst = sent_list['tst']
    trn = sent_list['trn']
    trn_file = open(dir_path+'/koreanframenet/data/training.tsv', 'w')
    dev_file = open(dir_path+'/koreanframenet/data/dev.tsv', 'w')
    tst_file = open(dir_path+'/koreanframenet/data/test.tsv', 'w')

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
                for t in conll:
                    if t[14] in ['B_x', 'I_x', 'S_x']:
                        add = False
                if add == True:
                    sent_id = str(anno['sent_id'])
                    sent = anno['ko_text']
                    tst_file.write("#sentid:"+sent_id+"\n")
                    tst_file.write("#text:"+sent+"\n")
                    for token in conll:
                        line = '\t'.join(map(str,token))
                        tst_file.write(line+"\n")
                    tst_file.write('\n')
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
                for t in conll:
                    if t[14] in ['B_x', 'I_x', 'S_x']:
                        add = False
                if add == True:
                    sent_id = str(anno['sent_id'])
                    sent = anno['ko_text']
                    dev_file.write("#sentid:"+sent_id+"\n")
                    dev_file.write("#text:"+sent+"\n")
                    for token in conll:
                        line = '\t'.join(map(str,token))
                        dev_file.write(line+"\n")
                    dev_file.write('\n')
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
                for t in conll:
                    if t[14] in ['B_x', 'I_x', 'S_x']:
                        add = False
                if add == True:
                    sent_id = str(anno['sent_id'])
                    sent = anno['ko_text']
                    trn_file.write("#sentid:"+sent_id+"\n")
                    trn_file.write("#text:"+sent+"\n")
                    for token in conll:
                        line = '\t'.join(map(str,token))
                        trn_file.write(line+"\n")
                    trn_file.write('\n')
    trn_file.close()
    tst_file.close()
    dev_file.close()
    preprocessor.data_stat()
write_data()

