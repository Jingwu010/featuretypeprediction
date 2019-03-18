import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import pytz
from keras.models import Model
from keras.layers import Dense, Embedding, Input, Flatten
from keras.layers import Conv1D, MaxPooling1D, GlobalMaxPool1D, Dropout, concatenate
from keras.preprocessing import text as keras_text, sequence as keras_seq
from keras.callbacks import EarlyStopping, ModelCheckpoint

from sklearn.metrics import accuracy_score, confusion_matrix
np.random.seed(512)
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn import preprocessing
from keras.layers import LeakyReLU
from keras import initializers
from keras.callbacks import ModelCheckpoint
from keras.callbacks import ReduceLROnPlateau
from keras.models import load_model
from keras.utils import to_categorical
import keras
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.model_selection import KFold,StratifiedKFold
from keras.models import load_model

# base = 'drive/My Drive/snow/downsteam_model/'
base = ''
data = pd.read_csv(base+'processed_raw_4.csv')
labels = np.loadtxt(base+'train_marginals_4.txt')

def abs_limit(x):
    if abs(x) > 10000:
        return 10000*np.sign(x)
    return x

data = data.fillna(0)
data['scaled_mean'] = data['mean'].apply(abs_limit)
data['scaled_min_val'] = data['min_val'].apply(abs_limit)
data['scaled_max_val'] = data['max_val'].apply(abs_limit)
data['scaled_std_dev'] = data['std_dev'].apply(abs_limit)

column_names_to_normalize = ['scaled_max_val', 'scaled_mean', 'scaled_min_val','scaled_std_dev']
x = data[column_names_to_normalize].values
x = np.nan_to_num(x)
x_scaled = StandardScaler().fit_transform(x)
df_temp = pd.DataFrame(x_scaled, columns=column_names_to_normalize, index = data.index)
data[column_names_to_normalize] = df_temp

data_train, data_test = train_test_split(data, test_size=0.2, random_state=100)

x_columns =  ['Attribute_name',
                  'sample_1',
                  'sample_2',
                  'sample_3',
                  'sample_4',
                  'sample_5',
                  'p_nans',
                  'p_dist_val',
                  'scaled_max_val', 
                  'scaled_mean', 
                  'scaled_min_val',
                  'scaled_std_dev',
                  'castability',
                  'extractability',
                  'len_val']

y_columns = ['0','1','2','3']

X_train = data_train[x_columns].values
X_test = data_test[x_columns].values
y_train = data_train[y_columns].values.astype(float)
y_test = data_test[y_columns].values.astype(float)
y_act = data_test['y_act'].values.astype(int)

sample_base = 'sample_'
# samples_train = []
# samples_test = []

i = 1
field_name = sample_base + str(i)
field_idx = x_columns.index(field_name)

samples1_train = X_train[:,field_idx].astype(str)
samples1_test = X_test[:,field_idx].astype(str)

field_name = 'Attribute_name'
atr_Xtrain = X_train[:,x_columns.index(field_name)].astype(str)
atr_Xtest = X_test[:,x_columns.index(field_name)].astype(str)

# define network parameters
max_features = 128
maxlen = 128

def generate_padded_tokens(train_list, test_list, maxlen=maxlen):
    tokenizer = keras_text.Tokenizer(char_level = True)
    tokenizer.fit_on_texts(train_list)
    tokenized_train = tokenizer.texts_to_sequences(train_list)
    pad_train = keras_seq.pad_sequences(tokenized_train, maxlen)

    tokenized_test = tokenizer.texts_to_sequences(test_list)
    pad_test = keras_seq.pad_sequences(tokenized_test, maxlen)
    return tokenizer, pad_train, pad_test

atr_tokenizer, atr_pad_train, atr_pad_test = generate_padded_tokens(atr_Xtrain, atr_Xtest)
sam_tokenizer, sam_pad_train, sam_pad_test = generate_padded_tokens(samples1_train, samples1_test)

X_train_left = X_train[:,6:]
X_test_left = X_test[:,6:]
X_train_left.shape, X_test_left.shape

X_t = atr_pad_train
X_t1 = sam_pad_train
structured_data_train = X_train_left
X_te = atr_pad_test
X_te1 = sam_pad_test
structured_data_test = X_test_left
X_t.shape, X_t1.shape, structured_data_train.shape

import datetime
timestamp = datetime.datetime.now(pytz.timezone("America/Los_Angeles")).strftime('%Y-%m-%d-%H')
output_base = base+str(timestamp)+'/'
import os
if not os.path.exists(output_base):
    os.makedirs(output_base)
with open(output_base+'log.txt', 'a') as fw:
    fw.write('============================================================\n')
    fw.write('training starts at: \t' + str(timestamp) + '\n')
    fw.write('============================================================\n')
    fw.flush()

# http://sujitpal.blogspot.com/2018/02/using-snorkel-probabilistic-labels-for.html

def build_model(numfilters, embed_size, num_classes, tokenizer1, tokenizer2, maxlen):
    # name space input
    seq_input = Input(shape=(maxlen,))
    x = Embedding(input_dim = len(tokenizer1.word_counts)+1, output_dim = embed_size)(seq_input)
    x = Dropout(0.25)(x)
    x = Conv1D(numfilters*2**(i), kernel_size = 3, activation = 'relu')(x)
    out_conv = [Dropout(0.5)(GlobalMaxPool1D()(x)), GlobalMaxPool1D()(x)]
    seq1 = concatenate(out_conv, axis = -1)  

    # sample space input
    seq_input2 = Input(shape=(maxlen, ))
    x = Embedding(input_dim = len(tokenizer2.word_counts)+1, output_dim = embed_size)(seq_input2)
    x = Dropout(0.25)(x)
    x = Conv1D(numfilters*2**(i), kernel_size = 3, activation = 'relu')(x)
    out_conv = [Dropout(0.5)(GlobalMaxPool1D()(x)), GlobalMaxPool1D()(x)]
    seq2 = concatenate(out_conv, axis = -1)

    # feature space input
    list_input = Input(shape=(9,))

    layersfin = keras.layers.concatenate([seq1, seq2, list_input])
    x = Dense(500, activation='relu')(layersfin)
    x = Dropout(0.25)(x)
    x = Dense(500, activation='relu')(x)
    x = Dropout(0.1)(x)
    
    preds = Dense(num_classes, activation='softmax')(x)
    model = Model(inputs=[seq_input,seq_input2,list_input], outputs=[preds])
    return model

def compile_model(model):
    model.compile(loss='categorical_crossentropy',optimizer='adam',metrics=['accuracy'])
    return model

def fit_model(model, best_model_file, Xtrain, Ytrain, epochs=20, verbose=1):
    checkpoint = ModelCheckpoint(filepath=best_model_file,
                                 monitor='val_acc', 
                                 verbose=verbose,
                                 save_best_only=True)

    early = EarlyStopping(monitor="val_acc", patience=20)
    callbacks_list = [checkpoint, early] #early            

    history = model.fit(Xtrain, Ytrain, 
                        validation_split=0.1, 
                        epochs=epochs, 
                        batch_size=64,
                        verbose=verbose,
                        callbacks=callbacks_list)
    return history
  
def eval_report(title, Ytest, Ytest_, prob, verbose=True):
    if prob:
        ytest = np.argmax(Ytest, axis=1)
    else:
        ytest = Ytest
    ytest_ = np.argmax(Ytest_, axis=1)
    acc = accuracy_score(ytest, ytest_)
    cm = confusion_matrix(ytest, ytest_)
    if verbose:
      print("\n*** {:s}".format(title.upper()))
      print("accuracy: {:.3f}".format(acc*100))
      print("confusion matrix")
      print(cm)
    return acc

X_t = atr_pad_train
X_t1 = sam_pad_train
structured_data_train = X_train_left
X_te = atr_pad_test
X_te1 = sam_pad_test
structured_data_test = X_test_left
X_t.shape, X_t1.shape, structured_data_train.shape

Xtrain = [X_t, X_t1, structured_data_train]
Xtest = [X_te, X_te1, structured_data_test]
Yptrain = y_train
Yptest = y_test
Yctest = y_act
X_t.shape, X_te.shape, Yptrain.shape, Yptest.shape, Yctest.shape

nes = [16, 32, 64, 128, 512]
mds = [16, 32, 64, 128]
epoches = [10, 20, 50, 100]

num_classes = Yptrain.shape[1]

scores = list()
with open(output_base+'log.txt', 'a') as fw:
  fw.write('[{:5s} {:5s} {:5s}]  -  {:6s}  -  {:6s}  -  {:6s}'.format('ne', 'md', 'epoch','train','test','real'))
  fw.write('\n')
  for i, ne in enumerate(nes):
    for j, md in enumerate(mds):
      for k, epoch in enumerate(epoches):
        model_p = build_model(ne, md, num_classes, atr_tokenizer, sam_tokenizer, maxlen)
        model_p = compile_model(model_p)

        BEST_MODEL_P = output_base+'best_weights='+\
                        '_ne'+str(ne)+\
                        '_md'+str(md)+\
                        '_ep'+str(epoch)+'.h5'
        fit_model(model_p, BEST_MODEL_P, Xtrain, Yptrain, epoch, verbose=0)
        best_model_p = load_model(BEST_MODEL_P)
        Yptest_ = best_model_p.predict(Xtest)
        score0 = eval_report("test. probabilistic VS pred. probabilistic", Yptest, Yptest_, prob=True, verbose=False)
        score1 = eval_report("test. categorical VS pred. probabilistic", Yctest, Yptest_, prob=False, verbose=False)
        score2 = eval_report("test. categorical VS test. probabilistic", Yctest, Yptest, prob=False, verbose=False)
        scores.append((ne, md, epoch, score0, score1, score2))
        print('[%5d %5d %5d]\t' % (ne, md, epoch), 'Disc. Model Acc.: ', round(score1*100,2))
        fw.write('[{:5d} {:5d} {:5d}]  -    {:.2f}  -    {:.2f}  -    {:.2f}'.format(ne, md, epoch,
                                                                               round(score0*100,2),
                                                                               round(score1*100,2),
                                                                               round(score2*100,2)))
        fw.write('\n')
        fw.flush()