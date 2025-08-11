import streamlit as st
import pandas as pd
import requests
import json
import folium
import matplotlib.pyplot as plt
import altair as alt

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
    headers = {'Accept': 'application/json'}
    response = requests.get(endpoint, headers=headers, params={'query': query})
    return response.json()

# Function to connect to MCP server
def connect_mcp(server_url, input_data):
    response = requests.post(server_url, json={'input': input_data})
    return response.json()

# Streamlit application
st.title("Online Data Scientist")

# Sidebar for resource selection
st.sidebar.header("Select Data Source")
data_source = st.sidebar.selectbox("Choose a data source", ["OData", "WFS", "GraphQL", "SPARQL"])

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

# MCP server interaction
mcp_server_url = st.sidebar.text_input("Enter MCP Server URL")
mcp_input = st.sidebar.text_input("Enter input for MCP")
if st.sidebar.button("Send to MCP"):
    mcp_response = connect_mcp(mcp_server_url, mcp_input)
    st.write(mcp_response)

# Visualization options
if st.button("Show Map"):
    # Example: Create a simple map
    m = folium.Map(location=[45.5236, -122.6750], zoom_start=13)
    folium.Marker([45.5236, -122.6750], tooltip='Sample Marker').add_to(m)
    st.write(m)

if st.button("Show Chart"):
    # Example: Create a simple chart
    data = {'x': [1, 2, 3, 4], 'y': [10, 20, 30, 40]}
    df = pd.DataFrame(data)
    chart = alt.Chart(df).mark_line().encode(x='x', y='y')
    st.altair_chart(chart)

if st.button("Show Table"):
    # Example: Create a simple table
    data = {'Column 1': [1, 2, 3], 'Column 2': ['A', 'B', 'C']}
    df = pd.DataFrame(data)
    st.write(df)

# Dockerfile content
dockerfile_content = """
# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY . .

# Command to run the application
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
"""

# requirements.txt content
requirements_content = """
streamlit
pandas
requests
folium
matplotlib
altair
"""

# Save Dockerfile
with open("Dockerfile", "w") as f:
    f.write(dockerfile_content.strip())

# Save requirements.txt
with open("requirements.txt", "w") as f:
    f.write(requirements_content.strip())

st.sidebar.success("Dockerfile and requirements.txt created successfully.")