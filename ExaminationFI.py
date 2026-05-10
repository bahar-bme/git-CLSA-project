# -*- coding: utf-8 -*-
"""
Created on Sun May  3 21:06:49 2026

@author: mmogh
"""
"FI-EXAMINATION"  
import pandas as pd
from sklearn.preprocessing import StandardScaler

file_path = 'E:/CLSA/CLSA/data/2310011_UCalgary_RRose_BL/2310011_UCalgary_RRose_BL/2310011_UCalgary_RRose_Baseline_CoPv7.csv'
# Define specific dtypes for columns to optimize memory
# optimized_dtypes = {
#     'MEDI_DOSE_FRQ_1_COF1': 'int8',
    
# }

"""
def stratify_normalize(df, target_col, group_col='SEX_ASK_COM'):

    #Applies sex-stratified normalization (Z-score) to a specific column.
    #Returns a Series of normalized values.

    # Calculate group-specific mean and std for the chosen column
    means = df.groupby(group_col)[target_col].transform('mean')
    stds = df.groupby(group_col)[target_col].transform('std')
    
    # Return the normalized column
    return (df[target_col] - means) / stds


# sex-stratified function:
def rescale_by_percentile(df, target_col, group_col='SEX_ASK_COM'):
    def apply_rescale(group):
        # Calculate the specific percentile thresholds
        p05 = group.quantile(0.005)
        p995 = group.quantile(0.995)
        
        # Apply the formula
        rescaled = (group - p05) / (p995 - p05)
        return rescaled.clip(0,1)
    # Use transform to apply this logic per group to the target column
    return df.groupby(group_col)[target_col].transform(apply_rescale)

"""


def stratified_scaling(df, target_col, group_col='SEX_ASK_COM', inverse=False):
    """
    Sex-stratified scaling between 0.5th and 95th percentiles.
    
    Parameters:
    - inverse=False: 0.5th -> 0, 95th -> 1 (Standard)
    - inverse=True:  0.5th -> 1, 95th -> 0 (Inversed)
    """
    def transform_group(group):
        p05 = group.quantile(0.005)
        p95 = group.quantile(0.95)
        
        # Handle cases where all values in a group are identical (p95 == p05)
        if p95 == p05:
            return group * 0 +0.5
        
        if inverse:
            # High raw values become 0, low raw values become 1
            scaled = (p95 - group) / (p95 - p05)
        else:
            # Low raw values become 0, high raw values become 1
            scaled = (group - p05) / (p95 - p05)
            
        return scaled.clip(0, 1)

    return df.groupby(group_col, dropna=False)[target_col].transform(transform_group)


ColumnNames = pd.read_csv(file_path, nrows=0).columns.tolist()
print(ColumnNames)
# df = pd.read_csv(file_path, dtype=optimized_dtypes)
FIExamination = 47;DF = pd.DataFrame()

required_columns =['AGE_NMBR_COM',
                   'SEX_ASK_COM', 'ED_HIGH_COM', 
                   'wlk_time_com','cr_avg_time_com',
                   'tug_time_com','gs_exam_max_com','bal_best_com',
                   'cog_reyi_score_com','COG_REYI_STARTLANG_COM','COG_REYI_LANG_COM',
                   'cog_reyii_score_com','COG_REYII_STARTLANG_COM','COG_REYII_LANG_COM',
                   'cog_mat_score_com','COG_MAT_STARTLANG_COM','COG_MAT_LANG_COM',
                   'cog_aft_score_2_com','COG_AFT_STARTLANG_COM','COG_AFT_LANG_COM',
                   'fas_f_score_com','fas_a_score_com','fas_s_score_com',
                   'FAS_F_LANG_COM','FAS_A_LANG_COM','FAS_S_LANG_COM',
                   'tmt_itpexact_com','tmt_acc_com','tmt_rmd_com','TMT_LANG_COM',
                   'pmt_itp_com','pmt_rem_com','pmt_acr_com','PMT_LANG_COM',
                   'crt_mrtwout_corrans_com','CRT_LANG_COM',
                   'stp_dottime_ss_com','stp_coltime_ss_com','STP_STARTLANG_COM']


required_columns = [f.upper() for f in required_columns]

required_columns.insert(0,'entity_id')


