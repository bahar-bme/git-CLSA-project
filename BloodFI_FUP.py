# -*- coding: utf-8 -*-
"""
Created on Wed Oct 29 22:03:16 2025

@author: mmogh
"""

import pandas as pd
import numpy as np

file_path_BL = 'E:/CLSA/CLSA/data/2310011_UCalgary_RRose_BL/2310011_UCalgary_RRose_BL/2310011_UCalgary_RRose_Baseline_CoPv7.csv'
file_path = r'E:\CLSA\CLSA\data\2310011_UCalgary_RRose_FUP1\2310011_UCalgary_RRose_FUP1\2310011_UCalgary_RRose_FUP1_CoPv5.csv'

# Define specific dtypes for columns to optimize memory
# optimized_dtypes = {
#     'MEDI_DOSE_FRQ_1_COF1': 'int8',
    
# }

required_columns_BL =['entity_id','SEX_ASK_COM']
df_BL = pd.read_csv(file_path_BL, usecols=required_columns_BL)

ColumnNames = pd.read_csv(file_path, nrows=0).columns.tolist()
# print(ColumnNames)
# df = pd.read_csv(file_path, dtype=optimized_dtypes)
FIBloodCount = 21#22
DF = pd.DataFrame()

required_columns =['entity_id','AGE_NMBR_COF1',
                   'BLD_GR_PER_COF1','BLD_Hct_COF1',
                   'BLD_LY_PER_COF1','BLD_MCH_COF1','BLD_Hgb_COF1','BLD_MO_PER_COF1',
                   'BLD_Plt_COF1','BLD_MCV_COF1','BLD_RBC_COF1','BLD_WBC_COF1',
                   'BLD_RDW_COF1','BLD_MPV_COF1','BLD_HBA1c_COF1',
                   'BLD_HSCRP_COF1','BLD_ALB_COF1','BLD_TSH_COF1',
                   'BLD_CREAT_COF1','BLD_FT4_COF1','BLD_FERR_COF1','BLD_CHOL_COF1',
                   'BLD_TRIG_COF1']
#'BLD_VITD_COF1',
df = pd.read_csv(file_path, usecols=required_columns)

