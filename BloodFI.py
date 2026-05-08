# -*- coding: utf-8 -*-
"""
Created on Wed Oct 29 22:03:16 2025

@author: mmogh
"""

import pandas as pd

file_path = 'E:/CLSA/CLSA/data/2310011_UCalgary_RRose_BL/2310011_UCalgary_RRose_BL/2310011_UCalgary_RRose_Baseline_CoPv7.csv'
# Define specific dtypes for columns to optimize memory
# optimized_dtypes = {
#     'MEDI_DOSE_FRQ_1_COF1': 'int8',
    
# }
ColumnNames = pd.read_csv(file_path, nrows=0).columns.tolist()
print(ColumnNames)
# df = pd.read_csv(file_path, dtype=optimized_dtypes)
FIBlood = 22;DF = pd.DataFrame()

required_columns =['entity_id','AGE_NMBR_COM',
                   'SEX_ASK_COM','BLD_GR_PER_COM','BLD_Hct_COM',
                   'BLD_LY_PER_COM','BLD_MCH_COM','BLD_Hgb_COM','BLD_MO_PER_COM',
                   'BLD_Plt_COM','BLD_MCV_COM','BLD_RBC_COM','BLD_WBC_COM',
                   'BLD_RDW_COM','BLD_MPV_COM','BLD_HBA1c_COM','BLD_VITD_COM',
                   'BLD_HSCRP_COM','BLD_ALB_COM','BLD_TSH_COM',
                   'BLD_CREAT_COM','BLD_FT4_COM','BLD_FERR_COM','BLD_CHOL_COM',
                   'BLD_TRIG_COM']

df = pd.read_csv(file_path, usecols=required_columns)
IsEmpty = df.isna() | (df == "")
DataNA = IsEmpty.sum(axis=1)
RowsToDrop = DataNA.index[DataNA>FIBlood*0.2]
df.drop(RowsToDrop, inplace=True)
IsEmpty = df.isna() | (df == "")
DataNA = IsEmpty.sum(axis=1)
NotEmpty = ~IsEmpty
DataAvailable = NotEmpty.sum(axis=1)-3
DF["BLD_GR_PER_COM"] = (df["BLD_GR_PER_COM"]<45) | (df["BLD_GR_PER_COM"]>75)    
DF["BLD_Hct_COM"] = ((df["SEX_ASK_COM"]=="M")&((df['BLD_Hct_COM']<0.41)|(df['BLD_Hct_COM']>0.53)))|((df["SEX_ASK_COM"]=='F')&((df['BLD_Hct_COM']<0.36)|(df['BLD_Hct_COM']>0.46)))
DF["BLD_LY_PER_COM"] = (df["BLD_LY_PER_COM"]<22) | (df["BLD_LY_PER_COM"]>44) 
DF["BLD_MCH_COM"] = (df["BLD_MCH_COM"]<26) | (df["BLD_MCH_COM"]>34)
DF["BLD_Hgb_COM"] = ((df["SEX_ASK_COM"]=="M")&((df['BLD_Hgb_COM']<13.5)|(df['BLD_Hgb_COM']>18)))|((df["SEX_ASK_COM"]=='F')&((df['BLD_Hgb_COM']<12)|(df['BLD_Hgb_COM']>16)))
DF["BLD_MO_PER_COM"] = (df["BLD_MO_PER_COM"]>8)
DF["BLD_Plt_COM"] = (df["BLD_Plt_COM"]<150) | (df["BLD_Plt_COM"]>450)
DF["BLD_MCV_COM"] = (df["BLD_MCV_COM"]<80) | (df["BLD_MCV_COM"]>96)
DF["BLD_RBC_COM"] = ((df["SEX_ASK_COM"]=="M")&((df['BLD_RBC_COM']<4.5)|(df['BLD_RBC_COM']>5.9)))|((df["SEX_ASK_COM"]=='F')&((df['BLD_RBC_COM']<4)|(df['BLD_RBC_COM']>5.2)))
DF["BLD_WBC_COM"] = (df["BLD_WBC_COM"]<1.8) | (df["BLD_WBC_COM"]>7.8)
DF["BLD_RDW_COM"] = df["BLD_RDW_COM"]>14.6
DF["BLD_MPV_COM"] = (df["BLD_MPV_COM"]<7) | (df["BLD_MPV_COM"]>13)
DF["BLD_HBA1c_COM"] = (df["BLD_HBA1c_COM"]<3.8) | (df["BLD_HBA1c_COM"]>6.4)
DF["BLD_VITD_COM"] = (df["BLD_VITD_COM"]<24.9) | (df["BLD_VITD_COM"]>169.5)
DF["BLD_HSCRP_COM"] = df["BLD_HSCRP_COM"]<8
DF["BLD_ALB_COM"] = (df["BLD_ALB_COM"]<40) | (df["BLD_ALB_COM"]>60)
#DF["BLD_EGFR_COM"] = df["BLD_EGFR_COM"]<60
DF["BLD_TSH_COM"] = (df["BLD_TSH_COM"]<0.5) | (df["BLD_TSH_COM"]>5)
DF["BLD_CREAT_COM"] = ((df["SEX_ASK_COM"]=="M")&((df['BLD_CREAT_COM']<60)|(df['BLD_CREAT_COM']>110)))|((df["SEX_ASK_COM"]=='F')&((df['BLD_CREAT_COM']<45)|(df['BLD_CREAT_COM']>90)))
DF["BLD_FT4_COM"] = df["BLD_FT4_COM"]>23.2
DF["BLD_FERR_COM"] = ((df["SEX_ASK_COM"]=="M")&((df['BLD_FERR_COM']<20)|(df['BLD_FERR_COM']>250)))|((df["SEX_ASK_COM"]=='F')&((df['BLD_FERR_COM']<10)|(df['BLD_FERR_COM']>120)))
DF["BLD_CHOL_COM"] = (df["BLD_CHOL_COM"]<3.9) | (df["BLD_CHOL_COM"]>6.5)
DF["BLD_TRIG_COM"] = ((df["SEX_ASK_COM"]=="M")&((df['BLD_TRIG_COM']<0.45)|(df['BLD_TRIG_COM']>1.81)))|((df["SEX_ASK_COM"]=='F')&((df['BLD_TRIG_COM']<0.36)|(df['BLD_TRIG_COM']>1.12)))
DeficitsCount = DF.sum(axis=1)
FIBlood = DeficitsCount/DataAvailable
FIBloodData = df[['entity_id','AGE_NMBR_COM', 'SEX_ASK_COM']]
FIBloodData['FI_blood'] = FIBlood
FIBloodData.loc[:,'FI_blood'] = FIBlood