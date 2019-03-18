import re
from .helper import *
from .lf_numerical import lf_cast_to_numbers

def lf_extractable_units(row):
    # Case b. A number present along with unit of measure string
    # A number present along with unit of measure string
    # PRIOTIRY: 2
    # e.g., ‘30 Mhz’, ‘30 degree’, ‘45 mm’
    # e.g. http://www.us-metric.org/detailed-list-of-metric-system-units-symbols-and-prefixes/
    # [0., 0., 2., 0., 0.]
    
    LENGTH_ABV  = ['in', 'ft', 'yd', 'mi', 'mm', 'cm', 'm', 'km']
    LENGTH_FULL = ['inch', 'feet', 'yard', 'mile', 'millimeter', 'centimeter', 'kilometer']

    # [TODO] AREA
    
    VOLUME_ABV  = ['fl', 'oz', 'gal', 'ml', 'l']

    MASS_ABV    = ['oz', 'lb', 't', 'g', 'kg', 'mg']
    MASS_FULL   = ['ounce', 'pound', 'ton', 'gram', 'kilogram', 'megagram']

    TEMP_ABV    = ['f', 'c']  # [TODO] Add degree symbol
    TEMP_FULL   = ['degree']

    PHYSICS_ABV = ['n', 'kpa', 'hz', 'w', 'pa', 'v']
    PHYSICS_FULL= ['newton', 'hertz', 'watt', 'volt', 'ohm']

    TIME_ABV    = ['m', 'h', 's', 'd', 'w', 'm']
    TIME_FULL   = ['min', 'minute', 'hour', 'second', 'day', 'week', 'month', 'year']
    
    CURENCY_ABV = ['$', '¥', '€']
    CURENCY_FULL= ['dolar', 'usd', 'yuan', 'cny','eur', 'rub']

    ABV_SET     = LENGTH_ABV + VOLUME_ABV + MASS_ABV + TEMP_ABV + PHYSICS_ABV + TIME_ABV + CURENCY_ABV
    FULL_SET    = LENGTH_FULL + [x+'s' for x in LENGTH_FULL] + [x+'es' for x in LENGTH_FULL] +\
                  MASS_FULL + [x+'s' for x in MASS_FULL] + [x+'es' for x in MASS_FULL] +\
                  TEMP_FULL + [x+'s' for x in MASS_FULL] + [x+'es' for x in MASS_FULL] +\
                  PHYSICS_FULL + [x+'s' for x in PHYSICS_FULL] + [x+'es' for x in PHYSICS_FULL] +\
                  TIME_FULL + [x+'s' for x in TIME_FULL] + [x+'es' for x in TIME_FULL] +\
                  CURENCY_FULL + [x+'s' for x in CURENCY_FULL] + [x+'es' for x in CURENCY_FULL]
    TRAILING_SET   = set(ABV_SET + FULL_SET)
    LEADING_SET = set(CURENCY_ABV)

    def check_unit_symbols(text, unitset):
        try:
            r = re.split(r'(\d+\.?\d+)', text)
            leading_unit = r[0].strip().lower()
            num = float(r[1])
            trailing_unit = r[2].strip().lower()
            if not len(leading_unit) and (trailing_unit in TRAILING_SET):
                # no leading unit
                # number + unit
                unitset.add(trailing_unit)
                return True
            elif leading_unit in LEADING_SET:
                # no trialing unit
                # unit + number
                unitset.add(leading_unit)
                return True
            else:
                return False
        except:
            return False

    samples = get_samples(row)
    unitset = set()
    flag = sum(check_unit_symbols(sample, unitset) for sample in samples)

    # At least 3/5 records should match the regex and they should with same units
    # Records comes from non - NaN samples
    if flag > 2 and len(unitset) < 3:
        return 3
    return 0

def lf_extractable_number_sci(row):
    # Case b. A number with scientific representation
    # PRIORITY: 2
    # e.g., 30,000, 1e9, 1^9, 1E9
    # https://en.wikipedia.org/wiki/Scientific_notation
    # https://stackoverflow.com/questions/18152597/extract-scientific-number-from-string
    # [1., 1., 0., 0., 0.]
    # Usable Directly Numeric   a   distance    258 126 0.0 0.000   0.000000    0.000   0.000000    28  12  11,2    12,9    18,5
    
    def check_scientific_rep(numberString):
        match_number = re.compile('\d+[eE^,]\d+')
        ret = re.findall(match_number, numberString)
        if len(ret) and len(ret[0]) == len(numberString.strip()):
            return True
        return False

    samples = get_samples(row)
    flag = sum(check_scientific_rep(sample) for sample in samples)
    
    # At least 3/5 records should match the regex
    # Records comes from non - NaN samples
    if flag > 2:
        return 3
    return 0

