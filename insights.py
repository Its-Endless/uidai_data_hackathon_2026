import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load combined files
demo_df = pd.read_csv('combined_demographic.csv')
bio_df = pd.read_csv('combined_biometric.csv')
enrol_df = pd.read_csv('combined_enrolment.csv')

# Convert dates
demo_df['date'] = pd.to_datetime(demo_df['date'], format='%d-%m-%Y')
bio_df['date'] = pd.to_datetime(bio_df['date'], format='%d-%m-%Y')
enrol_df['date'] = pd.to_datetime(enrol_df['date'], format='%d-%m-%Y')

# Add totals
demo_df['demo_total'] = demo_df['demo_age_5_17'] + demo_df['demo_age_17_']
bio_df['bio_total'] = bio_df['bio_age_5_17'] + bio_df['bio_age_17_']
enrol_df['enrol_total'] = enrol_df['age_0_5'] + enrol_df['age_5_17'] + enrol_df['age_18_greater']

# Group by state
demo_state = demo_df.groupby('state')['demo_total'].sum().reset_index()
bio_state = bio_df.groupby('state')['bio_total'].sum().reset_index()
enrol_state = enrol_df.groupby('state')['enrol_total'].sum().reset_index()  # Fixed!

# Population dict (expanded)
pop_dict = {
    'Andhra Pradesh': 53000000, 'Arunachal Pradesh': 1600000, 'Assam': 36000000, 'Bihar': 129000000,
    'Chhattisgarh': 30000000, 'Goa': 1600000, 'Gujarat': 73000000, 'Haryana': 30000000,
    'Himachal Pradesh': 7500000, 'Jammu and Kashmir': 14000000, 'Jharkhand': 40000000,
    'Karnataka': 68000000, 'Kerala': 36000000, 'Madhya Pradesh': 88000000, 'Maharashtra': 127000000,
    'Manipur': 3200000, 'Meghalaya': 3500000, 'Mizoram': 1300000, 'Nagaland': 2200000,
    'Odisha': 46000000, 'Punjab': 31000000, 'Rajasthan': 82000000, 'Sikkim': 700000,
    'Tamil Nadu': 76000000, 'Telangana': 38000000, 'Tripura': 4100000, 'Uttar Pradesh': 238000000,
    'Uttarakhand': 12000000, 'West Bengal': 99000000, 'Delhi': 21000000, 'Puducherry': 1600000,
    # Add any missing from your data
}

# Normalize per million
for df in [demo_state, bio_state, enrol_state]:
    col = 'demo_total' if 'demo_total' in df else 'bio_total' if 'bio_total' in df else 'enrol_total'
    per_mil_col = col.replace('_total', '_per_million')
    df[per_mil_col] = df.apply(lambda row: (row[col] / pop_dict.get(row['state'], 1)) * 1000000 if row['state'] in pop_dict else 0, axis=1)

# Print top/bottom 10 for each
for name, df_state, col in [('Demo', demo_state, 'demo_per_million'), ('Bio', bio_state, 'bio_per_million'), ('Enrol', enrol_state, 'enrol_per_million')]:
    print(f"\nTop 10 States by {name} per Million:\n", df_state.sort_values(col, ascending=False).head(10))
    print(f"\nBottom 10 States by {name} per Million:\n", df_state.sort_values(col, ascending=True).head(10))

# National time-series plot (all datasets)
demo_time = demo_df.groupby('date')['demo_total'].sum().reset_index()
bio_time = bio_df.groupby('date')['bio_total'].sum().reset_index()
enrol_time = enrol_df.groupby('date')['enrol_total'].sum().reset_index()

plt.figure(figsize=(12,6))
sns.lineplot(data=demo_time, x='date', y='demo_total', label='Demo')
sns.lineplot(data=bio_time, x='date', y='bio_total', label='Bio')
sns.lineplot(data=enrol_time, x='date', y='enrol_total', label='Enrol')
plt.title('National Trends Over Time (All Datasets)')
plt.savefig('national_trends_all.png')

# Odisha age breakdowns
odisha_demo_age = demo_df[demo_df['state'] == 'Odisha'][['demo_age_5_17', 'demo_age_17_']].sum()
odisha_bio_age = bio_df[bio_df['state'] == 'Odisha'][['bio_age_5_17', 'bio_age_17_']].sum()
odisha_enrol_age = enrol_df[enrol_df['state'] == 'Odisha'][['age_0_5', 'age_5_17', 'age_18_greater']].sum()
print("\nOdisha Demo Age Totals:\n", odisha_demo_age)
print("\nOdisha Bio Age Totals:\n", odisha_bio_age)
print("\nOdisha Enrol Age Totals:\n", odisha_enrol_age)

# Anomalies (z-score >2 for demo totals, example)
demo_time['z_score'] = (demo_time['demo_total'] - demo_time['demo_total'].mean()) / demo_time['demo_total'].std()
anomalies_demo = demo_time[abs(demo_time['z_score']) > 2]
print("\nDemo Anomalies:\n", anomalies_demo)
