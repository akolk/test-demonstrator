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

# Function to connect to MCP server
def connect_mcp_server(mcp_url, input_data):
    response = requests.post(mcp_url, json={'input': input_data})
    return response.json()

# Streamlit application
st.title("Online Data Scientist")

# Sidebar for selecting data source
st.sidebar.header("Select Data Source")
data_source = st.sidebar.selectbox("Choose a data source", ["OData", "WFS", "GraphQL", "SPARQL", "MCP"])

# Input fields based on selected data source
if data_source == "OData":
    odata_url = st.text_input("Enter OData URL")
    if st.button("Fetch OData"):
        data = fetch_odata(odata_url)
        st.write(data)

elif data_source == "WFS":
    wfs_url = st.text_input("Enter WFS URL")
    if st.button("Fetch WFS"):
        data = fetch_wfs(wfs_url)
        st.write(data)

elif data_source == "GraphQL":
    graphql_url = st.text_input("Enter GraphQL URL")
    graphql_query = st.text_area("Enter GraphQL Query")
    if st.button("Fetch GraphQL"):
        data = fetch_graphql(graphql_url, graphql_query)
        st.write(data)

elif data_source == "SPARQL":
    sparql_endpoint = st.text_input("Enter SPARQL Endpoint")
    sparql_query = st.text_area("Enter SPARQL Query")
    if st.button("Fetch SPARQL"):
        data = fetch_sparql(sparql_endpoint, sparql_query)
        st.write(data)

elif data_source == "MCP":
    mcp_url = st.text_input("Enter MCP Server URL")
    mcp_input = st.text_area("Enter input for MCP")
    if st.button("Send to MCP"):
        response = connect_mcp_server(mcp_url, mcp_input)
        st.write(response)

# Visualization options
if st.button("Show Map"):
    # Example: Create a simple map
    m = folium.Map(location=[45.5236, -122.6750], zoom_start=13)
    folium.Marker([45.5236, -122.6750], popup='Sample Location').add_to(m)
    folium_static(m)

if st.button("Show Chart"):
    # Example: Create a simple chart
    data = [1, 2, 3, 4, 5]
    plt.plot(data)
    st.pyplot()

if st.button("Show Table"):
    # Example: Create a simple table
    df = pd.DataFrame({'Column1': [1, 2, 3], 'Column2': ['A', 'B', 'C']})
    st.table(df)

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
folium
streamlit-folium
matplotlib
"""

# Save Dockerfile and requirements.txt
with open("Dockerfile", "w") as f:
    f.write(dockerfile_content)

with open("requirements.txt", "w") as f:
    f.write(requirements_content)

st.success("Dockerfile and requirements.txt have been created.")
```

This code creates a Streamlit application that allows users to fetch data from various online resources, connect to an MCP server, and visualize the data in different formats. It also generates a Dockerfile and a requirements.txt file for deployment.