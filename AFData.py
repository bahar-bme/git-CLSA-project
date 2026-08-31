import pandas as pd
from pathlib import Path

file_path = 'E:/CLSA/CLSA/data/2310011_UCalgary_RRose_BL/2310011_UCalgary_RRose_BL/2310011_UCalgary_RRose_Baseline_CoPv7.csv'
FIBlood_path = r'E:\CLSA\CLSA\results\FIBlood_BL.xlsx'
FIExamination_path = r'E:\CLSA\CLSA\results\FIExamination_BL.xlsx'
FIExaminationCR_path = r'E:\CLSA\CLSA\results\FIExamination_BL_CR.xlsx'
FICombined_path = r'E:\CLSA\CLSA\results\FICOMBINED_BL.xlsx'
FICombinedCR_path = r'E:\CLSA\CLSA\results\FICOMBINED_BL_CR.xlsx'
FISelfReport_path = r'E:\CLSA\CLSA\results\FISelfReport_BL.xlsx'
FISelfReportCR_path = r'E:\CLSA\CLSA\results\FISelfReport_BL_CR.xlsx'

required_columns =['entity_id','AGE_NMBR_COM',
                   'SEX_ASK_COM','ECG_RESULT_COM','ECG_DIAGNOSIS_DETAILS_COM']

df = pd.read_csv(file_path, usecols=required_columns)
df_Blood = pd.read_excel(FIBlood_path, sheet_name='Sheet1')
df_Exam = pd.read_excel(FIExamination_path, sheet_name='Sheet1')
df_Exam_CR = pd.read_excel(FIExaminationCR_path, sheet_name='Sheet1')
df_Combined = pd.read_excel(FICombined_path, sheet_name='Sheet1')
df_Combined_CR = pd.read_excel(FICombinedCR_path, sheet_name='Sheet1')
df_Self = pd.read_excel(FISelfReport_path, sheet_name='Sheet1')
df_Self_CR = pd.read_excel(FISelfReportCR_path, sheet_name='Sheet1')

df = df.merge(df_Blood[['entity_id','FI_blood']], on='entity_id', how='left')
df = df.merge(df_Exam[['entity_id','FI_Examination']], on='entity_id', how='left')
df = df.merge(df_Exam_CR[['entity_id','FI_Examination_CR']], on='entity_id', how='left')
df = df.merge(df_Combined[['entity_id','FI_COMBINED']], on='entity_id', how='left')
df = df.merge(df_Combined_CR[['entity_id','FI_COMBINED_CR']], on='entity_id', how='left')
df = df.merge(df_Self[['entity_id','FI_SelfReport']], on='entity_id', how='left')
df = df.merge(df_Self_CR[['entity_id','FI_SelfReport_CR']], on='entity_id', how='left')


df['AF']=df['ECG_DIAGNOSIS_DETAILS_COM'].str.contains('Atrial fibrillation')

# Define the folder and file name
AF = Path(r"E:\CLSA\CLSA\results\ECG_AF.xlsx")

# Create the folder automatically if it is missing
AF.parent.mkdir(parents=True, exist_ok=True)

# Save the DataFrame
df.to_excel(AF, index=False)

from scipy import stats
import numpy as np

#df = df.replace([np.inf, -np.inf], np.nan)

