#FI COMBINED

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
import gc
from pathlib import Path
import os

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
FIBloodCount = 22
FIExaminationCount = 40-12 #47
FISelfRedportCount = 51

DF = pd.DataFrame()

required_columns =['AGE_NMBR_COM','SEX_ASK_COM', 'ED_HIGH_COM',
                   'BLD_GR_PER_COM','BLD_Hct_COM',
                   'BLD_LY_PER_COM','BLD_MCH_COM','BLD_Hgb_COM','BLD_MO_PER_COM',
                   'BLD_Plt_COM','BLD_MCV_COM','BLD_RBC_COM','BLD_WBC_COM',
                   'BLD_RDW_COM','BLD_MPV_COM','BLD_HBA1c_COM','BLD_VITD_COM',
                   'BLD_HSCRP_COM','BLD_ALB_COM','BLD_TSH_COM',
                   'BLD_CREAT_COM','BLD_FT4_COM','BLD_FERR_COM','BLD_CHOL_COM',
                   'BLD_TRIG_COM']
required_columns2 =['wlk_time_com','cr_avg_time_com',
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
                   'ICQ_DERET3MO_COM','ICQ_SRGYEYE_COM','ICQ_EYEINF_COM'
                   ]
required_columns3=['GEN_HLTH_COM','VIS_SGHT_COM','HRG_HRG_COM',
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
                   'IAL_ABLGRO_COM','IAL_ABLML_COM','IAL_ABLWRK_COM','IAL_ABLMED_COM',
                   'IAL_ABLMO_COM','COG_AFT_SCORE_1_COM','COG_AFT_SCORE_2_COM',
                   'COG_REYI_SCORE_COM','COG_REYII_SCORE_COM','DEP_FFRT_COM','DEP_LONLY_COM',
                   'DEP_GTGO_COM']
required_columns2 = [f.upper() for f in required_columns2]
required_columns = ['entity_id']+required_columns+required_columns2+required_columns3
print(required_columns)
df = pd.read_csv(file_path, usecols=required_columns)
df = df.replace([-1111,-2222,-8888],np.nan)

