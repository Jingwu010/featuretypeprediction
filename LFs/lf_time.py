#########
# CASE D
#########

import datetime

# [TODO] Clever way to do matching
# Using regex?

def lf_date_extraction_name_and_samples(row):
    # to Amplify the importance 
    
    return lf_date_extraction_name(row) and lf_date_extraction_samples(row)

def lf_date_extraction_name(row):
    # [  6.,  21., 149.,  12.,   1.]

    # of high constrain
    # if row['Attribute_name'].values[0].lower().endswith('date'):
    #     checkPoint -= 1
    # elif row['Attribute_name'].values[0].lower().endswith('datetime'):
    #     checkPoint -=1
    
    # of low constrain
    if 'datetime' in str(row['Attribute_name']).lower():
        return 3
    elif 'date' in str(row['Attribute_name']).lower():
        return 3
    elif 'time' in str(row['Attribute_name']).lower():
        return 3
    return 0

def lf_date_extraction_samples(row):
    # [  5.,   0., 187.,   8.,  16.]
    # 
    def check_datetime(obj):
        datetimeString = str(obj)
        for _part in datetimeString.split():
            for part in _part.split('T'):
                if check_date_format(part) or check_time_format(part):
                    return True
        return False
    
    nSamples = 5
    base = 'sample_'
    flag = 0
    for i in range(1, nSamples+1):
        att_name = base+str(i)
        if check_datetime(row[att_name]):
            flag += 1
    
    # At least 3/5 records should match the regex
    # Records comes from non - NaN samples
    if flag > 2:
        return 3
    return 0

def check_date_format(datestring):
    # time consuming
    # https://querysurge.zendesk.com/hc/en-us/articles/208215646-Flat-Files-with-Custom-Date-Time-Timestamp-Formatted-Data
    
    try:
        datetime.datetime.strptime(datestring, '%Y-%m-%d')      # yyyy-mm-dd
        return True
    except:
        pass
    try:
        datetime.datetime.strptime(datestring, '%d/%b/%Y')      # yyyy-mmm-dd
        return True
    except:
        pass
    try:
        datetime.datetime.strptime(datestring, '%Y-%j')         # yyyy-ddd
        return True
    except:
        pass
    try:
        datetime.datetime.strptime(datestring, '%d/%m/%Y')      # dd/mm/yyyy
        return True
    except:
        pass
    try:
        datetime.datetime.strptime(datestring, '%m/%d/%Y')      # mm/dd/yyyy
        return True
    except:
        pass
    try:
        datetime.datetime.strptime(datestring, '%d/%m/%y')      # dd/mm/yy
        return True
    except:
        pass
    try:
        datetime.datetime.strptime(datestring, '%m/%d/%y')      # mm/dd/yy
        return True
    except:
        pass
    return False
    
def check_time_format(timestring):
    try:
        datetime.datetime.strptime(timestring, '%I:%M')     # 3:14
        return True
    except:
        pass
    try:
        datetime.datetime.strptime(timestring, '%H:%M')     # 13:14
        return True
    except:
        pass
    try:
        datetime.datetime.strptime(timestring, '%H:%M.%f')  # 13:14.00
        return True
    except:
        pass
    try:
        datetime.datetime.strptime(timestring, '%I:%M:%S')  # 3:14:00
        return True
    except:
        pass
    try:
        datetime.datetime.strptime(timestring, '%H:%M:%S')  # 13:14:00
        return True
    except:
        pass
    try:
        datetime.datetime.strptime(timestring, '%H:%M:%S.%f')  # 13:14:00.00
        return True
    except:
        pass
    return False

# import sys
# import numpy as np
# cm = np.zeros(5)

# sys.stdout = open('lf_time_output', 'w')
# for index, row in df.iterrows():
#     if lf_date_extraction_name(row) == 3 or lf_date_extraction_samples(row) == 3:
#         cm[categories[row.y_act]-1] += 1
#         if categories[row.y_act] != 3:
#             print(row.Attribute_name, '\t', categories[row.y_act])
# print(cm)
# cm