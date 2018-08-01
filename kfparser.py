
# coding: utf-8

# In[2]:


import json
from src import etri
import sys
from datetime import datetime
import time
from koreanframenet import kfn
from optparse import OptionParser


# In[5]:


import targetid
import frameid
import argid
import graphGeneration


# In[6]:


# options

now = datetime.now()
resultfname = './tmp/'+str(now.year)+'.'+str(now.month)+'.'+str(now.day)+'.'+str(time.time())

optpr = OptionParser()
optpr.add_option("--mode", dest='mode', type='choice', choices=['parsing', 'test'], default='parsing')
optpr.add_option("--targetid", dest='targetid', type='choice', choices=['baseline'], default='baseline')
optpr.add_option("--frameid", dest='frameid', type='choice', choices=['baseline'], default='baseline')
optpr.add_option("--argid", dest='argid', type='choice', choices=['baseline'], default='baseline')
optpr.add_option("--result", dest='resultfile', help="Saved result file", metavar="FILE", default=resultfname)
optpr.add_option("--input", dest='input', help="input a sentence", type="string", default=resultfname)
# (options, args) = optpr.parse_args()

optpr.mode = 'parsing'
optpr.targetid = 'baseline'
optpr.frameid = 'frequent'
optpr.argid = 'rulebased'
#optpr.argid = 'suffix_only'

#print options
#sys.stderr.write("\nCOMMAND: "+' '.join(sys.argv) + '\n')
sys.stderr.write("\nPARSER SETTINGS\n_____________________\n")
sys.stderr.write("Target Identification     \t" + str(optpr.targetid) + '\n')
sys.stderr.write("Frame Identification      \t" + str(optpr.frameid) + '\n')
sys.stderr.write("Argument Identification   \t" + str(optpr.argid) + '\n')
if optpr.mode in ['parsing']:
    sys.stderr.write("RESULT WILL BE SAVED TO\t%s\n" %resultfname)


# In[7]:


# parset options

target_identifier = targetid.target_identifier
frame_identifier = frameid.frame_identifier
arg_identifier = argid.arg_identifier


# In[8]:


def frameparsing(sent):
    conll = etri.getETRI_CoNLL2009(sent)
    conll_target = target_identifier(conll, optpr.targetid)
    conll_frame = frame_identifier(conll_target, optpr.frameid)
    conll_arg = arg_identifier(conll_frame, optpr.argid)
    
    return conll_arg


# In[10]:


# parsing

def test():
    if optpr.mode == 'parsing':
        #sent = optpr.input = "기계 학습(機械學習) 또는 머신 러닝(영어: machine learning)은 인공 지능의 한 분야로, 기계가 정보를 학습하도록 하는 알고리즘과 기술을 개발하는 분야를 말한다."
        sent = "지미_카터 는 조지아_주  섬터 카운티 플레인스 마을에서 태어났다."
        parsed = frameparsing(sent)

        graph = graphGeneration.conll2graph(parsed)
        for triple in graph:
            print(triple)
#test()


# In[6]:


def cnn_test():
    with open('/disk_4/cnndata/result_sample_corpus.json','r') as f:
        cnn = json.load(f)
    sentences = []
    for i in cnn:
        sentences.append(i['ko_sentence'])
    print('CNN 문장수:', len(sentences))
    s_f_count, s_fe_count = 0,0
    f_count, fe_count = 0,0
    
    cnn_result = open('./tmp/cnnresult.rulebased.txt','w')

    for sent in sentences:
        cnn_result.write(sent+'\n')
        try:
            parsed = frameparsing(sent)
            graph = graphGeneration.conll2graph(parsed)
            if len(graph) > 0:
                s_f_count += 1
                add = False
                for t in graph:
                    cnn_result.write(str(t)+'\n')
                    if 'frdf:lu' not in t[1]:
                        fe_count += 1
                        add = True
                    else:
                        f_count += 1
                if add:
                    s_fe_count += 1
        except KeyboardInterrupt:
            raise
        except:
            pass
        cnn_result.write('\n')
    
    stat = '#sent: '+str(len(sentences))+', #sent_f: '+str(s_f_count)+', #sent_fe: '+str(s_fe_count)+', #frame: '+str(f_count)+', #fe: '+str(fe_count)
    print(s_f_count, s_fe_count, f_count, fe_count)
    cnn_result.write(stat)
#cnn_test()


# In[16]:


import csv
import re
def get_triples_from_ds(line):
    sent = line[0]
    sbj = re.search('\<e1\>(.*?)\<\/e1\>', sent).group(1)
    obj = re.search('\<e2\>(.*?)\<\/e2\>', sent).group(1)
    pred = line[1]
    triple = (sbj, pred, obj)
    return triple

def ds_test():
    ds_file = open('/disk_4/dsData/usingELU/ds_label_sen.csv','r', encoding='utf-8')
    rdr = csv.reader(ds_file)
    sent_ids = set()

    result = []
    n = 0
    triples = []
    for i in rdr:
        try:
            sent = i[0]
            sent = sent.replace("<e1>", "")
            sent = sent.replace("</e1> ", "")
            sent = sent.replace("</e1>", "")
            sent = sent.replace("<e2>", "")
            sent = sent.replace("</e2> ", "")
            sent = sent.replace("</e2>", "")
            sent = sent.replace("[", "")
            sent = sent.replace("] ", "")
            sent = sent.replace("]", "")
            sent_id = int(i[4])
            if sent_id not in sent_ids:
                n = n+1
                print('sent_id: ', str(sent_id), '(processed :', str(n))
                sent_ids.add(sent_id)
                parsed = frameparsing(sent)
                graph = graphGeneration.conll2graph(parsed)
                triples = []
                #graph = []
            else:
                pass
            triple = get_triples_from_ds(i)
            if sent_id not in sent_ids:
                pass
            else:
                triples.append(triple)
            d = {}
            d['sent_id'] = int(sent_id)
            d['text'] = sent
            d['dbpedia'] = triples
            d['frame'] = list(set(graph))

            add = True
            for r in result:
                if sent_id == r['sent_id']:
                    old_triples = d['dbpedia']
                    new_triples = old_triples + triples
                    new_triples = list(set(new_triples))
                    r['dbpedia'] = new_triples
                    add = False

                else:
                    pass
            if add == True:
                result.append(d)
        except KeyboardInterrupt:
            raise
        except:
            pass
#          n = n+1
#         if n > 5:
#             break
        
    ds_file.close()

    with open('/disk_4/dsData/ds_result.json','w') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)
    print(len(result))

            
ds_test()
        


# In[11]:


# import preprocessor
# trn, tst, dev, exemplar = preprocessor.load_data()
# preprocessor.data_stat()


# In[13]:


# n,v,a = [],[],[]
# for i in tst:
#     for j in i:
#         if j[12] != '_':
#             lu = j[12]
#     pos = lu.split('.')[1]
#     if pos == 'n':
#         n.append(lu)
#     elif pos == 'v':
#         v.append(lu)
#     else:
#         a.append(lu)
# print(len(n),len(v), len(a))
# print(len(list(set(n))), len(list(set(v))), len(list(set(a))))

