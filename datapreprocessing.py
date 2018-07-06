
# coding: utf-8

# In[1]:

from koreanframenet import kfn
import json
import etri


# In[2]:

def load_kfn():
    with open('./koreanframenet/resource/KFN_lus.json.bak3', 'r') as f:
        kolu = json.load(f)
    with open('./koreanframenet/resource/KFN_annotations.json','r') as f:
        koanno = json.load(f)
    print('### load KFN ###')
    return kolu, koanno
kolu, koanno = load_kfn()


# In[6]:

l = []
for i in koanno:
    sent_id = i['text']['sent_id']
    l.append(sent_id)
print(len(l))


# In[18]:

def gen_fe_list_for_lu():
    result = []
    n = 0
    for i in kolu:
        luid = i['lu_id']
        anno = kfn.annotation(luid)
        felist = []
        for j in anno:
            for d in j['denotations']:
                if d['obj'] != 'target':
                    felist.append(d['obj'])
        #felist = list(set(felist))
        d = {}
        d['lu_id'] = luid
        d['fe_list'] = felist
        n += 1
        result.append(d)
        #print(n, '/', len(kolu))
    with open('./data/fes_of_each_lus.json','w') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)
#gen_fe_list_for_lu()


# In[ ]:

def gen_list_bylu():
    with open('./data/fes_of_each_lus.json','r') as f:
        fes_of_lu = json.load(f)
    lexs = []
    for i in kolu:
        lex = i['lu'].split('.')[0]
        lexs.append(lex)           
        
    n = 0
    num_of_test = 0
    result = []
    for i in koanno:
        annos = i['frameAnnotation']['ko_annotations']
        sent_id = i['text']['sent_id']
        anno_ids = []
        for a in annos:
            anno_ids.append(a['ko_annotation_id'])
        mylus = []
        for aid in anno_ids:
            for lu in kolu:
                if aid in lu['ko_annotation_id']:
                    mylus.append(lu['lu'])
        check_list_1 = []
        for mylu in mylus:
            lex = mylu.split('.')[0]
            lu_count = lexs.count(lex)
            if lu_count > 1:
                check_list_1.append('t')
        if len(check_list_1) == len(anno_ids):
            num_of_test += 1
            print(num_of_test, len(koanno))
            result.append(sent_id)
            #break
    print(num_of_test)
    with open('./data/sent_list_by_lu.json', 'w') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)
#gen_list_bylu()


# In[75]:

def get_fes(deno):
    fes = []
    for d in deno:
        if d['obj'] != 'target':
            fe = d['obj']
            fes.append(fe)
    fes = list(set(fes))
    return fes

def get_luid(sent_id):
    luid = False
    for lu in kolu:
        if sent_id in lu['ko_annotation_id']:
            luid = lu['lu_id']
            #print(luid)
            break
    return luid

def gen_list_by_FE():
    sents = []
    anno_ids = []
    with open('./data/fes_of_each_lus.json','r') as f:
        fes_of_lu = json.load(f)
    with open('./data/sent_list_by_lu.json','r') as f:
        sent_list = json.load(f)
    
#     fes_of_frame = []
#     for f in fes_of_lu:
#         frame = kfn.lu(f['lu_id'])['frameName']
#         fes = f['fe_list']
#         d = {}
#         d['frame'] = frame
#         d['fe_list'] = fes
#         add = True
#         for ff in fes_of_frame:
#             if frame == ff['frame']:
#                 new_fes = []
#                 new_fes = ff['fe_list'] + fes
#                 ff['fe_list'] = new_fes
#                 add = False
#         if add == True:
#             fes_of_frame.append(d)
#     print(len(fes_of_frame))
                
    num_of_sent = 0
    lu_list = []
    for i in koanno:
        sent_id = i['text']['sent_id']
        annos = i['frameAnnotation']['ko_annotations']
        text = i['text']

        if sent_id in sent_list:
            #print(luid)
            for anno in annos:
                
                anno_id = anno['ko_annotation_id']
                luid = get_luid(anno_id)
                frame = kfn.lu(luid)['frameName']
                lu_list.append(kfn.lu(luid)['lu'])

                deno = anno['denotations']
                my_fes = get_fes(deno)
                
#                 check_list_1 = []
#                 for f in fes_of_frame:
#                     if frame == f['frame']:
#                         frame_fes = f['fe_list']
#                 for my_f in my_fes:
#                     if frame_fes.count(my_f) > 1:
#                         check_list_1.append('t')
#                 if len(check_list_1) > 0:
#                      if len(check_list_1) == len(my_fes):
#                         #lu_list.append(kfn.lu(luid)['lu'])
#                         sents.append(sent_id)
#                         anno_ids.append(anno_id)                
                
                for fe_of_lu in fes_of_lu:
                    if luid == fe_of_lu['lu_id']:
                        lu_fes = fe_of_lu['fe_list']
                        break                   
                
                check_list_1 = []

                for my_f in my_fes:
                    if lu_fes.count(my_f) > 1:
                        check_list_1.append('t')
                #if len(check_list_1) > 0:
                if len(check_list_1) == len(my_fes):

                    sents.append(sent_id)
                    anno_ids.append(anno_id)
                            
    print(sent_id, len(list(set(sents))), len(anno_ids), len(sent_list))
    lu_list = list(set(lu_list))
    n,v,a = 0,0,0
    for i in lu_list:
        pos = i.split('.')[1]
        if pos == 'n':
            n += 1
        elif pos == 'a':
            a += 1
        elif pos == 'v':
            v += 1
    print(n,v,a)
    
    sents = list(set(sents))
        
    with open('./data/sent_list_by_FE.json', 'w') as f:
        json.dump(sents, f, ensure_ascii=False, indent=4)
#gen_list_by_FE()


# In[3]:

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


# In[50]:

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


# In[5]:

def getBIO_list(sent_list):
    result = []
    fe_list = []
    for i in range(len(sent_list)):
        fe = sent_list[i][14]
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


# In[49]:

def genCoNLLdata(anno):
    result = []
    with open('./data/sent_list_by_FE.json', 'r') as f:
        d = json.load(f)
    #for anno in koanno:
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

#genCoNLLdata()


# In[7]:

def load_sejong():
    with open('./koreanframenet/resource/KFN_annotations_from_sejong.json','r') as f:
        sejong = json.load(f)
    return sejong
sejong = load_sejong()


# In[51]:

def write_data():
    with open('./data/sent_list_by_FE.json', 'r') as f:
        d = json.load(f)
    dev = d[:200]
    tst = d[200:]
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
        

