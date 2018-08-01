
# coding: utf-8

# In[1]:


import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import os
import sys
import os
import pprint
os.environ["CUDA_VISIBLE_DEVICES"]= "0"
os.environ['CUDA_LAUNCH_BLOCKING'] = "1"
import torch.backends.cudnn as cudnn
cudnn.benchmark = True

sys.path.insert(0,'../')
import preprocessor

import time
start_time = time.time()

torch.manual_seed(1)


# In[2]:


print('GPU:', torch.cuda.get_device_name(0), ', # of gpu:('+str(torch.cuda.device_count())+')')
print('Torch Version:', torch.version.cuda)


# In[3]:


training_data, test_data, dev_data, exemplar_data = preprocessor.load_data()


# In[4]:


preprocessor.data_stat()


# In[5]:


configuration = {'token_dim': 60,
                 'hidden_dim': 64,
                 'pos_dim': 4,
                 'lu_dim': 64,
                 'lu_pos_dim': 5,
                 'lstm_input_dim': 64,
                 'lstm_dim': 64,
                 'lstm_depth': 2,
                 'hidden_dim': 64,
                 'num_epochs': 25,
                 'learning_rate': 0.0005,
                 'using_GPU': True}
print('\n### CONFIGURATION ###\n')
pprint.pprint(configuration)


# In[6]:


model_path = './model/lstm180731'


# In[7]:


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
# TOKDIM = 6
# HIDDENDIM =6
NUM_EPOCHS = configuration['num_epochs']
learning_rate = configuration['learning_rate']

# num_layers = 1
# num_epochs = 5
# num_samples = 1000     # number of words to be sampled
# batch_size = 20
# seq_length = 30


# In[8]:


def prepare_index():
    word_to_ix = {}
    pos_to_ix = {}
    frame_to_ix = {}
    for tokens in training_data:
        for t in tokens:
            word = t[1]
            if word not in word_to_ix:
                word_to_ix[word] = len(word_to_ix)            
#             pos = t[4]
#             if pos not in pos_to_ix:
#                 pos_to_ix[pos] = len(pos_to_ix)
            frame = t[13]
            if frame != '_':
                if frame not in frame_to_ix:
                    frame_to_ix[frame] = len(frame_to_ix)
    return word_to_ix, frame_to_ix
word_to_ix, frame_to_ix = prepare_index()
print('###  word vocab size:', len(word_to_ix))
print('### frame vocab size:', len(frame_to_ix))


# In[9]:


def prepare_sequence(seq, to_ix):
    idxs = [to_ix[w] for w in seq]
    if usingGPU:
        return torch.tensor(idxs).type(torch.cuda.LongTensor)
    else:
        return torch.tensor(idxs, dtype=torch.long)


# In[10]:


def prepare_frame_sequence(seq, to_ix):
    idxs = [to_ix[w] for w in seq if w != '_']
    idxs = list(set(idxs))
    if usingGPU:
        return torch.tensor(idxs).type(torch.cuda.LongTensor)
    else:
        return torch.tensor(idxs, dtype=torch.long)


# In[11]:


def prepare_sentence(tokens):
    sentence = []
    pos = []
    frame = []
    for token in tokens:
        w = token[1]
        p = token[4]
        f = token[13]
        sentence.append(w)
        pos.append(p)
        frame.append(f)
    return sentence, pos, frame


# In[12]:


def get_targetpositions(tokens):
    positions = []
    for i in tokens:
        if i[12] != '_':
            positions.append(int(i[0]))
    return positions


# In[13]:


def get_target_span(sentence, targetpositions):
    start, end = targetpositions[0], targetpositions[-1]
    span = {}
    if start == 0: span['start'] = 0
    else: span['start'] = start -1
    if end == len(sentence): span['end'] = end+1
    else: span['end'] = end+2
    return span


# In[14]:


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
        return (torch.zeros(1, 1, HIDDENDIM),
                torch.zeros(1, 1, HIDDENDIM))
    
    def init_hidden_lstm_1(self):
        return (torch.zeros(2, 1, HIDDENDIM//2),
                torch.zeros(2, 1, HIDDENDIM//2))
        
    def init_hidden_lstm_2(self):
        return (torch.zeros(1, 1, HIDDENDIM),
                torch.zeros(1, 1, HIDDENDIM))


    def forward(self, sentence, targetpositions):
        embeds = self.word_embeddings(sentence)
        if usingGPU:
            embeds = embeds.view(len(sentence), 1, -1)
        else:
            embeds = embeds.view(len(sentence), 1, -1).cuda()
        lstm_out_1, self.hidden_lstm_1 = self.lstm_1(
            embeds, self.hidden_lstm_1)

        span = get_target_span(sentence, targetpositions)  
        target_lstm = lstm_out_1[span['start']:span['end']]
        
        lstm_out_2, self.hidden = self.lstm_2(
            target_lstm, self.hidden_lstm_2)
        
        target_vec = lstm_out_2[-1]

        tag_space = self.target2hidden(target_vec)
        tag_space = F.relu(tag_space)
        tag_space = self.hidden2tag(tag_space)

        tag_scores = F.log_softmax(tag_space, dim=1)
        return tag_scores


# In[15]:


model = LSTMTagger(len(word_to_ix), len(frame_to_ix))
if usingGPU:
    model.cuda()
else:
    pass

loss_function = nn.NLLLoss()
optimizer = optim.SGD(model.parameters(), lr=learning_rate)

total_step = len(training_data)
for epoch in range(NUM_EPOCHS):
    n = 0
    for tokens in training_data:
        sentence, pos, frame = prepare_sentence(tokens)
        targetpositions = get_targetpositions(tokens)
        model.zero_grad()
        model.hidden = model.init_hidden()
        sentence_in = prepare_sequence(sentence, word_to_ix)
        frames = prepare_frame_sequence(frame, frame_to_ix)
        tag_scores = model(sentence_in, targetpositions)
        loss = loss_function(tag_scores, frames)
        loss.backward(retain_graph=True)
        optimizer.step()
        
        n = n+1
        if n % 10 == 0:
            print('Epoch [{}/{}], Step [{}/{}], Loss: {:.4f}' 
                   .format(epoch+1, NUM_EPOCHS, n, total_step, loss.item()))
            
torch.save(model, model_path)
        
with torch.no_grad():
    sentence, pos, frame = prepare_sentence(training_data[0])
    targetpositions = get_targetpositions(training_data[0])
    inputs = prepare_sequence(sentence, word_to_ix)
    tag_scores = model(inputs,targetpositions)
    print('after')
    print(tag_scores)
    print('\n')
    
print('your model is saved:', model_path)
print('time spent:', time.time()-start_time)

