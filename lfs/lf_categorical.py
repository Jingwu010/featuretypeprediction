from .helper import *
from .lf_numerical import lf_sample_cast_to_float, lf_cast_to_numbers

def lf_binary_category(row):
    # Case e. Yes/No type values, including binary 0/1 answers
    # PRIORITY: 2
    # [0, 928, 46, 7, 101, 154]
    if row['num of dist_val'] == 2 or row['num of dist_val'] == 3:
        # [TODO] check binary 0/1 answers?
        return 1
    return 0

def lf_name_category(row):
    # Case f. Country names, city names, food type names, and other object type names
    # PRIORITY: 2
    # [TODO] add more reasonable groups here
    # [TODO] handle name like 'velocity'
    # [0, 330, 100, 22, 48, 11]
    
    category_names = ['city', 'country', 'state', 'nationality', 'region', 'category', 'type', 'level', 'stage']
    category_names_pronoun = ['cities', 'countries', 'nationalities', 'categories']
    
    sets = category_names + category_names_pronoun
    if sum([x in str(row['Attribute_name']).lower() for x in sets]) > 0:
        return 1
    return 0

def lf_coded_abbreviation(row):
    # Case g. Coded numbers that are short forms of names
    # PRIORITY: 2
    # e.g. CHN USA
    # abbreviation = upper case + same length + only alpha
    # [0, 103, 0, 0, 27, 11]
    
    samples = get_samples(row)
    samples_case = [sample.upper() == sample for sample in samples]
    samples_len = [len(sample) for sample in samples]
    samples_alpha = [sample.isalpha() for sample in samples]
    if sum(samples_case)>3 and sum(samples_alpha)>3 and len(set(samples_len)) < 3:
        return 1
    return 0

def lf_finite_set_name(row):
    # Case h. Short names that indicate type from a known finite set/domain
    # Case j. A coded number that encodes real-world entities from a known finite/ domain set
    # PRIORITY: 2
    # e.g. product id, department number, and zipcode
    # e.g. type of funding from the set {“seed funding”, “private equity”, etc.}
    # e.g. job title from the set {“politician”, “actor”, “scientist”, etc.}
    # e.g. gender from the set {“male”, “female”, “other”, etc.}
    # 1. attribute names indicates the samples ['job title', 'type', 'gender']
    # [0, 252, 11, 67, 101, 94]
    
    finite_set_names = ['job',      # [0, 44, 4, 13, 17, 0]
                        'title',    # [0, 18, 0, 15, 1, 2]
                        'type',     # [0, 97, 0, 12, 13, 7]
                        'level',    # [0, 17, 0, 1, 2, 0]
                        'currency', # [0, 15, 0, 2, 0, 0]
                        'status',   # [0, 18, 6, 1, 8, 1]
                        'serie',    # [0, 15, 1, 0, 4, 3]
                        'code',     # [0, 106, 1, 15, 51, 13]
                        'gender',   # [0, 45, 0, 1, 1, 0]
                        'topic',    # [0, 6, 0, 2, 1, 3]
                        'label',    # [0, 14, 1, 1, 5, 0]
                        'zip',      # [0, 20, 0, 1, 1, 0]
                        'block'     # [0, 6, 0, 0, 0, 0]
                        ]
    if sum([x in str(row['Attribute_name']).lower() for x in finite_set_names]) > 0:
        return 1
    return 0

def lf_finite_set_sample(row):
    # Case h. Short names that indicate type from a known finite set/domain
    # PRIORITY: 2
    # e.g. type of funding from the set {“seed funding”, “private equity”, etc.}
    # e.g. job title from the set {“politician”, “actor”, “scientist”, etc.}
    # e.g. gender from the set {“male”, “female”, “other”, etc.}
    # 2. attribute samples are usually with meadian length 10-25,
    # 3. attribute samples are mostly composed by alphabeta letters 
    # [0, 226, 1, 83, 64, 79]
    
    def alphabet_percent(string):
        return sum(c.isalpha() for c in string) / len(string)

    samples = get_samples(row)
    samples_len = [len(sample) for sample in samples]
    samples_percent = [alphabet_percent(sample) for sample in samples]
    
    samples_len_mean = sum(samples_len)/len(samples_len)
    samples_percent_mean = sum(samples_percent)/len(samples_percent)
    if samples_len_mean > 10 and samples_len_mean < 25 and samples_percent_mean > 0.8:
        return 1
    return 0

def lf_dist_string_percentage(row):
    # samples are in a small range of dist values (non digits)
    # PRIORITY: 2
    # 1. dist_val > 1
    # 2. (dist_val/total_val) < 0.01
    # 3. 3/5 samples are non digits 
    # [0, 808, 161, 210, 100, 185]
    
    samples = get_samples(row)
    samples_non_digits = [1-sample.isdigit() for sample in samples]
    
    total_val = row['Total_val']
    dist_val = row['num of dist_val']
    if dist_val > 1 and  (dist_val/total_val) < 0.01 and sum(samples_non_digits) > 2:
        return 1
    return 0

def lf_dist_num_percentage(row):
    # samples are in a small range of dist values (only digits)
    # PRIORITY: 2
    # 1. dist_val > 1
    # 2. (dist_val/total_val) < 0.0005
    # 3. 3/5 samples are digits 
    # [0, 515, 143, 0, 17, 265]

    samples = get_samples(row)
    samples_non_digits = [sample.isdigit() for sample in samples]
    
    total_val = row['Total_val']
    dist_val = row['num of dist_val']
    if dist_val > 1 and  (dist_val/total_val) < 0.0005 and sum(samples_non_digits) > 2:
        return 1
    return 0

def lf_same_len_num_lt(row):
    samples = get_samples(row)
    if lf_sample_cast_to_float(row):
        return 0
    sample_len = [len(sample) for sample in samples]
    sample_len_min = sum(lens<=2 for lens in sample_len)
    if len(set(sample_len)) < 2 and sample_len_min>3:
        return 3
    return 0

def lf_same_len_string_lt(row):
    samples = get_samples(row)
    if lf_cast_to_numbers(row):
        return 0
    sample_len = [len(sample) for sample in samples]
    sample_len_min = sum(lens<=10 for lens in sample_len)
    if len(set(sample_len)) < 2 and sample_len_min>3:
        return 3
    return 0

def lf_max_eq_dist(row):
    if row['num of dist_val'] == 1 or row['num of dist_val'] == 0:
        return 0
    if row['max_val'] == row['num of dist_val']:
        return 3
    return 0