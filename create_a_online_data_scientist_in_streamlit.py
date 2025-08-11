import streamlit as st
import pandas as pd
import requests
import geopandas as gpd
import matplotlib.pyplot as plt
import json
import os

# Function to fetch data from OData
def fetch_odata(url):
    response = requests.get(url)
    return response.json()

# Function to fetch data from WFS
def fetch_wfs(url):
    response = requests.get(url)
    return gpd.read_file(response.url)

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
def connect_mcp_server(mcp_url, query):
    response = requests.post(mcp_url, json={'query': query})
    return response.json()

# Streamlit application
st.title("Online Data Scientist")

# Input for online resource URLs
odata_url = st.text_input("OData URL")
wfs_url = st.text_input("WFS URL")
graphql_url = st.text_input("GraphQL URL")
sparql_endpoint = st.text_input("SPARQL Endpoint")
mcp_url = st.text_input("MCP Server URL")

# Input for GraphQL query
graphql_query = st.text_area("GraphQL Query")

# Input for SPARQL query
sparql_query = st.text_area("SPARQL Query")

# Fetch and display OData
if st.button("Fetch OData"):
    odata_data = fetch_odata(odata_url)
    st.write(odata_data)

# Fetch and display WFS
if st.button("Fetch WFS"):
    wfs_data = fetch_wfs(wfs_url)
    st.map(wfs_data)

# Fetch and display GraphQL
if st.button("Fetch GraphQL"):
    graphql_data = fetch_graphql(graphql_url, graphql_query)
    st.write(graphql_data)

# Fetch and display SPARQL
if st.button("Fetch SPARQL"):
    sparql_data = fetch_sparql(sparql_endpoint, sparql_query)
    st.write(sparql_data)

# Fetch and display MCP
if st.button("Connect to MCP Server"):
    mcp_data = connect_mcp_server(mcp_url, graphql_query)
    st.write(mcp_data)

# Dockerfile content
dockerfile_content = """
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
"""

# Requirements.txt content
requirements_content = """
streamlit
pandas
requests
geopandas
matplotlib
"""

# Write Dockerfile
with open("Dockerfile", "w") as f:
    f.write(dockerfile_content.strip())

# Write requirements.txt
with open("requirements.txt", "w") as f:
    f.write(requirements_content.strip())

# Save the Streamlit app as app.py
with open("app.py", "w") as f:
    f.write("""
import streamlit as st
import pandas as pd
import requests
import geopandas as gpd
import matplotlib.pyplot as plt
import json
import os

# Function to fetch data from OData
def fetch_odata(url):
    response = requests.get(url)
    return response.json()

# Function to fetch data from WFS
def fetch_wfs(url):
    response = requests.get(url)
    return gpd.read_file(response.url)

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
def connect_mcp_server(mcp_url, query):
    response = requests.post(mcp_url, json={'query': query})
    return response.json()

# Streamlit application
st.title("Online Data Scientist")

# Input for online resource URLs
odata_url = st.text_input("OData URL")
wfs_url = st.text_input("WFS URL")
graphql_url = st.text_input("GraphQL URL")
sparql_endpoint = st.text_input("SPARQL Endpoint")
mcp_url = st.text_input("MCP Server URL")

# Input for GraphQL query
graphql_query = st.text_area("GraphQL Query")

# Input for SPARQL query
sparql_query = st.text_area("SPARQL Query")

# Fetch and display OData
if st.button("Fetch OData"):
    odata_data = fetch_odata(odata_url)
    st.write(odata_data)

# Fetch and display WFS
if st.button("Fetch WFS"):
    wfs_data = fetch_wfs(wfs_url)
    st.map(wfs_data)

# Fetch and display GraphQL
if st.button("Fetch GraphQL"):
    graphql_data = fetch_graphql(graphql_url, graphql_query)
    st.write(graphql_data)

# Fetch and display SPARQL
if st.button("Fetch SPARQL"):
    sparql_data = fetch_sparql(sparql_endpoint, sparql_query)
    st.write(sparql_data)

# Fetch and display MCP
if st.button("Connect to MCP Server"):
    mcp_data = connect_mcp_server(mcp_url, graphql_query)
    st.write(mcp_data)
""")