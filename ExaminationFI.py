# -*- coding: utf-8 -*-
"""
Created on Sun May  3 21:06:49 2026

@author: mmogh
"""
"FI-EXAMINATION"  
import pandas as pd
from sklearn.preprocessing import StandardScaler
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import gc

file_path = 'E:/CLSA/CLSA/data/2310011_UCalgary_RRose_BL/2310011_UCalgary_RRose_BL/2310011_UCalgary_RRose_Baseline_CoPv7.csv'
# Define specific dtypes for columns to optimize memory
# optimized_dtypes = {
#     'MEDI_DOSE_FRQ_1_COF1': 'int8',
    
# }
def prevalence(df, target_col):
    """Plots a chosen target column against age."""
    prevalence = df[target_col].mean()
    print(f"Prevalence of {target_col}: {prevalence:.2%}")
    # Alternative: Automated binned scatter plot with error bars
    plt.figure()
    sns.regplot(
        data=df, x="AGE_NMBR_COM", y=target_col, x_bins=np.arange(45, 90, 1), fit_reg=False
    )
    #plt.show()



#Plot a parameter vs Age
def GroupedPlot(df, target_col):
        # Create your plot axis
        fig, ax = plt.subplots(figsize=(6, 5))

        # Define your 2 groups and 2 colors
        categories = df["SEX_ASK_COM"].unique()
        colors = ["#1f77b4", "#d62728"]
        # Loop through each group and overlay them on the same axis ('ax=ax')
        for category, color in zip(categories, colors):
            subset = df[df["SEX_ASK_COM"] == category]
            plt.figure()
            sns.regplot(
                data=subset,
                x="AGE_NMBR_COM",
                y=target_col,
                x_bins=np.arange(45, 90, 1), fit_reg=False,
                ax=ax,  # Tells regplot to draw on the same chart
                color=color,
                label=category,
                #scatter=False,  # Hides scatter points as you wanted before
                #ci=None,
            )

        # Add the legend manually since regplot won't make a grouped one automatically
        sns.despine(trim=True)





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
            return group * 0 + 0.5
        
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
FIExaminationCount = 44 #47
DF = pd.DataFrame()

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
                   'hrg_left_500_com','hrg_left_1k_com','hrg_left_2k_com','hrg_left_4k_com',
                   'ICQ_HRTCOND_COM','ICQ_SRGYHRT_COM','ICQ_SRGYCHT_COM','ICQ_BLDSP3MO_COM',
                   'ICQ_ANEURY_COM','ICQ_EMB6WK_COM','ICQ_EMBMED_COM','ICQ_NGTUBE_COM',
                   'ICQ_DERET3MO_COM','ICQ_SRGYEYE_COM','ICQ_EYEINF_COM']


#'imt_r_avg_com','imt_l_avg_com'
#'dxa_wb_wbtot_t_com'
required_columns = [f.upper() for f in required_columns]
required_columns.insert(0,'entity_id')


df = pd.read_csv(file_path, usecols=required_columns)
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
df.loc[df['wlk_time_com'.upper()].isin([-88]),'wlk_time_com'.upper()] = np.nan
DF['wlk_time_com'.upper()] = stratified_scaling(df, 'wlk_time_com'.upper() , inverse=False)
DF['cr_avg_time_com'.upper()] = stratified_scaling(df, 'cr_avg_time_com'.upper(), inverse=False)
df.loc[df['TUG_TIME_COM'].isin([-88]),'TUG_TIME_COM'] = np.nan
DF['tug_time_com'.upper()] = stratified_scaling(df, 'tug_time_com'.upper(), inverse=False)
DF['gs_exam_max_com'.upper()] = stratified_scaling(df, 'gs_exam_max_com'.upper(), inverse=True)
DF['bal_best_com'.upper()] = stratified_scaling(df, 'bal_best_com'.upper(), inverse=True)
# Domain 2: Cognition
df.loc[df['ED_HIGH_COM'].isin([97,98,99]),'ED_HIGH_COM'] = np.nan
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

df.loc[df['stp_dottime_ss_com'.upper()].isin([-888]),'stp_dottime_ss_com'.upper()] = np.nan
df.loc[df['stp_coltime_ss_com'.upper()].isin([-888]),'stp_coltime_ss_com'.upper()] = np.nan
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
DF['ecg_result_com'.upper()] = np.nan
DF.loc[((df['ecg_result_com'.upper()] == 4) | (df['ecg_result_com'.upper()] == 5)),'ecg_result_com'.upper()]= 1
DF.loc[(df['ecg_result_com'.upper()] == 3),'ecg_result_com'.upper()] = 0.66
DF.loc[(df['ecg_result_com'.upper()] == 2),'ecg_result_com'.upper()] = 0.33
DF.loc[(df['ecg_result_com'.upper()] == 1),'ecg_result_com'.upper()] = 0

