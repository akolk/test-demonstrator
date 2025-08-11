import streamlit as st
import pandas as pd
import requests
import json
import folium
from streamlit_folium import folium_static

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
    st.dataframe(df)

# Function to display data as a map
def display_map(location_data):
    m = folium.Map(location=[location_data['latitude'], location_data['longitude']], zoom_start=10)
    folium.Marker([location_data['latitude'], location_data['longitude']], popup=location_data['name']).add_to(m)
    folium_static(m)

# Function to display data as a chart
def display_chart(data):
    df = pd.DataFrame(data)
    st.line_chart(df)

# Main application
def main():
    st.title("Online Data Scientist")

    resource_type = st.selectbox("Select Resource Type", ["OData", "WFS", "GraphQL", "SPARQL"])
    url = st.text_input("Enter Resource URL")

    if resource_type == "OData":
        if st.button("Fetch OData"):
            data = fetch_odata(url)
            display_table(data)

    elif resource_type == "WFS":
        if st.button("Fetch WFS"):
            data = fetch_wfs(url)
            st.text(data)  # Display raw WFS response

    elif resource_type == "GraphQL":
        query = st.text_area("Enter GraphQL Query")
        if st.button("Fetch GraphQL"):
            data = fetch_graphql(url, query)
            display_table(data)

    elif resource_type == "SPARQL":
        query = st.text_area("Enter SPARQL Query")
        if st.button("Fetch SPARQL"):
            data = fetch_sparql(url, query)
            display_table(data)

    # Example of displaying a map
    if st.button("Display Map"):
        location_data = {'latitude': 37.7749, 'longitude': -122.4194, 'name': 'San Francisco'}  # Example data
        display_map(location_data)

if __name__ == "__main__":
    main()
```

### Dockerfile
```dockerfile
# Use the official Python image from the Docker Hub
FROM python:3.9

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