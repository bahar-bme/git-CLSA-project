import pandas as pd
import numpy as np

DF = pd.DataFrame()
file_path = 'E:/CLSA/CLSA/data/2310011_UCalgary_RRose_BL/2310011_UCalgary_RRose_BL/2310011_UCalgary_RRose_Baseline_CoPv7.csv'
# Define specific dtypes for columns to optimize memory
# optimized_dtypes = {
#     'MEDI_DOSE_FRQ_1_COF1': 'int8',
    
# }
ColumnNames = pd.read_csv(file_path, nrows=0).columns.tolist()
#print(ColumnNames)
# df = pd.read_csv(file_path, dtype=optimized_dtypes)
FIBloodCount = 22;DF = pd.DataFrame()

required_columns =['entity_id','AGE_NMBR_COM',
                   'SEX_ASK_COM','GEN_HLTH_COM','VIS_SGHT_COM','HRG_HRG_COM',
                   'CCC_OAKNEE_COM','CCC_OAHAND_COM','CCC_OAHIP_COM',
                   'CCC_RA_COM','CCC_COPD_COM','CCC_HBP_COM','DIA_DIAB_COM',
                   'CCC_HEART_COM','CCC_ANGI_COM','CCC_AMI_COM','CCC_PVD_COM',
                   'CCC_TIA_COM','CCC_CVA_COM','CCC_MEMPB_COM','CCC_ALZH_COM',
                   'CCC_PARK_COM','CCC_ULCR_COM','CCC_IBDIBS_COM','CCC_BOWINC_COM',
                   'ADL_INCNT_COM','ICQ_CATRCT_COM','ICQ_GLAUC_COM','CCC_MACDEG_COM',
                   'CCC_OSTPO_COM','CCC_CANC_COM','CCC_BCKP_COM','CCC_UTHYR_COM',
                   'CCC_OTHYR_COM','CCC_KIDN_COM','CCC_DRPNEU_COM','CCC_DRUTI_COM',
                   'FAL_NMBR_NB_COM','ADL_ABLDR_COM','ADL_ABLAP_COM','ADL_ABLWK_COM',
                   'ADL_ABLBD_COM','ADL_ABLBT_COM','IAL_ABLTEL_COM','IAL_ABLTRV_COM',
                   'IAL_ABLGRO_COM','IAL_ABLML_COM','IAL_ABLWRK_COM']

df = pd.read_csv(file_path, usecols=required_columns)
IsEmpty = df.isna() | (df == "")
DataNA = IsEmpty.sum(axis=1)
RowsToDrop = DataNA.index[DataNA>FIBloodCount*0.2]
df.drop(RowsToDrop, inplace=True)
IsEmpty = df.isna() | (df == "")
DataNA = IsEmpty.sum(axis=1)
NotEmpty = ~IsEmpty
DataAvailable = NotEmpty.sum(axis=1)-3
#print(DataAvailable)
df["GEN_HLTH_COM"].loc[df["GEN_HLTH_COM"]==8] = np.nan
df["GEN_HLTH_COM"].loc[df["GEN_HLTH_COM"]==9] = np.nan
DF['Health'] = (df['GEN_HLTH_COM']-1)/4

df["VIS_SGHT_COM"].loc[df["VIS_SGHT_COM"]==8] = np.nan
df["VIS_SGHT_COM"].loc[df["VIS_SGHT_COM"]==9] = np.nan
DF['Vision'] = (df['VIS_SGHT_COM']-1)/4

df["HRG_HRG_COM"].loc[(df["HRG_HRG_COM"]==8)|(df["HRG_HRG_COM"]==9)] = np.nan
DF['Hearing'] = (df['HRG_HRG_COM']-1)/4

df["CCC_OAKNEE_COM"].loc[(df["CCC_OAKNEE_COM"]==8)|(df["CCC_OAKNEE_COM"]==9)] = np.nan
df["CCC_OAHAND_COM"].loc[(df["CCC_OAHAND_COM"]==8)|(df["CCC_OAHAND_COM"]==9)] = np.nan
df["CCC_OAHIP_COM"] .loc[(df["CCC_OAHIP_COM"] ==8)|(df["CCC_OAHIP_COM"] ==9)] = np.nan

df['CCC_OAKNEE_COM']=2-df['CCC_OAKNEE_COM']
df['CCC_OAHAND_COM']=2-df['CCC_OAHAND_COM']
df['CCC_OAHIP_COM']=2-df['CCC_OAHIP_COM']
df['Osteoarthritis'] = df[['CCC_OAKNEE_COM','CCC_OAHAND_COM','CCC_OAHIP_COM']].sum(axis=1 , min_count=1)
DF['Osteoarthritis'] = df['Osteoarthritis'].gt(0).astype(int)

df["CCC_RA_COM"] .loc[(df["CCC_RA_COM"] ==8)|(df["CCC_RA_COM"] ==9)] = np.nan
DF['Arthritis']=2-df['CCC_RA_COM']

