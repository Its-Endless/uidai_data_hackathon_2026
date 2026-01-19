import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt
import numpy as np

# Load data
demo_df = pd.read_csv('combined_demographic.csv')
bio_df = pd.read_csv('combined_biometric.csv')
enrol_df = pd.read_csv('combined_enrolment.csv')

# Convert dates
demo_df['date'] = pd.to_datetime(demo_df['date'], format='%d-%m-%Y')
bio_df['date'] = pd.to_datetime(bio_df['date'], format='%d-%m-%Y')
enrol_df['date'] = pd.to_datetime(enrol_df['date'], format='%d-%m-%Y')

# Add totals
demo_df['total'] = demo_df['demo_age_5_17'] + demo_df['demo_age_17_']
bio_df['total'] = bio_df['bio_age_5_17'] + bio_df['bio_age_17_']
enrol_df['total'] = enrol_df['age_0_5'] + enrol_df['age_5_17'] + enrol_df['age_18_greater']

# Aggregate and resample weekly
def aggregate_resample(df):
    time_df = df.groupby('date')['total'].sum().resample('W').sum().reset_index()  # Weekly sum
    time_df.columns = ['ds', 'y']
    time_df['y'] = np.log(time_df['y'] + 1)  # Log transform for positivity
    return time_df

demo_time = aggregate_resample(demo_df.set_index('date'))
bio_time = aggregate_resample(bio_df.set_index('date'))
enrol_time = aggregate_resample(enrol_df.set_index('date'))

# Function to fit and forecast
def prophet_forecast(time_df, name):
    if len(time_df) < 3:  # Need more for weekly
        print(f"Not enough data for {name}")
        return None
    m = Prophet(yearly_seasonality=True, changepoint_prior_scale=0.1)
    m.fit(time_df)
    future = m.make_future_dataframe(periods=4, freq='W')  # 4 weeks into 2026
    forecast = m.predict(future)
    # Back-transform
    forecast[['yhat', 'yhat_lower', 'yhat_upper']] = np.exp(forecast[['yhat', 'yhat_lower', 'yhat_upper']]) - 1
    print(f"\n{name} Forecast (last 10 rows, back-transformed):\n", forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(10))
    fig = m.plot(forecast)
    plt.title(f'{name} National Weekly Forecast')
    fig.savefig(f'{name.lower()}_forecast.png')
    return forecast

# Run
prophet_forecast(demo_time, 'Demo')
prophet_forecast(bio_time, 'Bio')
prophet_forecast(enrol_time, 'Enrol')