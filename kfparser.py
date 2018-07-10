
# coding: utf-8

# In[1]:

import json
import etri
import sys
from datetime import datetime
import time
from koreanframenet import kfn
from optparse import OptionParser


# In[32]:

import targetid
import frameid
import argid
import graphGeneration


# In[3]:

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


# In[30]:

def frameparsing(sent):
    conll = etri.getETRI_CoNLL2009(sent)
    conll_target = target_identifier(conll, optpr.targetid)
    conll_frame = frame_identifier(conll_target, optpr.frameid)
    conll_arg = arg_identifier(conll_frame, optpr.argid)
    
    return conll_arg


# In[33]:

# parsing

def test():
    if optpr.mode == 'parsing':
        sent = optpr.input = "기계 학습(機械學習) 또는 머신 러닝(영어: machine learning)은 인공 지능의 한 분야로, 기계가 정보를 학습하도록 하는 알고리즘과 기술을 개발하는 분야를 말한다."
        parsed = frameparsing(sent)
        graph = graphGeneration.conll2graph(parsed)
        for triple in graph:
            print(triple)
test()


# In[ ]:



