import streamlit as st
import pandas as pd
import geopy.geocoders 
import folium
from streamlit_folium import folium_static

st.write("Please sign my guestbook! No need to put in any data that is too personal. Just a fun way to track visitors!")

# Load existing data from CSV file or create an empty DataFrame
data_file = 'user_data.csv'
try:
    df = pd.read_csv(data_file)
except FileNotFoundError:
    df = pd.DataFrame()

inputs = {}

with st.form("user_input"):
    inputs["Nickname"] = st.text_input("Nickname", max_chars=10)
    inputs["Age"] = st.text_input("Age", max_chars=3)
    inputs["City"] = st.text_input("City", max_chars=20)
    inputs["State/Province"] = st.text_input("State/Province (full name, not abbreviation)", max_chars=20)
    inputs["Country"] = st.text_input("Country", max_chars=20)
    inputs["Message"] = st.text_input("Message", max_chars=50)

    submit_button = st.form_submit_button("Submit")

if submit_button:
    # Geocode the user input to obtain latitude and longitude
    geolocator = Nominatim(user_agent="my_geocoder")
    location = f"{inputs['City']}, {inputs['State/Province']}, {inputs['Country']}"
    location_data = geolocator.geocode(location)

    # Add user input and coordinates to the DataFrame
    if location_data:
        inputs["Latitude"] = location_data.latitude
        inputs["Longitude"] = location_data.longitude
        df = df.append(inputs, ignore_index=True)
        st.success('Data added to DataFrame!')

        # Save the updated DataFrame to the CSV file
        df.to_csv(data_file, index=False)
    else:
        st.error('Location not found. Please check your input.')

# Display the updated DataFrame
st.write(df)

# Create a Folium map
m = folium.Map(location=[df['Latitude'].mean(), df['Longitude'].mean()], zoom_start=4)

# Add markers to the map
for _, row in df.iterrows():
    folium.Marker(location=[row['Latitude'], row['Longitude']], popup=row['Nickname']).add_to(m)

# Display the map in Streamlit using folium_static
folium_static(m)
#
