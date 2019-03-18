import numpy as np
import pandas as pd

categories = {'Usable Directly Categorical':    1, 
              'Usable Directly Numeric':        2, 
              'Usable With Extraction':         3, 
              'Unusable':                       4, 
              'Context_Specific':               5, 
              'None':                           0
              }

categories_size = {'Context_Specific':              2050,
                   'Unusable':                      891,
                   'Usable Directly Categorical':   2087,
                   'Usable Directly Numeric':       5063,
                   'Usable With Extraction':        650
                   }
                   
def label_mapper(row):
    x = row['y_act']
    try:
        if 'categorical' in x.lower():
            return 'Usable Directly Categorical'
        if 'numeric' in x.lower():
            return 'Usable Directly Numeric'
        if 'extra' in x.lower():
            return 'Usable With Extraction'
        if 'unusable' in x.lower():
            return 'Unusable'
        if 'context' in x.lower():
            return 'Context_Specific'
    except:
        print(x)
        return 'NaN'

def find_key_word(key, df, attribute='Attribute_name'):
    occurrence = [0] * len(categories)
    for index, row in df.iterrows():
        if key in str(row[attribute]).lower():
            occurrence[categories[row['y_act']]] += 1
    return occurrence

def get_samples(row):
    nSamples = 5
    base = 'sample_'
    return [str(row[base+str(i)]) for i in range(1, nSamples+1)]

def test_lf(lf, df, verbose=False, small_df=False, sets=None):
    # test a labeling function through rows in dataframe
    # output a confusion matrix for labeling function

    cm = [0] * len(categories)
    for index, row in df.iterrows():
        ret = lf(row)
        if categories[row.y_act] == ret and sets != None:
            sets.add(row['Attribute_name'])
        if categories[row.y_act] != ret and ret != 0 and verbose:
            print(row['Attribute_name'], end = '\t')
            print(categories[row.y_act], end = '\t')
            print(ret)
        if small_df:
            print(row['Attribute_name'], end = '\t')
            print(categories[row.y_act], end = '\t')
            print(ret)
        if ret!= 0:
            cm[categories[row.y_act]] += 1
    return cm

def test_lfs(lfs, df, verbose=True):
    # extensive version of test_lf
    # test a list labeling function through rows in dataframe
    # output a confusion matrix for all labeling functions
    
    cms = np.zeros((len(lfs), len(categories)), dtype=int)
    for index, row in df.iterrows():
        for i in range(len(lfs)):
            lf = lfs[i]   
            ret = lf(row)
            if ret!= 0:
                cms[i][categories[row.y_act]] += 1
    if verbose:
        print('%-30s'%'labeling function names', end='\t')
        print('%10s'%'nan', end='')
        print('%10s'%'category', end='')
        print('%10s'%'numeric', end='')
        print('%10s'%'extract', end='')
        print('%10s'%'unusable', end='')
        print('%10s'%'context')

        for i in range(len(lfs)):
            print('%-30s'%lfs[i].__name__, end='\t')
            for cm in cms[i]:
                print('%10d' % cm, end='')
            print()
    return cms

def test_lfs_onecategory(lfs, df, category):
    # more precise version of test_lfs
    # test a list labeling function through rows in dataframe for one category
    # output the abstained data samples and mismatched data samples
    
    cm = [0] * len(categories)
    cid = categories[category]
    abstained = pd.DataFrame()
    mismatched = pd.DataFrame()
    if not isinstance(lfs, list):
        lfs = [lfs]
    for index, row in df.iterrows():
        y_true = categories[row.y_act]
        predictions = [0] * len(lfs)
        for i, lf in enumerate(lfs):
            y_pred = lf(row)
            predictions[i] = y_pred
        if sum(predictions) != 0:
            cm[categories[row.y_act]] += 1
            if y_true != cid:
                mismatched = mismatched.append(row)
        else:
            if cid == y_true:
                abstained = abstained.append(row)
    if category == 'Unusable':
        accuracy = cm[cid]/sum(cm)
    else:
        accuracy = cm[cid]/(sum(cm)-cm[categories['Unusable']])
    coverage = cm[cid]/categories_size[category]
    return cm, abstained, mismatched, accuracy, coverage