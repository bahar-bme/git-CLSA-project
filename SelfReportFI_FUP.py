import pandas as pd
import numpy as np

DF = pd.DataFrame()
file_path_BL = 'E:/CLSA/CLSA/data/2310011_UCalgary_RRose_BL/2310011_UCalgary_RRose_BL/2310011_UCalgary_RRose_Baseline_CoPv7.csv'
file_path = r'E:\CLSA\CLSA\data\2310011_UCalgary_RRose_FUP1\2310011_UCalgary_RRose_FUP1\2310011_UCalgary_RRose_FUP1_CoPv5.csv'

# Define specific dtypes for columns to optimize memory
# optimized_dtypes = {
#     'MEDI_DOSE_FRQ_1_COF1': 'int8',
    
# }

required_columns_BL =['entity_id','SEX_ASK_COM']
df_BL = pd.read_csv(file_path_BL, usecols=required_columns_BL)

ColumnNames = pd.read_csv(file_path, nrows=0).columns.tolist()
#print(ColumnNames)
#print(df['entity_id'])
# df = pd.read_csv(file_path, dtype=optimized_dtypes)
FISelfRedportCount = 51;DF = pd.DataFrame()

required_columns =['entity_id','AGE_NMBR_COF1',
                   'GEN_HLTH_COF1','VIS_SGHT_COF1','HRG_HRG_COF1',
                   'CCC_OAKNEE_COF1','CCC_OAHAND_COF1','CCC_OAHIP_COF1',
                   'CCC_RA_COF1','CCC_COPD_COF1','CCC_HBP_COF1','DIA_DIAB_COF1',
                   'CCC_HEART_COF1','CCC_ANGI_COF1','CCC_AMI_COF1','CCC_PVD_COF1',
                   'CCC_TIA_COF1','CCC_CVA_COF1','CCC_MEMPB_COF1','CCC_ALZH_COF1',
                   'CCC_PARK_COF1','CCC_ULCR_COF1','CCC_IBDIBS_COF1','CCC_BOWINC_COF1',
                   'ADL_INCNT_COF1','ICQ_CATRCT_COF1','ICQ_GLAUC_COF1','CCC_MACDEG_COF1',
                   'CCC_OSTPO_COF1','CCC_CANC_COF1','CCC_BCKP_COF1','CCC_UTHYR_COF1',
                   'CCC_OTHYR_COF1','CCC_KIDN_COF1','CCC_DRPNEU_COF1','CCC_DRUTI_COF1',
                   'FAL_NMBR_NB_COF1','ADL_ABLDR_COF1','ADL_ABLAP_COF1','ADL_ABLWK_COF1',
                   'ADL_ABLBD_COF1','ADL_ABLBT_COF1','IAL_ABLTEL_COF1','IAL_ABLTRV_COF1',
                   'IAL_ABLGRO_COF1','IAL_ABLML_COF1','IAL_ABLWRK_COF1','IAL_ABLMED_COF1',
                   'IAL_ABLMO_COF1','COG_AFT_SCORE_1_COF1','COG_AFT_SCORE_2_COF1',
                   'COG_REYI_SCORE_COF1','COG_REYII_SCORE_COF1','DEP_FFRT_COF1','DEP_LONLY_COF1',
                   'DEP_GTGO_COF1']

df = pd.read_csv(file_path, usecols=required_columns)
df = df.merge(df_BL[['entity_id', 'SEX_ASK_COM']], on='entity_id', how='left')
""""
IsEmpty = df.isna() | (df == "")
DataNA = IsEmpty.sum(axis=1)
RowsToDrop = DataNA.index[DataNA>FIBloodCount*0.2]
df.drop(RowsToDrop, inplace=True)
IsEmpty = df.isna() | (df == "")
DataNA = IsEmpty.sum(axis=1)
NotEmpty = ~IsEmpty
DataAvailable = NotEmpty.sum(axis=1)-3
#print(DataAvailable)
"""
#df["GEN_HLTH_COF1"].loc[df["GEN_HLTH_COF1"]==8] = np.nan
#df["GEN_HLTH_COF1"].loc[df["GEN_HLTH_COF1"]==9] = np.nan
df.loc[df['GEN_HLTH_COF1'].isin([8,9]),'GEN_HLTH_COF1'] = np.nan
DF['Health'] = (df['GEN_HLTH_COF1']-1)/4