# FI BLOOD:::::>>
DF["BLD_GR_PER_COM"] = (df["BLD_GR_PER_COM"]<45) | (df["BLD_GR_PER_COM"]>75)    
DF["BLD_Hct_COM"] = ((df["SEX_ASK_COM"]=="M")&((df['BLD_Hct_COM']<0.41)|(df['BLD_Hct_COM']>0.53)))|((df["SEX_ASK_COM"]=='F')&((df['BLD_Hct_COM']<0.36)|(df['BLD_Hct_COM']>0.46)))
DF["BLD_LY_PER_COM"] = (df["BLD_LY_PER_COM"]<22) | (df["BLD_LY_PER_COM"]>44) 
DF["BLD_MCH_COM"] = (df["BLD_MCH_COM"]<26) | (df["BLD_MCH_COM"]>34)
DF["BLD_Hgb_COM"] = ((df["SEX_ASK_COM"]=="M")&((df['BLD_Hgb_COM']<=135)|(df['BLD_Hgb_COM']>180)))|((df["SEX_ASK_COM"]=='F')&((df['BLD_Hgb_COM']<=120)|(df['BLD_Hgb_COM']>160)))
DF["BLD_MO_PER_COM"] = (df["BLD_MO_PER_COM"]>8)
DF["BLD_Plt_COM"] = (df["BLD_Plt_COM"]<150) | (df["BLD_Plt_COM"]>450)
DF["BLD_MCV_COM"] = (df["BLD_MCV_COM"]<80) | (df["BLD_MCV_COM"]>96)
DF["BLD_RBC_COM"] = ((df["SEX_ASK_COM"]=="M")&((df['BLD_RBC_COM']<4.5)|(df['BLD_RBC_COM']>5.9)))|((df["SEX_ASK_COM"]=='F')&((df['BLD_RBC_COM']<4)|(df['BLD_RBC_COM']>5.2)))
DF["BLD_WBC_COM"] = (df["BLD_WBC_COM"]<1.8) | (df["BLD_WBC_COM"]>7.8)
DF["BLD_RDW_COM"] = df["BLD_RDW_COM"]>14.6
DF["BLD_MPV_COM"] = (df["BLD_MPV_COM"]<7) | (df["BLD_MPV_COM"]>13)
df.loc[df['BLD_HBA1c_COM'].isin([-2222,-8888]),'BLD_HBA1c_COM'] = np.nan
DF["BLD_HBA1c_COM"] = (df["BLD_HBA1c_COM"]<3.8) | (df["BLD_HBA1c_COM"]>6.4)
df.loc[df['BLD_VITD_COM'].isin([-1111,-2222,-8888]),'BLD_VITD_COM'] = np.nan
DF["BLD_VITD_COM"] = (df["BLD_VITD_COM"]<24.9) | (df["BLD_VITD_COM"]>169.5)
df.loc[df['BLD_HSCRP_COM'].isin([-2222,-8888]),'BLD_HSCRP_COM'] = np.nan
DF["BLD_HSCRP_COM"] = (df["BLD_HSCRP_COM"]<8) & (df["BLD_HSCRP_COM"]>0.1)
df.loc[df['BLD_ALB_COM'].isin([-8888]),'BLD_ALB_COM'] = np.nan
DF["BLD_ALB_COM"] = (df["BLD_ALB_COM"]<40) | (df["BLD_ALB_COM"]>60)
#DF["BLD_EGFR_COM"] = df["BLD_EGFR_COM"]<60
df.loc[df['BLD_TSH_COM'].isin([-2222,-8888]),'BLD_TSH_COM'] =np.nan
DF["BLD_TSH_COM"] = (df["BLD_TSH_COM"]<0.5) | (df["BLD_TSH_COM"]>5)
df.loc[df['BLD_CREAT_COM'].isin([-8888]),'BLD_CREAT_COM'] = np.nan
DF["BLD_CREAT_COM"] = ((df["SEX_ASK_COM"]=="M")&((df['BLD_CREAT_COM']<60)|(df['BLD_CREAT_COM']>110)))|((df["SEX_ASK_COM"]=='F')&((df['BLD_CREAT_COM']<45)|(df['BLD_CREAT_COM']>90)))
df.loc[df['BLD_FT4_COM'].isin([-1111,-2222,-8888]),'BLD_FT4_COM'] = np.nan
DF["BLD_FT4_COM"] = df["BLD_FT4_COM"]>23.2
df.loc[df['BLD_FERR_COM'].isin([-1111,-2222,-8888]),'BLD_FERR_COM'] = np.nan
DF["BLD_FERR_COM"] = ((df["SEX_ASK_COM"]=="M")&((df['BLD_FERR_COM']<20)|(df['BLD_FERR_COM']>250)))|((df["SEX_ASK_COM"]=='F')&((df['BLD_FERR_COM']<10)|(df['BLD_FERR_COM']>120)))
df.loc[df['BLD_CHOL_COM'].isin([-8888]),'BLD_CHOL_COM'] = np.nan
DF["BLD_CHOL_COM"] = (df["BLD_CHOL_COM"]<3.9) | (df["BLD_CHOL_COM"]>6.5)
df.loc[df['BLD_TRIG_COM'].isin([-8888]),'BLD_TRIG_COM'] = np.nan
DF["BLD_TRIG_COM"] = ((df["SEX_ASK_COM"]=="M")&((df['BLD_TRIG_COM']<0.45)|(df['BLD_TRIG_COM']>1.81)))|((df["SEX_ASK_COM"]=='F')&((df['BLD_TRIG_COM']<0.36)|(df['BLD_TRIG_COM']>1.12)))


