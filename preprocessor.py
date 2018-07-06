
# coding: utf-8

# In[31]:

import json

def load_tsv(lines):
    result = []
    sent = []
    sent_ids = []
    for line in lines:
        line = line.rstrip('\n')
        if line.startswith('#'):
            if line[1] == 's':
                sent_id = line.split(':')[1]
                sent_ids.append(sent_id)                
            pass
        else:
            if line != '':
                token = line.split('\t')
                sent.append(token)
            else:
                result.append(sent)
                sent = []
    sent_num = len(list(set(sent_ids)))
    return result, sent_num

def load_data():
    print('### loading data now...')
    with open('./koreanframenet/data/training.tsv','r') as f:
        d = f.readlines()
        training, n_training = load_tsv(d)
        #print(len(training_fe))
    with open('./koreanframenet/data/test.tsv','r') as f:
        d = f.readlines()
        test, n_test = load_tsv(d)
        #print(len(test))
    with open('./koreanframenet/data/dev.tsv','r') as f:
        d = f.readlines()
        dev, n_dev = load_tsv(d)
        #print(len(training))
    with open('./koreanframenet/data/exemplar.tsv','r') as f:
        d = f.readlines()
        exemplar, n_exemplar = load_tsv(d)
        
    print('# training_data')
    print(' - number of full-sentences:', n_training)
    print(' - number of sentences:', len(training), '\n')
    
    print('# test_data')
    print(' - number of full-sentences:', n_test)
    print(' - number of sentences:', len(test), '\n')
    
    print('# dev_data')
    print(' - number of full-sentences:', n_dev)
    print(' - number of sentences:', len(dev), '\n')
    
    print('# exemplar data (from sejong)')
    print(' - number of full-sentences:', n_exemplar)
    print(' - number of sentences:', len(exemplar), '\n')
    
    return training, test, dev, exemplar
              
#training, test, training_fe = load_data()   


# In[ ]:



