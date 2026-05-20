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
#print(ColumnNames)
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
                   'stp_dottime_ss_com','stp_coltime_ss_com','STP_STARTLANG_COM',
                   'bp_systolic_avg_com','bp_diastolic_avg_com','bp_pulse_avg_com',
                   'bp_pulse_avg_com','ecg_result_com','ecg_pq_interval_com','ecg_qrs_duration_com',
                   'ecg_qtc_interval_com','ecg_p_axis_com','ecg_r_axis_com','ecg_t_axis_com',
                   'ecg_p_duration_com','hwt_dbmi_com','whc_ratio_com',
                   'dxa_wb_head_bmd_com','dxa_wb_larm_bmd_com','dxa_wb_rarm_bmd_com',
                   'dxa_wb_lrib_bmd_com', 'dxa_wb_rrib_bmd_com','dxa_wb_t_s_bmd_com',
                   'dxa_wb_l_s_bmd_com','dxa_wb_pelv_bmd_com','dxa_wb_lleg_bmd_com',
                   'dxa_wb_rleg_bmd_com','DXA_WB_WBTOT_BMD_COM','DXA_OI_APDG_LEAN_MASS_H2_COM',
                   'DXA_OI_TOTAL_PERCENT_FAT_COM',
                   'DXA_WBC_LARM_PFAT_COM','DXA_WBC_RARM_PFAT_COM','DXA_WBC_L_LEG_PFAT_COM',
                   'DXA_WBC_R_LEG_PFAT_COM','DXA_WBC_TRUNK_PFAT_COM','DXA_WBC_HEAD_PFAT_COM',
                   'spr_fvc_t1_com','spr_fvc_t2_com','spr_fvc_t3_com','spr_fvc_t4_com',
                   'spr_fvc_t5_com','spr_fvc_t6_com','spr_fvc_t7_com','spr_fvc_t8_com',
                   'SPR_FEV1_FVC_T1_COM','SPR_FEV1_FVC_T2_COM','SPR_FEV1_FVC_T3_COM',
                   'SPR_FEV1_FVC_T4_COM','SPR_FEV1_FVC_T5_COM','SPR_FEV1_FVC_T6_COM',
                   'SPR_FEV1_FVC_T7_COM','SPR_FEV1_FVC_T8_COM',
                   'va_etdrs_l_rslt_com','va_etdrs_r_rslt_com','ton_iopcc_r_com','ton_iopcc_l_com',
                   'ton_ch_l_com','ton_ch_r_com','ton_iopg_r_com','ton_iopg_l_com',
                   'bp_systolic_avg_com','bp_diastolic_avg_com',
                   'hrg_right_500_com','hrg_right_1k_com','hrg_right_2k_com','hrg_right_4k_com',
                   'hrg_left_500_com','hrg_left_1k_com','hrg_left_2k_com','hrg_left_4k_com']

#'imt_r_avg_com','imt_l_avg_com'
#'dxa_wb_wbtot_t_com'
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
FAS_F_SCORE = stratified_scaling(df, target_col='fas_f_score_com'.upper(),
                                                       group_col=strat_list, inverse=True)

strat_list = ['SEX_ASK_COM', 'ED_HIGH_COM','FAS_A_LANG_COM']
FAS_A_SCORE = stratified_scaling(df, target_col='fas_a_score_com'.upper(),
                                                       group_col=strat_list, inverse=True)

strat_list = ['SEX_ASK_COM', 'ED_HIGH_COM','FAS_S_LANG_COM']
FAS_S_SCORE = stratified_scaling(df, target_col='fas_s_score_com'.upper(),
                                                       group_col=strat_list, inverse=True)                                                       

DF['Controlled_Oral_Word_Association']=pd.concat([FAS_A_SCORE,FAS_F_SCORE,FAS_S_SCORE], axis=1).mean(axis=1,skipna=True)

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
DF["bp_systolic_avg_com".upper()]  = (df["bp_systolic_avg_com".upper()]<90) | (df["bp_systolic_avg_com".upper()]>140)    
DF["bp_diastolic_avg_com".upper()] = (df["bp_diastolic_avg_com".upper()]<=60)
df["pulse_pressure".upper()]       = df['bp_systolic_avg_com'.upper()]-df['bp_diastolic_avg_com'.upper()]
DF['pulse_pressure'.upper()]       = (df['pulse_pressure'.upper()]<=30) | (df['pulse_pressure'.upper()]>60)
DF['bp_pulse_avg_com'.upper()]     = (df['bp_pulse_avg_com'.upper()]<=60) | (df['bp_pulse_avg_com'.upper()]>99)
#DF['imt_r_avg_com'.upper()]        = (df['imt_r_avg_com'.upper()]<0.5) | (df['imt_r_avg_com'.upper()]>0.8)
#DF['imt_l_avg_com'.upper()]         = (df['imt_l_avg_com'.upper()]<0.5) | (df['imt_l_avg_com'.upper()]>0.8)
DF['ecg_result_com'.upper()] = 'Nan'
DF['ecg_result_com'.upper()].loc[(df['ecg_result_com'.upper()] == 4) | (df['ecg_result_com'.upper()] == 5)]= 1
DF['ecg_result_com'.upper()].loc[df['ecg_result_com'.upper()] == 3] = 0.66
DF['ecg_result_com'.upper()].loc[df['ecg_result_com'.upper()] == 2] = 0.33
DF['ecg_result_com'.upper()].loc[df['ecg_result_com'.upper()] == 1] = 0
DF['ecg_pq_interval_com'.upper()] = (df['ecg_pq_interval_com'.upper()]<=12) | (df['ecg_pq_interval_com'.upper()]>200)
DF['ecg_qrs_duration_com'.upper()] = df['ecg_qrs_duration_com'.upper()] >= 100
DF['ecg_qtc_interval_com'.upper()] = ((df["SEX_ASK_COM"]=="M") & (df['ecg_qtc_interval_com'.upper()]>430))|((df["SEX_ASK_COM"]=="F") & (df['ecg_qtc_interval_com'.upper()]>450))
DF['ecg_p_axis_com'.upper()] = (df['ecg_p_axis_com'.upper()]<0) | (df['ecg_p_axis_com'.upper()]>75)
DF['ecg_r_axis_com'.upper()] = (df['ecg_r_axis_com'.upper()]<-30) | (df['ecg_r_axis_com'.upper()]>90)
DF['ecg_t_axis_com'.upper()] = (df['ecg_t_axis_com'.upper()]<0) | (df['ecg_t_axis_com'.upper()]>90)
DF['ecg_p_duration_com'.upper()] = df['ecg_p_duration_com'.upper()]>120
# Domain 4: Anthropometric measures
DF['hwt_dbmi_com'.upper()] = 'Nan'
DF['hwt_dbmi_com'.upper()].loc[(df['hwt_dbmi_com'.upper()]<=18.5)|(df['hwt_dbmi_com'.upper()]>=30)] = 1
DF['hwt_dbmi_com'.upper()].loc[(df['hwt_dbmi_com'.upper()]>=25)&(df['hwt_dbmi_com'.upper()]<=29.9)] = 0.5 
DF['hwt_dbmi_com'.upper()].loc[(df['hwt_dbmi_com'.upper()]>=18.5)&(df['hwt_dbmi_com'.upper()]<=24.9)] = 0
DF['whc_ratio_com'.upper()] = ((df['SEX_ASK_COM']=='M')&(df['whc_ratio_com'.upper()]>0.9)) | ((df['SEX_ASK_COM']=='F')&(df['whc_ratio_com'.upper()]>0.85))
DXA_WB_WBTOT_BMD_T_COM = (df['DXA_WB_WBTOT_BMD_COM']-df['DXA_WB_WBTOT_BMD_COM'].mean()) /df['DXA_WB_WBTOT_BMD_COM'].std()
DF['DXA_WB_WBTOT_T_COM'.upper()] = 'Nan'
DF['DXA_WB_WBTOT_T_COM'.upper()].loc[DXA_WB_WBTOT_BMD_T_COM<=-2.5]=1
DF['DXA_WB_WBTOT_T_COM'.upper()].loc[(DXA_WB_WBTOT_BMD_T_COM>=-2.5)&(DXA_WB_WBTOT_BMD_T_COM<1)]=0.5
DF['DXA_WB_WBTOT_T_COM'.upper()].loc[DXA_WB_WBTOT_BMD_T_COM<=-1]=0
Osteoporosis =['dxa_wb_head_bmd_com'.upper(),'dxa_wb_larm_bmd_com'.upper(),
               'dxa_wb_rarm_bmd_com'.upper(),'dxa_wb_lrib_bmd_com'.upper(),
               'dxa_wb_rrib_bmd_com'.upper(),'dxa_wb_t_s_bmd_com'.upper(),
               'dxa_wb_l_s_bmd_com'.upper(),'dxa_wb_pelv_bmd_com'.upper(),
               'dxa_wb_lleg_bmd_com'.upper(),'dxa_wb_rleg_bmd_com'.upper()]