# FI EXAMINATION:::::>>
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
"""# Domain 3: Cardiac
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
"""
# Domain 4: Anthropometric measures
df.loc[df['hwt_dbmi_com'.upper()].isin([999.96, 999.99]),'hwt_dbmi_com.upper()'] = np.nan
DF['hwt_dbmi_com'.upper()] = np.nan
DF.loc[((df['hwt_dbmi_com'.upper()]<=18.5)|(df['hwt_dbmi_com'.upper()]>=30))  ,'hwt_dbmi_com'.upper()] = 1
DF.loc[((df['hwt_dbmi_com'.upper()]>=25)&(df['hwt_dbmi_com'.upper()]<=29.9))  ,'hwt_dbmi_com'.upper()] = 0.5 
DF.loc[((df['hwt_dbmi_com'.upper()]>=18.5)&(df['hwt_dbmi_com'.upper()]<=24.9)),'hwt_dbmi_com'.upper()] = 0

DF['whc_ratio_com'.upper()] = ((df['SEX_ASK_COM']=='M')&(df['whc_ratio_com'.upper()]>0.9)) | ((df['SEX_ASK_COM']=='F')&(df['whc_ratio_com'.upper()]>0.85))
#DXA_WB_WBTOT_BMD_T_COM = (df['DXA_WB_WBTOT_BMD_COM']-df['DXA_WB_WBTOT_BMD_COM'].mean()) /df['DXA_WB_WBTOT_BMD_COM'].std()
#DF['DXA_WB_WBTOT_T_COM'] = np.nan
#DF.loc[(DXA_WB_WBTOT_BMD_T_COM<=-2.5),'DXA_WB_WBTOT_T_COM'] = 1
#DF.loc[((DXA_WB_WBTOT_BMD_T_COM>=-2.5)&(DXA_WB_WBTOT_BMD_T_COM<1)),'DXA_WB_WBTOT_T_COM'] = 0.5
#DF.loc[(DXA_WB_WBTOT_BMD_T_COM<=-1),'DXA_WB_WBTOT_T_COM'] = 0

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

#DF['DXA_OI_APDG_LEAN_MASS_H2_COM'] = stratified_scaling(df, 'DXA_OI_APDG_LEAN_MASS_H2_COM', inverse=True)
#DF['DXA_OI_TOTAL_PERCENT_FAT_COM'] = stratified_scaling(df, 'DXA_OI_TOTAL_PERCENT_FAT_COM', inverse=False)
#BodyFatAreas =['DXA_WBC_LARM_PFAT_COM','DXA_WBC_RARM_PFAT_COM','DXA_WBC_L_LEG_PFAT_COM',
#                   'DXA_WBC_R_LEG_PFAT_COM','DXA_WBC_TRUNK_PFAT_COM','DXA_WBC_HEAD_PFAT_COM']
#BodyFatAreas_Individual = df[BodyFatAreas]
#BodyFatAreas_P95 = BodyFatAreas_Individual.quantile(0.95)
#ExcessBodyFatArea=BodyFatAreas_Individual>=BodyFatAreas_P95
#ExcessBodyFatArea_Count=ExcessBodyFatArea.sum(axis=1)
#DF['AGGREGATE_BODY_FAT'] = np.nan
#DF.loc[(ExcessBodyFatArea_Count==0),'AGGREGATE_BODY_FAT']=0
#DF.loc[(ExcessBodyFatArea_Count==1),'AGGREGATE_BODY_FAT']=0.2
#DF.loc[(ExcessBodyFatArea_Count==2),'AGGREGATE_BODY_FAT']=0.4
#DF.loc[(ExcessBodyFatArea_Count==3),'AGGREGATE_BODY_FAT']=0.5
#DF.loc[(ExcessBodyFatArea_Count==4),'AGGREGATE_BODY_FAT']=0.8
#DF.loc[(ExcessBodyFatArea_Count>=5),'AGGREGATE_BODY_FAT']=1

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

df['FEV1_FVC_MAX'] = FEV1DF.max(axis=1, skipna=True)
DF['FEV1_FVC_MAX'] = stratified_scaling(df, 'FEV1_FVC_MAX' , inverse=True)
DF.loc[(FEV1DF_VALID<3) , 'FEV1_FVC_MAX'.upper()] = np.nan

# Domain 6: Hearing and vision
df.loc[df['va_etdrs_l_rslt_com'.upper()].isin([-88.8]),'va_etdrs_l_rslt_com'.upper()] = np.nan
DF['va_etdrs_l_rslt_com'.upper()] = stratified_scaling(df, 'va_etdrs_l_rslt_com'.upper() , inverse=False)
df.loc[df['va_etdrs_r_rslt_com'.upper()].isin([-88.8]),'va_etdrs_r_rslt_com'.upper()] = np.nan
DF['va_etdrs_r_rslt_com'.upper()] = stratified_scaling(df, 'va_etdrs_r_rslt_com'.upper() , inverse=False)
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
tmpdf['SEX_ASK_COM'] = df['SEX_ASK_COM']
tmpDF = pd.DataFrame()
for col_name in columns_to_average:
    tmpDF[col_name]=stratified_scaling(tmpdf, col_name, inverse = False)

# 2. Calculate the average across the rows (axis=1)
DF['Pure_Tone_R'.upper()] = tmpDF[columns_to_average].mean(axis=1)
#DF['Pure_Tone_R'.upper()] = stratified_scaling(df, 'Pure_Tone_R'.upper() , inverse=True)

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
gc.collect()

#FI SELFREPORT::::>>>>>>
#df["GEN_HLTH_COM"].loc[df["GEN_HLTH_COM"]==8] = np.nan
#df["GEN_HLTH_COM"].loc[df["GEN_HLTH_COM"]==9] = np.nan
df.loc[df['GEN_HLTH_COM'].isin([8,9]),'GEN_HLTH_COM'] = np.nan
DF['Health'] = (df['GEN_HLTH_COM']-1)/4

#df["VIS_SGHT_COM"].loc[df["VIS_SGHT_COM"]==8] = np.nan
#df["VIS_SGHT_COM"].loc[df["VIS_SGHT_COM"]==9] = np.nan
df.loc[df['VIS_SGHT_COM'].isin([8,9]),'VIS_SGHT_COM'] = np.nan
DF['Vision'] = (df['VIS_SGHT_COM']-1)/4

#df["HRG_HRG_COM"].loc[(df["HRG_HRG_COM"]==8)|(df["HRG_HRG_COM"]==9)] = np.nan
df.loc[df['HRG_HRG_COM'].isin([8,9]),'HRG_HRG_COM'] = np.nan
DF['Hearing'] = (df['HRG_HRG_COM']-1)/4

#df["CCC_OAKNEE_COM"].loc[(df["CCC_OAKNEE_COM"]==8)|(df["CCC_OAKNEE_COM"]==9)] = np.nan
#df["CCC_OAHAND_COM"].loc[(df["CCC_OAHAND_COM"]==8)|(df["CCC_OAHAND_COM"]==9)] = np.nan
#df["CCC_OAHIP_COM"] .loc[(df["CCC_OAHIP_COM"] ==8)|(df["CCC_OAHIP_COM"] ==9)] = np.nan

df.loc[~df['CCC_OAKNEE_COM'].isin([1,2]),'CCC_OAKNEE_COM'] = np.nan
df.loc[~df['CCC_OAHAND_COM'].isin([1,2]),'CCC_OAHAND_COM'] = np.nan
df.loc[~df['CCC_OAHIP_COM'].isin([1,2]),'CCC_OAHIP_COM']   = np.nan

df['CCC_OAKNEE_COM']=2-df['CCC_OAKNEE_COM']
df['CCC_OAHAND_COM']=2-df['CCC_OAHAND_COM']
df['CCC_OAHIP_COM']=2-df['CCC_OAHIP_COM']
df['Osteoarthritis'] = df[['CCC_OAKNEE_COM','CCC_OAHAND_COM','CCC_OAHIP_COM']].sum(axis=1 , min_count=1)
DF['Osteoarthritis'] = df['Osteoarthritis'].gt(0).astype(int)

#df["CCC_RA_COM"] .loc[(df["CCC_RA_COM"] ==8)|(df["CCC_RA_COM"] ==9)] = np.nan
df.loc[~df['CCC_RA_COM'].isin([1,2]),'CCC_RA_COM'] = np.nan
DF['Arthritis']=2-df['CCC_RA_COM']

