from .helper import *

def lf_unusable(row):
    # Case k. A number indicating the position of a record in its dataset table, e.g., serial number
    # Case l. An attribute that is likely the primary key in its dataset table, or an attribute whose values will almost surely be unique for all records in its dataset table but is not a numeric feature
    # PRIORITY: 1
    # 1. # distinct == 1
    # 2. % distinct == 100%
    # 3. % nans     > 99%
    # [TODO] total_nans seems to be a loose contrain here
    # [51, 191, 80, 786, 219, 0]
    total_val = row['Total_val']
    dist_val = row['num of dist_val']
    total_nans = row['% nans']
    if dist_val <= 1 or (dist_val/total_val) > 0.99 or total_nans > 99:
        return 4
    return 0


def lf_unusable_nans(row):
    # Case k. A number indicating the position of a record in its dataset table, e.g., serial number
    # Case l. An attribute that is likely the primary key in its dataset table, or an attribute whose values will almost surely be unique for all records in its dataset table but is not a numeric feature
    # PRIORITY: 1
    # 1. samples are of NaN values
    # [TODO] % nans should be more precise here, while some of them are not available
    # [30, 2, 0, 337, 12, 0]
    def check_nan(string):
        return string == 'nan'

    samples = get_samples(row)
    nans_in_samples = [check_nan(sample) for sample in samples]
    if sum(nans_in_samples) >= 3:
        return 4
    return 0