
# coding: utf-8

# In[2]:

import json
import etri
import sys
from datetime import datetime
import time
from koreanframenet import kfn
from optparse import OptionParser


# In[3]:

import targetid
import frameid


# In[4]:

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
optpr.argid = 'baseline'

#print options
#sys.stderr.write("\nCOMMAND: "+' '.join(sys.argv) + '\n')
sys.stderr.write("\nPARSER SETTINGS\n_____________________\n")
sys.stderr.write("Target Identification     \t" + str(optpr.targetid) + '\n')
sys.stderr.write("Frame Identification      \t" + str(optpr.frameid) + '\n')
sys.stderr.write("Argument Identification   \t" + str(optpr.argid) + '\n')
if optpr.mode in ['parsing']:
    sys.stderr.write("RESULT WILL BE SAVED TO\t%s\n" %resultfname)


# In[5]:

# parset options

target_identifier = targetid.target_identifier
frame_identifier = frameid.frame_identifier


# In[12]:

def frameparsing(sent):
    conll = etri.getETRI_CoNLL2009(sent)
    conll_target = target_identifier(conll, optpr.targetid)
    #print(conll_target[0])
    conll_frame = frame_identifier(conll_target, optpr.frameid)
    
    return conll_frame


# In[14]:

# parsing

def test():
    if optpr.mode == 'parsing':
        sent = optpr.input = '나는 밥을 먹고 학교에 갔다'
        frameparsing(sent)
test()

