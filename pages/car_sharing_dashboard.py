import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
 trips = pd.read_csv("dataset/trips.csv")
 cars = pd.read_csv("dataset/cars.csv")
 cities = pd.read_csv("dataset/cities.csv")
 return trips, cars, cities

trips, cars, cities = load_data()

trips_merged = trips.merge(cars, left_on='car_id', right_on="id", how="left")

trips_merged = trips_merged.merge(cities, on='city_id', how='left')

trips_merged = trips_merged.drop(columns=["car_id", "city_id", "id","customer_id"], errors="ignore")

trips_merged['pickup_time'] = pd.to_datetime(trips_merged['pickup_time'])
trips_merged['dropoff_time'] = pd.to_datetime(trips_merged['dropoff_time'])
trips_merged['pickup_date'] = trips_merged['pickup_time'].dt.date
trips_merged['trip_duration'] = (trips_merged['dropoff_time'] - trips_merged['pickup_time']).dt.total_seconds() / 60  # en minutes


cars_brand = st.sidebar.multiselect("Select the Car Brand", trips_merged['brand'].unique())

if len(cars_brand) > 0:
    trips_merged_filtered = trips_merged[trips_merged['brand'].isin(cars_brand)]
else:
    trips_merged_filtered = trips_merged


total_trips = trips_merged_filtered.shape[0]  
total_distance = trips_merged_filtered['distance'].sum()  

top_car_revenue = trips_merged_filtered.groupby('model')['revenue'].sum()
top_car = top_car_revenue.idxmax() 
   

col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Total Trips", value=total_trips)
with col2:
    st.metric(label="Top Car Model by Revenue", value=top_car)
with col3:
    st.metric(label="Total Distance (km)", value=f"{total_distance:,.2f}")

st.header("Visualization")
st.subheader("Trips Over Time")
trips_over_time = trips_merged['pickup_date'].value_counts().sort_index()
st.line_chart(trips_over_time)

st.subheader("Revenue Per Car Model")
revenue_per_car_model = trips_merged.groupby('model')['revenue'].sum()
st.bar_chart(revenue_per_car_model)

st.subheader("Cumulative Revenue Growth Over Time")
cumulative_revenue = trips_merged.groupby('pickup_date')['revenue'].sum().cumsum()
st.area_chart(cumulative_revenue)

st.subheader("Number of Trips Per Car Model")
trips_per_car_model = trips_merged.groupby('model')['pickup_time'].count()
st.bar_chart(trips_per_car_model)

st.subheader("Average Trip Duration by City")
average_trip_duration = trips_merged.groupby('city_name')['trip_duration'].mean()
st.bar_chart(average_trip_duration)

st.subheader("Revenue by City")
revenue_by_city = trips_merged.groupby('city_name')['revenue'].sum()
st.bar_chart(revenue_by_city)

st.subheader("Revenue by Car Model Over Time")
revenue_by_car_model_over_time = trips_merged.groupby(['pickup_date', 'model'])['revenue'].sum().unstack()
st.line_chart(revenue_by_car_model_over_time)
