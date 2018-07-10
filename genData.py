
# coding: utf-8

# In[2]:

from koreanframenet import kfn
import json
import etri


# In[3]:

def load_kfn():
    with open('./koreanframenet/resource/KFN_lus.json', 'r') as f:
        kolu = json.load(f)
    with open('./koreanframenet/resource/KFN_annotations.json','r') as f:
        koanno = json.load(f)
    print('### load KFN ###')
    return kolu, koanno
kolu, koanno = load_kfn()


# In[ ]:

def gen_lu_list():
    lus_in_annos = []
    for i in koanno:
        annos = i['frameAnnotation']['ko_annotations']
        sent_id = i['text']['sent_id']
        print(sent_id)
        anno_ids = []
        for a in annos:
            anno_ids.append(a['ko_annotation_id'])

        for aid in anno_ids:
            for lu in kolu:
                if aid in lu['ko_annotation_id']:
                    lus_in_annos.append(lu['lu'])
    lus_in_annos = list(set(lus_in_annos))
    
    result = []
    for lu_in_annos in lus_in_annos:
        for i in kolu:
            if lu_in_annos == i['lu']:
                count = len(i['ko_annotation_id'])
                if count > 1:
                    result.append(lu_in_annos)                    
    print(len(result))
    with open('./data/ambi_lu_in_annos.json','w') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)
#gen_lu_list()


# In[8]:

with open('./data/fes_of_each_lus.json','r') as f:
    fes_of_lu = json.load(f)

def get_fes(deno):
    fes = []
    for d in deno:
        if d['obj'] != 'target':
            fe = d['obj'].lower()
            fes.append(fe)
    fes = list(set(fes))
    return fes

def double_check(luid, fes):
    for i in fes_of_lu:
        if luid == i['lu_id']:
            fe_list = i['fe_list']
            for j in fe_list:
                j = j.lower()
            break
    check_list = []
    for i in fes:
        count = fe_list.count(i)
        if count > 1:
            check_list.append('t')
    
    if len(check_list) == len(fes):
        result = True
    else:
        result = False

    return result

def get_koanno():
    with open('./data/ambi_lu_in_annos.json','r') as f:
        ambi_lus = json.load(f)
    result = []
    n =0
    for ambi_lu in ambi_lus:
        print(n, len(ambi_lus))
        for i in kolu:
            if ambi_lu == i['lu']:
                luid = i['lu_id']
                annos = kfn.annotation(luid)
                for a in annos:
                    anno_id = a['ko_annotation_id']
                    deno = a['denotations']
                    fes = get_fes(deno)
                    check = double_check(luid, fes)
                    if check:
                        result.append(anno_id)
                        print(anno_id, 'is added', len(result))
                        break
                    else:
                        pass
            else:
                pass
        n += 1
    print(len(result))
    with open('./data/dummy.json','w') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)
get_koanno()