Osteoporosis_T = (df[Osteoporosis] - df[Osteoporosis].mean()) / df[Osteoporosis].std()
Osteoporosis_T_TF = Osteoporosis_T<=-2.5
Osteoporosis_T_Count = Osteoporosis_T_TF.sum(axis=1)
DF['DXA_Osteoporosis_BMD_T']='Nan'
DF['DXA_Osteoporosis_BMD_T'].loc[Osteoporosis_T_Count>=2]=1
DF['DXA_Osteoporosis_BMD_T'].loc[Osteoporosis_T_Count==1]=0.5
DF['DXA_Osteoporosis_BMD_T'].loc[Osteoporosis_T_Count==0]=0
DF['DXA_OI_APDG_LEAN_MASS_H2_COM'] = stratified_scaling(df, 'DXA_OI_APDG_LEAN_MASS_H2_COM', inverse=True)
DF['DXA_OI_TOTAL_PERCENT_FAT_COM'] = stratified_scaling(df, 'DXA_OI_TOTAL_PERCENT_FAT_COM', inverse=False)
BodyFatAreas =['DXA_WBC_LARM_PFAT_COM','DXA_WBC_RARM_PFAT_COM','DXA_WBC_L_LEG_PFAT_COM',
                   'DXA_WBC_R_LEG_PFAT_COM','DXA_WBC_TRUNK_PFAT_COM','DXA_WBC_HEAD_PFAT_COM']
BodyFatAreas_Individual = df[BodyFatAreas]
BodyFatAreas_P95 = BodyFatAreas_Individual.quantile(0.95)
ExcessBodyFatArea=BodyFatAreas_Individual>=BodyFatAreas_P95
ExcessBodyFatArea_Count=ExcessBodyFatArea.sum(axis=1)
DF['AGGREGATE_BODY_FAT'] = 'Nan'
DF['AGGREGATE_BODY_FAT'].loc[ExcessBodyFatArea_Count==0]=0
DF['AGGREGATE_BODY_FAT'].loc[ExcessBodyFatArea_Count==1]=0.2
DF['AGGREGATE_BODY_FAT'].loc[ExcessBodyFatArea_Count==2]=0.4
DF['AGGREGATE_BODY_FAT'].loc[ExcessBodyFatArea_Count==3]=0.5
DF['AGGREGATE_BODY_FAT'].loc[ExcessBodyFatArea_Count==4]=0.8
DF['AGGREGATE_BODY_FAT'].loc[ExcessBodyFatArea_Count>=5]=1

# Domain 5: Spirometry measures
FVC = ['spr_fvc_t1_com'.upper(),'spr_fvc_t2_com'.upper(),'spr_fvc_t3_com'.upper(),
         'spr_fvc_t4_com'.upper(),'spr_fvc_t5_com'.upper(),'spr_fvc_t6_com'.upper(),
         'spr_fvc_t7_com'.upper(),'spr_fvc_t8_com'.upper()]
