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
    'nan': np.nan
}


def get_tc_col_name(t):
    return 'OHX{tooth:02d}TC'.format(tooth=t)


def get_tooth_count(df, tooth_list, codings=None):
    """
    Gets tooth count from merging TOOTH_COUNT cols for all teeth in tooth_list
    @param codings:
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


#
#
# Code 	Description	                                                            Count	Cumulative  Convert
# A	    Primary tooth with a restored surface condition	                        0	    0           1
# D	    Sound primary tooth	                                                    0	    0           0
# E	    Missing due to dental disease	                                        1197	1197        3
# F	    Permanent tooth with a restored surface condition	                    2908	4105        1
# J	    Permanent root tip is present but no restorative replacement is present	131	    4236        3
# K	    Primary tooth with a dental carious surface condition	                0	    4236        2
# M	    Missing due to other causes	                                            47	    4283        3
# P	    Missing due to dental disease but replaced by a removable restoration	1019	5302        3
# Q	    Missing due to other causes but replaced by a removable restoration	    37	    5339        3
# R	    Missing due to dental disease but replaced by a fixed restoration	    13	    5352        3
# S	    Sound permanent tooth	                                                4394    9746        0
# T	    Permanent root tip is present but a restorative replacement is present	0	    9746        3
# U	    Unerupted	                                                            3297	13043       nan
# X	    Missing due to other causes but replaced by a fixed restoration	        0	    13043       nan
# Y	    Tooth present, condition cannot be assessed	                            11	    13054       nan
# Z	    Permanent tooth with a dental carious surface condition	                220	    13274       2
# nan	Missing	                                                                498	    13772       nan

CARIES_CODINGS = {
    'A': 1,
    'D': 0,
    'E': 3,
    'F': 1,
    'J': 3,
    'K': 2,
    'M': 3,
    'P': 3,
    'Q': 3,
    'R': 3,
    'S': 0,
    'T': 3,
    'U': np.nan,
    'X': np.nan,
    'Y': np.nan,
    'Z': 2,
    'nan': np.nan,
    '': np.nan
}


def get_tooth_caries_col_name(t):
    return 'OHX{tooth:02d}CTC'.format(tooth=t)


def del_not_present_cols(l, np):
    l1 = l.copy()
    for x in np:
        if x in l1:
            del l1[l1.index(x)]
    return l1


def get_caries_count(df, tooth_list, codings=None):
    """
    Gets tooth count from merging TOOTH_COUNT cols for all teeth in tooth_list
    @param codings:
    @param df: DataFrame
    @type df: pd.DataFrame
    @param tooth_list: ANTERIOR or POSTERIOR
    @return: pd.Series of Tooth Count
    """
    if codings is None:
        codings = CARIES_CODINGS
    # No Caries Col for 1,32
    tl = del_not_present_cols(tooth_list, [1, 16, 17, 32])

    cols = list(map(get_tooth_caries_col_name, tl))
    data = df[cols]
    return data.applymap(lambda x: codings[x.decode()]).sum(axis=1)


#  Dental Sealants Data Description
#
# Code  Description	                                    Count	Cumulative	Convert
# 0	    Sealant not present	                            4194	4194	    0
# 1	    Occlusal sealant on permanent tooth	            102 	4296	    1
# 2	    Facial sealant on permanent tooth	            0	    4296	    1
# 3	    Lingual sealant on permanent tooth	            0	    4296	    1
# 4	    Occlusal sealant on primary tooth	            51	    4347	    1
# 9	    Cannot be assessed	                            41	    4388	    nan
# 12	Occlusal-facial sealant on permanent tooth	    0	    4388	    1
# 13	Occlusal-lingual sealant on permanent tooth	    0	    4388	    1
# nan	Missing	                                        9384	13772       nan

SEALANT_CODINGS = {
    0: 0,
    1: 1,
    2: 1,
    3: 1,
    4: 1,
    9: np.nan,
    12: 1,
    13: 1,
    'nan': np.nan,
    '': np.nan
}


def get_sealant_col_name(t):
    return 'OHX{tooth:02d}SE'.format(tooth=t)


def get_sealant_count(df, tooth_list, codings=None):
    """
    Gets tooth count from merging TOOTH_COUNT cols for all teeth in tooth_list
    @param codings:
    @param df: DataFrame
    @type df: pd.DataFrame
    @param tooth_list: ANTERIOR or POSTERIOR
    @return: pd.Series of Tooth Count
    """
    if codings is None:
        codings = SEALANT_CODINGS
    # No Sealant Col for 1,32
    tl = del_not_present_cols(tooth_list, [1, 6, 8, 9, 11, 16, 17, 22, 23, 24, 25, 26, 27, 32])
    cols = list(map(get_sealant_col_name, tl))
    data = df[cols]
    return data.applymap(lambda x: codings[''] if not x.decode() else codings[int(x.decode())]).sum(axis=1)


#   Root Caries, other lesions X [restored , not] Data Description
# Code Description	            Count   Convert
# 1	    Yes	                    1085    1
# 2	    No	                    6916	0
# 9	    Cannot be accessed	    7		nan
# .	    Missing	                5764	nan

ROOT_CODINGS = {
    1:1,
    2:0,
    9: np.nan,
    'nan': np.nan
}

def get_root_caries(df, codings=None):
    if codings is None:
        codings = ROOT_CODINGS
    data = df[['OHXRCAR', 'OHXRRES']]
    return data.applymap(lambda x: codings['nan'] if np.isnan(x) else codings[x]).sum(axis=1)

def get_other_non_carious_restoration(df, codings=None):
    if codings is None:
        codings = ROOT_CODINGS
    data = df[['OHXRCARO', 'OHXRRESO']]
    return data.applymap(lambda x: codings['nan'] if np.isnan(x) else codings[x]).sum(axis=1)


def preprocess_dental_data():
    df = get_data()
    data = pd.DataFrame(df['SEQN'])
    data['ANTERIOR_TOOTH_COUNT'] = get_tooth_count(df, ANTERIOR)
    data['POSTERIOR_TOOTH_COUNT'] = get_tooth_count(df, POSTERIOR)
    data['ANTERIOR_CARIES_COUNT'] = get_caries_count(df, ANTERIOR)
    data['POSTERIOR_CARIES_COUNT'] = get_caries_count(df, POSTERIOR)
    data['ANTERIOR_DENTAL_SEALANT_COUNT'] = get_sealant_count(df, ANTERIOR)
    data['POSTERIOR_DENTAL_SEALANT_COUNT'] = get_sealant_count(df, POSTERIOR)
    data['ROOT_CARIES'] = get_root_caries(df)
    data['OTHER_NON_CARIOUS_ROOT_LESION'] = get_other_non_carious_restoration(df)
    return data


if __name__ == "__main__":
    # print(get_tooth_count(get_data(), ANTERIOR))
    # print(get_caries_count(get_data(), ANTERIOR))
    # print(get_sealant_count(get_data(), ANTERIOR))
    print(get_root_caries(get_data()))
    print(get_other_non_carious_restoration(get_data()))
