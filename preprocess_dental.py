import pandas as pd
import numpy as np
import os

# Anterior and Posterior Teeth as defined by American Dental Association
# https://radiopaedia.org/articles/american-dental-association-universal-numbering-system?lang=us

ANTERIOR = list(range(6, 12)) + list(range(22, 28))
POSTERIOR = list(range(1, 6)) + list(range(12, 22)) + list(range(28, 33))
ALL_TEETH = ANTERIOR + POSTERIOR

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
    '''
    Get Col Name in data
    @param t: Tooth Number
    @return: Col Name
    '''
    return 'OHX{tooth:02d}TC'.format(tooth=t)


def get_tooth_count(df, tooth_list, codings=None, skipna=True):
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
    return data.applymap(lambda x: codings['nan'] if np.isnan(x) else codings[x]).sum(axis=1, skipna=skipna)


#
# Caries
# Code 	Description	                                                            Count	Cumulative  Convert
# A	    Primary tooth with a restored surface condition	                        0	    0           1
# D	    Sound primary tooth	                                                    0	    0           0
# E	    Missing due to dental disease	                                        1197	1197        1
# F	    Permanent tooth with a restored surface condition	                    2908	4105        1
# J	    Permanent root tip is present but no restorative replacement is present	131	    4236        1
# K	    Primary tooth with a dental carious surface condition	                0	    4236        1
# M	    Missing due to other causes	                                            47	    4283        1
# P	    Missing due to dental disease but replaced by a removable restoration	1019	5302        1
# Q	    Missing due to other causes but replaced by a removable restoration	    37	    5339        1
# R	    Missing due to dental disease but replaced by a fixed restoration	    13	    5352        1
# S	    Sound permanent tooth	                                                4394    9746        0
# T	    Permanent root tip is present but a restorative replacement is present	0	    9746        1
# U	    Unerupted	                                                            3297	13043       nan
# X	    Missing due to other causes but replaced by a fixed restoration	        0	    13043       nan
# Y	    Tooth present, condition cannot be assessed	                            11	    13054       nan
# Z	    Permanent tooth with a dental carious surface condition	                220	    13274       1
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

CARIES_CODINGS_01 = {
    'A': 1,
    'D': 0,
    'E': 1,
    'F': 1,
    'J': 1,
    'K': 1,
    'M': 1,
    'P': 1,
    'Q': 1,
    'R': 1,
    'S': 0,
    'T': 1,
    'U': np.nan,
    'X': np.nan,
    'Y': np.nan,
    'Z': 1,
    'nan': np.nan,
    '': np.nan
}


def get_tooth_caries_col_name(t):
    '''
    Get Caries Col Name in Dataset
    @param t: Tooth Number
    @return: Col name
    '''
    return 'OHX{tooth:02d}CTC'.format(tooth=t)


def del_not_present_cols(l, np):
    l1 = l.copy()
    for x in np:
        if x in l1:
            del l1[l1.index(x)]
    return l1


def get_caries_count(df, tooth_list, codings=None, usage='01', skipna=True):
    """
    Gets tooth count from merging TOOTH_COUNT cols for all teeth in tooth_list
    @param usage: 01 for 01 data
    @param codings:
    @param df: DataFrame
    @type df: pd.DataFrame
    @param tooth_list: ANTERIOR or POSTERIOR
    @return: pd.Series of Tooth Count
    """
    if codings is None:
        codings = CARIES_CODINGS
    if usage == '01':
        codings = CARIES_CODINGS_01
    # No Caries Col for 1,32
    tl = del_not_present_cols(tooth_list, [1, 16, 17, 32])

    cols = list(map(get_tooth_caries_col_name, tl))
    data = df[cols]
    return data.applymap(lambda x: codings[x.decode()]).sum(axis=1, skipna=skipna)


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
    '''
    Get Sealant Col Name in Datset
    @param t: Tooth Number
    @return: Col Name
    '''
    return 'OHX{tooth:02d}SE'.format(tooth=t)


def get_sealant_count(df, tooth_list, codings=None, skipna=True):
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
    return data.applymap(lambda x: codings[''] if not x.decode() else codings[int(x.decode())]).sum(axis=1,
                                                                                                    skipna=skipna)


#   Root Caries, other lesions X [restored , not] Data Description
# Code Description	            Count   Convert
# 1	    Yes	                    1085    1
# 2	    No	                    6916	0
# 9	    Cannot be accessed	    7		nan
# .	    Missing	                5764	nan

ROOT_CODINGS = {
    1: 1,
    2: 0,
    9: np.nan,
    'nan': np.nan
}


def get_root_caries(df, codings=None, skipna=True):
    '''
    Sum Root Caries and Root caries Restorartion
    @param df: Dataset
    @param codings: Converion Matrix
    @param skipna: How to treat NA values
    @return: pd.Series
    '''
    if codings is None:
        codings = ROOT_CODINGS
    data = df[['OHXRCAR', 'OHXRRES']]
    return data.applymap(lambda x: codings['nan'] if np.isnan(x) else codings[x]).sum(axis=1, skipna=skipna)


def get_other_non_carious_restoration(df, codings=None, skipna=True):
    '''
    Sum Other Caries and Other Restorartions
    @param df: Dataset
    @param codings: Converion Matrix
    @param skipna: How to treat NA values
    @return: pd.Series
    '''
    if codings is None:
        codings = ROOT_CODINGS
    data = df[['OHXRCARO', 'OHXRRESO']]
    return data.applymap(lambda x: codings['nan'] if np.isnan(x) else codings[x]).sum(axis=1, skipna=skipna)