#df["VIS_SGHT_COF1"].loc[df["VIS_SGHT_COF1"]==8] = np.nan
#df["VIS_SGHT_COF1"].loc[df["VIS_SGHT_COF1"]==9] = np.nan
df.loc[df['VIS_SGHT_COF1'].isin([8,9]),'VIS_SGHT_COF1'] = np.nan
DF['Vision'] = (df['VIS_SGHT_COF1']-1)/4

#df["HRG_HRG_COF1"].loc[(df["HRG_HRG_COF1"]==8)|(df["HRG_HRG_COF1"]==9)] = np.nan
df.loc[df['HRG_HRG_COF1'].isin([8,9]),'HRG_HRG_COF1'] = np.nan
DF['Hearing'] = (df['HRG_HRG_COF1']-1)/4

#df["CCC_OAKNEE_COF1"].loc[(df["CCC_OAKNEE_COF1"]==8)|(df["CCC_OAKNEE_COF1"]==9)] = np.nan
#df["CCC_OAHAND_COF1"].loc[(df["CCC_OAHAND_COF1"]==8)|(df["CCC_OAHAND_COF1"]==9)] = np.nan
#df["CCC_OAHIP_COF1"] .loc[(df["CCC_OAHIP_COF1"] ==8)|(df["CCC_OAHIP_COF1"] ==9)] = np.nan

df.loc[~df['CCC_OAKNEE_COF1'].isin([1,2]),'CCC_OAKNEE_COF1'] = np.nan
df.loc[~df['CCC_OAHAND_COF1'].isin([1,2]),'CCC_OAHAND_COF1'] = np.nan
df.loc[~df['CCC_OAHIP_COF1'].isin([1,2]),'CCC_OAHIP_COF1']   = np.nan

df['CCC_OAKNEE_COF1']=2-df['CCC_OAKNEE_COF1']
df['CCC_OAHAND_COF1']=2-df['CCC_OAHAND_COF1']
df['CCC_OAHIP_COF1']=2-df['CCC_OAHIP_COF1']
df['Osteoarthritis'] = df[['CCC_OAKNEE_COF1','CCC_OAHAND_COF1','CCC_OAHIP_COF1']].sum(axis=1 , min_count=1)
DF['Osteoarthritis'] = df['Osteoarthritis'].gt(0).astype(int)
#df["CCC_RA_COF1"] .loc[(df["CCC_RA_COF1"] ==8)|(df["CCC_RA_COF1"] ==9)] = np.nan
df.loc[~df['CCC_RA_COF1'].isin([1,2]),'CCC_RA_COF1'] = np.nan
DF['Arthritis']=2-df['CCC_RA_COF1']

#df["DIA_DIAB_COF1"] .loc[(df["DIA_DIAB_COF1"] ==8)|(df["DIA_DIAB_COF1"] ==9)] = np.nan
df.loc[~df['DIA_DIAB_COF1'].isin([1,2]),'DIA_DIAB_COF1'] = np.nan
DF['Diabetes_mellitus']=2-df['DIA_DIAB_COF1']

# Cardiovascular
#df["CCC_COPD_COF1"] .loc[(df["CCC_COPD_COF1"] ==8)|(df["CCC_COPD_COF1"] ==9)] = np.nan
df.loc[~df['CCC_COPD_COF1'].isin([1,2]),'CCC_COPD_COF1'] = np.nan
DF['Chronic_obstructive_pulmonary_disease']=2-df['CCC_COPD_COF1']

