
# coding: utf-8

# In[1]:


import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import torch.utils.data
from torch.nn.utils.rnn import pack_padded_sequence, pad_packed_sequence
from optparse import OptionParser
import torch.autograd as autograd
import os
import sys
import os
import pprint
import numpy as np
os.environ["CUDA_VISIBLE_DEVICES"]= "0"
os.environ['CUDA_LAUNCH_BLOCKING'] = "1"
import torch.backends.cudnn as cudnn
cudnn.benchmark = True
sys.path.insert(0,'../')
import preprocessor
import time
import datetime
import json
start_time = time.time()
torch.manual_seed(1)


# In[2]:


optpr = OptionParser()
optpr.add_option("--mode", dest='mode', type='choice', choices=['train', 'test', 'parsing'], default='test')

optpr.mode = 'train'


# In[3]:


print('GPU:', torch.cuda.get_device_name(0), ', # of gpu:('+str(torch.cuda.device_count())+')')
print('Torch Version:', torch.version.cuda)


# In[4]:


training_data, test_data, dev_data, exemplar_data = preprocessor.load_data()


# In[5]:


preprocessor.data_stat()


# In[6]:


configuration = {'token_dim': 60,
                 'hidden_dim': 64,
                 'pos_dim': 4,
                 'lu_dim': 64,
                 'lu_pos_dim': 5,
                 'lstm_input_dim': 64,
                 'lstm_dim': 64,
                 'lstm_depth': 2,
                 'hidden_dim': 64,
                 'num_epochs': 100,
                 'learning_rate': 0.001,
                 'using_GPU': True,
                 'batch_size': 64}
print('\n### CONFIGURATION ###\n')
pprint.pprint(configuration)


# In[7]:


today = datetime.date.today()
model_dir = './model/lstm-'+str(today)
if not os.path.exists(model_dir):
    os.makedirs(model_dir)
model_path = model_dir+'/model.pt'


# In[8]:


#Hyper-parameters
usingGPU = configuration['using_GPU']
TOKDIM= configuration['token_dim']
POSDIM = configuration['pos_dim']
LUDIM = configuration['lu_dim']
LPDIM = configuration['lu_pos_dim']
INPDIM = LUDIM + LPDIM
LSTMINPDIM = configuration['lstm_input_dim']
LSTMDIM = configuration['lstm_dim']
LSTMDEPTH = configuration['lstm_depth']
HIDDENDIM = configuration['hidden_dim']
NUM_EPOCHS = configuration['num_epochs']
learning_rate = configuration['learning_rate']
batch_size = configuration['batch_size']

# num_layers = 1
# num_epochs = 5
# num_samples = 1000     # number of words to be sampled
# batch_size = 20
# seq_length = 30
seq_length = 0
for i in training_data:
    new_len = len(i)
    if new_len > seq_length:
        seq_length = new_len


# Unseen word, <PAD> 에 대한 index 필요

# In[9]:


def prepare_index():
    word_to_ix = {}
    pos_to_ix = {}
    frame_to_ix = {}
    word_to_ix['UNSEEN'] = 0
    word_vocab, pos_vocab, frame_vocab = [],[],[]
    for tokens in training_data:
        for t in tokens:
            word = t[1]
            if word not in word_to_ix:
                word_to_ix[word] = len(word_to_ix)
                word_vocab.append(word)
            pos = t[4]
            if pos not in pos_to_ix:
                pos_to_ix[pos] = len(pos_to_ix)
                pos_vocab.append(pos)
            frame = t[13]
            if frame != '_':
                if frame not in frame_to_ix:
                    frame_to_ix[frame] = len(frame_to_ix)
                    frame_vocab.append(frame)
    return word_to_ix, pos_to_ix, frame_to_ix
word_to_ix, pos_to_ix, frame_to_ix = prepare_index()
print('\n###  word vocab size:', len(word_to_ix))
print('### frame vocab size:', len(frame_to_ix))


# In[10]:


def prepare_sentence(tokens):
    sentence, pos, frame = [],[],[]
    for token in tokens:
        w,p,f = token[1],token[4],token[13]
        sentence.append(w)
        pos.append(p)
        frame.append(f)
    return sentence, pos, frame


# In[11]:


def prepare_sequence(seq, to_ix):
    vocab = list(to_ix.keys())
    idxs = []
    for w in seq:
        if w in vocab:
            idxs.append(to_ix[w])
        else:
            idxs.append(0)            
#     idxs = [to_ix[w] for w in seq]
    if usingGPU:
        return torch.tensor(idxs).type(torch.cuda.LongTensor)
    else:
        return torch.tensor(idxs, dtype=torch.long)


# In[12]:


def prepare_frame_sequence(seq, to_ix):
    idxs = [to_ix[w] for w in seq if w != '_']
    idxs = list(set(idxs))
    if usingGPU:
        return torch.tensor(idxs).type(torch.cuda.LongTensor)
    else:
        return torch.tensor(idxs, dtype=torch.long)    


# In[13]:


# # def gen_sequence_data(data, bs=batch_size):
# #     print('\n### generate batch data ###')
# #     print('batch size:', bs)
# #     num_batches = len(data) // bs
# #     print('num batches:', num_batches)


# def gen_sequence_data(data, bs=batch_size):
#     print('\n### generate batch data ###')
#     print('batch size:', bs)
#     num_batches = len(data) // bs
#     print('num batches:', num_batches)
#     seq_data = []
#     for tokens in data:
#         sentence, pos, frame = prepare_sentence(tokens)
#         sentence_in = prepare_sequence(sentence, word_to_ix)
#         frames = prepare_frame_sequence(frame, frame_to_ix)
#         targetpositions = get_targetpositions(tokens)
#         seq_data.append( (sentence_in, frames, targetpositions) )
# #     return seq_data
#     seq_data = seq_data[:num_batches*bs]
    
#     n = 0
#     batch_data = []
#     sent_list, frame_list, targetpositions = [],[],[]
#     for (sent,frame,targetposition) in rev_data:
#         sent_list.append(sent)
#         frame_list.append(frame)
#         targetpositions.append(targetposition)
#         n += 1
#         if n % bs == 0:
#             intuple = ( sent_list, frame_list, targetposition )
#             batch_data.append(intuple)
#             sent_list, frame_list = [],[]
#     print(len(batch_data))
#     return batch_data


# d = gen_sequence_data(training_data)



# ## TODO 0803: batch data 다시만들기
# #batch 0 : 1개 튜플, 각 튜플에는 sentence tensor 64개, frame tensor 64개
# # 그리고 padding 까지 해서 --> 주말 돌림


# In[14]:


# seq_data = gen_sequence_data(training_data)
# n = 0
# for i in seq_data:
#     n += 1
#     if n >= 5:
#         print(i)
#         print('\n ###')
        
#     if n > 11:
#         break

# print(seq_data[0])


# batch_data = torch.utils.data.DataLoader(seq_data, batch_size=2)

# print('batch')
# n = 0
# for i in batch_data:
#     print(i)
#     n += 1
#     if n >= 11:
#         print(i)
#         break


# In[15]:


def prepare_frame_vector(seq, to_ix):
    if usingGPU:
        frame_vector =  torch.zeros(len(to_ix)).type(torch.cuda.LongTensor)
#         frame_vector[0][fid] = 1
    else:
        frame_vector =  torch.zeros(len(to_ix), dtype=torch.long)
#         frame_vector[0][fid] = 1
    for f in seq:
        if f != '_':
            fid = frame_to_ix[f]
            frame_vector[fid] = 1
    return frame_vector

# _, _, seq = prepare_sentence(training_data[50])
# d = prepare_frame_vector(seq, frame_to_ix)
# print(d)


# In[16]:


def get_targetpositions(tokens):
    positions = []
    for i in tokens:
        if i[12] != '_':
            positions.append(int(i[0]))
    positions = np.asarray(positions)
    positions = torch.from_numpy(positions)
    if usingGPU:
        return positions.type(torch.cuda.LongTensor)
    else:
        return positions


