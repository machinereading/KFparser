
# coding: utf-8

# In[31]:

import json
import os

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

def data_stat():
    dir_path = os.path.dirname(os.path.abspath(__file__))
    with open('./training.tsv','r') as f:
        d = f.readlines()
        training, n_training = load_tsv(d)
        #print(len(training_fe))

        
    print('# training_data')
    print(' - number of sentences:', n_training)
    print(' - number of annotations:', len(training), '\n')


def load_data():
    dir_path = os.path.dirname(os.path.abspath(__file__))
    print('### loading data now...')
    with open('./training.tsv','r') as f:
        d = f.readlines()
        training, n_training = load_tsv(d)
        #print(len(training_fe))

        
#     print('# training_data')
#     print(' - number of sentences:', n_training)
#     print(' - number of annotations:', len(training), '\n')
    
#     print('# test_data')
#     print(' - number of sentences:', n_test)
#     print(' - number of annotations:', len(test), '\n')
    
#     print('# dev_data')
#     print(' - number of sentences:', n_dev)
#     print(' - number of annotations:', len(dev), '\n')
    
#     print('# exemplar data (from sejong)')
#     print(' - number of sentences:', n_exemplar)
#     print(' - number of annotations:', len(exemplar), '\n')
    
    return training
              
#training, test, training_fe = load_data()   


# In[ ]:



