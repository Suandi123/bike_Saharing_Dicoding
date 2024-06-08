# Import Libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from datetime import datetime
import streamlit as st

# Load the dataset
data_url = "https://raw.githubusercontent.com/slvyarc/Bike-Sharing_Dicoding/main/Dataset/day.csv"
day_data = pd.read_csv(data_url)

# Drop irrelevant columns
irrelevant_columns = ['instant', 'windspeed']
day_data.drop(columns=irrelevant_columns, inplace=True)

# Rename columns for clarity
day_data.rename(columns={
    'dteday': 'date',
    'yr': 'year',
    'mnth': 'month',
    'cnt': 'total_count'
}, inplace=True)

# Convert date column to datetime type
day_data['date'] = pd.to_datetime(day_data['date'])

# Extract weekday names and year from date
day_data['weekday'] = day_data['date'].dt.day_name()
day_data['year'] = day_data['date'].dt.year

# Map seasons and weather situations to descriptive labels
day_data['season'] = day_data['season'].map({1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'})
day_data['weathersit'] = day_data['weathersit'].map({
    1: 'Clear/Partly Cloudy',
    2: 'Misty/Cloudy',
    3: 'Light Snow/Rain',
    4: 'Severe Weather'
})

# Aggregate data monthly
monthly_aggregated = day_data.resample('M', on='date').agg({
    "casual": "sum",
    "registered": "sum",
    "total_count": "sum"
}).reset_index()

# Format the month-year for readability
monthly_aggregated['date'] = monthly_aggregated['date'].dt.strftime('%b-%y')

# Rename columns for consistency
monthly_aggregated.rename(columns={
    "date": "month_year",
    "total_count": "total_rides",
    "casual": "casual_rides",
    "registered": "registered_rides"
}, inplace=True)

# Aggregate statistics by different groupings
monthly_stats = day_data.groupby('month')['total_count'].agg(['max', 'min', 'mean', 'sum'])
weather_stats = day_data.groupby('weathersit')['total_count'].agg(['max', 'min', 'mean', 'sum'])
holiday_stats = day_data.groupby('holiday')['total_count'].agg(['max', 'min', 'mean', 'sum'])
weekday_stats = day_data.groupby('weekday')['total_count'].agg(['max', 'min', 'mean'])
workingday_stats = day_data.groupby('workingday')['total_count'].agg(['max', 'min', 'mean'])

# Season-based statistics for different metrics
season_stats = day_data.groupby('season').agg({
    'casual': 'mean',
    'registered': 'mean',
    'total_count': ['max', 'min', 'mean'],
    'temp': ['max', 'min', 'mean'],
    'atemp': ['max', 'min', 'mean'],
    'hum': ['max', 'min', 'mean']
})

# Filter setup in Streamlit
min_date = day_data["date"].min()
max_date = day_data["date"].max()

# Display logo and filter in sidebar
st.sidebar.image("https://jugnoo.io/wp-content/uploads/2022/05/on-demand-bike-sharing-1-1024x506.jpg")
st.sidebar.header("Filter:")
start_date, end_date = st.sidebar.date_input(
    label="Date Range",
    min_value=min_date,
    max_value=max_date,
    value=[min_date, max_date]
)

# Sidebar footer with contact information
st.sidebar.header("Connect:")
st.sidebar.markdown("Created by: Suandi Simanjorang")
st.sidebar.markdown("[LinkedIn](https://www.linkedin.com/in/suandi-simanjorang-8631b81a0/)")
st.sidebar.markdown("Feel free to contact for any inquiries.")
st.sidebar.markdown("---")
st.sidebar.markdown("[Dataset](https://drive.google.com/file/d/1RaBmV6Q6FYWU4HWZs80Suqd7KQC34diQ/view)")
st.sidebar.markdown("[GitHub Repository](https://github.com/Suandi123/bike_Saharing_Dicoding.git)")  # Tambahkan link GitHub di sini

# Filter main dataframe
filtered_data = day_data[
    (day_data["date"] >= pd.to_datetime(start_date)) &
    (day_data["date"] <= pd.to_datetime(end_date))
]

# Main title
st.title("Bike Sharing Dashboard")
st.markdown("##")

# Display metrics
col1, col2, col3 = st.columns(3)
with col1:
    total_rides = filtered_data['total_count'].sum()
    st.metric("Total Rides", value=total_rides)

with col2:
    casual_rides = filtered_data['casual'].sum()
    st.metric("Total Casual Rides", value=casual_rides)

with col3:
    registered_rides = filtered_data['registered'].sum()
    st.metric("Total Registered Rides", value=registered_rides)

st.markdown("---")

# Visualizations
# Monthly rental trends
monthly_aggregated['total_rides'] = monthly_aggregated['casual_rides'] + monthly_aggregated['registered_rides']
fig = px.bar(monthly_aggregated,
             x='month_year',
             y=['casual_rides', 'registered_rides', 'total_rides'],
             barmode='group',
             color_discrete_sequence=["#FFA07A", "#20B2AA", "#778899"],
             title="Monthly Bike Rental Trends",
             labels={'casual_rides': 'Casual', 'registered_rides': 'Registered', 'total_rides': 'Total'})

fig.update_layout(xaxis_title='', yaxis_title='Total Rentals',
                  xaxis=dict(showgrid=False, showline=True, linecolor='rgb(204, 204, 204)', linewidth=2, mirror=True),
                  yaxis=dict(showgrid=False, zeroline=False, showline=True, linecolor='rgb(204, 204, 204)', linewidth=2, mirror=True),
                  plot_bgcolor='rgba(255, 255, 255, 0)',
                  showlegend=True,
                  legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))

st.plotly_chart(fig, use_container_width=True)

# Weather condition analysis
fig = px.box(day_data, x='weathersit', y='total_count', color='weathersit', 
             title='Distribution of Bike Rentals by Weather',
             labels={'weathersit': 'Weather Condition', 'total_count': 'Total Rentals'},
             color_discrete_sequence=["#A52A2A", "#5F9EA0", "#D2691E", "#FF7F50"])

st.plotly_chart(fig, use_container_width=True)

# Working day analysis
fig1 = px.box(day_data, x='workingday', y='total_count', color='workingday',
              title='Bike Rentals by Working Day',
              labels={'workingday': 'Working Day', 'total_count': 'Total Rentals'},
              color_discrete_sequence=['#8A2BE2', '#A52A2A'])
fig1.update_xaxes(title_text='Working Day')
fig1.update_yaxes(title_text='Total Rentals')

# Holiday analysis
fig2 = px.box(day_data, x='holiday', y='total_count', color='holiday',
              title='Bike Rentals by Holiday',
              labels={'holiday': 'Holiday', 'total_count': 'Total Rentals'},
              color_discrete_sequence=['#DC143C', '#00FFFF'])
fig2.update_xaxes(title_text='Holiday')
fig2.update_yaxes(title_text='Total Rentals')

# Weekday analysis
fig3 = px.box(day_data, x='weekday', y='total_count', color='weekday',
              title='Bike Rentals by Weekday',
              labels={'weekday': 'Weekday', 'total_count': 'Total Rentals'},
              color_discrete_sequence=['#6495ED', '#FF8C00', '#FFD700', '#ADFF2F', '#FF4500', '#DA70D6', '#8B0000'])
fig3.update_xaxes(title_text='Weekday')
fig3.update_yaxes(title_text='Total Rentals')

st.plotly_chart(fig1, use_container_width=True)
st.plotly_chart(fig2, use_container_width=True)
st.plotly_chart(fig3, use_container_width=True)

# Scatter plot for rentals by temperature
fig = px.scatter(day_data, x='temp', y='total_count', color='season',
                 title='Bike Rentals by Temperature and Season',
                 labels={'temp': 'Temperature (°C)', 'total_count': 'Total Rentals'},
                 color_discrete_sequence=['#FF4500', '#32CD32', '#1E90FF', '#FFD700'],
                 hover_name='season')

st.plotly_chart(fig, use_container_width=True)

# Bar plot for seasonal rentals
seasonal_rentals = day_data.groupby('season')[['registered', 'casual']].sum().reset_index()
fig = px.bar(seasonal_rentals, x='season', y=['registered', 'casual'],
             title='Seasonal Bike Rentals',
             labels={'season': 'Season', 'value': 'Total Rentals', 'variable': 'User Type'},
             color_discrete_sequence=["#00FF7F", "#4682B4"], barmode='group')

st.plotly_chart(fig, use_container_width=True)

st.caption('Data analysis by: Suandi Simanjorang')
