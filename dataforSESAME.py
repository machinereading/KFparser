
# coding: utf-8

# In[ ]:


import json

train_file = './koreanframenet/data/training.tsv'
test_file = './koreanframenet/data/test.tsv'
dev_file = './koreanframenet/data/dev.tsv'
file_list = [train_file, test_file, dev_file]
target_dir = './data/opensesame/'

def get_data(lines, file_name):
    file_type = file_name.split('/')[-1]
    print(file_type)
    result = []
    sent = []
    exemplar_sent_num = 0
    train_sent_num = 0
    test_sent_num = 0
    dev_sent_num = 0
    for line in lines:
        d = {}
        #line = line.rstip('\n')
        if line.startswith('#'):
            if line[1] == 's':
                if 'sejong' in line:
                    sent_type = 'exemplar'
                else:
                    if 'train' in file_type:
                        sent_type = 'train'
                    elif 'test' in file_type:
                        sent_type = 'test'
                    elif 'dev' in file_type:
                        sent_type = 'dev'
                    else:
                        pass
            else:
                sents = line[6:]
        else:
            if sent_type == 'exemplar':
                if line != '\n':           
                    line_list = line.split('\t')
                    line_list[6] = str(exemplar_sent_num)
                    line_text = '\t'.join(line_list)
                    sent.append(line_text)
                else:
                    d['sent_type'] = sent_type
                    d['sents'] = sents
                    d['conll'] = sent
                    result.append(d)
                    sent = []
                    exemplar_sent_num += 1
            elif sent_type == 'train':
                if line != '\n':           
                    line_list = line.split('\t')
                    line_list[6] = str(train_sent_num)
                    line_text = '\t'.join(line_list)
                    sent.append(line_text)
                else:
                    d['sent_type'] = sent_type
                    d['sents'] = sents
                    d['conll'] = sent
                    result.append(d)
                    sent = []
                    train_sent_num += 1
            elif sent_type == 'test':
                if line != '\n':           
                    line_list = line.split('\t')
                    line_list[6] = str(test_sent_num)
                    line_text = '\t'.join(line_list)
                    sent.append(line_text)
                else:
                    d['sent_type'] = sent_type
                    d['sents'] = sents
                    d['conll'] = sent
                    result.append(d)
                    sent = []
                    test_sent_num += 1
            elif sent_type == 'dev':
                if line != '\n':           
                    line_list = line.split('\t')
                    line_list[6] = str(dev_sent_num)
                    line_text = '\t'.join(line_list)
                    sent.append(line_text)
                else:
                    d['sent_type'] = sent_type
                    d['sents'] = sents
                    d['conll'] = sent
                    result.append(d)
                    sent = []
                    test_sent_num += 1
            else:
                pass
                
    print(len(result))
    return result
                
        
    

def gen_data(file_name):
    print('working for', file_name)
    with open(file_name, 'r') as f:
        lines = f.readlines()
    data = get_data(lines, file_name)    
    
    if 'training' in file_name:
        train_file = target_dir+'kofn1.7.fulltext.train.syntaxnet.conll'
        train_sents_file = target_dir+'kofn1.7.fulltext.train.syntaxnet.conll.sents'
        train = open(train_file, 'w')
        train_sents = open(train_sents_file, 'w')
        examplar_file = target_dir+'kofn1.7.exemplar.train.syntaxnet.conll'
        examplar_sents_file = target_dir+'kofn1.7.exemplar.train.syntaxnet.conll.sents'
        examplar = open(examplar_file, 'w')
        examplar_sents = open(examplar_sents_file, 'w')
    else:
        dev_file = target_dir+'kofn1.7.dev.syntaxnet.conll'
        dev_sents_file = target_dir+'kofn1.7.dev.syntaxnet.conll.sents'
        dev = open(dev_file, 'w')
        dev_sents = open(dev_sents_file, 'w')   
        test_file = target_dir+'kofn1.7.test.syntaxnet.conll'
        test_sents_file = target_dir+'kofn1.7.test.syntaxnet.conll.sents'
        test = open(test_file, 'w')
        test_sents = open(test_sents_file, 'w')
    
        
    
    
    
    
    for i in data:
        if i['sent_type'] == 'train':
            train_sents.write(i['sents'])
            for line in i['conll']:
                train.write(line)
            train.write('\n')
        elif i['sent_type'] == 'exemplar':
            examplar_sents.write(i['sents'])
            for line in i['conll']:
                examplar.write(line)
            examplar.write('\n')
        elif i['sent_type'] == 'test':
            test_sents.write(i['sents'])
            for line in i['conll']:
                test.write(line)
            test.write('\n')
        elif i['sent_type'] == 'dev':
            dev_sents.write(i['sents'])
            for line in i['conll']:
                dev.write(line)
            dev.write('\n')
    #dev.close()
    #dev_sents.close()
    #train.close()
    #train_sents.close()
    #test.close()
    #test_sents.close()
    #examplar.close()
    #examplar_sents.close()
            


# In[ ]:


for i in file_list:
    gen_data(i)