FVCDF = df[FVC]
df['FVC_Max'.upper()] = FVCDF.max(axis=1, skipna=True)
DF['FVC_Max'.upper()] = stratified_scaling(df, 'FVC_Max'.upper() , inverse=True)
FEV1 = ['SPR_FEV1_FVC_T1_COM','SPR_FEV1_FVC_T2_COM','SPR_FEV1_FVC_T3_COM',
        'SPR_FEV1_FVC_T4_COM','SPR_FEV1_FVC_T5_COM','SPR_FEV1_FVC_T6_COM',
        'SPR_FEV1_FVC_T7_COM','SPR_FEV1_FVC_T8_COM']
FEV1DF = df[FEV1]
df['FEV1_MAX'] = FEV1DF.max(axis=1, skipna=True)
DF['FEV1_MAX'] = stratified_scaling(df, 'FEV1_MAX' , inverse=True)

# Domain 6: Hearing and vision
DF['va_etdrs_l_rslt_com'.upper()] = stratified_scaling(df, 'va_etdrs_l_rslt_com'.upper() , inverse=True)
DF['va_etdrs_r_rslt_com'.upper()] = stratified_scaling(df, 'va_etdrs_r_rslt_com'.upper() , inverse=True)
DF['ton_iopcc_r_com'.upper()] = (df['ton_iopcc_r_com'.upper()]<11) | (df['ton_iopcc_r_com'.upper()]>21)
DF['ton_iopcc_l_com'.upper()] = (df['ton_iopcc_l_com'.upper()]<11) | (df['ton_iopcc_l_com'.upper()]>21)
DF['ton_ch_r_com'.upper()] = df['ton_ch_r_com'.upper()]<=9
DF['ton_ch_l_com'.upper()] = df['ton_ch_l_com'.upper()]<=9

Mean_Arterial_Pressure = df['bp_systolic_avg_com'.upper()] + 2*df['bp_diastolic_avg_com'.upper()] 
Mean_Intraocular_Pressure = (df['ton_iopg_r_com'.upper()] + df['ton_iopg_l_com'.upper()])/2
Ocular_Perfusion_Pressure = ((2/3)*Mean_Arterial_Pressure) - Mean_Intraocular_Pressure
DF['Mean_Ocular_Perfusion_Pressure'.upper()] = Ocular_Perfusion_Pressure >= 42

columns_to_average = ['hrg_right_500_com'.upper(),'hrg_right_1k_com'.upper(),
                      'hrg_right_2k_com'.upper(),'hrg_right_4k_com'.upper()]

# 2. Calculate the average across the rows (axis=1)
df['Pure_Tone_R'.upper()] = df[columns_to_average].mean(axis=1)
DF['Pure_Tone_R'.upper()] = stratified_scaling(df, 'Pure_Tone_R'.upper() , inverse=True)

columns_to_average = ['hrg_left_500_com'.upper(),'hrg_left_1k_com'.upper(),
                      'hrg_left_2k_com'.upper(),'hrg_left_4k_com'.upper()]

# 2. Calculate the average across the rows (axis=1)
df['Pure_Tone_L'.upper()] = df[columns_to_average].mean(axis=1)
DF['Pure_Tone_L'.upper()] = stratified_scaling(df, 'Pure_Tone_L'.upper() , inverse=True)


print(DF)

#print(K)
#print(df['ecg_result_com'.upper()])
#print(max(df['tmt_itpexact_com'.upper()]))
#import matplotlib.pyplot as plt
#import numpy as np
#plt.hist(DF['va_etdrs_r_rslt_com'.upper()], bins=20,color='skyblue', edgecolor='black')
#plt.show()

"""
# Select boolean columns and overwrite them with 1 and 0
bool_cols = df.select_dtypes(include='bool').columns
df[bool_cols] = df[bool_cols].astype(int)
"""