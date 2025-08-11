import streamlit as st
import pandas as pd
import requests
import json
import folium
from streamlit_folium import folium_static
import matplotlib.pyplot as plt

# Function to fetch data from OData
def fetch_odata(url):
    response = requests.get(url)
    return response.json()

# Function to fetch data from WFS
def fetch_wfs(url):
    response = requests.get(url)
    return response.content

# Function to fetch data from GraphQL
def fetch_graphql(url, query):
    response = requests.post(url, json={'query': query})
    return response.json()

# Function to fetch data from SPARQL
def fetch_sparql(endpoint, query):
    response = requests.get(endpoint, params={'query': query, 'format': 'json'})
    return response.json()

# Function to display data as a table
def display_table(data):
    df = pd.DataFrame(data)
    st.write(df)

# Function to display data as a chart
def display_chart(data):
    df = pd.DataFrame(data)
    st.line_chart(df)

# Function to display data on a map
def display_map(location_data):
    m = folium.Map(location=[location_data['latitude'], location_data['longitude']], zoom_start=10)
    folium.Marker([location_data['latitude'], location_data['longitude']], tooltip='Location').add_to(m)
    folium_static(m)

# Main application
def main():
    st.title("Online Data Scientist")

    # Input for data source
    data_source = st.selectbox("Choose a data source", ["OData", "WFS", "GraphQL", "SPARQL"])
    
    if data_source == "OData":
        url = st.text_input("Enter OData URL")
        if st.button("Fetch Data"):
            data = fetch_odata(url)
            display_table(data)

    elif data_source == "WFS":
        url = st.text_input("Enter WFS URL")
        if st.button("Fetch Data"):
            data = fetch_wfs(url)
            st.write(data)

    elif data_source == "GraphQL":
        url = st.text_input("Enter GraphQL URL")
        query = st.text_area("Enter GraphQL Query")
        if st.button("Fetch Data"):
            data = fetch_graphql(url, query)
            display_table(data)

    elif data_source == "SPARQL":
        endpoint = st.text_input("Enter SPARQL Endpoint")
        query = st.text_area("Enter SPARQL Query")
        if st.button("Fetch Data"):
            data = fetch_sparql(endpoint, query)
            display_table(data)

    # Example of displaying data on a map
    if st.button("Show Example Map"):
        location_data = {'latitude': 37.7749, 'longitude': -122.4194}  # Example coordinates
        display_map(location_data)

if __name__ == "__main__":
    main()
```

### Dockerfile
```dockerfile
# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Command to run the application
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### requirements.txt
```
streamlit
pandas
requests
folium
streamlit-folium
matplotlib