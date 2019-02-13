#########
# CASE B
#########
#
import re
def lf_extractable_units(row):
    # A number present along with unit of measure string
    # e.g., ‘30 Mhz’, ‘30 degree’, ‘45 mm’
    # http://www.us-metric.org/detailed-list-of-metric-system-units-symbols-and-prefixes/
    # [1., 0., 3., 0., 0.]
    
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
            # no leading unit
            if len(r) < 4 and (trailing_unit in TRAILING_SET) and not len(leading_unit):
                unitset.add(trailing_unit)
                return True
            # no trialing unit
            elif len(r) < 3 and leading_unit in LEADING_SET:
                unitset.add(leading_unit)
                return True
            else:
                return False
        except:
            return False

    nSamples = 5
    base = 'sample_'
    flag = 0
    unitset = set()
    for i in range(1, nSamples+1):
        att_name = base+str(i)
        if check_unit_symbols(str(row[att_name]), unitset):
            flag += 1

    # At least 3/5 records should match the regex and they should with same units
    # Records comes from non - NaN samples
    if flag > 2 and len(unitset) < 3:
        return 3
    return 0

def lf_extractable_number_sci(row):
    # A number with scientific representation
    # e.g., 30,000, 1e9, 1^9, 1E9
    # https://en.wikipedia.org/wiki/Scientific_notation
    # https://stackoverflow.com/questions/18152597/extract-scientific-number-from-string
    # [1., 1., 0., 0., 0.]
    # Usable Directly Numeric   a   distance    258 126 0.0 0.000   0.000000    0.000   0.000000    28  12  11,2    12,9    18,5
    # 
    def check_scientific_rep(numberString):
        match_number = re.compile('\d+[eE^,]\d+')
        ret = re.findall(match_number, numberString)
        if len(ret) and len(ret[0]) == len(numberString.strip()):
            return True
        return False

    nSamples = 5
    base = 'sample_'
    flag = 0
    for i in range(1, nSamples+1):
        att_name = base+str(i)
        if check_scientific_rep(str(row[att_name])):
            flag += 1
    
    # At least 3/5 records should match the regex
    # Records comes from non - NaN samples
    if flag > 2:
        return 3
    return 0

def lf_extractable_pattern(row):
    # A String representation following some pattern
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