def lf_extractable_pattern(row):
    # A String representation following some pattern
    # # PRIORITY: 2
    # e.g. pg 1, pg 2, pg 5
    # [25.,  1., 78., 14., 14.]
    
    def hasNumbers(inputString):
        return any(char.isdigit() for char in inputString)
    
    def avg_intersection(one_set, sets):
        if len(one_set):
            return sum([len(one_set.intersection(_set))/len(one_set.union(_set)) for _set in sets])/len(sets)
        return 0
    
    nSamples = 5
    base = 'sample_'
    pattern_sets = [None]*nSamples
    num_sets = [None]*nSamples
    for i in range(1, nSamples+1):
        att_name = base+str(i)
        sample_string = str(row[att_name])
        pattern_set = set()
        num_set = set()
        for part in re.split('[^a-zA-Z0-9]', sample_string):
            if not len(part.strip()):
                continue
            if not hasNumbers(part):
                pattern_set.add(part.strip().lower())
            if hasNumbers(part):
                num_set.add(part.strip().lower())
        pattern_sets[i-1] = pattern_set
        num_sets[i-1] = num_set
    
    flag = 0
    for i in range(len(pattern_sets)):
        _set1 = pattern_sets[i]
        _set2 = num_sets[i]
        # share some similarity in pattern while different in numbers
        if avg_intersection(_set1, pattern_sets) >= 0.5 and\
            avg_intersection(_set2, num_sets) != 1 and len(_set2) != 0:
            flag += 1
    
    # At least 3/5 records should match the regex
    # Records comes from non - NaN samples
    if flag > 2:
        return 3
    return 0

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

def lf_extractable_name(row):
    # Case c. A text corpus with semantic meaning, URL, address
    # PRIORITY: 2
    # e.g., review text, remarks text,
    # [0, 84, 61, 182, 52, 11]
    

    # [TODO] add more meaningful semantic attribute key words
    # Most of extractable should fall into this check
    extractable_names = ['url',
                         'link',
                         'content',
                         'comment',
                         'address',
                         'title',
                         'text',
                         'description',
                         'review',
                         'talk',
                         'remark',
                         'measure',
                         'other',
                         'reason',
                         'location']
    for name in extractable_names:
        if name in str(row['Attribute_name']).lower():
            return 3
    return 0

def lf_extractable_list(row):
    # Case c. A list of items in a single sample separated by symbols
    # PRIORITY: 2
    # e.g. department list such as ‘{men|clothing, women|clothing, children|toys etc}’ ( text ),  (]
    # [0, 2, 3, 27, 5, 0]

    def check_parentheses(text):
        text = text.strip()
        if (text.startswith('(') or text.startswith('[')) and (text.endswith(')') or text.endswith(']')):
            return True
        if text.startswith('{') and text.endswith('}'):
            return True
        return False

    samples = get_samples(row)
    flag = sum(check_parentheses(sample) for sample in samples)

    # At least 3/5 records should match the regex
    # Records comes from non - NaN samples
    if flag > 2:
        return 3
    return 0

def lf_extractable_sample_length(row):
    # extremely long textual data (integer could not be that long)
    # [0, 123, 3, 274, 37, 57]
    Threshold = 25

    samples = get_samples(row)
    samples_length = [len(sample) for sample in samples]
    meanLen = sum(samples_length)/len(samples_length)
    if meanLen > 25:
        return 3
    # leave one out
    meanLen = sum(sorted(samples_length)[1:])/(len(samples_length)-1)
    if meanLen > 25:
        return 3
    return 0

def lf_date_extraction_samples(row):
    # Case d. Date or time stamp
    # PRIORITY: 2
    #  e.g., ‘7/11/2018’, and ‘21hrs:15min:3sec’
    # [0, 19, 0, 264, 17, 51]
    
    def check_datetime(obj):
        datetimeString = str(obj).lower()
        if re.match('\d{1,4}\/\d{1,2}\/\d{1,4}', datetimeString) or\
            re.match('\d{1,4}-\d{1,2}-\d{1,4}', datetimeString) or\
            re.match('\d{1,2}:\d{1,2}(:\d{1,2})?', datetimeString):
            return True

        months  = ['january',    'jan',
                   'february',   'feb',
                   'march',      'mar',
                   'april',      'apr',
                   'may',        'may',
                   'june',       'jun',
                   'july',       'jul',
                   'august',     'aug',
                   'september',  'sep',
                   'october',    'oct',
                   'november',   'nov',
                   'december',   'dec', 'month']
        secs    = ['sec', 'second']
        mins    = ['min', 'minute']
        timeunits =  secs + mins + ['hour'] + ['day'] + ['week'] + months + ['year']
        if sum([timeunit in datetimeString for timeunit in timeunits]) > 0:
            return True
        return False
    
    samples = get_samples(row)
    flag = sum(check_datetime(sample) for sample in samples)
    
    # At least 3/5 records should match the regex
    # Records comes from non - NaN samples
    if flag > 2:
        return 3
    return 0


def lf_extractable_email_url(row):
    # Case c. extractable text, url or email
    # PRIORITY: 2
    # e.g. www.google.com   user@gmail.com
    # [0, 0, 33, 10, 4, 0]

    def check_email_url(string):
        if re.match('\"?([-a-zA-Z0-9.`?{}]+@\w+\.\w+)\"?', string):
            # email match
            return True
        if re.match('^(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?$', string):
            # url match
            return True
        return False
    
    samples = get_samples(row)
    flag = sum(check_email_url(sample) for sample in samples)
    
    # At least 3/5 records should match the regex
    # Records comes from non - NaN samples
    if flag > 2:
        return 3
    return 0

def lf_same_len_string(row):
    samples = get_samples(row)
    if lf_cast_to_numbers(row):
        return 0
    sample_len = [len(sample) for sample in samples]
    sample_len_min = sum(lens>10 for lens in sample_len)
    if len(set(sample_len)) < 2 and sample_len_min>3:
        return 3
    return 0