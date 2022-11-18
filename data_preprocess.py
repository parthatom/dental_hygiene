import pandas as pd
import numpy as np
import os


def preprocess(
        dietary_url='https://wwwn.cdc.gov/Nchs/Nhanes/2017-2018/P_DSQTOT.XPT',
        nutrition_url='https://wwwn.cdc.gov/Nchs/Nhanes/2017-2018/P_DR1TOT.XPT',
        dental_url='https://wwwn.cdc.gov/Nchs/Nhanes/2017-2018/P_OHXDEN.XPT'):
    '''
    @description: 
        Pre-process the Dietary Supplement, Nutrient Intakes, and Dental Health data
    @param: 
        URLs of the three data
    @return: 
        Pre-processed Pandas DataFrame
    '''
    # please be patient for data download
    dietary_path = './dataset/P_DR1TOT.XPT'
    nutrition_path = './dataset/P_DSQTOT.XPT'
    dental_path = './dataset/P_OHXDEN.XPT'

    df_dietary = pd.read_sas(
        dietary_path if os.path.exists(dietary_path) else dietary_url)
    df_nutrition = pd.read_sas(nutrition_path if os.path.exists(
        nutrition_path) else nutrition_url)
    df_dental = pd.read_sas(
        dental_path if os.path.exists(dental_path) else dental_url)

    df_data = pd.merge(df_dietary, df_nutrition, on='SEQN')
    df_data = pd.merge(df_data, df_dental, on='SEQN')

    # fill the missing precise quantatative or special dietary data with 0
    attrs_set_0 = ['DR1SKY']
    for attr in df_data.columns:
        if attr.startswith('DSQ') or attr.startswith('DRQS') or attr.startswith('DRD'):
            attrs_set_0.append(attr)
    df_data[attrs_set_0] = df_data[attrs_set_0].fillna(0)

    # drop Coronal Caries and Sealants attributes from dental data
    attrs_keep = []
    for attr in df_data.columns:
        if not (attr.startswith('OHX') and (attr.endswith('CTC') or attr.endswith('CSC')
                or attr.endswith('RTC') or attr.endswith('RSC') or attr.endswith('SE'))):
            attrs_keep.append(attr)
    df_data = df_data[attrs_keep]

    # fill missing "dental implant or not?" with "no"
    df_data.loc[:, 'OHXIMP'].fillna(2, inplace=True)
    # fill missing "how often add salt?" with "don't know"
    df_data.loc[:, 'DBD100'].fillna(9, inplace=True)

    # fill missing "Root Caries, Non-carious Lesion, Root Caries Restoration, Non-carious Lesion Restoration" with "not detected"
    df_data.update(
        df_data[['OHXRCAR', 'OHXRCARO', 'OHXRRES', 'OHXRRESO']].fillna(0))

    # Change 'Refused'/'Don't know'/'Incomplete' to either appropriate value or NaN
    df_data.loc[df_data['WTDRD1PP'] == 0, 'WTDRD1PP'] = np.NaN      # incomplete -> NaN
    df_data.loc[df_data['WTDR2DPP'] == 0, 'WTDR2DPP'] = np.NaN      # incomplete -> NaN
    df_data.loc[df_data['DR1DRSTZ'] == 5, 'DR1DRSTZ'] = 1           # incomplete -> meet minimum criteria
    df_data.loc[df_data['DR1MRESP'] >= 77, 'DR1MRESP'] = np.NaN     # Refused/dont know -> NaN
    df_data.loc[df_data['DR1HELP'] >= 77, 'DR1HELP'] = np.NaN       # Refused/dont know -> NaN
    df_data.loc[df_data['DBQ095Z'] == 99, 'DBQ095Z'] = np.NaN       # Refused/dont know -> NaN
    df_data.loc[df_data['DBD100'] >= 7, 'DBD100'] = np.NaN          # Refused/dont know -> NaN
    df_data.loc[(df_data['DRQSPREP'] == 9) | (df_data['DRQSPREP'] == 0), 'DRQSPREP'] = np.NaN   # Refused/dont know -> NaN
    df_data.loc[df_data['DR1STY'] == 9, 'DR1STY'] = 2               # Refused/dont know -> 2
    df_data.loc[(df_data['DRQSDIET'] == 9) | (df_data['DRQSDIET'] == 0), 'DRQSDIET'] = 2        # Refused/dont know -> 2
    df_data.loc[df_data['DR1_300'] >= 7, 'DR1_300'] = 2             # Refused/dont know -> 2
    df_data.loc[df_data['DR1TWSZ'] == 99, 'DR1TWSZ'] = np.NaN       # Refused/dont know -> NaN

    df_data.loc[df_data['DSDCOUNT'] >= 77, 'DSDCOUNT'] = 0          # Refused/dont know -> 0
    df_data.loc[df_data['DSDANCNT'] >= 77, 'DSDANCNT'] = 0          # Refused/dont know -> 0
    df_data.loc[df_data['DSD010'] >= 7, 'DSD010'] = 2               # Refused/dont know -> 2
    df_data.loc[df_data['DSD010AN'] >= 7, 'DSD010AN'] = 2           # Refused/dont know -> 2

    df_data = df_data.dropna()

    # Change categorical data to categorical columns
    cat_attrs = [
        'DR1DRSTZ', 'DRABF', 'DRDINT', 'DR1DAY', 'DR1LANG', 'DR1MRESP', 'DR1HELP', 'DBQ095Z',
        'DBD100', 'DRQSPREP', 'DR1STY', 'DR1SKY', 'DRQSDIET', 'DR1_300', 'DR1TWSZ'
    ]
    for attr in df_data.columns:
        if attr.startswith('DRQSDT'):
            cat_attrs.append(attr)
    for attr in cat_attrs:
        df_data[attr] = pd.Categorical(df_data[attr])

    return df_data



if __name__ == '__main__':
    df_data = preprocess()