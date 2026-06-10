# -*- coding: utf-8 -*-
"""
Created on Sun May  3 21:06:49 2026

@author: mmogh
"""
"FI-EXAMINATION"  
import pandas as pd
from sklearn.preprocessing import StandardScaler
import numpy as np

file_path_BL = 'E:/CLSA/CLSA/data/2310011_UCalgary_RRose_BL/2310011_UCalgary_RRose_BL/2310011_UCalgary_RRose_Baseline_CoPv7.csv'
file_path = r'E:\CLSA\CLSA\data\2310011_UCalgary_RRose_FUP1\2310011_UCalgary_RRose_FUP1\2310011_UCalgary_RRose_FUP1_CoPv5.csv'

# Define specific dtypes for columns to optimize memory
# optimized_dtypes = {
#     'MEDI_DOSE_FRQ_1_COF1': 'int8',
    
# }

required_columns_BL =['entity_id','SEX_ASK_COM','ED_HIGH_COM']
df_BL = pd.read_csv(file_path_BL, usecols=required_columns_BL)

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
            # High raw values becof1e 0, low raw values becof1e 1
            scaled = (p95 - group) / (p95 - p05)
        else:
            # Low raw values becof1e 0, high raw values becof1e 1
            scaled = (group - p05) / (p95 - p05)
            
        return scaled.clip(0, 1)

    return df.groupby(group_col, dropna=False)[target_col].transform(transform_group)


ColumnNames = pd.read_csv(file_path, nrows=0).columns.tolist()
#print(ColumnNames)
# df = pd.read_csv(file_path, dtype=optimized_dtypes)
FIExaminationCount = 42 #47
DF = pd.DataFrame()

required_columns =['AGE_NMBR_COF1',
                   'wlk_time_cof1','cr_avg_time_cof1',
                   'tug_time_cof1','gs_exam_max_cof1','bal_best_cof1',
                   'cog_reyi_score_cof1','COG_REYI_STARTLANG_COF1','COG_REYI_LANG_COF1',
                   'cog_reyii_score_cof1','COG_REYII_STARTLANG_COF1','COG_REYII_LANG_COF1',
                   'cog_mat_score_cof1','COG_MAT_STARTLANG_COF1','COG_MAT_LANG_COF1',
                   'cog_aft_score_2_cof1','COG_AFT_STARTLANG_COF1','COG_AFT_LANG_COF1',
                   'fas_f_score_cof1','fas_a_score_cof1','fas_s_score_cof1',
                   'FAS_F_LANG_COF1','FAS_A_LANG_COF1','FAS_S_LANG_COF1',
                   'tmt_itpexact_cof1','tmt_acc_cof1','tmt_rmd_cof1','TMT_LANG_COF1',
                   'pmt_itp_cof1','pmt_rem_cof1','pmt_acr_cof1','PMT_LANG_COF1',
                   'crt_mrtwout_corrans_cof1',
                   'stp_dottime_ss_cof1','stp_coltime_ss_cof1',
                   'bp_systolic_avg_cof1','bp_diastolic_avg_cof1','bp_pulse_avg_cof1',
                   'bp_pulse_avg_cof1','ecg_result_cof1','ecg_pq_interval_cof1','ecg_qrs_duration_cof1',
                   'ecg_qtc_interval_cof1','ecg_p_axis_cof1','ecg_r_axis_cof1','ecg_t_axis_cof1',
                   'ecg_p_duration_cof1','hwt_dbmi_cof1','whc_ratio_cof1',
                   'dxa_wb_head_bmd_cof1','dxa_wb_larm_bmd_cof1','dxa_wb_rarm_bmd_cof1',
                   'dxa_wb_lrib_bmd_cof1', 'dxa_wb_rrib_bmd_cof1','dxa_wb_t_s_bmd_cof1',
                   'dxa_wb_l_s_bmd_cof1','dxa_wb_pelv_bmd_cof1','dxa_wb_lleg_bmd_cof1',
                   'dxa_wb_rleg_bmd_cof1','DXA_WB_WBTOT_BMD_COF1','DXA_OI_APDG_LEAN_MASS_H2_COF1',
                   'DXA_OI_TOTAL_PERCENT_FAT_COF1',
                   'DXA_WBC_LARM_PFAT_COF1','DXA_WBC_RARM_PFAT_COF1','DXA_WBC_L_LEG_PFAT_COF1',
                   'DXA_WBC_R_LEG_PFAT_COF1','DXA_WBC_TRUNK_PFAT_COF1','DXA_WBC_HEAD_PFAT_COF1',
                   'va_etdrs_l_rslt_cof1','va_etdrs_r_rslt_cof1','ton_iopcc_r_cof1','ton_iopcc_l_cof1',
                   'ton_ch_l_cof1','ton_ch_r_cof1','ton_iopg_r_cof1','ton_iopg_l_cof1',
                   'bp_systolic_avg_cof1','bp_diastolic_avg_cof1',
                   'hrg_right_500_cof1','hrg_right_1k_cof1','hrg_right_2k_cof1','hrg_right_4k_cof1',
                   'hrg_left_500_cof1','hrg_left_1k_cof1','hrg_left_2k_cof1','hrg_left_4k_cof1',
                   'ICQ_DERET3MO_COF1','ICQ_SRGYEYE_COF1','ICQ_EYEINF_COF1']


