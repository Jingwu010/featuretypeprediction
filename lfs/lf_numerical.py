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