def preprocess_dental_data(usage='', set_index=False, skipna=True, drop_all_na=False, drop_any_na=False):
    '''
    Pre Process the Dental Health Data
    @param usage: '01' if using for modelling
    @param set_index: Whether or not to set the SEQN col as index
    @param skipna: How to treat the NA values
    @param drop_all_na: Drop rows with all na values
    @param drop_any_na: Drop rows with any value as na
    @return: pd.DataFrame
    '''
    df = get_data()
    data = pd.DataFrame(df['SEQN'])
    data['ANTERIOR_TOOTH_COUNT'] = get_tooth_count(df, ANTERIOR, skipna=skipna)
    data['POSTERIOR_TOOTH_COUNT'] = get_tooth_count(df, POSTERIOR, skipna=skipna)
    data['TOTAL_TOOTH_COUNT'] = get_tooth_count(df, ALL_TEETH, skipna=skipna)
    data['ANTERIOR_CARIES_COUNT'] = get_caries_count(df, ANTERIOR, usage=usage, skipna=skipna)
    data['POSTERIOR_CARIES_COUNT'] = get_caries_count(df, POSTERIOR, usage=usage, skipna=skipna)
    data['TOTAL_CARIES_COUNT'] = get_caries_count(df, ALL_TEETH, usage=usage, skipna=skipna)
    data['ANTERIOR_DENTAL_SEALANT_COUNT'] = get_sealant_count(df, ANTERIOR, skipna=skipna)
    data['POSTERIOR_DENTAL_SEALANT_COUNT'] = get_sealant_count(df, POSTERIOR, skipna=skipna)
    data['TOTAL_SEALANT_COUNT'] = get_sealant_count(df, ALL_TEETH, skipna=skipna)
    data['ROOT_CARIES'] = get_root_caries(df, skipna=skipna)
    data['OTHER_NON_CARIOUS_ROOT_LESION'] = get_other_non_carious_restoration(df, skipna=skipna)
    if drop_all_na:
        data = data.dropna(subset=['ANTERIOR_CARIES_COUNT', 'POSTERIOR_CARIES_COUNT', 'ANTERIOR_DENTAL_SEALANT_COUNT',
                                   'POSTERIOR_DENTAL_SEALANT_COUNT', 'ROOT_CARIES', 'OTHER_NON_CARIOUS_ROOT_LESION'],
                           how='all')
    if drop_any_na:
        data = data.dropna(subset=['ANTERIOR_CARIES_COUNT', 'POSTERIOR_CARIES_COUNT', 'ANTERIOR_DENTAL_SEALANT_COUNT',
                                   'POSTERIOR_DENTAL_SEALANT_COUNT', 'ROOT_CARIES', 'OTHER_NON_CARIOUS_ROOT_LESION'],
                           how='any')
    if set_index:
        data = data.set_index('SEQN')
    data['ANTERIOR_SIMPLE_01'] = data[get_teeth_subset_labels('ANTERIOR')].max(axis=1).\
        map(lambda x: 1 if x > 0 else 0)
    data['POSTERIOR_SIMPLE_01'] = data[get_teeth_subset_labels('POSTERIOR')].max(axis=1).\
        map(lambda x: 1 if x > 0 else 0)
    data['TOTAL_SIMPLE_01'] = data[get_teeth_subset_labels('')].max(axis=1).\
        map(lambda x: 1 if x > 0 else 0)
    data['SERIOUS_01'] = data.apply(get_serious_01_label, axis=1)
    return data


ANTERIOR_LABELS = ['ANTERIOR_CARIES_COUNT', 'ANTERIOR_DENTAL_SEALANT_COUNT']
POSTERIOR_LABELS = ['POSTERIOR_CARIES_COUNT', 'POSTERIOR_DENTAL_SEALANT_COUNT']
ROOT_LABELS = ['ROOT_CARIES', 'OTHER_NON_CARIOUS_ROOT_LESION']


def get_teeth_subset_labels(teeth_subset):
    if teeth_subset == 'ANTERIOR':
        return ANTERIOR_LABELS + ROOT_LABELS
    if teeth_subset == 'POSTERIOR':
        return POSTERIOR_LABELS + ROOT_LABELS
    return ANTERIOR_LABELS + POSTERIOR_LABELS + ROOT_LABELS


def get_serious_01_label(row):
    for col in ['TOTAL_CARIES_COUNT', 'TOTAL_SEALANT_COUNT', 'OTHER_NON_CARIOUS_ROOT_LESION']:
        if (not np.isnan(row[col])) and row[col] >= 6:
            return 1
    col = 'ROOT_CARIES'
    if (not np.isnan(row[col])) and row[col] > 0:
        return 1
    return 0


if __name__ == "__main__":
    # print(get_tooth_count(get_data(), ANTERIOR))
    # print(get_caries_count(get_data(), ANTERIOR))
    # print(get_sealant_count(get_data(), ANTERIOR))
    # print(get_root_caries(get_data()))
    # print(get_other_non_carious_restoration(get_data()))
    print(preprocess_dental_data(usage='01', set_index=True, drop_all_na=True, skipna=False).describe())
