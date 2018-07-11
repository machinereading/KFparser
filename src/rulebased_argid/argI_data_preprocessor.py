import json
import re

def load_tsv(lines):
    result = []
    sent = []
    sent_ids = []
    dic = {}
    for line in lines:
        line = line.rstrip('\n')
		line = re.sub("\ufeff", "", line)
        if line.startswith('#'):
            if line[1] == 's':
                dic = {}
                sent_id = line.split(':')[1]
                sent_ids.append(sent_id)
                dic['sentid'] = sent_id                
            else:
                text = line.split(':')[1]
                dic['text'] = text
        else:
            if line != '':
                token = line.split('\t')
                sent.append(token)
            else:
                dic['tokens'] = sent
                result.append(dic)
                sent = []
    sent_num = len(list(set(sent_ids)))
    return result, sent_num

def load_data(file_name):
    print('### loading data now...')
    with open(file_name,'r',encoding='utf-8') as f:
        d = f.readlines()
        result, n_result = load_tsv(d)
        
    print('# data')
    print(' - number of full-sentences:', n_result)
    print(' - number of sentences:', len(result), '\n')
    
    
    return result




