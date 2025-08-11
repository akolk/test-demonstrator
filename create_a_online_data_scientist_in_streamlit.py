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
    response = requests.get(endpoint, params={'query': query}, headers=headers)
    return response.json()

# Function to connect to MCP server
def connect_to_mcp_server(input_data):
    # Placeholder for MCP server connection logic
    # Replace with actual connection logic
    return f"Response from MCP server for input: {input_data}"

# Streamlit UI
st.title("Online Data Scientist")

# Input for online resource URLs
odata_url = st.text_input("Enter OData URL:")
wfs_url = st.text_input("Enter WFS URL:")
graphql_url = st.text_input("Enter GraphQL URL:")
sparql_endpoint = st.text_input("Enter SPARQL Endpoint:")
mcp_input = st.text_input("Enter input for MCP server:")

if st.button("Fetch OData"):
    data = fetch_odata(odata_url)
    st.write(data)

if st.button("Fetch WFS"):
    data = fetch_wfs(wfs_url)
    st.write(data)

if st.button("Fetch GraphQL"):
    query = st.text_area("Enter GraphQL query:")
    data = fetch_graphql(graphql_url, query)
    st.write(data)

if st.button("Fetch SPARQL"):
    query = st.text_area("Enter SPARQL query:")
    data = fetch_sparql(sparql_endpoint, query)
    st.write(data)

if st.button("Connect to MCP Server"):
    response = connect_to_mcp_server(mcp_input)
    st.write(response)

# Visualization options
if st.button("Show Map"):
    # Placeholder for map visualization
    m = folium.Map(location=[45.5236, -122.6750], zoom_start=13)
    folium.Marker([45.5236, -122.6750], popup='Sample Location').add_to(m)
    st.map(m)

if st.button("Show Chart"):
    # Placeholder for chart visualization
    data = pd.DataFrame({
        'x': [1, 2, 3, 4],
        'y': [10, 20, 30, 40]
    })
    chart = alt.Chart(data).mark_line().encode(x='x', y='y')
    st.altair_chart(chart)

if st.button("Show Table"):
    # Placeholder for table visualization
    data = pd.DataFrame({
        'Column1': ['A', 'B', 'C'],
        'Column2': [1, 2, 3]
    })
    st.table(data)

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
matplotlib
altair
"""

# Write Dockerfile and requirements.txt
with open("Dockerfile", "w") as f:
    f.write(dockerfile_content.strip())

with open("requirements.txt", "w") as f:
    f.write(requirements_content.strip())