#df["DIA_DIAB_COM"] .loc[(df["DIA_DIAB_COM"] ==8)|(df["DIA_DIAB_COM"] ==9)] = np.nan
df.loc[~df['DIA_DIAB_COM'].isin([1,2]),'DIA_DIAB_COM'] = np.nan
DF['Diabetes_mellitus']=2-df['DIA_DIAB_COM']

"""
# Cardiovascular
#df["CCC_COPD_COM"] .loc[(df["CCC_COPD_COM"] ==8)|(df["CCC_COPD_COM"] ==9)] = np.nan
df.loc[~df['CCC_COPD_COM'].isin([1,2]),'CCC_COPD_COM'] = np.nan
DF['Chronic_obstructive_pulmonary_disease']=2-df['CCC_COPD_COM']

#df["CCC_HBP_COM"] .loc[(df["CCC_HBP_COM"] ==8)|(df["CCC_HBP_COM"] ==9)] = np.nan
df.loc[~df['CCC_HBP_COM'].isin([1,2]),'CCC_HBP_COM'] = np.nan
DF['High_blood_pressure']=2-df['CCC_HBP_COM']

#df["CCC_HEART_COM"] .loc[(df["CCC_HEART_COM"] ==8)|(df["CCC_HEART_COM"] ==9)] = np.nan
df.loc[~df['CCC_HEART_COM'].isin([1,2]),'CCC_HEART_COM'] = np.nan
DF['Chronic_heart_failure']=2-df['CCC_HEART_COM']

#df["CCC_ANGI_COM"] .loc[(df["CCC_ANGI_COM"] ==8)|(df["CCC_ANGI_COM"] ==9)] = np.nan
df.loc[df['CCC_ANGI_COM'].isin([1,2]),'CCC_ANGI_COM'] = np.nan
DF['Angina']=2-df['CCC_ANGI_COM']

#df["CCC_AMI_COM"] .loc[(df["CCC_AMI_COM"] ==8)|(df["CCC_AMI_COM"] ==9)] = np.nan
df.loc[~df['CCC_AMI_COM'].isin([1,2]),'CCC_AMI_COM'] = np.nan
DF['Acute_myocardial_infarction']=2-df['CCC_AMI_COM']

#df["CCC_PVD_COM"] .loc[(df["CCC_PVD_COM"] ==8)|(df["CCC_PVD_COM"] ==9)] = np.nan
df.loc[~df['CCC_PVD_COM'].isin([1,2]),'CCC_PVD_COM'] = np.nan
DF['Peripheral_vascular_disease']=2-df['CCC_PVD_COM']

#df["CCC_CVA_COM"] .loc[(df["CCC_CVA_COM"] ==8)|(df["CCC_CVA_COM"] ==9)] = np.nan
df.loc[~df['CCC_CVA_COM'].isin([1,2]),'CCC_CVA_COM'] = np.nan
DF['Stroke']=2-df['CCC_CVA_COM']
"""

#df["CCC_TIA_COM"] .loc[(df["CCC_TIA_COM"] ==8)|(df["CCC_TIA_COM"] ==9)] = np.nan
df.loc[~df['CCC_TIA_COM'].isin([1,2]),'CCC_TIA_COM'] = np.nan
DF['Transient_ischemic_attack']=2-df['CCC_TIA_COM']

#Brain

#df["CCC_MEMPB_COM"] .loc[(df["CCC_MEMPB_COM"] ==8)|(df["CCC_MEMPB_COM"] ==9)] = np.nan
df.loc[~df['CCC_MEMPB_COM'].isin([1,2]),'CCC_MEMPB_COM'] = np.nan
DF['Memory_problem']=2-df['CCC_MEMPB_COM']

#df["CCC_ALZH_COM"] .loc[(df["CCC_ALZH_COM"] ==8)|(df["CCC_ALZH_COM"] ==9)] = np.nan
df.loc[~df['CCC_ALZH_COM'].isin([1,2]),'CCC_ALZH_COM'] = np.nan
DF['Alzheimer_disease']=2-df['CCC_ALZH_COM']

