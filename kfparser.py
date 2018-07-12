
# coding: utf-8

# In[1]:


import json
import etri
import sys
from datetime import datetime
import time
from koreanframenet import kfn
from optparse import OptionParser


# In[2]:


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


# In[4]:


# parset options

target_identifier = targetid.target_identifier
frame_identifier = frameid.frame_identifier
arg_identifier = argid.arg_identifier


# In[5]:


def frameparsing(sent):
    conll = etri.getETRI_CoNLL2009(sent)
    conll_target = target_identifier(conll, optpr.targetid)
    #print(conll_target)
    conll_frame = frame_identifier(conll_target, optpr.frameid)
    conll_arg = arg_identifier(conll_frame, optpr.argid)
    
    return conll_arg


# In[7]:


# parsing

def test():
    if optpr.mode == 'parsing':
        sent = optpr.input = "기계 학습(機械學習) 또는 머신 러닝(영어: machine learning)은 인공 지능의 한 분야로, 기계가 정보를 학습하도록 하는 알고리즘과 기술을 개발하는 분야를 말한다."
        parsed = frameparsing(sent)

        graph = graphGeneration.conll2graph(parsed)
        for triple in graph:
            print(triple)
#test()


# In[1]:


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
                for t in graph:
                    cnn_result.write(str(t)+'\n')
                    if t[1] != 'frdf:lu':
                        s_fe_count += 1
                        break
                    if 'frdf:lu' not in t[1]:
                        fe_count += 1
                    else:
                        f_count += 1
        except KeyboardInterrupt:
            raise
        except:
            pass
        cnn_result.write('\n')

    print(s_f_count, s_fe_count, f_count, fe_count)
        
cnn_test()


# In[16]:


# import preprocessor
# trn, tst, dev, exemplar = preprocessor.load_data()
# preprocessor.data_stat()