# Drop rows where either column has a NaN value
#df = df.dropna(subset=['AF', 'FI_blood'])
"""
df['AF'] = pd.to_numeric(df['AF'], errors='coerce')
df['FI_blood'] = pd.to_numeric(df['FI_blood'], errors='coerce')
df['FI_Examination'] = pd.to_numeric(df['FI_Examination'], errors='coerce')
df['FI_Examination_CR'] = pd.to_numeric(df['FI_Examination_CR'], errors='coerce')
df['FI_COMBINED'] = pd.to_numeric(df['FI_COMBINED'], errors='coerce')
df['FI_COMBINED_CR'] = pd.to_numeric(df['FI_COMBINED_CR'], errors='coerce')
df['FI_SelfReport'] = pd.to_numeric(df['FI_SelfReport'], errors='coerce')
df['FI_SelfReport_CR'] = pd.to_numeric(df['FI_SelfReport_CR'], errors='coerce')
# 2. Drop the newly exposed hidden NaNs
df = df.dropna(subset=['AF', 'FI_blood','FI_Examination','FI_Examination_CR','FI_COMBINED',
                       'FI_COMBINED_CR','FI_SelfReport','FI_SelfReport_CR'])
"""
"""
# Calculate the population-wide point-biserial correlation
correlation, p_value = stats.pointbiserialr(df['AF'], df['FI_blood'])
print(f"Global Correlation AF/FIBlood: {correlation:.4f}")
print(f"P-value: {p_value:.4e}")

correlation, p_value = stats.pointbiserialr(df['AF'], df['FI_Examination'])
print(f"Global Correlation AF/FI_Examination: {correlation:.4f}")
print(f"P-value: {p_value:.4e}")

correlation, p_value = stats.pointbiserialr(df['AF'], df['FI_Examination_CR'])
print(f"Global Correlation AF/FI_Examination_CR: {correlation:.4f}")
print(f"P-value: {p_value:.4e}")

correlation, p_value = stats.pointbiserialr(df['AF'], df['FI_COMBINED'])
print(f"Global Correlation AF/FI_COMBINED: {correlation:.4f}")
print(f"P-value: {p_value:.4e}")

correlation, p_value = stats.pointbiserialr(df['AF'], df['FI_COMBINED_CR'])
print(f"Global Correlation AF/FI_COMBINED_CR: {correlation:.4f}")
print(f"P-value: {p_value:.4e}")

correlation, p_value = stats.pointbiserialr(df['AF'], df['FI_SelfReport'])
print(f"Global Correlation AF/FI_SelfReport: {correlation:.4f}")
print(f"P-value: {p_value:.4e}")

correlation, p_value = stats.pointbiserialr(df['AF'], df['FI_SelfReport_CR'])
print(f"Global Correlation AF/FI_SelfReport_CR: {correlation:.4f}")
print(f"P-value: {p_value:.4e}")
"""

#Calculate Distribution Metrics & Visualise FI 
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from scipy import stats


import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from scipy import stats


import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats


def evaluate_distribution_and_significance(df, continuous_col, binary_col):
        temp_numeric = pd.to_numeric(df[continuous_col], errors="coerce")

        failed_rows = df[df[continuous_col].notna() & temp_numeric.isna()]

        if len(failed_rows) > 0:
            print("!!! FOUND CONVERSION ERRORS IN BINARY COLUMN !!!")
            print(f"Total problematic rows found: {len(failed_rows)}")
            print("Here is a sample of how they look in your original data:")
            # Prints up to 10 examples showing the index and the exact raw value
            print(failed_rows[[continuous_col]].head(10))
            print("==================================================\n")
        else:
            print("✓ No formatting errors found in the binary column.\n")
        # 1. Clean data by isolating target columns and dropping NaNs
        cleaned_df = df[[continuous_col, binary_col]].dropna()

        # 2. STRIP ALL METADATA: Convert to completely raw, clean NumPy arrays
        continuous_array = pd.to_numeric(
            cleaned_df[continuous_col], errors="coerce"
        ).to_numpy()

        binary_array = (
            pd.to_numeric(cleaned_df[binary_col], errors="coerce")
            .astype(int)
            .to_numpy()
        )

        # 3. Separate arrays by group
        group_0 = continuous_array[binary_array == 0]
        group_1 = continuous_array[binary_array == 1]

        print("==================================================")
        print(f"  ANALYSIS FOR: {continuous_col.upper()} by {binary_col.upper()}")
        print("==================================================")
        print(f"Healthy (0) Group Sample Size:  {len(group_0)}")
        print(f"AF (1) Group Sample Size: {len(group_1)}\n")

        # 4. Distribution Metrics
        print("--- Distribution Metrics ---")
        print(f"[Healthy (0)] Skewness: {pd.Series(group_0).skew():.3f}")
        print(f"[Healthy (0)] Kurtosis: {pd.Series(group_0).kurt():.3f}")
        print(f"[AF (1)] Skewness: {pd.Series(group_1).skew():.3f}")
        print(f"[AF (1)] Kurtosis: {pd.Series(group_1).kurt():.3f}\n")

        # 5. Statistical Hypothesis Testing
        print("--- Hypothesis Testing P-Values ---")
        _, t_pval = stats.ttest_ind(group_0, group_1, equal_var=False)
        print(f"Welch's T-Test p-value:       {t_pval:.4e}")

        _, u_pval = stats.mannwhitneyu(group_0, group_1, alternative="two-sided")
        print(f"Mann-Whitney U Test p-value:  {u_pval:.4e}\n")

        # Clean up column labels for titles
        clean_cont_label = continuous_col.replace("_", " ") 
        clean_bin_label = binary_col.replace("_", " ") 

        # 6. Set up a grid with 2 plots side-by-side (1 row, 2 columns)
        fig, axes = plt.subplots(1, 2, figsize=(16, 6))

        # --- PLOT 1: Density / Histogram ---
        # Plot Group 0 (Healthy) Histogram & Curve
        axes[0].hist(
            group_0,
            bins=30,
            density=True,
            alpha=0.4,
            color="skyblue",
            label="Healthy (0)",
        )
        kde_0 = stats.gaussian_kde(group_0)
        x_axis_0 = np.linspace(group_0.min(), group_0.max(), 200)
        axes[0].plot(x_axis_0, kde_0(x_axis_0), color="deepskyblue", linewidth=2)

        # Plot Group 1 (AF) Histogram & Curve
        axes[0].hist(
            group_1,
            bins=30,
            density=True,
            alpha=0.4,
            color="salmon",
            label="AF Present (1)",
        )
        kde_1 = stats.gaussian_kde(group_1)
        x_axis_1 = np.linspace(group_1.min(), group_1.max(), 200)
        axes[0].plot(x_axis_1, kde_1(x_axis_1), color="crimson", linewidth=2)

        axes[0].set_title(
            f"Distribution Check: {clean_cont_label} by {clean_bin_label}",
            fontsize=12,
        )
        axes[0].set_xlabel(clean_cont_label, fontsize=11)
        axes[0].set_ylabel("Density", fontsize=11)
        axes[0].legend(loc="upper right")
        axes[0].grid(axis="y", linestyle="--", alpha=0.3)

        # --- PLOT 2: Box Plot (Built cleanly using Matplotlib) ---
        # pass both groups as a list to create side-by-side boxes
        box = axes[1].boxplot(
            [group_0, group_1],
            patch_artist=True,  # Allows us to fill the boxes with color
            showmeans=True,  # Adds a point representing the raw average (mean)
            meanprops={
                "marker": "D",
                "markerfacecolor": "white",
                "markeredgecolor": "black",
                "markersize": 6,
            },
            labels=["Healthy (0)", "AF Present (1)"],
        )

        # Add custom matching color styles to the boxes
        colors = ["skyblue", "salmon"]
        for patch, color in zip(box["boxes"], colors):
            patch.set_facecolor(color)
            patch.set_alpha(0.6)

        axes[1].set_title(
            f"{clean_cont_label} Spread by {clean_bin_label} Status", fontsize=12
        )
        axes[1].set_xlabel(clean_bin_label, fontsize=11)
        axes[1].set_ylabel(clean_cont_label, fontsize=11)
        axes[1].grid(axis="y", linestyle="--", alpha=0.3)

        # Automatically fit and clean up layout spacing
        plt.tight_layout()
        plt.show()


