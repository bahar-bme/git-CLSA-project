# -*- coding: utf-8 -*-
"""
Created on Wed Oct 29 22:03:16 2025

@author: mmogh
"""



import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

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






ColumnNames = pd.read_csv(file_path, nrows=0).columns.tolist()
#print(ColumnNames)
# df = pd.read_csv(file_path, dtype=optimized_dtypes)
FIBloodCount = 22;DF = pd.DataFrame()

required_columns =['entity_id','AGE_NMBR_COM',
                   'SEX_ASK_COM','BLD_GR_PER_COM','BLD_Hct_COM',
                   'BLD_LY_PER_COM','BLD_MCH_COM','BLD_Hgb_COM','BLD_MO_PER_COM',
                   'BLD_Plt_COM','BLD_MCV_COM','BLD_RBC_COM','BLD_WBC_COM',
                   'BLD_RDW_COM','BLD_MPV_COM','BLD_HBA1c_COM','BLD_VITD_COM',
                   'BLD_HSCRP_COM','BLD_ALB_COM','BLD_TSH_COM',
                   'BLD_CREAT_COM','BLD_FT4_COM','BLD_FERR_COM','BLD_CHOL_COM',
                   'BLD_TRIG_COM']

df = pd.read_csv(file_path, usecols=required_columns)
df = df.replace([-1111,-2222,-8888],np.nan)

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
FIBloodData = df[['entity_id','AGE_NMBR_COM', 'SEX_ASK_COM']].copy()
#FIBloodData['FI_blood'] = FIBlood
FIBloodData.loc[:,'FI_blood'] = FIBlood



from pathlib import Path

# Define the folder and file name
output_file = Path(r"E:\CLSA\CLSA\results\FIBlood_BL.xlsx")

# Create the folder automatically if it is missing
output_file.parent.mkdir(parents=True, exist_ok=True)

# Save the DataFrame
FIBloodData.to_excel(output_file, index=False)


DF['AGE_NMBR_COM'] = df['AGE_NMBR_COM']
DF['SEX_ASK_COM'] = df['SEX_ASK_COM']
prevalence(DF, "bld_hscrp_com".upper())
GroupedPlot(DF,'bld_hscrp_com'.upper())
prevalence(FIBloodData, "FI_blood")

plt.figure()
plt.scatter(FIBloodData['AGE_NMBR_COM'], FIBloodData['FI_blood'], color='blue', marker='o', alpha=0.8)

plt.figure()
plt.scatter(df['AGE_NMBR_COM'], df["bld_hscrp_com".upper()], color='green', marker='o', alpha=0.8)

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
# Plot FI vs Age

# Create your plot axis
fig, ax = plt.subplots(figsize=(6, 5))

# Define your 2 groups and 2 colors
categories = FIBloodData["SEX_ASK_COM"].unique()
colors = ["#1f77b4", "#d62728"]
# Loop through each group and overlay them on the same axis ('ax=ax')
for category, color in zip(categories, colors):
    subset = FIBloodData[FIBloodData["SEX_ASK_COM"] == category]

    sns.regplot(
        data=subset,
        x="AGE_NMBR_COM",
        y="FI_blood",
        x_bins=np.arange(45, 90, 1), fit_reg=False,
        ax=ax,  # Tells regplot to draw on the same chart
        color=color,
        label=category,
        #scatter=False,  # Hides scatter points as you wanted before
        #ci=None,
    )

# Add the legend manually since regplot won't make a grouped one automatically
ax.legend(title="FI Blood Baseline")
sns.despine(trim=True)


plt.show()