#df["CCC_PARK_COM"] .loc[(df["CCC_PARK_COM"] ==8)|(df["CCC_PARK_COM"] ==9)] = np.nan
df.loc[~df['CCC_PARK_COM'].isin([1,2]),'CCC_PARK_COM'] = np.nan
DF['Parkinson_disease']=2-df['CCC_PARK_COM']

#Gatrointestin
#df["CCC_ULCR_COM"] .loc[(df["CCC_ULCR_COM"] ==8)|(df["CCC_ULCR_COM"] ==9)] = np.nan
df.loc[~df['CCC_ULCR_COM'].isin([1,2]),'CCC_ULCR_COM'] = np.nan
DF['Peptic_ulcer_diseae']=2-df['CCC_ULCR_COM']

#df["CCC_IBDIBS_COM"] .loc[(df["CCC_IBDIBS_COM"] ==8)|(df["CCC_IBDIBS_COM"] ==9)] = np.nan
df.loc[~df['CCC_IBDIBS_COM'].isin([1,2]),'CCC_IBDIBS_COM'] = np.nan
DF['Colitis']=2-df['CCC_IBDIBS_COM']

#df["CCC_BOWINC_COM"] .loc[(df["CCC_BOWINC_COM"] ==8)|(df["CCC_BOWINC_COM"] ==9)] = np.nan
df.loc[~df['CCC_BOWINC_COM'].isin([1,2]),'CCC_BOWINC_COM'] = np.nan
DF['Bowel_incontinence']=2-df['CCC_BOWINC_COM']

#df["ADL_INCNT_COM"].loc[(df["ADL_INCNT_COM"]==8)|(df["ADL_INCNT_COM"]==9)] = np.nan
df.loc[df['ADL_INCNT_COM'].isin([8,9]),'ADL_INCNT_COM'] = np.nan
DF['Urinary_incontinence'] = (df['ADL_INCNT_COM']-1)/2

#vision
#df["ICQ_CATRCT_COM"] .loc[(df["ICQ_CATRCT_COM"] ==8)|(df["ICQ_CATRCT_COM"] ==9)] = np.nan
df.loc[~df['ICQ_CATRCT_COM'].isin([1,2]),'ICQ_CATRCT_COM'] = np.nan
DF['Cataract']=2-df['ICQ_CATRCT_COM']

#df["ICQ_GLAUC_COM"] .loc[(df["ICQ_GLAUC_COM"] ==8)|(df["ICQ_GLAUC_COM"] ==9)] = np.nan
df.loc[~df['ICQ_GLAUC_COM'].isin([1,2]),'ICQ_GLAUC_COM'] = np.nan
DF['Glaucoma']=2-df['ICQ_GLAUC_COM']

#df["CCC_MACDEG_COM"] .loc[(df["CCC_MACDEG_COM"] ==8)|(df["CCC_MACDEG_COM"] ==9)] = np.nan
df.loc[~df['CCC_MACDEG_COM'].isin([1,2]),'CCC_MACDEG_COM'] = np.nan
DF['Macular_degeneration']=2-df['CCC_MACDEG_COM']

#Cancer
#df["CCC_CANC_COM"] .loc[(df["CCC_CANC_COM"] ==8)|(df["CCC_CANC_COM"] ==9)] = np.nan
df.loc[~df['CCC_CANC_COM'].isin([1,2]),'CCC_CANC_COM'] = np.nan
DF['Cancer']=2-df['CCC_CANC_COM']

#Orthopedic
#df["CCC_OSTPO_COM"] .loc[(df["CCC_OSTPO_COM"] ==8)|(df["CCC_OSTPO_COM"] ==9)] = np.nan
df.loc[~df['CCC_OSTPO_COM'].isin([1,2]),'CCC_OSTPO_COM'] = np.nan
DF['Osteoporosis']=2-df['CCC_OSTPO_COM']

#df["CCC_BCKP_COM"] .loc[(df["CCC_BCKP_COM"] ==8)|(df["CCC_BCKP_COM"] ==9)] = np.nan
df.loc[~df['CCC_BCKP_COM'].isin([1,2]),'CCC_BCKP_COM'] = np.nan
DF['Back_pain']=2-df['CCC_BCKP_COM']

