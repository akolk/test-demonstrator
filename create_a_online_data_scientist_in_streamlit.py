import streamlit as st
import pandas as pd
import requests
import json
import altair as alt
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

# Function to connect to MCP server
def connect_mcp(server_url, input_data):
    response = requests.post(server_url, json={'input': input_data})
    return response.json()

# Streamlit UI
st.title("Online Data Scientist")

# Input for data source
data_source = st.selectbox("Select Data Source", ["OData", "WFS", "GraphQL", "SPARQL"])

# Input for URL or endpoint
url = st.text_input("Enter the URL or endpoint")

# For GraphQL, input query
if data_source == "GraphQL":
    query = st.text_area("Enter GraphQL Query")

# Button to fetch data
if st.button("Fetch Data"):
    if data_source == "OData":
        data = fetch_odata(url)
        st.write(data)
    elif data_source == "WFS":
        data = fetch_wfs(url)
        st.write(data)
    elif data_source == "GraphQL":
        data = fetch_graphql(url, query)
        st.write(data)
    elif data_source == "SPARQL":
        query = st.text_area("Enter SPARQL Query")
        data = fetch_sparql(url, query)
        st.write(data)

# Input for MCP server
mcp_url = st.text_input("Enter MCP Server URL")
mcp_input = st.text_input("Enter input for MCP")

# Button to connect to MCP
if st.button("Connect to MCP"):
    mcp_response = connect_mcp(mcp_url, mcp_input)
    st.write(mcp_response)

# Display results as Map, Chart or Table
if 'data' in locals():
    if isinstance(data, dict):
        df = pd.DataFrame(data)
        st.write(df)
        chart = alt.Chart(df).mark_line().encode(x='x_column', y='y_column')
        st.altair_chart(chart, use_container_width=True)
    elif isinstance(data, bytes):
        st.write("WFS data received, displaying as raw content.")
        st.text(data.decode('utf-8'))
    else:
        st.write("Data format not recognized.")

# Folium map example
if st.button("Show Map"):
    m = folium.Map(location=[45.5236, -122.6750], zoom_start=13)
    folium.Marker([45.5236, -122.6750], popup='Sample Marker').add_to(m)
    folium_static(m)

```

**Dockerfile**
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

**requirements.txt**
```
streamlit
pandas
requests
altair
folium
streamlit-folium