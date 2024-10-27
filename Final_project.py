#Final project Kimmo J ; Data Analytics and Mathematics KA00EH66-3002 
import pandas as pd

#Data file Electricity_20-09-2024.csv contains information about hourly electricity consumption (column Energy (kWh)) 
# and Temperature. Another file sahkon-hinta-010121-240924.csv contains information about hourly electricity prices.
url_A = "https://raw.githubusercontent.com/transsendentalisti/KA00EH66-3002/refs/heads/main/Electricity_20-09-2024.csv"
url_B = "https://raw.githubusercontent.com/transsendentalisti/KA00EH66-3002/refs/heads/main/sahkon-hinta-010121-240924.csv"
dfA = pd.read_csv(url_A,delimiter=';')
dfB = pd.read_csv(url_B)

#Change time format of both files to Pandas datetime
dfA['Time'] = pd.to_datetime(dfA['Time'],format = ' %d.%m.%Y %H:%M')
dfB['Time'] = pd.to_datetime(dfB['Time'],format = '%d-%m-%Y %H:%M:%S')

#- Join the two data frames according to time
df = pd.merge(dfA,dfB, on = 'Time', how = 'outer')#All the Time values from dfA and dfB are included.

#- Calculate the hourly bill paid (using information about the price and the consumption)
df['Energy (kWh)'] = (df['Energy (kWh)'].str.replace(',','.'))
df['Energy (kWh)'] = pd.to_numeric(df['Energy (kWh)'])
df['Bill (cent/hour)']=(df['Energy (kWh)']*df['Price (cent/kWh)'])

#- Calculated grouped values of daily, weekly or monthly consumption, bill, average price and average temperature
df['Temperature'] = (df['Temperature'].str.replace(',','.'))
df['Temperature'] = pd.to_numeric(df['Temperature'])

df_daily = (df.groupby(pd.Grouper(key = 'Time', freq = 'D'))[['Time' , 'Price (cent/kWh)', 'Temperature']].mean())
df_daily['Daily consumption (kWh)'] = (df.groupby(pd.Grouper(key = 'Time', freq = 'D'))[['Energy (kWh)']].sum())
df_daily['Bill (€/day)'] = (((df.groupby(pd.Grouper(key = 'Time', freq = 'D'))[['Bill (cent/hour)']].sum()))/100)
df_daily['Time'] = pd.to_datetime(df_daily['Time']).dt.date

df_weekly = (df.groupby(pd.Grouper(key = 'Time', freq = 'W'))[['Time', 'Price (cent/kWh)', 'Temperature']].mean())
df_weekly['Weekly consumption (kWh)'] = (df.groupby(pd.Grouper(key = 'Time', freq = 'W'))[['Energy (kWh)']].sum())
df_weekly['Bill (€/weekly)'] = (((df.groupby(pd.Grouper(key = 'Time', freq = 'W'))[['Bill (cent/hour)']].sum()))/100)
df_weekly['Time'] = pd.to_datetime(df_weekly['Time']).dt.date

df_monthly = (df.groupby(pd.Grouper(key = 'Time', freq = 'ME'))[['Time', 'Price (cent/kWh)', 'Temperature']].mean())
df_monthly['Monthly consumption (kWh)'] = (df.groupby(pd.Grouper(key = 'Time', freq = 'ME'))[['Energy (kWh)']].sum())
df_monthly['Bill (€/month)'] = (((df.groupby(pd.Grouper(key = 'Time', freq = 'ME'))[['Bill (cent/hour)']].sum()))/100)
df_monthly['Time'] = pd.to_datetime(df_monthly['Time']).dt.date

#Create a visualization which includes
import streamlit as st

#Define the Figure title
st.title('Energy Consumption')

#Define a selector (columns to draw)
#- A selector for time interval included in the analysis
import datetime
start_date = st.date_input("Start day", datetime.date(2021, 1, 1))
end_date = st.date_input("End day", datetime.date(2024, 9, 22))
st.write("Showing range:", start_date, " - ", end_date)

#- Consumption, bill, average price and average temperature over selected period
df_timeframe = (df_daily.loc[start_date:end_date])
timeframe_consumption = df_timeframe['Daily consumption (kWh)'].sum().round(1)
st.write("Total consumption over the period:", timeframe_consumption, " kWh")

timeframe_bill = df_timeframe['Bill (€/day)'].sum().round(1)
st.write("Total bill over the period:", timeframe_bill, " €")

timeframe_av_h_price = df_timeframe['Price (cent/kWh)'].mean().round(2)
st.write("Average hourly price:", timeframe_av_h_price, " cent/kWh")

timeframe_av_paid_price = ((timeframe_bill*100) / timeframe_consumption).round(2)
st.write("Average paid price:", timeframe_av_paid_price, " cent/kWh")

#- Selector for grouping interval 
period = st.multiselect('Averaging period: ', ['Daily', 'Weekly', 'Monthly'], default = ['Weekly'], max_selections=(1))

#- Line graph of consumption, bill, average price and average temperature over the range selected 
#using the grouping interval selected. 
if 'Daily' in period:
  df_visu = (df_daily.loc[start_date:end_date])
  st.line_chart(df_visu,x = 'Time', y = 'Daily consumption (kWh)', y_label = 'Electricity consumptions [kWh/day]',x_label = 'Time')
  st.line_chart(df_visu,x = 'Time', y = 'Price (cent/kWh)', y_label = 'Electricity price [cents/kWh]',x_label = 'Time')
  st.line_chart(df_visu,x = 'Time', y = 'Bill (€/day)', y_label = 'Electricity bill [€/day]',x_label = 'Time')
  st.line_chart(df_visu,x = 'Time', y = 'Temperature', y_label = 'Temperature [C]',x_label = 'Time')

if 'Weekly' in period:
  df_visu = (df_weekly.loc[start_date:end_date])
  st.line_chart(df_visu,x = 'Time', y = 'Weekly consumption (kWh)', y_label = 'Electricity consumptions [kWh/week]',x_label = 'Time')
  st.line_chart(df_visu,x = 'Time', y = 'Price (cent/kWh)', y_label = 'Electricity price [cents/kWh]',x_label = 'Time')
  st.line_chart(df_visu,x = 'Time', y = 'Bill (€/weekly)', y_label = 'Electricity bill [€/week]',x_label = 'Time')
  st.line_chart(df_visu,x = 'Time', y = 'Temperature', y_label = 'Temperature [C]',x_label = 'Time')

if 'Monthly' in period:
  df_visu = (df_monthly.loc[start_date:end_date])
  st.line_chart(df_visu,x = 'Time', y = 'Monthly consumption (kWh)', y_label = 'Electricity consumptions [kWh/month]',x_label = 'Time')
  st.line_chart(df_visu,x = 'Time', y = 'Price (cent/kWh)', y_label = 'Electricity price [cents/kWh]',x_label = 'Time')
  st.line_chart(df_visu,x = 'Time', y = 'Bill (€/month)', y_label = 'Electricity bill [€/month]',x_label = 'Time')
  st.line_chart(df_visu,x = 'Time', y = 'Temperature', y_label = 'Temperature [C]',x_label = 'Time')