# 'spr_fvc_t2_cof1','SPR_FEV1_FVC_T2_COF1','SPR_FEV1_FVC_T3_COF1','SPR_FEV1_FVC_T8_COF1','SPR_FEV1_FVC_T6_COF1','SPR_FEV1_FVC_T1_COF1',
#'STP_STARTLANG_COF1','spr_fvc_t4_cof1','spr_fvc_t5_cof1','spr_fvc_t7_cof1','SPR_FEV1_FVC_T7_COF1','spr_fvc_t8_cof1','SPR_FEV1_FVC_T5_COF1',
# 'spr_fvc_t6_cof1','spr_fvc_t3_cof1','spr_fvc_t1_cof1','SPR_FEV1_FVC_T4_COF1','CRT_LANG_COF1',

#'imt_r_avg_cof1','imt_l_avg_cof1'
#'dxa_wb_wbtot_t_cof1'
required_columns = [f.upper() for f in required_columns]
required_columns.insert(0,'entity_id')


df = pd.read_csv(file_path, usecols=required_columns)
df = df.merge(df_BL[['entity_id', 'SEX_ASK_COM','ED_HIGH_COM']], on='entity_id', how='left')

""""
IsEmpty = df.isna() | (df == "")
DataNA = IsEmpty.sum(axis=1)
RowsToDrop = DataNA.index[DataNA>FIExamination*0.2]
df.drop(RowsToDrop, inplace=True)
IsEmpty = df.isna() | (df == "")
DataNA = IsEmpty.sum(axis=1)
NotEmpty = ~IsEmpty
DataAvailable = NotEmpty.sum(axis=1)-3
"""

# Domain 1: Physical Performance
df.loc[df['wlk_time_cof1'.upper()].isin([-88888,-99999,-99991,-88880]),'wlk_time_cof1'.upper()] = np.nan
DF['wlk_time_cof1'.upper()] = stratified_scaling(df, 'wlk_time_cof1'.upper() , inverse=False)

df.loc[df['cr_avg_time_cof1'.upper()].isin([-88880,-99999,-99991,-88888]),'cr_avg_time_cof1'.upper()] = np.nan
DF['cr_avg_time_cof1'.upper()] = stratified_scaling(df, 'cr_avg_time_cof1'.upper(), inverse=False)

df.loc[df['TUG_TIME_COF1'].isin([-88888,-99999,-99991,-88880]),'TUG_TIME_COF1'] = np.nan
DF['tug_time_cof1'.upper()] = stratified_scaling(df, 'tug_time_cof1'.upper(), inverse=False)

df.loc[df['gs_exam_max_cof1'.upper()].isin([-88888,-99999,-99991,-88880]),'gs_exam_max_cof1'.upper()] = np.nan
DF['gs_exam_max_cof1'.upper()] = stratified_scaling(df, 'gs_exam_max_cof1'.upper(), inverse=True)

df.loc[df['bal_best_cof1'.upper()].isin([-88888,-99999,-99991,-88880]),'bal_best_cof1'.upper()] = np.nan
DF['bal_best_cof1'.upper()] = stratified_scaling(df, 'bal_best_cof1'.upper(), inverse=True)
# Domain 2: Cognition
df.loc[df['COG_REYI_STARTLANG_COF1'].isin([-88888,-99999]),'COG_REYI_STARTLANG_COF1'] = np.nan
df.loc[df['COG_REYI_LANG_COF1'].isin([-88888,-99999]),'COG_REYI_LANG_COF1'] = np.nan
df.loc[df['cog_reyi_score_cof1'.upper()].isin([-88888,-99999]),'cog_reyi_score_cof1'.upper()] = np.nan
strat_list = ['SEX_ASK_COM', 'ED_HIGH_COM','COG_REYI_STARTLANG_COF1','COG_REYI_LANG_COF1']
DF['cog_reyi_score_cof1'.upper()] = stratified_scaling(df, target_col='cog_reyi_score_cof1'.upper(),
                                                       group_col=strat_list, inverse=True)

df.loc[df['COG_REYII_STARTLANG_COF1'].isin([-88888,-99999]),'COG_REYII_STARTLANG_COF1'] = np.nan
df.loc[df['COG_REYII_LANG_COF1'].isin([-88888,-99999]),'COG_REYII_LANG_COF1'] = np.nan
df.loc[df['cog_reyii_score_cof1'.upper()].isin([-88888,-99999]),'cog_reyii_score_cof1'.upper()] = np.nan
strat_list = ['SEX_ASK_COM', 'ED_HIGH_COM','COG_REYII_STARTLANG_COF1','COG_REYII_LANG_COF1']
DF['cog_reyii_score_cof1'.upper()] = stratified_scaling(df, target_col='cog_reyii_score_cof1'.upper(),
                                                       group_col=strat_list, inverse=True)

df.loc[df['COG_MAT_STARTLANG_COF1'].isin([-88888,-99999]),'COG_MAT_STARTLANG_COF1'] = np.nan
df.loc[df['COG_MAT_LANG_COF1'].isin([-88888,-99999]),'COG_MAT_LANG_COF1'] = np.nan
df.loc[df['cog_mat_score_cof1'.upper()].isin([-88888,-99999]),'cog_mat_score_cof1'.upper()] = np.nan
strat_list = ['SEX_ASK_COM', 'ED_HIGH_COM','COG_MAT_STARTLANG_COF1','COG_MAT_LANG_COF1']
DF['cog_mat_score_cof1'.upper()] = stratified_scaling(df, target_col='cog_mat_score_cof1'.upper(),
                                                       group_col=strat_list, inverse=True)

