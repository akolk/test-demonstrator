import streamlit as st
import pandas as pd
import requests
import json
import folium
import altair as alt

# Function to fetch data from OData
def fetch_odata(url):
    response = requests.get(url)
    return response.json()

# Function to fetch data from WFS
def fetch_wfs(url):
    response = requests.get(url)
    return response.text

# Function to fetch data from GraphQL
def fetch_graphql(url, query):
    response = requests.post(url, json={'query': query})
    return response.json()

# Function to fetch data from SPARQL
def fetch_sparql(endpoint, query):
    response = requests.get(endpoint, params={'query': query, 'format': 'json'})
    return response.json()

# Function to display data as a map
def display_map(data):
    m = folium.Map(location=[data['latitude'].mean(), data['longitude'].mean()], zoom_start=10)
    for _, row in data.iterrows():
        folium.Marker([row['latitude'], row['longitude']], popup=row['name']).add_to(m)
    return m

# Function to display data as a chart
def display_chart(data):
    chart = alt.Chart(data).mark_bar().encode(
        x='category:N',
        y='value:Q'
    ).interactive()
    return chart

# Function to display data as a table
def display_table(data):
    return pd.DataFrame(data)

# Main Streamlit application
def main():
    st.title("Online Data Scientist")

    # Input for data source
    data_source = st.selectbox("Select Data Source", ["OData", "WFS", "GraphQL", "SPARQL"])
    
    if data_source == "OData":
        url = st.text_input("Enter OData URL")
        if st.button("Fetch Data"):
            data = fetch_odata(url)
            st.write(data)

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
            st.write(data)

    elif data_source == "SPARQL":
        endpoint = st.text_input("Enter SPARQL Endpoint")
        query = st.text_area("Enter SPARQL Query")
        if st.button("Fetch Data"):
            data = fetch_sparql(endpoint, query)
            st.write(data)

    # Display options for visualization
    if st.button("Display as Map"):
        if 'latitude' in data and 'longitude' in data:
            map_display = display_map(data)
            st.write(map_display)

    if st.button("Display as Chart"):
        chart_display = display_chart(data)
        st.altair_chart(chart_display)

    if st.button("Display as Table"):
        table_display = display_table(data)
        st.write(table_display)

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
altair