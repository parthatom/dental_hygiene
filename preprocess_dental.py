import pandas as pd
import numpy as np
import os

# Anterior and Posterior Teeth as defined by American Dental Association
# https://radiopaedia.org/articles/american-dental-association-universal-numbering-system?lang=us

ANTERIOR = list(range(6, 12)) + list(range(22, 28))
POSTERIOR = list(range(1, 6)) + list(range(12, 22)) + list(range(28, 33))

# Some codings for easier usage later
CODINGS = {
    'ABSENT': 0,
    'PRESENT': 1,

}


def get_data(url='https://wwwn.cdc.gov/Nchs/Nhanes/2017-2018/P_OHXDEN.XPT', path='./dataset/P_OHXDEN.XPT'):
    """
    Load data from path if exists, else pull from url
    @param url: URL of the data
    @type url: str
    @param path: Path of dataset on file system if exists
    @type path: str
    @return: Entire pd.DataFrame
    """
    return pd.read_sas(path if os.path.exists(path) else url)


# OHXxxTC Column Description :
# Code  Description	                            Count	Cumulative  Convert Explanation
# 1	    Primary tooth (deciduous) present	    0	    0           1       Present
# 2	    Permanent tooth present	                7534	7534        1       Present
# 3	    Dental implant	                        4	    7538        0       Absent
# 4	    Tooth not present	                    5609	13147       0       Absent
# 5	    Permanent dental root fragment present	131	    13278       0       Absent
# 9	    Could not assess	                    0	    13278       0       Treat as Absent
# .	    Missing	                                494	    13772       0       Treat as Absent


TOOTH_COUNT_CODINGS = {
    1: 1,  # Primary tooth
    2: 1,  # Perm tooth
    3: 0,  # Implant
    4: 0,
    5: 0,
    9: 0,
    'nan': 0
}


def get_tc_col_name(t):
    return 'OHX{tooth:02d}TC'.format(tooth=t)


def get_tooth_count(df, tooth_list, codings=None):
    """
    Gets tooth count from merging TOOTH_COUNT cols for all teeth in tooth_list
    @param df: DataFrame
    @type df: pd.DataFrame
    @param tooth_list: ANTERIOR or POSTERIOR
    @return: pd.Series of Tooth Count
    """
    if codings is None:
        codings = TOOTH_COUNT_CODINGS
    cols = list(map(get_tc_col_name, tooth_list))
    data = df[cols]
    return data.applymap(lambda x: codings['nan'] if np.isnan(x) else codings[x]).sum(axis=1)

if __name__ == "__main__":
    print(get_tooth_count(get_data(), ANTERIOR))