#Internal
#df["CCC_UTHYR_COM"] .loc[(df["CCC_UTHYR_COM"] ==8)|(df["CCC_UTHYR_COM"] ==9)] = np.nan
df.loc[~df['CCC_UTHYR_COM'].isin([1,2]),'CCC_UTHYR_COM'] = np.nan
DF['Hypothyroidism']=2-df['CCC_UTHYR_COM']

#df["CCC_OTHYR_COM"] .loc[(df["CCC_OTHYR_COM"] ==8)|(df["CCC_OTHYR_COM"] ==9)] = np.nan
df.loc[~df['CCC_OTHYR_COM'].isin([1,2]),'CCC_OTHYR_COM'] = np.nan
DF['Hyperthyroidism']=2-df['CCC_OTHYR_COM']

#df["CCC_KIDN_COM"] .loc[(df["CCC_KIDN_COM"] ==8)|(df["CCC_KIDN_COM"] ==9)] = np.nan
df.loc[~df['CCC_KIDN_COM'].isin([1,2]),'CCC_KIDN_COM'] = np.nan
DF['Kidney_failure']=2-df['CCC_KIDN_COM']

#df["CCC_DRPNEU_COM"] .loc[(df["CCC_DRPNEU_COM"] ==8)|(df["CCC_DRPNEU_COM"] ==9)] = np.nan
df.loc[~df['CCC_DRPNEU_COM'].isin([1,2]),'CCC_DRPNEU_COM'] = np.nan
DF['Pneumonia']=2-df['CCC_DRPNEU_COM']

#df["CCC_DRUTI_COM"] .loc[(df["CCC_DRUTI_COM"] ==8)|(df["CCC_DRUTI_COM"] ==9)] = np.nan
df.loc[~df['CCC_DRUTI_COM'].isin([1,2]),'CCC_DRUTI_COM'] = np.nan
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

df.loc[~df['IAL_ABLTRV_COM'].isin([1,2]),'IAL_ABLTRV_COM'] = np.nan
DF['Transport'] = df['IAL_ABLTRV_COM']-1

df.loc[~df['IAL_ABLGRO_COM'].isin([1,2]),'IAL_ABLGRO_COM'] = np.nan
DF['Shopping'] = df['IAL_ABLGRO_COM']-1

df.loc[~df['IAL_ABLML_COM'].isin([1,2]),'IAL_ABLML_COM'] = np.nan
DF['Cooking'] = df['IAL_ABLML_COM'] -1

df.loc[~df['IAL_ABLWRK_COM'].isin([1,2]),'IAL_ABLWRK_COM'] = np.nan
DF['Housework'] = df['IAL_ABLWRK_COM']-1

df.loc[~df['IAL_ABLMED_COM'].isin([1,2]),'IAL_ABLMED_COM'] = np.nan
DF['Medicine'] = df['IAL_ABLMED_COM'] -1

df.loc[~df['IAL_ABLMO_COM'].isin([1,2]),'IAL_ABLMO_COM'] = np.nan
DF['Money'] = df['IAL_ABLMO_COM']-1

# Cognition

#DF['Mental_alternation_test']

DF['Animal_Recall'] = ((1-(df['COG_AFT_SCORE_1_COM']/df['COG_AFT_SCORE_1_COM'].max())) + 
                       (1-(df['COG_AFT_SCORE_2_COM']/df['COG_AFT_SCORE_2_COM'].max())))/2


DF['immediate_Recall'] = 1-(df['COG_REYI_SCORE_COM']/df['COG_REYI_SCORE_COM'].max())

DF['Delayed_Recall'] = 1-(df['COG_REYII_SCORE_COM']/df['COG_REYII_SCORE_COM'].max())

# Mental Health
df.loc[df['DEP_FFRT_COM'].isin([-8,8,9]),'DEP_FFRT_COM'] = np.nan
DF['Effort'] = (4-df['DEP_FFRT_COM'])/3

df.loc[df['DEP_LONLY_COM'].isin([-8,8,9]),'DEP_LONLY_COM'] = np.nan
DF['Felt_Lonely'] = (4-df['DEP_LONLY_COM'])/3


