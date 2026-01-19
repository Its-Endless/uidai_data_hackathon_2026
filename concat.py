import pandas as pd

# Combine demographic files
demo_files = [
    'api_data_aadhar_demographic_0_500000.csv',  # Add .csv if needed
    'api_data_aadhar_demographic_500000_1000000.csv',
    'api_data_aadhar_demographic_1000000_1500000.csv',
    'api_data_aadhar_demographic_1500000_2000000.csv',
    'api_data_aadhar_demographic_2000000_2071700.csv'
]
demo_df = pd.concat([pd.read_csv(file) for file in demo_files], ignore_index=True)

# Combine biometric files
bio_files = [
    'api_data_aadhar_biometric_0_500000.csv',
    'api_data_aadhar_biometric_500000_1000000.csv',
    'api_data_aadhar_biometric_1000000_1500000.csv',
    'api_data_aadhar_biometric_1500000_1861108.csv'
]
bio_df = pd.concat([pd.read_csv(file) for file in bio_files], ignore_index=True)

# Combine enrolment files
enrol_files = [
    'api_data_aadhar_enrolment_0_500000.csv',
    'api_data_aadhar_enrolment_500000_1000000.csv',
    'api_data_aadhar_enrolment_1000000_1006029.csv'
]
enrol_df = pd.concat([pd.read_csv(file) for file in enrol_files], ignore_index=True)

# Basic checks
print("Demographic shape:", demo_df.shape)
print("Biometric shape:", bio_df.shape)
print("Enrolment shape:", enrol_df.shape)
print("\nDemographic columns:", demo_df.columns.tolist())
print("Biometric columns:", bio_df.columns.tolist())
print("Enrolment columns:", enrol_df.columns.tolist())
print("\nDemographic sample:\n", demo_df.head(10))
print("\nBiometric sample:\n", bio_df.head(10))
print("\nEnrolment sample:\n", enrol_df.head(10))

# Save combined CSVs for later (optional)
demo_df.to_csv('combined_demographic.csv', index=False)
bio_df.to_csv('combined_biometric.csv', index=False)
enrol_df.to_csv('combined_enrolment.csv', index=False)