evaluate_distribution_and_significance(df, continuous_col='FI_blood', binary_col='AF')
evaluate_distribution_and_significance(df, continuous_col='FI_Examination', binary_col='AF')
evaluate_distribution_and_significance(df, continuous_col='FI_Examination_CR', binary_col='AF')
evaluate_distribution_and_significance(df, continuous_col='FI_SelfReport', binary_col='AF')
evaluate_distribution_and_significance(df, continuous_col='FI_SelfReport_CR', binary_col='AF')
evaluate_distribution_and_significance(df, continuous_col='FI_COMBINED', binary_col='AF')
evaluate_distribution_and_significance(df, continuous_col='FI_COMBINED_CR', binary_col='AF')


"""
import matplotlib.pyplot as plt
import seaborn as sns

# Ensure True/False is converted to 1/0 integers for clean plotting
df["AF"] = df["AF"].astype(int)

# Set the size of the visualization
plt.figure(figsize=(8, 6))

# Generate the box plots side-by-side
sns.boxplot(
    data=df[['AF','FI_blood']],
    x="AF",  # Splits the data into 0 (Healthy) and 1 (AF Present)
    y="FI_blood",  # Measures the continuous FI_COMBINED distribution
    palette="Set2",  # Gives distinct, clean colors to both groups
    showmeans=True,  # Adds a marker showing the exact average (mean) FI_COMBINED
    meanprops={
        "marker": "D",
        "markerfacecolor": "white",
        "markeredgecolor": "black",
        "markersize": 8,
    },
)

# Clean up the labels for presentation
plt.title("FI Blood Distribution by AF Presence (N=30,000)", fontsize=14)
plt.xlabel("AF status", fontsize=12)
plt.ylabel("FI Blood", fontsize=12)

# Rename the x-axis tick marks for clarity
plt.xticks(ticks=[0, 1], labels=["Healthy (0)", "AF Present (1)"])

plt.grid(axis="y", linestyle="--", alpha=0.5)
plt.show()

"""