df = pd.read_csv(file_path, usecols=required_columns)
"""
IsEmpty = df.isna() | (df == "")
DataNA = IsEmpty.sum(axis=1)
RowsToDrop = DataNA.index[DataNA>FIBlood*0.2]
df.drop(RowsToDrop, inplace=True)
IsEmpty = df.isna() | (df == "")
DataNA = IsEmpty.sum(axis=1)
NotEmpty = ~IsEmpty
DataAvailable = NotEmpty.sum(axis=1)-3
"""
# Domain 1: Physical Performance
DF['wlk_time_com'.upper()] = stratified_scaling(df, 'wlk_time_com'.upper() , inverse=False)
DF['cr_avg_time_com'.upper()] = stratified_scaling(df, 'cr_avg_time_com'.upper(), inverse=False)
DF['tug_time_com'.upper()] = stratified_scaling(df, 'tug_time_com'.upper(), inverse=False)
DF['gs_exam_max_com'.upper()] = stratified_scaling(df, 'gs_exam_max_com'.upper(), inverse=True)
DF['bal_best_com'.upper()] = stratified_scaling(df, 'bal_best_com'.upper(), inverse=True)
# Domain 2: Cognition
strat_list = ['SEX_ASK_COM', 'ED_HIGH_COM','COG_REYI_STARTLANG_COM','COG_REYI_LANG_COM']
DF['cog_reyi_score_com'.upper()] = stratified_scaling(df, target_col='cog_reyi_score_com'.upper(),
                                                       group_col=strat_list, inverse=True)

strat_list = ['SEX_ASK_COM', 'ED_HIGH_COM','COG_REYII_STARTLANG_COM','COG_REYII_LANG_COM']
DF['cog_reyii_score_com'.upper()] = stratified_scaling(df, target_col='cog_reyii_score_com'.upper(),
                                                       group_col=strat_list, inverse=True)

strat_list = ['SEX_ASK_COM', 'ED_HIGH_COM','COG_MAT_STARTLANG_COM','COG_MAT_LANG_COM']
DF['cog_mat_score_com'.upper()] = stratified_scaling(df, target_col='cog_mat_score_com'.upper(),
                                                       group_col=strat_list, inverse=True)

strat_list = ['SEX_ASK_COM', 'ED_HIGH_COM','COG_AFT_STARTLANG_COM','COG_AFT_LANG_COM']
DF['cog_aft_score_2_com'.upper()] = stratified_scaling(df, target_col='cog_aft_score_2_com'.upper(),
                                                       group_col=strat_list, inverse=True)

strat_list = ['SEX_ASK_COM', 'ED_HIGH_COM','FAS_F_LANG_COM']
DF['FAS_F_SCORE'] = stratified_scaling(df, target_col='fas_f_score_com'.upper(),
                                                       group_col=strat_list, inverse=True)

strat_list = ['SEX_ASK_COM', 'ED_HIGH_COM','FAS_A_LANG_COM']
DF['FAS_A_SCORE'] = stratified_scaling(df, target_col='fas_a_score_com'.upper(),
                                                       group_col=strat_list, inverse=True)

strat_list = ['SEX_ASK_COM', 'ED_HIGH_COM','FAS_S_LANG_COM']
DF['FAS_S_SCORE'] = stratified_scaling(df, target_col='fas_s_score_com'.upper(),
                                                       group_col=strat_list, inverse=True)                                                       

DF['Controlled_Oral_Word_Association']=pd.concat([DF['FAS_A_SCORE'], DF['FAS_F_SCORE'], DF['FAS_S_SCORE']], axis=1).mean(axis=1,skipna=True)

df['Time_Based_Memory'] = df['tmt_rmd_com'.upper()].add(df['tmt_acc_com'.upper()], fill_value=0).add(df['tmt_itpexact_com'.upper()], fill_value=0)
strat_list = ['SEX_ASK_COM', 'ED_HIGH_COM','TMT_LANG_COM']
DF['Time_Based_Memory'] = stratified_scaling(df, target_col='Time_Based_Memory',
                                                       group_col=strat_list, inverse=True)                                                       

df['Event_Based_Memory'] = df['pmt_itp_com'.upper()].add(df['pmt_rem_com'.upper()],fill_value=0).add(df['pmt_acr_com'.upper()],fill_value=0)

strat_list = ['SEX_ASK_COM', 'ED_HIGH_COM','PMT_LANG_COM']
DF['Event_Based_Memory'] = stratified_scaling(df, target_col='Event_Based_Memory',
                                                       group_col=strat_list, inverse=True)                                                       

strat_list = ['SEX_ASK_COM', 'ED_HIGH_COM','CRT_LANG_COM']
DF['crt_mrtwout_corrans_com'.upper()] = stratified_scaling(df, target_col='crt_mrtwout_corrans_com'.upper(),
                                                       group_col=strat_list, inverse=True)                                                       


df['Stroop_Test_Interference_Time'] = df['stp_dottime_ss_com'.upper()]-df['stp_coltime_ss_com'.upper()]
strat_list = ['SEX_ASK_COM', 'ED_HIGH_COM','STP_STARTLANG_COM']
DF['Stroop_Test_Interference_Time'] = stratified_scaling(df, target_col='Stroop_Test_Interference_Time',
                                                       group_col=strat_list, inverse=True)                                                       
# Domain 3: Cardiac


print(DF)
#print(K)
print(df['Stroop_Test_Interference_Time'])
#print(max(df['tmt_itpexact_com'.upper()]))
import matplotlib.pyplot as plt
import numpy as np
plt.hist(DF['Stroop_Test_Interference_Time'], bins=20,color='skyblue', edgecolor='black')
plt.show()