df.loc[df['COG_AFT_STARTLANG_COF1'].isin([-88888,-99999]),'COG_AFT_STARTLANG_COF1'] = np.nan
df.loc[df['COG_AFT_LANG_COF1'].isin([-88888,-99999]),'COG_AFT_LANG_COF1'] = np.nan
df.loc[df['cog_aft_score_2_cof1'.upper()].isin([-88888,-99999]),'cog_aft_score_2_cof1'.upper()] = np.nan
strat_list = ['SEX_ASK_COM', 'ED_HIGH_COM','COG_AFT_STARTLANG_COF1','COG_AFT_LANG_COF1']
DF['cog_aft_score_2_cof1'.upper()] = stratified_scaling(df, target_col='cog_aft_score_2_cof1'.upper(),
                                                       group_col=strat_list, inverse=True)

df.loc[df['FAS_F_LANG_COF1'].isin([-88888,-99991,-88880,-99999]),'FAS_F_LANG_COF1'] = np.nan
df.loc[df['fas_f_score_cof1'.upper()].isin([-88888,-99991,-88880,-99999]),'fas_f_score_cof1'.upper()] = np.nan
strat_list = ['SEX_ASK_COM', 'ED_HIGH_COM','FAS_F_LANG_COF1']
FAS_F_SCORE = stratified_scaling(df, target_col='fas_f_score_cof1'.upper(),
                                                       group_col=strat_list, inverse=True)

df.loc[df['FAS_A_LANG_COF1'].isin([-88888,-99991,-88880,-99999]),'FAS_A_LANG_COF1'] = np.nan
df.loc[df['fas_a_score_cof1'.upper()].isin([-88888,-99991,-88880,-99999]),'fas_a_score_cof1'.upper()] = np.nan
strat_list = ['SEX_ASK_COM', 'ED_HIGH_COM','FAS_A_LANG_COF1']
FAS_A_SCORE = stratified_scaling(df, target_col='fas_a_score_cof1'.upper(),
                                                       group_col=strat_list, inverse=True)

df.loc[df['FAS_S_LANG_COF1'].isin([-88888,-99991,-88880,-99999]),'FAS_S_LANG_COF1'] = np.nan
df.loc[df['fas_s_score_cof1'.upper()].isin([-88888,-99991,-88880,-99999]),'fas_s_score_cof1'.upper()] = np.nan
strat_list = ['SEX_ASK_COM', 'ED_HIGH_COM','FAS_S_LANG_COF1']
FAS_S_SCORE = stratified_scaling(df, target_col='fas_s_score_cof1'.upper(),
                                                       group_col=strat_list, inverse=True)                                                       

DF['Controlled_Oral_Word_Association']=pd.concat([FAS_A_SCORE,FAS_F_SCORE,FAS_S_SCORE], axis=1).mean(axis=1,skipna=True)

df.loc[df['tmt_rmd_cof1'.upper()].isin([-88888,-99991,-88880,-99999]),'tmt_rmd_cof1'] = np.nan
df.loc[df['tmt_acc_cof1'.upper()].isin([-88888,-99991,-88880,-99999]),'tmt_acc_cof1'] = np.nan
df.loc[df['tmt_itpexact_cof1'.upper()].isin([-88888,-99991,-88880,-99999]),'tmt_itpexact_cof1'] = np.nan

df['Time_Based_Memory'] = df['tmt_rmd_cof1'.upper()].add(df['tmt_acc_cof1'.upper()], fill_value=0).add(df['tmt_itpexact_cof1'.upper()], fill_value=0)
strat_list = ['SEX_ASK_COM', 'ED_HIGH_COM','TMT_LANG_COF1']
DF['Time_Based_Memory'] = stratified_scaling(df, target_col='Time_Based_Memory',
                                                       group_col=strat_list, inverse=True)                                                       

df.loc[df['pmt_itp_cof1'.upper()].isin([-88888,-99991,-88880,-99999]),'pmt_itp_cof1'.upper()] = np.nan
df.loc[df['pmt_rem_cof1'.upper()].isin([-88888,-99991,-88880,-99999]),'pmt_rem_cof1'.upper()] = np.nan
df.loc[df['pmt_acr_cof1'.upper()].isin([-88888,-99991,-88880,-99999]),'pmt_acr_cof1'.upper()] = np.nan
df['Event_Based_Memory'] = df['pmt_itp_cof1'.upper()].add(df['pmt_rem_cof1'.upper()],fill_value=0).add(df['pmt_acr_cof1'.upper()],fill_value=0)

df.loc[df['PMT_LANG_COF1'].isin([-88888,-99991,-88880,-99999]),'PMT_LANG_COF1'] = np.nan
strat_list = ['SEX_ASK_COM', 'ED_HIGH_COM','PMT_LANG_COF1']
DF['Event_Based_Memory'] = stratified_scaling(df, target_col='Event_Based_Memory',
                                                       group_col=strat_list, inverse=True)                                                       

df.loc[df['crt_mrtwout_corrans_cof1'.upper()].isin([-88888,-99991,-88880,-99999]),'crt_mrtwout_corrans_cof1'.upper()] = np.nan
strat_list = ['SEX_ASK_COM', 'ED_HIGH_COM'] #,'CRT_LANG_COF1'
DF['crt_mrtwout_corrans_cof1'.upper()] = stratified_scaling(df, target_col='crt_mrtwout_corrans_cof1'.upper(),
                                                       group_col=strat_list, inverse=True)                                                       

df.loc[df['stp_dottime_ss_cof1'.upper()].isin([-88888,-99991,-88880,-99999]),'stp_dottime_ss_cof1'.upper()] = np.nan
df.loc[df['stp_coltime_ss_cof1'.upper()].isin([-88888,-99991,-88880,-99999]),'stp_coltime_ss_cof1'.upper()] = np.nan
df['Stroop_Test_Interference_Time'] = df['stp_dottime_ss_cof1'.upper()]-df['stp_coltime_ss_cof1'.upper()]
strat_list = ['SEX_ASK_COM', 'ED_HIGH_COM'] #,'STP_STARTLANG_COF1'
DF['Stroop_Test_Interference_Time'] = stratified_scaling(df, target_col='Stroop_Test_Interference_Time',
                                                       group_col=strat_list, inverse=True)                                                       
# Domain 3: Cardiac
df.loc[df['bp_systolic_avg_cof1'.upper()].isin([-88888,-99991,-88880,-99999]),'bp_systolic_avg_cof1'.upper()] = np.nan
DF["bp_systolic_avg_cof1".upper()]  = (df["bp_systolic_avg_cof1".upper()]<90) | (df["bp_systolic_avg_cof1".upper()]>140)
df.loc[df['bp_diastolic_avg_cof1'.upper()].isin([-88888,-99991,-88880,-99999]),'bp_diastolic_avg_cof1'.upper()] = np.nan
DF["bp_diastolic_avg_cof1".upper()] = (df["bp_diastolic_avg_cof1".upper()]<=60)
df["pulse_pressure".upper()]       = df['bp_systolic_avg_cof1'.upper()]-df['bp_diastolic_avg_cof1'.upper()]
DF['pulse_pressure'.upper()]       = (df['pulse_pressure'.upper()]<=30) | (df['pulse_pressure'.upper()]>60)

df.loc[df['bp_pulse_avg_cof1'.upper()].isin([-88888,-99991,-88880,-99999]),'bp_pulse_avg_cof1'.upper()] = np.nan
DF['bp_pulse_avg_cof1'.upper()]     = (df['bp_pulse_avg_cof1'.upper()]<=60) | (df['bp_pulse_avg_cof1'.upper()]>99)
#DF['imt_r_avg_cof1'.upper()]        = (df['imt_r_avg_cof1'.upper()]<0.5) | (df['imt_r_avg_cof1'.upper()]>0.8)
#DF['imt_l_avg_cof1'.upper()]         = (df['imt_l_avg_cof1'.upper()]<0.5) | (df['imt_l_avg_cof1'.upper()]>0.8)

df.loc[df['ecg_result_cof1'.upper()].isin([-88888,-99991,-88880,-99999]),'ecg_result_cof1'.upper()] = np.nan
DF['ecg_result_cof1'.upper()] = np.nan
DF.loc[((df['ecg_result_cof1'.upper()] == 4) | (df['ecg_result_cof1'.upper()] == 5)),'ecg_result_cof1'.upper()]= 1
DF.loc[(df['ecg_result_cof1'.upper()] == 3),'ecg_result_cof1'.upper()] = 0.66
DF.loc[(df['ecg_result_cof1'.upper()] == 2),'ecg_result_cof1'.upper()] = 0.33
DF.loc[(df['ecg_result_cof1'.upper()] == 1),'ecg_result_cof1'.upper()] = 0