DF['ecg_pq_interval_com'.upper()] = (df['ecg_pq_interval_com'.upper()]<=12) | (df['ecg_pq_interval_com'.upper()]>200)
DF['ecg_qrs_duration_com'.upper()] = df['ecg_qrs_duration_com'.upper()] >= 100
DF['ecg_qtc_interval_com'.upper()] = ((df["SEX_ASK_COM"]=="M") & (df['ecg_qtc_interval_com'.upper()]>430))|((df["SEX_ASK_COM"]=="F") & (df['ecg_qtc_interval_com'.upper()]>450))
DF['ecg_p_axis_com'.upper()] = (df['ecg_p_axis_com'.upper()]<0) | (df['ecg_p_axis_com'.upper()]>75)
DF['ecg_r_axis_com'.upper()] = (df['ecg_r_axis_com'.upper()]<-30) | (df['ecg_r_axis_com'.upper()]>90)
DF['ecg_t_axis_com'.upper()] = (df['ecg_t_axis_com'.upper()]<0) | (df['ecg_t_axis_com'.upper()]>90)
DF['ecg_p_duration_com'.upper()] = df['ecg_p_duration_com'.upper()]>120
# Domain 4: Anthropometric measures
df.loc[df['hwt_dbmi_com'.upper()].isin([999.96, 999.99]),'hwt_dbmi_com.upper()'] = np.nan
DF['hwt_dbmi_com'.upper()] = np.nan
DF.loc[((df['hwt_dbmi_com'.upper()]<=18.5)|(df['hwt_dbmi_com'.upper()]>=30))  ,'hwt_dbmi_com'.upper()] = 1
DF.loc[((df['hwt_dbmi_com'.upper()]>=25)&(df['hwt_dbmi_com'.upper()]<=29.9))  ,'hwt_dbmi_com'.upper()] = 0.5 
DF.loc[((df['hwt_dbmi_com'.upper()]>=18.5)&(df['hwt_dbmi_com'.upper()]<=24.9)),'hwt_dbmi_com'.upper()] = 0

DF['whc_ratio_com'.upper()] = ((df['SEX_ASK_COM']=='M')&(df['whc_ratio_com'.upper()]>0.9)) | ((df['SEX_ASK_COM']=='F')&(df['whc_ratio_com'.upper()]>0.85))
DXA_WB_WBTOT_BMD_T_COM = (df['DXA_WB_WBTOT_BMD_COM']-df['DXA_WB_WBTOT_BMD_COM'].mean()) /df['DXA_WB_WBTOT_BMD_COM'].std()
DF['DXA_WB_WBTOT_T_COM'] = np.nan
DF.loc[(DXA_WB_WBTOT_BMD_T_COM<=-2.5),'DXA_WB_WBTOT_T_COM'] = 1
DF.loc[((DXA_WB_WBTOT_BMD_T_COM>=-2.5)&(DXA_WB_WBTOT_BMD_T_COM<1)),'DXA_WB_WBTOT_T_COM'] = 0.5
DF.loc[(DXA_WB_WBTOT_BMD_T_COM<=-1),'DXA_WB_WBTOT_T_COM'] = 0

Osteoporosis =['dxa_wb_head_bmd_com'.upper(),'dxa_wb_larm_bmd_com'.upper(),
               'dxa_wb_rarm_bmd_com'.upper(),'dxa_wb_lrib_bmd_com'.upper(),
               'dxa_wb_rrib_bmd_com'.upper(),'dxa_wb_t_s_bmd_com'.upper(),
               'dxa_wb_l_s_bmd_com'.upper(),'dxa_wb_pelv_bmd_com'.upper(),
               'dxa_wb_lleg_bmd_com'.upper(),'dxa_wb_rleg_bmd_com'.upper()]

