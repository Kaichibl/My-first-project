import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
 trips = pd.read_csv("dataset/trips.csv")
 cars = pd.read_csv("dataset/cars.csv")
 cities = pd.read_csv("dataset/cities.csv")
 return trips, cars, cities

trips, cars, cities = load_data()

trips_merged = trips.merge(cars, on='id', how='left')

trips_merged = trips_merged.merge(cities, on='city_id', how='left')

trips_merged = trips_merged.drop(columns=["car_id", "city_id", "customer_id","id"])

st.dataframe(trips_merged)



