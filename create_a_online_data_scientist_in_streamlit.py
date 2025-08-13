import streamlit as st
import pandas as pd
import requests
import json
import matplotlib.pyplot as plt
import geopandas as gpd
import folium
from io import BytesIO
import base64

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
def connect_mcp_server(url, input_data):
    response = requests.post(url, json={'input': input_data})
    return response.json()

# Streamlit application
st.title("Online Data Scientist")

# Input for online resources
resource_type = st.selectbox("Select Resource Type", ["OData", "WFS", "GraphQL", "SPARQL"])
resource_url = st.text_input("Enter Resource URL")

if resource_type == "GraphQL":
    query = st.text_area("Enter GraphQL Query")
else:
    query = ""

if st.button("Fetch Data"):
    if resource_type == "OData":
        data = fetch_odata(resource_url)
    elif resource_type == "WFS":
        data = fetch_wfs(resource_url)
    elif resource_type == "GraphQL":
        data = fetch_graphql(resource_url, query)
    elif resource_type == "SPARQL":
        data = fetch_sparql(resource_url, query)
    
    st.write(data)

# Input for MCP server
mcp_url = st.text_input("Enter MCP Server URL")
mcp_input = st.text_area("Enter Input for MCP")

if st.button("Send to MCP"):
    if mcp_url and mcp_input:
        mcp_response = connect_mcp_server(mcp_url, mcp_input)
        st.write(mcp_response)

# Displaying results as Map, Chart, or Table
if 'data' in locals():
    if isinstance(data, dict) and 'features' in data:
        # Assuming GeoJSON format for map
        geo_df = gpd.GeoDataFrame.from_features(data['features'])
        m = folium.Map(location=[geo_df.geometry.y.mean(), geo_df.geometry.x.mean()], zoom_start=10)
        folium.GeoJson(geo_df).add_to(m)
        st.write(m)
    elif isinstance(data, list) and len(data) > 0:
        df = pd.DataFrame(data)
        st.write(df)
        st.bar_chart(df)
    else:
        st.write("Data format not recognized.")

# Dockerfile content
dockerfile_content = """
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
"""

# requirements.txt content
requirements_content = """
streamlit
pandas
requests
matplotlib
geopandas
folium
"""

# Save Dockerfile and requirements.txt
with open("Dockerfile", "w") as f:
    f.write(dockerfile_content)

with open("requirements.txt", "w") as f:
    f.write(requirements_content)

st.success("Dockerfile and requirements.txt have been created.")
```

This code creates a Streamlit application that allows users to fetch data from various online resources and connect to an MCP server. It also generates a Dockerfile and a requirements.txt file for deployment.