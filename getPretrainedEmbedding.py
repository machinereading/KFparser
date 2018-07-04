
# coding: utf-8

# In[1]:

import gensim
import preprocessor


# In[15]:

fasttext_folder = '/disk_4/fasttext'
fasttext_bin = '/wiki.ko.bin'
fasttext_txt = '/wiki.ko.vec'


# In[2]:

def load_data():
    training, test, training_fe = preprocessor.load_data()
    #result = training + test
    result = training + test
    return result

koreanFN = load_data()


# In[16]:

from gensim.models.wrappers import FastText
def load_fasttext():
    print('loading fasttext...')
    model = FastText.load_fasttext_format(fasttext_folder+fasttext_bin)
    print('fasttext is loaded')
    return model
#fasttext = load_fasttext()


# In[23]:

def get_vector_string(word):
    wv = fasttext[word]
    wv = wv.tolist()
    wv = [str(i) for i in wv]
    wv_string = ' '.join(wv)
    return wv_string


# In[18]:

def get_frame_voca():
    voca = []
    for sent_list in koreanFN:
        #print(sent_list)
        for token in sent_list:
            #print(token)
            tok = token[1]
            #print(tok)
            voca.append(tok)
        #voca.update(tok)
        #print(voca)
        #break
    voca = list(set(voca))
    print('KFN vocabulary size:', len(voca))
    return voca
    
koframevocab = get_frame_voca()


# In[32]:

def gen_wv_by_fasttext_lib():
    print('gen_wv_by_fasttext_lib')
    file_name = 'fasttext.bylib.koframevocab.txt'
    filtered_wvf = open(fasttext_folder+'/'+file_name, 'w')
    numwv = 0
    for w in koframevocab:
        wv = get_vector_string(w)
        line = w+' '+wv+'\n'
        filtered_wvf.write(line)
        numwv += 1
    filtered_wvf.close()
    print('total num word vectors in file +'+file_name+'='+str(numwv))
#gen_wv_by_fasttext_lib()


# In[37]:

def gen_wv_by_fasttext_txt():
    print('gen_wv_by_fasttext_txt')
    file_name = 'fasttext.bytxt.koframevocab.txt'
    wvf = open(fasttext_folder+fasttext_txt)
    filtered_wvf = open(fasttext_folder+'/'+file_name, 'w')
    numwv = 0
    for l in wvf:
        fields = l.strip().split(' ')
        wd = fields[0]
        if wd in koframevocab:
            filtered_wvf.write(l)
            numwv += 1
    wvf.close()
    filtered_wvf.close()
    print('total num word vectors in file +'+file_name+'='+str(numwv))   
gen_wv_by_fasttext_txt()