df.loc[df['ecg_pq_interval_cof1'.upper()].isin([-88888,-99991,-88880,-99999]),'ecg_pq_interval_cof1'.upper()] = np.nan
DF['ecg_pq_interval_cof1'.upper()] = (df['ecg_pq_interval_cof1'.upper()]<=12) | (df['ecg_pq_interval_cof1'.upper()]>200)
df.loc[df['ecg_qrs_duration_cof1'.upper()].isin([-88888,-99991,-88880,-99999]),'ecg_qrs_duration_cof1'.upper()] = np.nan
DF['ecg_qrs_duration_cof1'.upper()] = df['ecg_qrs_duration_cof1'.upper()] >= 100
df.loc[df['ecg_qtc_interval_cof1'.upper()].isin([-88888,-99991,-88880,-99999]),'ecg_qtc_interval_cof1'.upper()] = np.nan
DF['ecg_qtc_interval_cof1'.upper()] = ((df["SEX_ASK_COM"]=="M") & (df['ecg_qtc_interval_cof1'.upper()]>430))|((df["SEX_ASK_COM"]=="F") & (df['ecg_qtc_interval_cof1'.upper()]>450))
df.loc[df['ecg_p_axis_cof1'.upper()].isin([-88888,-99991,-88880,-99999]),'ecg_p_axis_cof1'.upper()] = np.nan
DF['ecg_p_axis_cof1'.upper()] = (df['ecg_p_axis_cof1'.upper()]<0) | (df['ecg_p_axis_cof1'.upper()]>75)
df.loc[df['ecg_r_axis_cof1'.upper()].isin([-88888,-99991,-88880,-99999]),'ecg_r_axis_cof1'.upper()] = np.nan
DF['ecg_r_axis_cof1'.upper()] = (df['ecg_r_axis_cof1'.upper()]<-30) | (df['ecg_r_axis_cof1'.upper()]>90)
df.loc[df['ecg_t_axis_cof1'.upper()].isin([-88888,-99991,-88880,-99999]),'ecg_t_axis_cof1'.upper()] = np.nan
DF['ecg_t_axis_cof1'.upper()] = (df['ecg_t_axis_cof1'.upper()]<0) | (df['ecg_t_axis_cof1'.upper()]>90)
df.loc[df['ecg_p_duration_cof1'.upper()].isin([-88888,-99991,-88880,-99999]),'ecg_p_duration_cof1'.upper()] = np.nan
DF['ecg_p_duration_cof1'.upper()] = df['ecg_p_duration_cof1'.upper()]>120
# Domain 4: Anthropometric measures
df.loc[df['hwt_dbmi_cof1'.upper()].isin([999.96, 999.99,-88888]),'hwt_dbmi_cof1.upper()'] = np.nan
DF['hwt_dbmi_cof1'.upper()] = np.nan
DF.loc[((df['hwt_dbmi_cof1'.upper()]<=18.5)|(df['hwt_dbmi_cof1'.upper()]>=30))  ,'hwt_dbmi_cof1'.upper()] = 1
DF.loc[((df['hwt_dbmi_cof1'.upper()]>=25)&(df['hwt_dbmi_cof1'.upper()]<=29.9))  ,'hwt_dbmi_cof1'.upper()] = 0.5 
DF.loc[((df['hwt_dbmi_cof1'.upper()]>=18.5)&(df['hwt_dbmi_cof1'.upper()]<=24.9)),'hwt_dbmi_cof1'.upper()] = 0

df.loc[df['whc_ratio_cof1'.upper()].isin([-88888,-99991,-88880,-99999]),'whc_ratio_cof1'.upper()] = np.nan
DF['whc_ratio_cof1'.upper()] = ((df['SEX_ASK_COM']=='M')&(df['whc_ratio_cof1'.upper()]>0.9)) | ((df['SEX_ASK_COM']=='F')&(df['whc_ratio_cof1'.upper()]>0.85))
df.loc[df['DXA_WB_WBTOT_BMD_COF1'].isin([-88888,-99991,-88880,-99999]),'DXA_WB_WBTOT_BMD_COF1'] = np.nan
DXA_WB_WBTOT_BMD_T_COF1 = (df['DXA_WB_WBTOT_BMD_COF1']-df['DXA_WB_WBTOT_BMD_COF1'].mean()) /df['DXA_WB_WBTOT_BMD_COF1'].std()
DF['DXA_WB_WBTOT_T_COF1'] = np.nan
DF.loc[(DXA_WB_WBTOT_BMD_T_COF1<=-2.5),'DXA_WB_WBTOT_T_COF1'] = 1
DF.loc[((DXA_WB_WBTOT_BMD_T_COF1>=-2.5)&(DXA_WB_WBTOT_BMD_T_COF1<1)),'DXA_WB_WBTOT_T_COF1'] = 0.5
DF.loc[(DXA_WB_WBTOT_BMD_T_COF1<=-1),'DXA_WB_WBTOT_T_COF1'] = 0


df.loc[df['dxa_wb_head_bmd_cof1'.upper()].isin([-88888,-99991,-88880,-99999]),'dxa_wb_head_bmd_cof1'.upper()] = np.nan
df.loc[df['dxa_wb_larm_bmd_cof1'.upper()].isin([-88888,-99991,-88880,-99999]),'dxa_wb_larm_bmd_cof1'.upper()] = np.nan
df.loc[df['dxa_wb_rarm_bmd_cof1'.upper()].isin([-88888,-99991,-88880,-99999]),'dxa_wb_rarm_bmd_cof1'.upper()] = np.nan
df.loc[df['dxa_wb_lrib_bmd_cof1'.upper()].isin([-88888,-99991,-88880,-99999]),'dxa_wb_lrib_bmd_cof1'.upper()] = np.nan
df.loc[df['dxa_wb_rrib_bmd_cof1'.upper()].isin([-88888,-99991,-88880,-99999]),'dxa_wb_rrib_bmd_cof1'.upper()] = np.nan
df.loc[df['dxa_wb_t_s_bmd_cof1'.upper()].isin([-88888,-99991,-88880,-99999]),'dxa_wb_t_s_bmd_cof1'.upper()] = np.nan
df.loc[df['dxa_wb_l_s_bmd_cof1'.upper()].isin([-88888,-99991,-88880,-99999]),'dxa_wb_l_s_bmd_cof1'.upper()] = np.nan
df.loc[df['dxa_wb_pelv_bmd_cof1'.upper()].isin([-88888,-99991,-88880,-99999]),'dxa_wb_pelv_bmd_cof1'.upper()] = np.nan
df.loc[df['dxa_wb_lleg_bmd_cof1'.upper()].isin([-88888,-99991,-88880,-99999]),'dxa_wb_lleg_bmd_cof1'.upper()] = np.nan
df.loc[df['dxa_wb_rleg_bmd_cof1'.upper()].isin([-88888,-99991,-88880,-99999]),'dxa_wb_rleg_bmd_cof1'.upper()] = np.nan