df = df.merge(df_BL[['entity_id', 'SEX_ASK_COM']], on='entity_id', how='left')
df = df.replace([-99999,-99991,-88880,-88888,-2222],np.nan)
""""
IsEmpty = df.isna() | (df == "")
DataNA = IsEmpty.sum(axis=1)
RowsToDrop = DataNA.index[DataNA>FIBloodCount*0.2]
df.drop(RowsToDrop, inplace=True)
IsEmpty = df.isna() | (df == "")
DataNA = IsEmpty.sum(axis=1)
NotEmpty = ~IsEmpty
DataAvailable = NotEmpty.sum(axis=1)-3
print(DataAvailable)
"""
#df.loc[df['BLD_GR_PER_COF1'].isin([-99999,-99991,-88880]),'BLD_GR_PER_COF1'] = np.nan
DF["BLD_GR_PER_COF1"] = (df["BLD_GR_PER_COF1"]<45) | (df["BLD_GR_PER_COF1"]>75)    
#df.loc[df['BLD_Hct_COF1'].isin([-99999,-99991,-88880]),'BLD_Hct_COF1'] = np.nan
DF["BLD_Hct_COF1"] = ((df["SEX_ASK_COM"]=="M")&((df['BLD_Hct_COF1']<0.41)|(df['BLD_Hct_COF1']>0.53)))|((df["SEX_ASK_COM"]=='F')&((df['BLD_Hct_COF1']<0.36)|(df['BLD_Hct_COF1']>0.46)))
#df.loc[df['BLD_LY_PER_COF1'].isin([-99999,-99991,-88880]),'BLD_LY_PER_COF1'] = np.nan
DF["BLD_LY_PER_COF1"] = (df["BLD_LY_PER_COF1"]<22) | (df["BLD_LY_PER_COF1"]>44) 
#df.loc[df['BLD_MCH_COF1'].isin([-99999,-99991,-88880]),'BLD_MCH_COF1'] = np.nan
DF["BLD_MCH_COF1"] = (df["BLD_MCH_COF1"]<26) | (df["BLD_MCH_COF1"]>34)
#df.loc[df['BLD_Hgb_COF1'].isin([-99999,-99991,-88880]),'BLD_Hgb_COF1'] = np.nan
DF["BLD_Hgb_COF1"] = ((df["SEX_ASK_COM"]=="M")&((df['BLD_Hgb_COF1']<13.5)|(df['BLD_Hgb_COF1']>18)))|((df["SEX_ASK_COM"]=='F')&((df['BLD_Hgb_COF1']<12)|(df['BLD_Hgb_COF1']>16)))
DF["BLD_MO_PER_COF1"] = (df["BLD_MO_PER_COF1"]>8)
DF["BLD_Plt_COF1"] = (df["BLD_Plt_COF1"]<150) | (df["BLD_Plt_COF1"]>450)
DF["BLD_MCV_COF1"] = (df["BLD_MCV_COF1"]<80) | (df["BLD_MCV_COF1"]>96)
DF["BLD_RBC_COF1"] = ((df["SEX_ASK_COM"]=="M")&((df['BLD_RBC_COF1']<4.5)|(df['BLD_RBC_COF1']>5.9)))|((df["SEX_ASK_COM"]=='F')&((df['BLD_RBC_COF1']<4)|(df['BLD_RBC_COF1']>5.2)))
DF["BLD_WBC_COF1"] = (df["BLD_WBC_COF1"]<1.8) | (df["BLD_WBC_COF1"]>7.8)
DF["BLD_RDW_COF1"] = df["BLD_RDW_COF1"]>14.6
DF["BLD_MPV_COF1"] = (df["BLD_MPV_COF1"]<7) | (df["BLD_MPV_COF1"]>13)
DF["BLD_HBA1c_COF1"] = (df["BLD_HBA1c_COF1"]<3.8) | (df["BLD_HBA1c_COF1"]>6.4)
#DF["BLD_VITD_COF1"] = (df["BLD_VITD_COF1"]<24.9) | (df["BLD_VITD_COF1"]>169.5)
DF["BLD_HSCRP_COF1"] = df["BLD_HSCRP_COF1"]<8
DF["BLD_ALB_COF1"] = (df["BLD_ALB_COF1"]<40) | (df["BLD_ALB_COF1"]>60)
#DF["BLD_EGFR_COF1"] = df["BLD_EGFR_COF1"]<60
DF["BLD_TSH_COF1"] = (df["BLD_TSH_COF1"]<0.5) | (df["BLD_TSH_COF1"]>5)
DF["BLD_CREAT_COF1"] = ((df["SEX_ASK_COM"]=="M")&((df['BLD_CREAT_COF1']<60)|(df['BLD_CREAT_COF1']>110)))|((df["SEX_ASK_COM"]=='F')&((df['BLD_CREAT_COF1']<45)|(df['BLD_CREAT_COF1']>90)))
DF["BLD_FT4_COF1"] = df["BLD_FT4_COF1"]>23.2
DF["BLD_FERR_COF1"] = ((df["SEX_ASK_COM"]=="M")&((df['BLD_FERR_COF1']<20)|(df['BLD_FERR_COF1']>250)))|((df["SEX_ASK_COM"]=='F')&((df['BLD_FERR_COF1']<10)|(df['BLD_FERR_COF1']>120)))
DF["BLD_CHOL_COF1"] = (df["BLD_CHOL_COF1"]<3.9) | (df["BLD_CHOL_COF1"]>6.5)
DF["BLD_TRIG_COF1"] = ((df["SEX_ASK_COM"]=="M")&((df['BLD_TRIG_COF1']<0.45)|(df['BLD_TRIG_COF1']>1.81)))|((df["SEX_ASK_COM"]=='F')&((df['BLD_TRIG_COF1']<0.36)|(df['BLD_TRIG_COF1']>1.12)))

print(DF)
RAWDF=DF
IsEmpty = DF.isna() | (DF == "")
DataNA = IsEmpty.sum(axis=1)
RowsToDrop = DataNA.index[DataNA>FIBloodCount*0.2]
DF.drop(RowsToDrop, inplace=True)
IsEmpty = DF.isna() | (DF == "")
NotEmpty = ~IsEmpty
DataAvailable = NotEmpty.sum(axis=1)
#print(DataAvailable)

DeficitsCount = DF.sum(axis=1)
FIBlood = DeficitsCount/DataAvailable
FIBloodData = df[['entity_id','AGE_NMBR_COF1', 'SEX_ASK_COM']].copy()
FIBloodData['FI_blood'] = FIBlood
FIBloodData.loc[:,'FI_blood'] = FIBlood


from pathlib import Path

# Define the folder and file name
output_file = Path(r"E:\CLSA\CLSA\results\FIBlood_FUP.xlsx")

# Create the folder automatically if it is missing
output_file.parent.mkdir(parents=True, exist_ok=True)

# Save the DataFrame
FIBloodData.to_excel(output_file, index=False)