df["DIA_DIAB_COM"] .loc[(df["DIA_DIAB_COM"] ==8)|(df["DIA_DIAB_COM"] ==9)] = np.nan
DF['Diabetes_mellitus']=2-df['DIA_DIAB_COM']

# Cardiovascular
df["CCC_COPD_COM"] .loc[(df["CCC_COPD_COM"] ==8)|(df["CCC_COPD_COM"] ==9)] = np.nan
DF['Chronic_obstructive_pulmonary_disease']=2-df['CCC_COPD_COM']

df["CCC_HBP_COM"] .loc[(df["CCC_HBP_COM"] ==8)|(df["CCC_HBP_COM"] ==9)] = np.nan
DF['High_blood_pressure']=2-df['CCC_HBP_COM']

df["CCC_HEART_COM"] .loc[(df["CCC_HEART_COM"] ==8)|(df["CCC_HEART_COM"] ==9)] = np.nan
DF['Chronic_heart_failure']=2-df['CCC_HEART_COM']

df["CCC_ANGI_COM"] .loc[(df["CCC_ANGI_COM"] ==8)|(df["CCC_ANGI_COM"] ==9)] = np.nan
DF['Angina']=2-df['CCC_ANGI_COM']

df["CCC_AMI_COM"] .loc[(df["CCC_AMI_COM"] ==8)|(df["CCC_AMI_COM"] ==9)] = np.nan
DF['Acute_myocardial_infarction']=2-df['CCC_AMI_COM']

df["CCC_PVD_COM"] .loc[(df["CCC_PVD_COM"] ==8)|(df["CCC_PVD_COM"] ==9)] = np.nan
DF['Peripheral_vascular_disease']=2-df['CCC_PVD_COM']

df["CCC_CVA_COM"] .loc[(df["CCC_CVA_COM"] ==8)|(df["CCC_CVA_COM"] ==9)] = np.nan
DF['Stroke']=2-df['CCC_CVA_COM']

df["CCC_TIA_COM"] .loc[(df["CCC_TIA_COM"] ==8)|(df["CCC_TIA_COM"] ==9)] = np.nan
DF['Transient_ischemic_attack']=2-df['CCC_TIA_COM']

#Brain

df["CCC_MEMPB_COM"] .loc[(df["CCC_MEMPB_COM"] ==8)|(df["CCC_MEMPB_COM"] ==9)] = np.nan
DF['Memory_problem']=2-df['CCC_MEMPB_COM']

df["CCC_ALZH_COM"] .loc[(df["CCC_ALZH_COM"] ==8)|(df["CCC_ALZH_COM"] ==9)] = np.nan
DF['Alzheimer_disease']=2-df['CCC_ALZH_COM']

df["CCC_PARK_COM"] .loc[(df["CCC_PARK_COM"] ==8)|(df["CCC_PARK_COM"] ==9)] = np.nan
DF['Parkinson_disease']=2-df['CCC_PARK_COM']

#Gatrointestin
df["CCC_ULCR_COM"] .loc[(df["CCC_ULCR_COM"] ==8)|(df["CCC_ULCR_COM"] ==9)] = np.nan
DF['Peptic_ulcer_diseae']=2-df['CCC_ULCR_COM']

df["CCC_IBDIBS_COM"] .loc[(df["CCC_IBDIBS_COM"] ==8)|(df["CCC_IBDIBS_COM"] ==9)] = np.nan
DF['Colitis']=2-df['CCC_IBDIBS_COM']

df["CCC_BOWINC_COM"] .loc[(df["CCC_BOWINC_COM"] ==8)|(df["CCC_BOWINC_COM"] ==9)] = np.nan
DF['Bowel_incontinence']=2-df['CCC_BOWINC_COM']

df["ADL_INCNT_COM"].loc[(df["ADL_INCNT_COM"]==8)|(df["ADL_INCNT_COM"]==9)] = np.nan
DF['Urinary_incontinence'] = (df['ADL_INCNT_COM']-1)/2

#vision
df["ICQ_CATRCT_COM"] .loc[(df["ICQ_CATRCT_COM"] ==8)|(df["ICQ_CATRCT_COM"] ==9)] = np.nan
DF['Cataract']=2-df['ICQ_CATRCT_COM']

df["ICQ_GLAUC_COM"] .loc[(df["ICQ_GLAUC_COM"] ==8)|(df["ICQ_GLAUC_COM"] ==9)] = np.nan
DF['Glaucoma']=2-df['ICQ_GLAUC_COM']

df["CCC_MACDEG_COM"] .loc[(df["CCC_MACDEG_COM"] ==8)|(df["CCC_MACDEG_COM"] ==9)] = np.nan
DF['Macular_degeneration']=2-df['CCC_MACDEG_COM']

#Cancer
df["CCC_CANC_COM"] .loc[(df["CCC_CANC_COM"] ==8)|(df["CCC_CANC_COM"] ==9)] = np.nan
DF['Cancer']=2-df['CCC_CANC_COM']