Osteoporosis =['dxa_wb_head_bmd_cof1'.upper(),'dxa_wb_larm_bmd_cof1'.upper(),
               'dxa_wb_rarm_bmd_cof1'.upper(),'dxa_wb_lrib_bmd_cof1'.upper(),
               'dxa_wb_rrib_bmd_cof1'.upper(),'dxa_wb_t_s_bmd_cof1'.upper(),
               'dxa_wb_l_s_bmd_cof1'.upper(),'dxa_wb_pelv_bmd_cof1'.upper(),
               'dxa_wb_lleg_bmd_cof1'.upper(),'dxa_wb_rleg_bmd_cof1'.upper()]

Osteoporosis_T = pd.DataFrame(index=df.index)
for region in Osteoporosis:
    ref_stats = (
        df.loc[df['AGE_NMBR_COF1'] == 45]
        .groupby('SEX_ASK_COM')[region]
        .agg(['mean', 'std'])
    )

    ref_mean = df['SEX_ASK_COM'].map(ref_stats['mean'])
    ref_std = df['SEX_ASK_COM'].map(ref_stats['std'])

    Osteoporosis_T[f'{region}_Tscore'] = (df[region] - ref_mean) / ref_std

#Osteoporosis_T = (df[Osteoporosis] - df[Osteoporosis].mean()) / df[Osteoporosis].std()
Osteoporosis_T_TF = Osteoporosis_T<=-2.5
Osteoporosis_T_Count = Osteoporosis_T_TF.sum(axis=1)
DF['DXA_Osteoporosis_BMD_T'] = np.nan
DF.loc[(Osteoporosis_T_Count>=2),'DXA_Osteoporosis_BMD_T']=1
DF.loc[(Osteoporosis_T_Count==1),'DXA_Osteoporosis_BMD_T']=0.5
DF.loc[(Osteoporosis_T_Count==0),'DXA_Osteoporosis_BMD_T']=0

df.loc[df['DXA_OI_APDG_LEAN_MASS_H2_COF1'].isin([-88888,-99991,-88880,-99999]),'DXA_OI_APDG_LEAN_MASS_H2_COF1'] = np.nan
df.loc[df['DXA_OI_TOTAL_PERCENT_FAT_COF1'].isin([-88888,-99991,-88880,-99999]),'DXA_OI_TOTAL_PERCENT_FAT_COF1'] = np.nan
DF['DXA_OI_APDG_LEAN_MASS_H2_COF1'] = stratified_scaling(df, 'DXA_OI_APDG_LEAN_MASS_H2_COF1', inverse=True)
DF['DXA_OI_TOTAL_PERCENT_FAT_COF1'] = stratified_scaling(df, 'DXA_OI_TOTAL_PERCENT_FAT_COF1', inverse=False)

########
df.loc[df['DXA_WBC_LARM_PFAT_COF1'].isin([-88888,-99991,-88880,-99999]),'DXA_WBC_LARM_PFAT_COF1'] = np.nan 
df.loc[df['DXA_WBC_RARM_PFAT_COF1'].isin([-88888,-99991,-88880,-99999]),'DXA_WBC_RARM_PFAT_COF1'] = np.nan 
df.loc[df['DXA_WBC_L_LEG_PFAT_COF1'].isin([-88888,-99991,-88880,-99999]),'DXA_WBC_L_LEG_PFAT_COF1'] = np.nan 
df.loc[df['DXA_WBC_R_LEG_PFAT_COF1'].isin([-88888,-99991,-88880,-99999]),'DXA_WBC_R_LEG_PFAT_COF1'] = np.nan 
df.loc[df['DXA_WBC_TRUNK_PFAT_COF1'].isin([-88888,-99991,-88880,-99999]),'DXA_WBC_TRUNK_PFAT_COF1'] = np.nan 
df.loc[df['DXA_WBC_HEAD_PFAT_COF1'].isin([-88888,-99991,-88880,-99999]),'DXA_WBC_HEAD_PFAT_COF1'] = np.nan

BodyFatAreas =['DXA_WBC_LARM_PFAT_COF1','DXA_WBC_RARM_PFAT_COF1','DXA_WBC_L_LEG_PFAT_COF1',
                   'DXA_WBC_R_LEG_PFAT_COF1','DXA_WBC_TRUNK_PFAT_COF1','DXA_WBC_HEAD_PFAT_COF1']

BodyFatAreas_Individual = df[BodyFatAreas]
BodyFatAreas_P95 = BodyFatAreas_Individual.quantile(0.95)
ExcessBodyFatArea=BodyFatAreas_Individual>=BodyFatAreas_P95
ExcessBodyFatArea_Count=ExcessBodyFatArea.sum(axis=1)
DF['AGGREGATE_BODY_FAT'] = np.nan
DF.loc[(ExcessBodyFatArea_Count==0),'AGGREGATE_BODY_FAT']=0
DF.loc[(ExcessBodyFatArea_Count==1),'AGGREGATE_BODY_FAT']=0.2
DF.loc[(ExcessBodyFatArea_Count==2),'AGGREGATE_BODY_FAT']=0.4
DF.loc[(ExcessBodyFatArea_Count==3),'AGGREGATE_BODY_FAT']=0.5
DF.loc[(ExcessBodyFatArea_Count==4),'AGGREGATE_BODY_FAT']=0.8
DF.loc[(ExcessBodyFatArea_Count>=5),'AGGREGATE_BODY_FAT']=1

