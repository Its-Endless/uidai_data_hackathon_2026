import pandas as pd

# Load the combined files (this should be fast if you already have them)
demo_df = pd.read_csv('combined_demographic.csv')
bio_df   = pd.read_csv('combined_biometric.csv')
enrol_df = pd.read_csv('combined_enrolment.csv')

# 1. Date range & unique dates
for name, df in [('Demographic', demo_df), ('Biometric', bio_df), ('Enrolment', enrol_df)]:
    df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y', errors='coerce')
    print(f"\n{name}:")
    print("Date range:", df['date'].min().date(), "to", df['date'].max().date())
    print("Number of unique dates:", df['date'].nunique())
    print("Missing dates (NaT count):", df['date'].isna().sum())

# 2. Missing values overview
print("\nMissing values summary:")
print("Demographic:\n", demo_df.isna().sum())
print("Biometric:\n", bio_df.isna().sum())
print("Enrolment:\n", enrol_df.isna().sum())

# 3. Top 10 states by total volume (quick look at activity)
print("\nTop 10 states - Demographic total counts:")
print(demo_df['state'].value_counts().head(10))

print("\nTop 10 states - Biometric total counts:")
print(bio_df['state'].value_counts().head(10))

print("\nTop 10 states - Enrolment total counts:")
print(enrol_df['state'].value_counts().head(10))

# 4. Quick totals per dataset (overall scale)
print("\nOverall totals:")
print("Demographic total demo captures:", demo_df['demo_age_5_17'].sum() + demo_df['demo_age_17_'].sum())
print("Biometric total bio captures:", bio_df['bio_age_5_17'].sum() + bio_df['bio_age_17_'].sum())
print("Enrolment total enrolments:", enrol_df[['age_0_5','age_5_17','age_18_greater']].sum().sum())