#df["CCC_HBP_COF1"] .loc[(df["CCC_HBP_COF1"] ==8)|(df["CCC_HBP_COF1"] ==9)] = np.nan
df.loc[~df['CCC_HBP_COF1'].isin([1,2]),'CCC_HBP_COF1'] = np.nan
DF['High_blood_pressure']=2-df['CCC_HBP_COF1']

#df["CCC_HEART_COF1"] .loc[(df["CCC_HEART_COF1"] ==8)|(df["CCC_HEART_COF1"] ==9)] = np.nan
df.loc[~df['CCC_HEART_COF1'].isin([1,2]),'CCC_HEART_COF1'] = np.nan
DF['Chronic_heart_failure']=2-df['CCC_HEART_COF1']

#df["CCC_ANGI_COF1"] .loc[(df["CCC_ANGI_COF1"] ==8)|(df["CCC_ANGI_COF1"] ==9)] = np.nan
df.loc[~df['CCC_ANGI_COF1'].isin([1,2]),'CCC_ANGI_COF1'] = np.nan
DF['Angina']=2-df['CCC_ANGI_COF1']

#df["CCC_AMI_COF1"] .loc[(df["CCC_AMI_COF1"] ==8)|(df["CCC_AMI_COF1"] ==9)] = np.nan
df.loc[~df['CCC_AMI_COF1'].isin([1,2]),'CCC_AMI_COF1'] = np.nan
DF['Acute_myocardial_infarction']=2-df['CCC_AMI_COF1']

#df["CCC_PVD_COF1"] .loc[(df["CCC_PVD_COF1"] ==8)|(df["CCC_PVD_COF1"] ==9)] = np.nan
df.loc[~df['CCC_PVD_COF1'].isin([1,2]),'CCC_PVD_COF1'] = np.nan
DF['Peripheral_vascular_disease']=2-df['CCC_PVD_COF1']

#df["CCC_CVA_COF1"] .loc[(df["CCC_CVA_COF1"] ==8)|(df["CCC_CVA_COF1"] ==9)] = np.nan
df.loc[~df['CCC_CVA_COF1'].isin([1,2]),'CCC_CVA_COF1'] = np.nan
DF['Stroke']=2-df['CCC_CVA_COF1']

#df["CCC_TIA_COF1"] .loc[(df["CCC_TIA_COF1"] ==8)|(df["CCC_TIA_COF1"] ==9)] = np.nan
df.loc[~df['CCC_TIA_COF1'].isin([1,2]),'CCC_TIA_COF1'] = np.nan
DF['Transient_ischemic_attack']=2-df['CCC_TIA_COF1']

#Brain

#df["CCC_MEMPB_COF1"] .loc[(df["CCC_MEMPB_COF1"] ==8)|(df["CCC_MEMPB_COF1"] ==9)] = np.nan
df.loc[~df['CCC_MEMPB_COF1'].isin([1,2]),'CCC_MEMPB_COF1'] = np.nan
DF['Memory_problem']=2-df['CCC_MEMPB_COF1']

#df["CCC_ALZH_COF1"] .loc[(df["CCC_ALZH_COF1"] ==8)|(df["CCC_ALZH_COF1"] ==9)] = np.nan
df.loc[~df['CCC_ALZH_COF1'].isin([1,2]),'CCC_ALZH_COF1'] = np.nan
DF['Alzheimer_disease']=2-df['CCC_ALZH_COF1']

#df["CCC_PARK_COF1"] .loc[(df["CCC_PARK_COF1"] ==8)|(df["CCC_PARK_COF1"] ==9)] = np.nan
df.loc[~df['CCC_PARK_COF1'].isin([1,2]),'CCC_PARK_COF1'] = np.nan
DF['Parkinson_disease']=2-df['CCC_PARK_COF1']

#Gatrointestin
#df["CCC_ULCR_COF1"] .loc[(df["CCC_ULCR_COF1"] ==8)|(df["CCC_ULCR_COF1"] ==9)] = np.nan
df.loc[~df['CCC_ULCR_COF1'].isin([1,2]),'CCC_ULCR_COF1'] = np.nan
DF['Peptic_ulcer_diseae']=2-df['CCC_ULCR_COF1']