# Domain 5: Spirometry measures
"""""
FVC = ['spr_fvc_t1_cof1'.upper(),'spr_fvc_t2_cof1'.upper(),'spr_fvc_t3_cof1'.upper(),
         'spr_fvc_t4_cof1'.upper(),'spr_fvc_t5_cof1'.upper(),'spr_fvc_t6_cof1'.upper(),
         'spr_fvc_t7_cof1'.upper(),'spr_fvc_t8_cof1'.upper()]
FVCDF = df[FVC]
df['FVC_Max'.upper()] = FVCDF.max(axis=1, skipna=True)
DF['FVC_Max'.upper()] = stratified_scaling(df, 'FVC_Max'.upper() , inverse=True)


FEV1 = ['SPR_FEV1_FVC_T1_COF1','SPR_FEV1_FVC_T2_COF1','SPR_FEV1_FVC_T3_COF1',
        'SPR_FEV1_FVC_T4_COF1','SPR_FEV1_FVC_T5_COF1','SPR_FEV1_FVC_T6_COF1',
        'SPR_FEV1_FVC_T7_COF1','SPR_FEV1_FVC_T8_COF1']
FEV1DF = df[FEV1]
df['FEV1_MAX'] = FEV1DF.max(axis=1, skipna=True)
DF['FEV1_MAX'] = stratified_scaling(df, 'FEV1_MAX' , inverse=True)
"""
# Domain 6: Hearing and vision
df.loc[df['va_etdrs_l_rslt_cof1'.upper()].isin([-88888,-99991,-88880,-99999]),'va_etdrs_l_rslt_cof1'.upper()] = np.nan
DF['va_etdrs_l_rslt_cof1'.upper()] = stratified_scaling(df, 'va_etdrs_l_rslt_cof1'.upper() , inverse=True)
df.loc[df['va_etdrs_r_rslt_cof1'.upper()].isin([-88888,-99991,-88880,-99999]),'va_etdrs_r_rslt_cof1'.upper()] = np.nan
DF['va_etdrs_r_rslt_cof1'.upper()] = stratified_scaling(df, 'va_etdrs_r_rslt_cof1'.upper() , inverse=True)
df.loc[df['ton_iopcc_r_cof1'.upper()].isin([-88888,-99991,-88880,-99999]),'ton_iopcc_r_cof1'.upper()] = np.nan
DF['ton_iopcc_r_cof1'.upper()] = (df['ton_iopcc_r_cof1'.upper()]<11) | (df['ton_iopcc_r_cof1'.upper()]>21)
DF.loc[(df['ICQ_DERET3MO_COF1']==1) | (df['ICQ_SRGYEYE_COF1'].isin([1,2,3])), 'ton_iopcc_r_cof1'.upper()] = 1
DF.loc[df['ICQ_EYEINF_COF1'].isin([1,2,3]) , 'ton_iopcc_r_cof1'.upper()] = np.nan
df.loc[df['ton_iopcc_l_cof1'.upper()].isin([-88888,-99991,-88880,-99999]),'ton_iopcc_l_cof1'.upper()] = np.nan
DF['ton_iopcc_l_cof1'.upper()] = (df['ton_iopcc_l_cof1'.upper()]<11) | (df['ton_iopcc_l_cof1'.upper()]>21)
DF.loc[(df['ICQ_DERET3MO_COF1']==1) | (df['ICQ_SRGYEYE_COF1'].isin([1,2,3])), 'ton_iopcc_l_cof1'.upper()] = 1
DF.loc[df['ICQ_EYEINF_COF1'].isin([1,2,3]) , 'ton_iopcc_l_cof1'.upper()] = np.nan
df.loc[df['ton_ch_r_cof1'.upper()].isin([-88888,-99991,-88880,-99999]),'ton_ch_r_cof1'.upper()] = np.nan
DF['ton_ch_r_cof1'.upper()] = df['ton_ch_r_cof1'.upper()]<=9
DF.loc[(df['ICQ_DERET3MO_COF1']==1) | (df['ICQ_SRGYEYE_COF1'].isin([1,2,3])), 'ton_ch_r_cof1'.upper()] = 1
DF.loc[df['ICQ_EYEINF_COF1'].isin([1,2,3]) , 'ton_ch_r_cof1'.upper()] = np.nan
df.loc[df['ton_ch_l_cof1'.upper()].isin([-88888,-99991,-88880,-99999]),'ton_ch_l_cof1'.upper()] = np.nan
DF['ton_ch_l_cof1'.upper()] = df['ton_ch_l_cof1'.upper()]<=9
DF.loc[(df['ICQ_DERET3MO_COF1']==1) | (df['ICQ_SRGYEYE_COF1'].isin([1,2,3])), 'ton_ch_l_cof1'.upper()] = 1
DF.loc[df['ICQ_EYEINF_COF1'].isin([1,2,3]) , 'ton_ch_l_cof1'.upper()] = np.nan

