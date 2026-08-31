import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

DF = pd.DataFrame()
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
    sns.regplot(
        data=df, x="AGE_NMBR_COM", y=target_col, x_bins=np.arange(45, 90, 1), fit_reg=False
    )
    plt.show()

ColumnNames = pd.read_csv(file_path, nrows=0).columns.tolist()
#print(ColumnNames)
# df = pd.read_csv(file_path, dtype=optimized_dtypes)
FISelfRedportCount = 51;DF = pd.DataFrame()

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
                   'IAL_ABLGRO_COM','IAL_ABLML_COM','IAL_ABLWRK_COM','IAL_ABLMED_COM',
                   'IAL_ABLMO_COM','COG_AFT_SCORE_1_COM','COG_AFT_SCORE_2_COM',
                   'COG_REYI_SCORE_COM','COG_REYII_SCORE_COM','DEP_FFRT_COM','DEP_LONLY_COM',
                   'DEP_GTGO_COM']

df = pd.read_csv(file_path, usecols=required_columns)
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

"""# Cardiovascular
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
RowsToDrop = DataNA.index[DataNA>FISelfRedportCount*0.2]
DF.drop(RowsToDrop, inplace=True)
IsEmpty = DF.isna() | (DF == "")
NotEmpty = ~IsEmpty
DataAvailable = NotEmpty.sum(axis=1)

print(DataAvailable)
print(DF.dtypes)

DeficitsCount = DF.sum(axis=1)
FISelfReport = DeficitsCount/DataAvailable
FISelfReportData = df[['entity_id','AGE_NMBR_COM', 'SEX_ASK_COM']].copy()
#FISelfReportData['FI_SelfReport'] = FISelfReport
FISelfReportData.loc[:,'FI_SelfReport_CR'] = FISelfReport

from pathlib import Path

# Define the folder and file name
output_file = Path(r"E:\CLSA\CLSA\results\FISelfReport_BL_CR.xlsx")

# Create the folder automatically if it is missing
output_file.parent.mkdir(parents=True, exist_ok=True)

# Save the DataFrame
FISelfReportData.to_excel(output_file, index=False)
"""
plt.scatter(FISelfReportData['AGE_NMBR_COM'], FISelfReportData['FI_SelfReport'], color='blue', marker='o', alpha=0.8)

# 3. Add labels and a title
plt.title("FI Self Report Baseline")
plt.xlabel("Age")
plt.ylabel("FI Self Report")

# 4. Display the graph
plt.show()
"""
prevalence(FISelfReportData, "FI_SelfReport_CR")

plt.figure()
plt.scatter(FISelfReportData['AGE_NMBR_COM'], FISelfReportData['FI_SelfReport_CR'], color='blue', marker='o', alpha=0.8)


# Create your plot axis
fig, ax = plt.subplots(figsize=(6, 5))

# Define your 2 groups and 2 colors
categories = FISelfReportData["SEX_ASK_COM"].unique()
colors = ["#1f77b4", "#d62728"]
# Loop through each group and overlay them on the same axis ('ax=ax')
for category, color in zip(categories, colors):
    subset = FISelfReportData[FISelfReportData["SEX_ASK_COM"] == category]

    sns.regplot(
        data=subset,
        x="AGE_NMBR_COM",
        y="FI_SelfReport_CR",
        x_bins=np.arange(45, 90, 1), fit_reg=False,
        ax=ax,  # Tells regplot to draw on the same chart
        color=color,
        label=category,
        #scatter=False,  # Hides scatter points as you wanted before
        #ci=None,
    )

# Add the legend manually since regplot won't make a grouped one automatically
ax.legend(title="FI Self Report Baseline")
sns.despine(trim=True)
plt.show()

#prevalence(FISelfReportData, "FI_SelfReport")


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




"""
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_theme(style="ticks", font_scale=1.2, font="DejaVu Sans")

journal_colors = ["#1f77b4", "#d62728"]
# lmplot creates the scatter plot, colors by hue, and draws individual trend lines
g = sns.lmplot(
    data=FISelfReportData, x="AGE_NMBR_COM", y="FI_SelfReport", hue="SEX_ASK_COM", ci=None,
    #palette=["red", "blue"],  # Changes both point and line colors per group
    palette=journal_colors,
    legend=False,  # We will place a cleaner manual legend
    line_kws={"lw": 2.5, "linestyle": "-"},  # Clean, solid lines
    height=5,
    aspect=1.2,
    #markers=["o", "s"],  # 'o' = circle for group 1, 's' = square for group 2
    #scatter_kws={
    #    "s": 80,  # Size of the scatter points
    #    "alpha": 0.2,  # Transparency of points (0 = clear, 1 = solid)
    #    "edgecolor": "none",  # Add a border around points
    #},
    scatter=False,
    #line_kws={
    #    "lw": 3,  # Line width/thickness of the trendlines
    #    "linestyle": "--",  # Makes the trendlines dashed (use '-' for solid)
    #},
)

# 4. Clean up the axes and labels
ax = g.ax
ax.set_xlabel("Age", fontsize=14, fontweight="bold")
ax.set_ylabel("FI Self Report", fontsize=14, fontweight="bold")
ax.set_title("FI Self Report Baseline", fontsize=16, pad=15)

# Remove the top and right spines (borders) for a clean look
sns.despine(trim=True)  # Trimmed spines look sharper in print

# 5. Add a precise, clean legend inside the plot area
ax.legend(
    title="Categories",
    title_fontsize=12,
    fontsize=11,
    loc="best",  # Automatically places it in the least crowded spot
    frameon=True,
    facecolor="white",
    edgecolor="none",
)

plt.title("FI Self Report Baseline")
plt.show()

"""