#df["CCC_IBDIBS_COF1"] .loc[(df["CCC_IBDIBS_COF1"] ==8)|(df["CCC_IBDIBS_COF1"] ==9)] = np.nan
df.loc[~df['CCC_IBDIBS_COF1'].isin([1,2]),'CCC_IBDIBS_COF1'] = np.nan
DF['Colitis']=2-df['CCC_IBDIBS_COF1']

#df["CCC_BOWINC_COF1"] .loc[(df["CCC_BOWINC_COF1"] ==8)|(df["CCC_BOWINC_COF1"] ==9)] = np.nan
df.loc[~df['CCC_BOWINC_COF1'].isin([1,2]),'CCC_BOWINC_COF1'] = np.nan
DF['Bowel_incontinence']=2-df['CCC_BOWINC_COF1']

#df["ADL_INCNT_COF1"].loc[(df["ADL_INCNT_COF1"]==8)|(df["ADL_INCNT_COF1"]==9)] = np.nan
df.loc[~df['ADL_INCNT_COF1'].isin([1,2,3]),'ADL_INCNT_COF1'] = np.nan
DF['Urinary_incontinence'] = (df['ADL_INCNT_COF1']-1)/2

#vision
#df["ICQ_CATRCT_COF1"] .loc[(df["ICQ_CATRCT_COF1"] ==8)|(df["ICQ_CATRCT_COF1"] ==9)] = np.nan
df.loc[~df['ICQ_CATRCT_COF1'].isin([1,2]),'ICQ_CATRCT_COF1'] = np.nan
DF['Cataract']=2-df['ICQ_CATRCT_COF1']

#df["ICQ_GLAUC_COF1"] .loc[(df["ICQ_GLAUC_COF1"] ==8)|(df["ICQ_GLAUC_COF1"] ==9)] = np.nan
df.loc[~df['ICQ_GLAUC_COF1'].isin([1,2]),'ICQ_GLAUC_COF1'] = np.nan
DF['Glaucoma']=2-df['ICQ_GLAUC_COF1']

#df["CCC_MACDEG_COF1"] .loc[(df["CCC_MACDEG_COF1"] ==8)|(df["CCC_MACDEG_COF1"] ==9)] = np.nan
df.loc[~df['CCC_MACDEG_COF1'].isin([1,2]),'CCC_MACDEG_COF1'] = np.nan
DF['Macular_degeneration']=2-df['CCC_MACDEG_COF1']

#Cancer
#df["CCC_CANC_COF1"] .loc[(df["CCC_CANC_COF1"] ==8)|(df["CCC_CANC_COF1"] ==9)] = np.nan
df.loc[~df['CCC_CANC_COF1'].isin([1,2]),'CCC_CANC_COF1'] = np.nan
DF['Cancer']=2-df['CCC_CANC_COF1']

#Orthopedic
#df["CCC_OSTPO_COF1"] .loc[(df["CCC_OSTPO_COF1"] ==8)|(df["CCC_OSTPO_COF1"] ==9)] = np.nan
df.loc[~df['CCC_OSTPO_COF1'].isin([1,2]),'CCC_OSTPO_COF1'] = np.nan
DF['Osteoporosis']=2-df['CCC_OSTPO_COF1']

#df["CCC_BCKP_COF1"] .loc[(df["CCC_BCKP_COF1"] ==8)|(df["CCC_BCKP_COF1"] ==9)] = np.nan
df.loc[~df['CCC_BCKP_COF1'].isin([1,2]),'CCC_BCKP_COF1'] = np.nan
DF['Back_pain']=2-df['CCC_BCKP_COF1']

#Internal
#df["CCC_UTHYR_COF1"] .loc[(df["CCC_UTHYR_COF1"] ==8)|(df["CCC_UTHYR_COF1"] ==9)] = np.nan
df.loc[~df['CCC_UTHYR_COF1'].isin([1,2]),'CCC_UTHYR_COF1'] = np.nan
DF['Hypothyroidism']=2-df['CCC_UTHYR_COF1']

