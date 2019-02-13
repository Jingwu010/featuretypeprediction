#########
# CASE C
#########
#
def lf_extractable_name(row):
    # [ 51.,  16., 122.,  32.,   8.]
    # 
    extractable_names = ['url', 'content', 'comment', 'address', 'note', 'title', 'text', 'description', 'review', 'talk', 'remark','measure']
    for name in extractable_names:
        if name in str(row['Attribute_name']).lower():
            return 3
    return 0

def lf_extractable_list(row):
    # [ 2.,  3., 26.,  5.,  0.]

    def check_parentheses(text):
        text = text.strip()
        if text.startswith('(') and text.endswith(')'):
            return True
        if text.startswith('[') and text.endswith(']'):
            return True
        if text.startswith('{') and text.endswith('}'):
            return True
        return False

    nSamples = 5
    base = 'sample_'
    flag = 0
    for i in range(1, nSamples+1):
        att_name = base+str(i)
        if check_parentheses(str(row[att_name])):
            flag += 1

    # At least 3/5 records should match the regex
    # Records comes from non - NaN samples
    if flag > 2:
        return 3
    return 0

def lf_extractable_sample_length(row):
    # extremely long textual data (integer could not be that long)
    # [123.,   3., 274.,  37.,  57.]
    Threshold = 25

    nSamples = 5
    base = 'sample_'
    lengths = [0] * 5
    for i in range(1, nSamples+1):
        att_name = base+str(i)
        lengths[i-1] = len(str(row[att_name]))

    meanLen = sum(lengths)/nSamples
    if meanLen > 25:
        return 3
    # leave one out
    meanLen = sum(sorted(lengths)[1:])/(nSamples-1)
    if meanLen > 25:
        return 3
    return 0