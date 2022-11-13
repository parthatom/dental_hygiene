import pandas as pd
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

    df_dietary = pd.read_sas(dietary_path if os.path.exists(dietary_path) else dietary_url)
    df_nutrition = pd.read_sas(nutrition_path if os.path.exists(nutrition_path) else nutrition_url)
    df_dental = pd.read_sas(dental_path if os.path.exists(dental_path) else dental_url)

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
    df_data.update(df_data[['OHXRCAR', 'OHXRCARO', 'OHXRRES', 'OHXRRESO']].fillna(0))

    df_data = df_data.dropna()

    return df_data
