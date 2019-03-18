from .helper import *
import re

def lf_key_word_year(row):
    # a key word in attribute name while has different representation from classes
    # PRIORITY: 2
    # e.g. Usable Directly Categorical  year 1995   2018
    # e.g. Usable Directly Numeric      year 36     24
    # 1. attribute name contains year
    # 2. samples in year format or not
    # [0, 77, 63, 17, 6, 2]
    
    def find_year(string):
        return re.match('\d{4}', string) != None

    key = 'year'
    if not key in str(row['Attribute_name']).lower():
        return 0

    samples = get_samples(row)
    year_in_samples = [find_year(sample) for sample in samples]
    
    if sum(year_in_samples) > 2:
        # if 3/5 samples are in year format
        # return Categorical
        return 1
    # else return Numeric
    return 2

# from nltk.corpus import stopwords 
# def lf_key_word_name(row):
#     # a key word in attribute name while has different representation from classes
#     # PRIORITY: 2
#     # e.g. Usable Directly Categorical  loan_purpose_name Home purchase Home improvement
#     # e.g. Usable Directly Numeric      ri_2nd_ad_newspaper_name    Milwaukee Journal Sentinel  Clarion Ledger  Denver Post
#     # 1. attribute name contains name
#     # 2. samples have overlap key words or not
#     # 
    
#     def string_to_word_set(string, stop_words):
#         wordset = set(re.findall('[A-Za-z0-9]+', 'Malaysian Grand Prix'))
#         for word in wordset:
#             if word in stop_words:
#                 wordset.remove(word)
#         return wordset

#     def avg_intersection(one_set, sets):
#         if len(one_set):
#             return sum([len(one_set.intersection(_set))/len(one_set.union(_set)) for _set in sets])/len(sets)
#         return 0

#     key = 'name'
#     if not key in str(row['Attribute_name']).lower():
#         return 0
    
#     stop_words = set(stopwords.words('english')) 
    
#     samples = get_samples(row)
#     samples_word_set = [string_to_word_set(sample, stop_words) for sample in samples]
    
#     flag = 0
#     for i in range(len(samples_word_set)):
#         _set = samples_word_set[i]
#         # share some similarity in pattern while different in numbers
#         if avg_intersection(_set, samples_word_set) >= 0.5:
#             flag += 1

#     if sum(samples_flag) > 2:
#         # if 3/5 samples has overlap
#         # return Categorical
#         return 1
#     # else return Context_Specific
#     return 5