#df["CCC_OTHYR_COF1"] .loc[(df["CCC_OTHYR_COF1"] ==8)|(df["CCC_OTHYR_COF1"] ==9)] = np.nan
df.loc[~df['CCC_OTHYR_COF1'].isin([1,2]),'CCC_OTHYR_COF1'] = np.nan
DF['Hyperthyroidism']=2-df['CCC_OTHYR_COF1']

#df["CCC_KIDN_COF1"] .loc[(df["CCC_KIDN_COF1"] ==8)|(df["CCC_KIDN_COF1"] ==9)] = np.nan
df.loc[~df['CCC_KIDN_COF1'].isin([1,2]),'CCC_KIDN_COF1'] = np.nan
DF['Kidney_failure']=2-df['CCC_KIDN_COF1']

#df["CCC_DRPNEU_COF1"] .loc[(df["CCC_DRPNEU_COF1"] ==8)|(df["CCC_DRPNEU_COF1"] ==9)] = np.nan
df.loc[~df['CCC_DRPNEU_COF1'].isin([1,2]),'CCC_DRPNEU_COF1'] = np.nan
DF['Pneumonia']=2-df['CCC_DRPNEU_COF1']

#df["CCC_DRUTI_COF1"] .loc[(df["CCC_DRUTI_COF1"] ==8)|(df["CCC_DRUTI_COF1"] ==9)] = np.nan
df.loc[~df['CCC_DRUTI_COF1'].isin([1,2]),'CCC_DRUTI_COF1'] = np.nan
DF['Urinary_tract_infection']=2-df['CCC_DRUTI_COF1']

#ADL
df.loc[df["FAL_NMBR_NB_COF1"].isin([98, 99,-99999,-88888]), "FAL_NMBR_NB_COF1"] = np.nan
#df["FAL_NMBR_NB_COF1"].loc[(df["FAL_NMBR_NB_COF1"]==98)|(df["FAL_NMBR_NB_COF1"]==99)] = np.nan
MaxFall = df['FAL_NMBR_NB_COF1'].max()
DF['Falls'] = (df['FAL_NMBR_NB_COF1'])/MaxFall

df.loc[~df['ADL_ABLDR_COF1'].isin([1,2]),'ADL_ABLDR_COF1'] = np.nan
DF['Dressing'] = df['ADL_ABLDR_COF1']-1

df.loc[~df['ADL_ABLAP_COF1'].isin([1,2]),'ADL_ABLAP_COF1'] = np.nan
DF['Grooming'] = df['ADL_ABLAP_COF1']-1

df.loc[~df['ADL_ABLWK_COF1'].isin([1,2]),'ADL_ABLWK_COF1'] = np.nan
DF['Walking'] = df['ADL_ABLWK_COF1']-1

df.loc[~df['ADL_ABLBD_COF1'].isin([1,2]),'ADL_ABLBD_COF1'] = np.nan
DF['Getting_in_out_bed'] = df['ADL_ABLBD_COF1']-1

df.loc[~df['ADL_ABLBT_COF1'].isin([1,2]),'ADL_ABLBT_COF1'] = np.nan
DF['Bathing'] = df['ADL_ABLBT_COF1']-1

df.loc[~df['IAL_ABLTEL_COF1'].isin([1,2]),'IAL_ABLTEL_COF1'] = np.nan
DF['Phone'] = df['IAL_ABLTEL_COF1']-1

df.loc[~df['IAL_ABLTRV_COF1'].isin([1,2]),'IAL_ABLTRV_COF1'] = np.nan
DF['Transport'] = df['IAL_ABLTRV_COF1']-1

df.loc[~df['IAL_ABLGRO_COF1'].isin([1,2]),'IAL_ABLGRO_COF1'] = np.nan
DF['Shopping'] = df['IAL_ABLGRO_COF1']-1

df.loc[~df['IAL_ABLML_COF1'].isin([1,2]),'IAL_ABLML_COF1'] = np.nan
DF['Cooking'] = df['IAL_ABLML_COF1'] -1

