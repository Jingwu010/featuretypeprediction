from .helper import *

def lf_cast_to_numbers(row):
    # Case a. Should be usable directly as a number feature for ML 
    # is not any of cases b, e, g, i, j, k, l, or n
    # PRIORITY: 3
    # [TODO] highly depend on other lfs' output
    # [1092, 5055, 24, 596, 1747, 0]
    nSamples = 5
    base = 'sample_'
    flag = 0
    for i in range(1, nSamples+1):
        att_name = base+str(i)
        try:
            float(str(row[att_name]))
            flag += 1
        except:
            pass
    
    # At least 4/5 records should match the regex
    # Records comes from non - NaN samples
    if flag > 3:
        return 2
    return 0

def lf_has_mean_std(row):
    if row['mean'] != 0 and row['std_dev'] != 0:
        return 2
    return 0

def lf_has_mean_dev_min(row):
    if row['mean'] != 0 and row['std_dev'] != 0 and row['min_val'] != 0:
        return 2
    return 0

def lf_max_min_difference(row):
    if not lf_has_mean_std(row):
        return 0
    if row['max_val'] - row['min_val'] > row['Total_val']:
        return 2
    return 0

def lf_sample_cast_to_float(row):
    samples = get_samples(row)
    flag = 0
    for sample in samples:
        try:
            _sample = float(sample)
            if _sample - int(_sample) != 0:
                flag += 1
        except:
            pass
    if flag > 3:
        return 2
    return 0

def lf_std_gt_mean(row):
    if not lf_has_mean_std(row):
        return 0
    if row['std_dev'] > row['mean']:
        return 2
    return 0