# In[17]:


def get_target_span(sentence, targetpositions):
    start, end = int(targetpositions[0]), int(targetpositions[-1])
    span = {}
    if start == 0: span['start'] = 0
    else: span['start'] = start -1
    if end == len(sentence): span['end'] = end+1
    else: span['end'] = end+2
    return span


# In[18]:


class LSTMTagger(nn.Module):
    
    def __init__(self, vocab_size, tagset_size):
        super(LSTMTagger, self).__init__()
        self.word_embeddings = nn.Embedding(vocab_size, TOKDIM)
        
        # 1st LSTM network (bi-LSTM)
        self.lstm_1 = nn.LSTM(TOKDIM, HIDDENDIM//2, bidirectional=True)
        self.hidden_lstm_1 = self.init_hidden_lstm_1()
        
        # 2nd LSTM network (LSTM)
        self.hidden_lstm_2 = self.init_hidden_lstm_2()
        self.lstm_2 = nn.LSTM(HIDDENDIM, HIDDENDIM)
        
        self.target2hidden = nn.Linear(HIDDENDIM, HIDDENDIM)
        self.hidden2tag = nn.Linear(HIDDENDIM, tagset_size) 
    
    def init_hidden(self):
        if usingGPU:
            return (torch.zeros(1, 1, HIDDENDIM).cuda(),
                torch.zeros(1, 1, HIDDENDIM).cuda())
        else:
            return (torch.zeros(1, 1, HIDDENDIM),
                torch.zeros(1, 1, HIDDENDIM))
    
    def init_hidden_lstm_1(self):
        if usingGPU:
            return (torch.zeros(2, 1, HIDDENDIM//2).cuda(),
                torch.zeros(2, 1, HIDDENDIM//2).cuda())
        else:
            return (torch.zeros(2, 1, HIDDENDIM//2),
                torch.zeros(2, 1, HIDDENDIM//2))
        
    def init_hidden_lstm_2(self):
        if usingGPU:
            return (torch.zeros(1, 1, HIDDENDIM).cuda(),
                torch.zeros(1, 1, HIDDENDIM).cuda())
        else:
            return (torch.zeros(1, 1, HIDDENDIM),
                torch.zeros(1, 1, HIDDENDIM))
        
    def forward(self, sentence, targetpositions):
#         if usingGPU: 
#             sentence.cuda()
#         else: 
#             pass

        embeds = self.word_embeddings(sentence)
        embeds = embeds.view(len(sentence), 1, -1)
        
        self.lstm_1.flatten_parameters()        
        lstm_out_1, self.hidden_lstm_1 = self.lstm_1(
            embeds, self.hidden_lstm_1)

        span = get_target_span(sentence, targetpositions)  

        target_lstm = lstm_out_1[span['start']:span['end']]
        

        self.lstm_2.flatten_parameters()    
        lstm_out_2, self.hidden = self.lstm_2(
            target_lstm, self.hidden_lstm_2)        

        target_vec = lstm_out_2[-1]

        tag_space = self.target2hidden(target_vec)        
        tag_space = F.relu(tag_space)
        tag_space = self.hidden2tag(tag_space)
#         tag_space = F.softmax(tag_space)
#         tag_space = autograd.Variable(tag_space, requires_grad=True)
        tag_scores = F.log_softmax(tag_space, dim=1)

        return tag_scores


# In[19]:


def get_frame_by_tensor(t):
    value, indices = t.max(1)
    score = pow(10, value)
    
    pred = None
    for frame, idx in frame_to_ix.items():
        if idx == indices:
            pred = frame
            break
    return score, pred


# In[20]:


def eval_dev(model):
    acc = 0
    for sent in dev_data:
        for t in sent:
            if t[13] != '_':
                gold = t[13]
        sentence, pos, frame = prepare_sentence(sent)
        targetpositions = get_targetpositions(sent)
        inputs = prepare_sequence(sentence, word_to_ix)
        tag_scores = model(inputs,targetpositions)
        score, pred = get_frame_by_tensor(tag_scores)
        if gold == pred:
            acc += 1
        else:
            pass
    accuracy = acc / len(dev_data)
    return accuracy


# In[22]:


# training_data = training_data[:100]
# total_step = len(training_data)
# NUM_EPOCHS = 3
# EMBEDDING_DIM = 6
# HIDDEN_DIM = 6

# seq_data = gen_sequence_data(training_data)
# batch_data = torch.utils.data.DataLoader(seq_data, batch_size=batch_size)
# total_step = len(batch_data)
# for epoch in range(NUM_EPOCHS):
#     for step, (sent, frame, targetposition) in enumerate(batch_data):
#         model.zero_grad()
#         model.hidden_lstm_1 = model.init_hidden_lstm_1()
#         model.hidden_lstm_2 = model.init_hidden_lstm_2()
        
#         tag_scores = model(sent, targetposition)
#         loss = loss_function(tag_scores, frames)
#         loss.backward()
#         optimizer.step()     

#         if n % 10 == 0:
#             print('Epoch [{}/{}], Step [{}/{}], Loss: {:.4f}' 
#                    .format(epoch+1, NUM_EPOCHS, step, total_step, loss.item()))
#         break

model = False
optpr.mode = 'train'
if optpr.mode == 'train':
    model = LSTMTagger(len(word_to_ix), len(frame_to_ix))
    if usingGPU:
        model.cuda()
    else:
        pass
    loss_function = nn.NLLLoss()
#     loss_function = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)
    total_step = len(training_data)
    dev_eval = []
    for epoch in range(NUM_EPOCHS):
        n = 0
        for tokens in training_data:
            model.zero_grad()
            model.hidden_lstm_1 = model.init_hidden_lstm_1()
            model.hidden_lstm_2 = model.init_hidden_lstm_2()

            sentence, pos, frame = prepare_sentence(tokens)
            targetpositions = get_targetpositions(tokens)
            sentence_in = prepare_sequence(sentence, word_to_ix)
            frames = prepare_frame_sequence(frame, frame_to_ix)
    #         frames = prepare_frame_vector(frame, frame_to_ix)
            tag_scores = model(sentence_in, targetpositions)
            loss = loss_function(tag_scores, frames)
            loss.backward()
            optimizer.step()        
            n = n+1

            if n % 100 == 0:
                print('Epoch [{}/{}], Step [{}/{}], Loss: {:.4f}' 
                       .format(epoch+1, NUM_EPOCHS, n, total_step, loss.item()))
            
        accuracy = eval_dev(model)
        print('Epoch [{}/{}], Accuracy: {:4f}' 
                       .format(epoch+1, NUM_EPOCHS, accuracy))
        dev_eval.append((str(epoch+1), str(accuracy)))
    #         break

    torch.save(model, model_path)  

    print('your model is saved:', model_path)
    print('time spent:', time.time()-start_time)
    with open(model_dir+'/configure.json','w') as f:
        json.dump(configuration, f, ensure_ascii=False, indent=4)
    eval_dev_epoch = open(model_dir+'/eval_dev_epoch.tsv', 'w')
    for i in dev_eval:
        eval_dev_epoch.write(i[0]+'\t'+i[1]+'\n')
    eval_dev_epoch.close()


# In[ ]:


if optpr.mode == 'test' or model != False:
    model = torch.load(model_path)
    acc = 0
    for sent in test_data:
        for t in sent:
            if t[13] != '_':
                gold = t[13]
        sentence, pos, frame = prepare_sentence(sent)
        targetpositions = get_targetpositions(sent)
        inputs = prepare_sequence(sentence, word_to_ix)
        tag_scores = model(inputs,targetpositions)
        score, pred = get_frame_by_tensor(tag_scores)
        if gold == pred:
            acc += 1
        else:
            pass
    accuracy = acc / len(test_data)
    with open(model_dir+'/result','w') as f:
        line = 'accuracy: '+str(accuracy)
        f.write(line)
    print('accuracy over TEST:', accuracy)