df.loc[~df['IAL_ABLWRK_COF1'].isin([1,2]),'IAL_ABLWRK_COF1'] = np.nan
DF['Housework'] = df['IAL_ABLWRK_COF1']-1

df.loc[~df['IAL_ABLMED_COF1'].isin([1,2]),'IAL_ABLMED_COF1'] = np.nan
DF['Medicine'] = df['IAL_ABLMED_COF1'] -1

df.loc[~df['IAL_ABLMO_COF1'].isin([1,2]),'IAL_ABLMO_COF1'] = np.nan
DF['Money'] = df['IAL_ABLMO_COF1']-1

# Cognition

#DF['Mental_alternation_test']
df.loc[df['COG_AFT_SCORE_1_COF1'].isin([-88888,-99999]),'COG_AFT_SCORE_1_COF1'] = np.nan
df.loc[df['COG_AFT_SCORE_2_COF1'].isin([-88888,-99999]),'COG_AFT_SCORE_2_COF1'] = np.nan
DF['Animal_Recall'] = ((1-(df['COG_AFT_SCORE_1_COF1']/df['COG_AFT_SCORE_1_COF1'].max())) + 
                       (1-(df['COG_AFT_SCORE_2_COF1']/df['COG_AFT_SCORE_2_COF1'].max())))/2

df.loc[df['COG_REYI_SCORE_COF1'].isin([-88888,-99999]),'COG_REYI_SCORE_COF1'] = np.nan
DF['immediate_Recall'] = 1-(df['COG_REYI_SCORE_COF1']/df['COG_REYI_SCORE_COF1'].max())

df.loc[df['COG_REYII_SCORE_COF1'].isin([-88888,-99999]),'COG_REYII_SCORE_COF1'] = np.nan
DF['Delayed_Recall'] = 1-(df['COG_REYII_SCORE_COF1']/df['COG_REYII_SCORE_COF1'].max())

# Mental Health
df.loc[df['DEP_FFRT_COF1'].isin([8,9,-88888,-88880]),'DEP_FFRT_COF1'] = np.nan
DF['Effort'] = (4-df['DEP_FFRT_COF1'])/3

df.loc[df['DEP_LONLY_COF1'].isin([8,9,-88888,-88880]),'DEP_LONLY_COF1'] = np.nan
DF['Felt_Lonely'] = (4-df['DEP_LONLY_COF1'])/3


df.loc[df['DEP_GTGO_COF1'].isin([8,9,-88888,-88880]),'DEP_GTGO_COF1'] = np.nan
DF['Get_Going'] = (4-df['DEP_GTGO_COF1'])/3

print(DF)


RAWDF=DF
IsEmpty = DF.isna() | (DF == "")
DataNA = IsEmpty.sum(axis=1)
RowsToDrop = DataNA.index[DataNA>FISelfRedportCount*0.2]
DF.drop(RowsToDrop, inplace=True)
IsEmpty = DF.isna() | (DF == "")
NotEmpty = ~IsEmpty
DataAvailable = NotEmpty.sum(axis=1)

print(DataAvailable)
print(DF.dtypes)

DeficitsCount = DF.sum(axis=1)
FISelfReport = DeficitsCount/DataAvailable
FISelfReportData = df[['entity_id','AGE_NMBR_COF1','SEX_ASK_COM']].copy()
#FISelfReportData['FI_SelfReport'] = FISelfReport
FISelfReportData.loc[:,'FI_SelfReport'] = FISelfReport

from pathlib import Path

# Define the folder and file name
#output_file = Path(r"E:\CLSA\CLSA\results\FISelfReport_BL.xlsx")
output_file = Path(r"E:\CLSA\CLSA\results\FISelfReport_FUP.xlsx")

# Create the folder automatically if it is missing
output_file.parent.mkdir(parents=True, exist_ok=True)

# Save the DataFrame
FISelfReportData.to_excel(output_file, index=False)