Osteoporosis_T = pd.DataFrame(index=df.index)
for region in Osteoporosis:
    ref_stats = (
        df.loc[df['AGE_NMBR_COM'] == 45]
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

DF['DXA_OI_APDG_LEAN_MASS_H2_COM'] = stratified_scaling(df, 'DXA_OI_APDG_LEAN_MASS_H2_COM', inverse=True)
DF['DXA_OI_TOTAL_PERCENT_FAT_COM'] = stratified_scaling(df, 'DXA_OI_TOTAL_PERCENT_FAT_COM', inverse=False)
BodyFatAreas =['DXA_WBC_LARM_PFAT_COM','DXA_WBC_RARM_PFAT_COM','DXA_WBC_L_LEG_PFAT_COM',
                   'DXA_WBC_R_LEG_PFAT_COM','DXA_WBC_TRUNK_PFAT_COM','DXA_WBC_HEAD_PFAT_COM']
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
FVC = ['spr_fvc_t1_com'.upper(),'spr_fvc_t2_com'.upper(),'spr_fvc_t3_com'.upper(),
         'spr_fvc_t4_com'.upper(),'spr_fvc_t5_com'.upper(),'spr_fvc_t6_com'.upper(),
         'spr_fvc_t7_com'.upper(),'spr_fvc_t8_com'.upper()]
FVCDF = df[FVC]
FVCDF_VALID = FVCDF.count(axis=1)
df['FVC_Max'.upper()] = FVCDF.max(axis=1, skipna=True)
DF['FVC_Max'.upper()] = stratified_scaling(df, 'FVC_Max'.upper() , inverse=True)
DF.loc[(FVCDF_VALID<3) , 'FVC_Max'.upper()] = np.nan


DF.loc[(df['ICQ_HRTCOND_COM']==1) | (df['ICQ_SRGYHRT_COM']==1) | (df['ICQ_SRGYCHT_COM'].isin([1,2,3])) |
       (df['ICQ_BLDSP3MO_COM']==1) | (df['ICQ_ANEURY_COM']==1) | (df['ICQ_EMB6WK_COM']==1) |
       (df['ICQ_EMBMED_COM']==1) , 'FVC_Max'.upper()] = 1

DF.loc[(df['ICQ_NGTUBE_COM']==1) | (df['ICQ_DERET3MO_COM']==1) | (df['ICQ_SRGYEYE_COM'].isin([1,2,3]))
       , 'FVC_Max'.upper()] = np.nan

df.loc[df['SPR_FEV1_FVC_T1_COM'].isin([777]),'SPR_FEV1_FVC_T1_COM'] = np.nan
df.loc[df['SPR_FEV1_FVC_T2_COM'].isin([777]),'SPR_FEV1_FVC_T2_COM'] = np.nan
df.loc[df['SPR_FEV1_FVC_T3_COM'].isin([777]),'SPR_FEV1_FVC_T3_COM'] = np.nan
df.loc[df['SPR_FEV1_FVC_T4_COM'].isin([777]),'SPR_FEV1_FVC_T4_COM'] = np.nan
df.loc[df['SPR_FEV1_FVC_T5_COM'].isin([777]),'SPR_FEV1_FVC_T5_COM'] = np.nan
df.loc[df['SPR_FEV1_FVC_T6_COM'].isin([777]),'SPR_FEV1_FVC_T6_COM'] = np.nan
df.loc[df['SPR_FEV1_FVC_T7_COM'].isin([777]),'SPR_FEV1_FVC_T7_COM'] = np.nan
df.loc[df['SPR_FEV1_FVC_T8_COM'].isin([777]),'SPR_FEV1_FVC_T8_COM'] = np.nan

FEV1 = ['SPR_FEV1_FVC_T1_COM','SPR_FEV1_FVC_T2_COM','SPR_FEV1_FVC_T3_COM',
        'SPR_FEV1_FVC_T4_COM','SPR_FEV1_FVC_T5_COM','SPR_FEV1_FVC_T6_COM',
        'SPR_FEV1_FVC_T7_COM','SPR_FEV1_FVC_T8_COM']
FEV1DF = df[FEV1]
FEV1DF_VALID = FEV1DF.count(axis=1)

df['FEV1_MAX'] = FEV1DF.max(axis=1, skipna=True)
DF['FEV1_MAX'] = stratified_scaling(df, 'FEV1_MAX' , inverse=True)
DF.loc[(FEV1DF_VALID<3) , 'FEV1_MAX'.upper()] = np.nan

# Domain 6: Hearing and vision
df.loc[df['va_etdrs_l_rslt_com'.upper()].isin([-88.8]),'va_etdrs_l_rslt_com'.upper()] = np.nan
DF['va_etdrs_l_rslt_com'.upper()] = stratified_scaling(df, 'va_etdrs_l_rslt_com'.upper() , inverse=True)
df.loc[df['va_etdrs_r_rslt_com'.upper()].isin([-88.8]),'va_etdrs_r_rslt_com'.upper()] = np.nan
DF['va_etdrs_r_rslt_com'.upper()] = stratified_scaling(df, 'va_etdrs_r_rslt_com'.upper() , inverse=True)
DF['ton_iopcc_r_com'.upper()] = (df['ton_iopcc_r_com'.upper()]<11) | (df['ton_iopcc_r_com'.upper()]>21)
DF.loc[(df['ICQ_DERET3MO_COM']==1) | (df['ICQ_SRGYEYE_COM'].isin([1,2,3])), 'ton_iopcc_r_com'.upper()] = 1
DF.loc[df['ICQ_EYEINF_COM'].isin([1,2,3]) , 'ton_iopcc_r_com'.upper()] = np.nan
DF['ton_iopcc_l_com'.upper()] = (df['ton_iopcc_l_com'.upper()]<11) | (df['ton_iopcc_l_com'.upper()]>21)
DF.loc[(df['ICQ_DERET3MO_COM']==1) | (df['ICQ_SRGYEYE_COM'].isin([1,2,3])), 'ton_iopcc_l_com'.upper()] = 1
DF.loc[df['ICQ_EYEINF_COM'].isin([1,2,3]) , 'ton_iopcc_l_com'.upper()] = np.nan
DF['ton_ch_r_com'.upper()] = df['ton_ch_r_com'.upper()]<=9
DF.loc[(df['ICQ_DERET3MO_COM']==1) | (df['ICQ_SRGYEYE_COM'].isin([1,2,3])), 'ton_ch_r_com'.upper()] = 1
DF.loc[df['ICQ_EYEINF_COM'].isin([1,2,3]) , 'ton_ch_r_com'.upper()] = np.nan
DF['ton_ch_l_com'.upper()] = df['ton_ch_l_com'.upper()]<=9
DF.loc[(df['ICQ_DERET3MO_COM']==1) | (df['ICQ_SRGYEYE_COM'].isin([1,2,3])), 'ton_ch_l_com'.upper()] = 1
DF.loc[df['ICQ_EYEINF_COM'].isin([1,2,3]) , 'ton_ch_l_com'.upper()] = np.nan

Mean_Arterial_Pressure = df['bp_systolic_avg_com'.upper()] + 2*df['bp_diastolic_avg_com'.upper()] 
Mean_Intraocular_Pressure = (df['ton_iopg_r_com'.upper()] + df['ton_iopg_l_com'.upper()])/2
Ocular_Perfusion_Pressure = ((2/3)*Mean_Arterial_Pressure) - Mean_Intraocular_Pressure
DF['Mean_Ocular_Perfusion_Pressure'.upper()] = Ocular_Perfusion_Pressure >= 42

df.loc[df['hrg_right_1k_com'.upper()].isin([-8]),'hrg_right_1k_com'.upper()] = np.nan
df.loc[df['hrg_right_2k_com'.upper()].isin([-8]),'hrg_right_2k_com'.upper()] = np.nan

columns_to_average = ['hrg_right_500_com'.upper(),'hrg_right_1k_com'.upper(),
                      'hrg_right_2k_com'.upper(),'hrg_right_4k_com'.upper()]

# 1. Normalised using sex-stratified distributions
tmpdf = df[columns_to_average].copy()
print(tmpdf)
tmpdf['SEX_ASK_COM'] = df['SEX_ASK_COM']
tmpDF = pd.DataFrame()
for col_name in columns_to_average:
    tmpDF[col_name]=stratified_scaling(tmpdf, col_name, inverse = False)
print(tmpdf)
print(tmpDF)

# 2. Calculate the average across the rows (axis=1)
DF['Pure_Tone_R'.upper()] = tmpDF[columns_to_average].mean(axis=1)
#DF['Pure_Tone_R'.upper()] = stratified_scaling(df, 'Pure_Tone_R'.upper() , inverse=True)
print(DF['Pure_Tone_R'.upper()])

df.loc[df['hrg_left_1k_com'.upper()].isin([-8]),'hrg_left_1k_com'.upper()] = np.nan
columns_to_average = ['hrg_left_500_com'.upper(),'hrg_left_1k_com'.upper(),
                      'hrg_left_2k_com'.upper(),'hrg_left_4k_com'.upper()]

"""
# average first then stratify and scale
df['Pure_Tone_L'.upper()] = df[columns_to_average].mean(axis=1)
DF['Pure_Tone_L'.upper()] = stratified_scaling(df, 'Pure_Tone_L'.upper() , inverse=False)
print(DF)
"""
# 1. Normalised using sex-stratified distributions
tmpdf = df[columns_to_average].copy()
tmpdf['SEX_ASK_COM'] = df['SEX_ASK_COM']
tmpDF = pd.DataFrame()
for col_name in columns_to_average:
    tmpDF[col_name]=stratified_scaling(tmpdf, col_name, inverse = False)

# 2. Calculate the average across the rows (axis=1)
DF['Pure_Tone_L'.upper()] = tmpDF[columns_to_average].mean(axis=1)
#DF['Pure_Tone_L'.upper()] = stratified_scaling(df, 'Pure_Tone_L'.upper() , inverse=False)
print(tmpdf)
print(tmpDF)
gc.collect()

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
FIExaminationData = df[['entity_id','AGE_NMBR_COM', 'SEX_ASK_COM']].copy()
FIExaminationData['FI_Examination'] = np.nan
FIExaminationData.loc[:,'FI_Examination'] = FIExamination

from pathlib import Path

# Define the folder and file name
output_file = Path(r"E:\CLSA\CLSA\results\FIExamination_BL.xlsx")

# Create the folder automatically if it is missing
output_file.parent.mkdir(parents=True, exist_ok=True)

# Save the DataFrame
FIExaminationData.to_excel(output_file, index=False)


##sorted_DF = DF.sort_values(by='AGE_NMBR_COM').reset_index(drop=True)
##print(sorted_DF)




DF['AGE_NMBR_COM'] = df['AGE_NMBR_COM']
DF['SEX_ASK_COM'] = df['SEX_ASK_COM']
#prevalence(DF, "BLD_Hgb_COM")
#GroupedPlot(DF,'BLD_Hgb_COM')
#prevalence(FIExaminationData, "FI_Examination")

#plt.figure()
#plt.scatter(FIExaminationData['AGE_NMBR_COM'], FIExaminationData['FI_Examination'], color='blue', marker='o', alpha=0.8)

"""
# plot each parameter vs age and output the prevalence
AGESEX = ['AGE_NMBR_COM','SEX_ASK_COM']
excluded_cols = set(AGESEX) # Using a set for O(1) membership checking

for col in DF.columns:
    if col not in excluded_cols:
        prevalence(DF, col)

# 4. Display all Seaborn plots at once
plt.show()
"""


""""""
# plot one specific parameter vs age and output the prevalence
AGESEX = ['AGE_NMBR_COM','SEX_ASK_COM']
excluded_cols = set(AGESEX) # Using a set for O(1) membership checking

for col in ['Pure_Tone_R'.upper(),'Pure_Tone_L'.upper()]:
    if col not in excluded_cols:
        prevalence(DF, col)

# 4. Display all Seaborn plots at once
plt.show()



"""
# Select boolean columns and overwrite them with 1 and 0
bool_cols = df.select_dtypes(include='bool').columns
df[bool_cols] = df[bool_cols].astype(int)
"""
""""
plt.scatter(FIExaminationData['AGE_NMBR_COM'], FIExaminationData['FI_Examination'], color='blue', marker='o', alpha=0.8)

# 3. Add labels and a title
plt.title("FI Examination Baseline")
plt.xlabel("Age")
plt.ylabel("FI Examination")

# 4. Display the graph
plt.show()
"""

#prevalence(FIExaminationData, "FI_Examination")

#Plot FI vs age

# Create your plot axis
fig, ax = plt.subplots(figsize=(6, 5))

# Define your 2 groups and 2 colors
categories = FIExaminationData["SEX_ASK_COM"].unique()
colors = ["#1f77b4", "#d62728"]
# Loop through each group and overlay them on the same axis ('ax=ax')
for category, color in zip(categories, colors):
    subset = FIExaminationData[FIExaminationData["SEX_ASK_COM"] == category]

    sns.regplot(
        data=subset,
        x="AGE_NMBR_COM",
        y="FI_Examination",
        x_bins=np.arange(45, 90, 1), fit_reg=False,
        ax=ax,  # Tells regplot to draw on the same chart
        color=color,
        label=category,
        #scatter=False,  # Hides scatter points as you wanted before
        #ci=None,
    )

# Add the legend manually since regplot won't make a grouped one automatically
ax.legend(title="FI Examination Baseline")
sns.despine(trim=True)
plt.show()