df.loc[df['bp_systolic_avg_cof1'.upper()].isin([-88888,-99991,-88880,-99999]),'bp_systolic_avg_cof1'.upper()] = np.nan
df.loc[df['bp_diastolic_avg_cof1'.upper()].isin([-88888,-99991,-88880,-99999]),'bp_diastolic_avg_cof1'.upper()] = np.nan
Mean_Arterial_Pressure = df['bp_systolic_avg_cof1'.upper()] + 2*df['bp_diastolic_avg_cof1'.upper()] 

df.loc[df['ton_iopg_r_cof1'.upper()].isin([-88888,-99991,-88880,-99999]),'ton_iopg_r_cof1'.upper()] = np.nan
df.loc[df['ton_iopg_l_cof1'.upper()].isin([-88888,-99991,-88880,-99999]),'ton_iopg_l_cof1'.upper()] = np.nan
Mean_Intraocular_Pressure = (df['ton_iopg_r_cof1'.upper()] + df['ton_iopg_l_cof1'.upper()])/2
Ocular_Perfusion_Pressure = ((2/3)*Mean_Arterial_Pressure) - Mean_Intraocular_Pressure
DF['Mean_Ocular_Perfusion_Pressure'.upper()] = Ocular_Perfusion_Pressure >= 42

df.loc[df['hrg_right_1k_cof1'.upper()].isin([-88888,-99991,-88880,-99999]),'hrg_right_1k_cof1'.upper()] = np.nan
df.loc[df['hrg_right_2k_cof1'.upper()].isin([-88888,-99991,-88880,-99999]),'hrg_right_2k_cof1'.upper()] = np.nan
df.loc[df['hrg_right_500_cof1'.upper()].isin([-88888,-99991,-88880,-99999]),'hrg_right_500_cof1'.upper()] = np.nan
df.loc[df['hrg_right_4k_cof1'.upper()].isin([-88888,-99991,-88880,-99999]),'hrg_right_4k_cof1'.upper()] = np.nan
columns_to_average = ['hrg_right_500_cof1'.upper(),'hrg_right_1k_cof1'.upper(),
                      'hrg_right_2k_cof1'.upper(),'hrg_right_4k_cof1'.upper()]

# 2. Calculate the average across the rows (axis=1)
df['Pure_Tone_R'.upper()] = df[columns_to_average].mean(axis=1)
DF['Pure_Tone_R'.upper()] = stratified_scaling(df, 'Pure_Tone_R'.upper() , inverse=True)

df.loc[df['hrg_left_500_cof1'.upper()].isin([-88888,-99991,-88880,-99999]),'hrg_left_500_cof1'.upper()] = np.nan
df.loc[df['hrg_left_1k_cof1'.upper()].isin([-88888,-99991,-88880,-99999]),'hrg_left_1k_cof1'.upper()] = np.nan
df.loc[df['hrg_left_2k_cof1'.upper()].isin([-88888,-99991,-88880,-99999]),'hrg_left_2k_cof1'.upper()] = np.nan
df.loc[df['hrg_left_4k_cof1'.upper()].isin([-88888,-99991,-88880,-99999]),'hrg_left_4k_cof1'.upper()] = np.nan
columns_to_average = ['hrg_left_500_cof1'.upper(),'hrg_left_1k_cof1'.upper(),
                      'hrg_left_2k_cof1'.upper(),'hrg_left_4k_cof1'.upper()]

# 2. Calculate the average across the rows (axis=1)
df['Pure_Tone_L'.upper()] = df[columns_to_average].mean(axis=1)
DF['Pure_Tone_L'.upper()] = stratified_scaling(df, 'Pure_Tone_L'.upper() , inverse=True)

print(DF)
RAWDF=DF
IsEmpty = DF.isna() | (DF == "")
DataNA = IsEmpty.sum(axis=1)
RowsToDrop = DataNA.index[DataNA>FIExaminationCount*0.2]
DF.drop(RowsToDrop, inplace=True)
IsEmpty = DF.isna() | (DF == "")
NotEmpty = ~IsEmpty
DataAvailable = NotEmpty.sum(axis=1)

DeficitsCount = DF.sum(axis=1)
FIExamination = DeficitsCount/DataAvailable
FIExaminationData = df[['entity_id','AGE_NMBR_COF1', 'SEX_ASK_COM']].copy()
FIExaminationData['FI_Examination'] = np.nan
FIExaminationData.loc[:,'FI_Examination'] = FIExamination

from pathlib import Path

# Define the folder and file name
output_file = Path(r"E:\CLSA\CLSA\results\FIExamination_FUP.xlsx")

# Create the folder automatically if it is missing
output_file.parent.mkdir(parents=True, exist_ok=True)

# Save the DataFrame
FIExaminationData.to_excel(output_file, index=False)




"""


#print(K)
#print(df['ecg_result_cof1'.upper()])
#print(max(df['tmt_itpexact_cof1'.upper()]))
#import matplotlib.pyplot as plt
#import numpy as np
#plt.hist(DF['va_etdrs_r_rslt_cof1'.upper()], bins=20,color='skyblue', edgecolor='black')
#plt.show()

# Select boolean columns and overwrite them with 1 and 0
bool_cols = df.select_dtypes(include='bool').columns
df[bool_cols] = df[bool_cols].astype(int)
"""