#Orthopedic
df["CCC_OSTPO_COM"] .loc[(df["CCC_OSTPO_COM"] ==8)|(df["CCC_OSTPO_COM"] ==9)] = np.nan
DF['Osteoporosis']=2-df['CCC_OSTPO_COM']

df["CCC_BCKP_COM"] .loc[(df["CCC_BCKP_COM"] ==8)|(df["CCC_BCKP_COM"] ==9)] = np.nan
DF['Back_pain']=2-df['CCC_BCKP_COM']

#Internal
#df["CCC_UTHYR_COM"] .loc[(df["CCC_UTHYR_COM"] ==8)|(df["CCC_UTHYR_COM"] ==9)] = np.nan
df.loc[df['CCC_UTHYR_COM'].isin([8,9]),'CCC_UTHYR_COM'] = np.nan
DF['Hypothyroidism']=2-df['CCC_UTHYR_COM']

#df["CCC_OTHYR_COM"] .loc[(df["CCC_OTHYR_COM"] ==8)|(df["CCC_OTHYR_COM"] ==9)] = np.nan
df.loc[df['CCC_OTHYR_COM'].isin([8,9]),'CCC_OTHYR_COM'] = np.nan
DF['Hyperthyroidism']=2-df['CCC_OTHYR_COM']

#df["CCC_KIDN_COM"] .loc[(df["CCC_KIDN_COM"] ==8)|(df["CCC_KIDN_COM"] ==9)] = np.nan
df.loc[df['CCC_KIDN_COM'].isin([8,9]),'CCC_KIDN_COM'] = np.nan
DF['Kidney_failure']=2-df['CCC_KIDN_COM']

#df["CCC_DRPNEU_COM"] .loc[(df["CCC_DRPNEU_COM"] ==8)|(df["CCC_DRPNEU_COM"] ==9)] = np.nan
df.loc[df['CCC_DRPNEU_COM'].isin([8,9]),'CCC_DRPNEU_COM'] = np.nan
DF['Pneumonia']=2-df['CCC_DRPNEU_COM']

#df["CCC_DRUTI_COM"] .loc[(df["CCC_DRUTI_COM"] ==8)|(df["CCC_DRUTI_COM"] ==9)] = np.nan
df.loc[df['CCC_DRUTI_COM'].isin([8,9]),'CCC_DRUTI_COM'] = np.nan
DF['Urinary_tract_infection']=2-df['CCC_DRUTI_COM']

#ADL
df.loc[df["FAL_NMBR_NB_COM"].isin([89, 99]), "FAL_NMBR_NB_COM"] = np.nan
#df["FAL_NMBR_NB_COM"].loc[(df["FAL_NMBR_NB_COM"]==98)|(df["FAL_NMBR_NB_COM"]==99)] = np.nan
MaxFall = df['FAL_NMBR_NB_COM'].max()
DF['Falls'] = (df['FAL_NMBR_NB_COM'])/MaxFall

df.loc[~df['ADL_ABLDR_COM'].isin([1,2]),'ADL_ABLDR_COM'] = np.nan
DF['Dressing'] = df['ADL_ABLDR_COM']-1

df.loc[~df['ADL_ABLAP_COM'].isin([1,2]),'ADL_ABLAP_COM'] = np.nan
DF['Grooming'] = df['ADL_ABLAP_COM']-1

df.loc[~df['ADL_ABLWK_COM'].isin([1,2]),'ADL_ABLWK_COM'] = np.nan
DF['Walking'] = df['ADL_ABLWK_COM']-1

df.loc[~df['ADL_ABLBD_COM'].isin([1,2]),'ADL_ABLBD_COM'] = np.nan
DF['Getting_in_out_bed'] = df['ADL_ABLBD_COM']-1

df.loc[~df['ADL_ABLBT_COM'].isin([1,2]),'ADL_ABLBT_COM'] = np.nan
DF['Bathing'] = df['ADL_ABLBT_COM']-1

df.loc[~df['IAL_ABLTEL_COM'].isin([1,2]),'IAL_ABLTEL_COM'] = np.nan
DF['Phone'] = df['IAL_ABLTEL_COM']-1

df.loc(~df['IAL_ABLTRV_COM'].isin([1,2]),'IAL_ABLTRV_COM') = np.nan
DF['Transport'] = df['IAL_ABLTRV_COM']-1

df.loc[~df['IAL_ABLGRO_COM'].isin([1,2]),'IAL_ABLGRO_COM'] = np.nan
DF['Shopping'] = df['IAL_ABLGRO_COM']-1

df.loc[~df['IAL_ABLML_COM'].isin([1,2]),'IAL_ABLML_COM'] = np.nan
DF['Cooking'] = df['IAL_ABLML_COM'] -1

df.loc[~df['IAL_ABLWRK_COM'].isin([1,2]),'IAL_ABLWRK_COM'] = np.nan
DF['Housework'] = df['IAL_ABLWRK_COM']-1


print(DF)