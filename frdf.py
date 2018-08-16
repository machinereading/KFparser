
# coding: utf-8

# In[43]:


import json
from src import etri
import sys
from datetime import datetime
import time
from koreanframenet import kfn
from optparse import OptionParser
import configparser


# In[44]:


import targetid
import frameid
import argid
import graphGeneration


# In[27]:


# option
targetid_model = 'baseline'
frameid_model = 'frequent'
argid_model = 'rulebased'

# config
#config_file = '/home/iterative/summarization/summary.ini'
config_file = '/disk_4/KFparser/test_summary.ini'
config = configparser.ConfigParser()
config.read(config_file)
input_path = config.get('FRDF', 'FRDF_input_path')
output_path = config.get('FRDF', 'FRDF_output_path')

#print options
sys.stderr.write("\nPARSER SETTINGS\n_____________________\n")
sys.stderr.write("Target Identification     \t" + str(targetid_model) + '\n')
sys.stderr.write("Frame Identification      \t" + str(frameid_model) + '\n')
sys.stderr.write("Argument Identification   \t" + str(argid_model) + '\n')
sys.stderr.write("\nINPUT FILE IS           \t" + str(input_path))
sys.stderr.write("\nRESULT WILL BE SAVED TO  \t" + str(output_path))


# In[45]:


# parset options
target_identifier = targetid.target_identifier
frame_identifier = frameid.frame_identifier
arg_identifier = argid.arg_identifier

def frameparsing(sent):
    conll = etri.getETRI_CoNLL2009(sent)
    conll_target = target_identifier(conll, targetid_model)
    conll_frame = frame_identifier(conll_target, frameid_model)
    conll_arg = arg_identifier(conll_frame, argid_model)
    
    return conll_arg


# In[40]:


def load_data():
    data = []
    f =  open(input_path)
    lines = f.readlines()
    for line in lines:
        line = line.rstrip().split('\t')
        d = {}
        d['text'], d['docid'], d['pid'], d['sid'] = line[0], line[1], line[2], line[3]
        data.append(d)
    f.close()
    return data


# In[116]:


def getBIO_list(sent_list):
    result = []
    fe_list = []
    for i in range(len(sent_list)):
        fe = sent_list[i][14].lower()
        fe_list.append(fe)
    for i in range(len(sent_list)):
        fe = sent_list[i][14].lower()
        if i == 0:
            if fe == '_' or fe =='o':
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
            if fe == '_' or fe =='o':
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

def get_span(sent_list):
    sent_list = getBIO_list(sent_list)
    begin = False
    result = []
    for i in range(len(sent_list)):
        token = sent_list[i]
        fe = False
        if token[14] != 'O':
            fe = token[14].split('_')[1]
        next_fe = False
        if i+1 < len(sent_list):
            if sent_list[i+1][14].startswith('I'):
                next_fe = True
        if token[14].startswith('S'):
            d = {}
            d['begin'], d['end'], d['tag'] = token[0], token[0], fe, 
            result.append(d)
        else:
            if token[14].startswith('B'):
                begin = token[0]
            elif token[14].startswith('I'):
                end = token[0]
                if next_fe:
                    pass
                else:
                    d = {}
                    d['begin'], d['end'], d['tag'] = begin, end, fe, 
                    result.append(d)
    frame, begin, end = False, False, False
    for token in sent_list:
        if token[13] != '_':
            frame = token[13]
            if begin == False:
                begin = token[0]
                end = token[0]
            else:
                end = token[0]
    if frame:
        d = {}
        d['begin'], d['end'], d['tag']= begin, end, 'frame:'+frame
        result.append(d)
    return result   


# In[120]:


def gen_annotation(parsed):
    result = []
    for sent_list in parsed:
        anno = get_span(sent_list)
        tokens = []
        for token in sent_list:
            tokens.append(token[1])
        for a in anno:
            begin,end, tag = a['begin'], a['end'], a['tag']
            
            for i in range(len(tokens)):
                if i == begin:
                    tokens[i] = '['+tokens[i]
                if i == end:
                    tokens[i] = tokens[i]+']/'+tag
        annotation = ' '.join(tokens)
        result.append(annotation)
    return result
input_data = load_data()


# In[125]:


def parsing():
    result = []
    for i in input_data:
        parsed = frameparsing(i['text'])
        annos = gen_annotation(parsed)
        for anno in annos:
            annotation = anno + '\t' +  i['docid'] + '\t' + i['pid'] + '\t' + i['sid']
            result.append(annotation)
    return result

def write_result(result):
    time_spent = time.time()-start_time
    sys.stderr.write("\nRESULT\n_____________________\n")
    sys.stderr.write("PROCESSED SENTENCES     \t" + str(len(input_data)) + ' sentences\n')
    sys.stderr.write("PROCESSING TIME         \t" + str(round(time_spent, 2)) + '\n')
    sys.stderr.write("ANNOTATIONS             \t" + str(len(result)) + ' annotations\n')
    with open(output_path, 'w') as f:
        for i in result:
            f.write(i+'\n')

start_time = time.time()
result = parsing()
write_result(result)

