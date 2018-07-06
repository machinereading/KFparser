
# coding: utf-8

# In[234]:

import json
import kfn


# TODO
# 일본어 annotation 에서 'Target' 으로 된걸 모두 'target'으로 바꿈
# Done

# In[207]:

def dum2():
    with open('./resource/KFN_annotations.json.bak2', 'r') as f:
        koanno = json.load(f)
    e = 0
    for i in koanno:
        annos = i['frameAnnotation']['ko_annotations']
        for anno in annos:
            denos = anno['denotations']
            for deno in denos:
                if type(deno['span']['begin']) == str:
                    #print(deno)
                    e = e+1
    print(e)
#dum2()


# In[185]:

def dum():
    with open('./resource/KFN_annotations.json.bak2', 'r') as f:
        koanno = json.load(f)
    new_koanno = []
    for i in koanno:
        print(i['text']['sent_id'])
        annos = i['frameAnnotation']['origin_annotations']
        new_annos = []
        for anno in annos:
            denos = anno['denotations']
            new_denos = []
            for deno in denos:
                deno['span']['begin'] = int(deno['span']['begin'])
                deno['span']['end'] = int(deno['span']['end'])
                if deno['obj'] == 'Target':
                    deno['obj'] = 'target'
                    print(deno)
                new_denos.append(deno)
            anno['denotations'] = new_denos
    
        annos = i['frameAnnotation']['ko_annotations']
        new_annos = []
        for anno in annos:
            denos = anno['denotations']
            new_denos = []
            for deno in denos:
                deno['span']['begin'] = int(deno['span']['begin'])
                deno['span']['end'] = int(deno['span']['end'])
                if deno['obj'] == 'Target':
                    deno['obj'] = 'target'
                    print(deno)
                new_denos.append(deno)
            anno['denotations'] = new_denos

        new_koanno.append(i)
        #print(i)
    with open('./resource/KFN_annotations.json', 'w') as f:
        json.dump(new_koanno, f, ensure_ascii=False, indent=4)

#dum()


# annotation 파일에서 span을 모두 int로 바꿈

# In[235]:

def load_kfn():
    with open('./resource/KFN_lus.json', 'r') as f:
        kolu = json.load(f)
    with open('./resource/KFN_annotations.json','r') as f:
        koanno = json.load(f)
    print('### load KFN ###')
    return kolu, koanno
kolu, koanno = load_kfn()


# In[247]:

def stat():
    n,v,a=0,0,0
    nn,vv,aa = 0,0,0
    for i in kolu:
        s = i['surface_forms']
        if len(s) > 0:
            pos = i['lu'].split('.')[1]
            if pos == 'n':
                n = n+1
            elif pos == 'v':
                v = v+1
            elif pos == 'a':
                a = a+1
        else:
            print(i['lu'])
        pos = i['lu'].split('.')[1]
        if pos == 'n':
            nn = nn+1
        elif pos == 'v':
            vv = vv+1
        elif pos == 'a':
            aa = aa+1
    print(len(kolu))
    print(nn,vv,aa)
    print(n,v,a)
    
#stat()


# 프리프로세싱
# 
# 1) for annotation
#    - 각 annotation 의 boundary는 어절단위로 되도록 함
#    - 그런데 이건 conll format 으로 만들때 해도 됨
# 
# 2) for LU
#    - 각 LU에 대한 surface form 만들기
#    - 각 LU sorface form에 대해 LU candidates indexing
#    
# 대상어휘
# 1) 동사

# 어노테이션 오류 '제외'
# - 만약 span 의 text 가 어절의 text의 substring 이 아닌 경우에는 제외하는 프로세스 필요
# - 이는 학습데이터 생성할때에도 필요함

# In[261]:

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
        if b <= i[0] or (b >=i[0] and e <= i[1]+k):
            begin = i[2]
            break
    for i in e_list:
        if e <= i[1]+k:
            end = i[2]
            break
    #print(e_list)
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

def lu_rev():
    new_kolu = []
    err = 0
    for i in kolu:
        surface_forms = []
        luid = i['lu_id']

        #if luid == 129:
        #if luid == 193:
        
        #if luid == 5:
        #if luid == 249:
        #if luid == 5392:

        annos = kfn.annotation(luid)
        print('###', luid, i['lu'])
        for anno in annos:
            denos = anno['denotations']
            text = anno['text']
            #print(text)
            for deno in denos:

                if deno['obj'] == 'target' or deno['obj'] == 'Target':
                    #print(deno)
                    target_span = deno['span']
                    b,e = target_span['begin'], target_span['end']
                    #annotation error 제외
                    if type(b) != str:
                        target = get_eojeol(target_span, text)
                        target_anno = text[b:e]
                        if target_anno in target:
                            print('target_anno:',target_anno, 'target:', target)
                            surface_forms.append(target)
                        else:
                            err = err+1
                            #print('eeee',err)
                    else:
                        #e = e+1
                        pass
        surface_forms = list(set(surface_forms))
        i['surface_forms'] = surface_forms
        #print('')
        new_kolu.append(i)
        print('error:', err)
        #else:
            #pass
        #break
    #print(new_kolu)

    with open('./resource/KFN_lus.json','w') as f:
        json.dump(new_kolu, f, ensure_ascii=False, indent=4)
lu_rev()