df.loc[df['DEP_GTGO_COM'].isin([-8,8,9]),'DEP_GTGO_COM'] = np.nan
DF['Get_Going'] = (4-df['DEP_GTGO_COM'])/3




print(DF)
RAWDF=DF

IsEmpty = DF.isna() | (DF == "")
DataNA = IsEmpty.sum(axis=1)
RowsToDrop = DataNA.index[DataNA>(FIBloodCount+FIExaminationCount+FISelfRedportCount)*0.2]
DF.drop(RowsToDrop, inplace=True)
IsEmpty = DF.isna() | (DF == "")
NotEmpty = ~IsEmpty
DataAvailable = NotEmpty.sum(axis=1)
#print(DataAvailable)



DeficitsCount = DF.sum(axis=1)
FICOMBINED = DeficitsCount/DataAvailable
FICOMBINEDData = df[['entity_id','AGE_NMBR_COM', 'SEX_ASK_COM']].copy()
#FICOMBINEDData['FI_COMBINED'] = FICOMBINED
FICOMBINEDData['FI_COMBINED_CR'] = np.nan
FICOMBINEDData.loc[:,'FI_COMBINED_CR'] = FICOMBINED

# Define the folder and file name
output_file = Path(r"E:\CLSA\CLSA\results\FICOMBINED_BL_CR.xlsx")

# Create the folder automatically if it is missing
output_file.parent.mkdir(parents=True, exist_ok=True)

# Save the DataFrame
FICOMBINEDData.to_excel(output_file, index=False)


DF['AGE_NMBR_COM'] = df['AGE_NMBR_COM']
DF['SEX_ASK_COM'] = df['SEX_ASK_COM']
#prevalence(DF, "bld_hscrp_com".upper())
#GroupedPlot(DF,'bld_hscrp_com'.upper())
prevalence(FICOMBINEDData, "FI_COMBINED_CR")

plt.figure()
plt.scatter(FICOMBINEDData['AGE_NMBR_COM'], FICOMBINEDData['FI_COMBINED_CR'], color='blue', marker='o', alpha=0.8)

"""
# plot each parameter vs age and output the prevalence
AGESEX = ['AGE_NMBR_COM','SEX_ASK_COM']
excluded_cols = set(AGESEX) # Using a set for O(1) membership checking
output_folder=Path(r"E:\CLSA\CLSA\results\FI COMBINED")
for col in DF.columns:
    if col not in excluded_cols:
        prevalence(DF, col)
        plt.ylim(-0.05,1.05)
        file_path = os.path.join(output_folder, f"Baseline_{col}.png")
        plt.savefig(file_path, dpi=300, bbox_inches='tight')
        
        # 4. Clear the memory to prevent freezing
        plt.close()

# 4. Display all Seaborn plots at once
plt.show()
"""
"""
# plot one specific parameter vs age and output the prevalence
for col in ['va_etdrs_l_rslt_com'.upper(),'va_etdrs_r_rslt_com'.upper()]:
    prevalence(DF, col)

# 4. Display all Seaborn plots at once
plt.show()
"""


# Plot FI vs Age

# Create your plot axis
fig, ax = plt.subplots(figsize=(6, 5))

# Define your 2 groups and 2 colors
categories = FICOMBINEDData["SEX_ASK_COM"].unique()
colors = ["#1f77b4", "#d62728"]
# Loop through each group and overlay them on the same axis ('ax=ax')
for category, color in zip(categories, colors):
    subset = FICOMBINEDData[FICOMBINEDData["SEX_ASK_COM"] == category]

    sns.regplot(
        data=subset,
        x="AGE_NMBR_COM",
        y="FI_COMBINED_CR",
        x_bins=np.arange(45, 90, 1), fit_reg=False,
        ax=ax,  # Tells regplot to draw on the same chart
        color=color,
        label=category,
        #scatter=False,  # Hides scatter points as you wanted before
        #ci=None,
    )

# Add the legend manually since regplot won't make a grouped one automatically
ax.legend(title="FI Combined Baseline")
sns.despine(trim=True)
plt.show()

