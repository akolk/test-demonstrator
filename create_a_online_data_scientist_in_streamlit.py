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
    return pd.DataFrame(response.json()['value'])

# Function to fetch data from WFS
def fetch_wfs(url):
    response = requests.get(url)
    return pd.DataFrame(response.json()['features'])

# Function to fetch data from GraphQL
def fetch_graphql(url, query):
    response = requests.post(url, json={'query': query})
    return pd.DataFrame(response.json()['data'])

# Function to fetch data from SPARQL
def fetch_sparql(endpoint, query):
    response = requests.get(endpoint, params={'query': query, 'format': 'json'})
    return pd.DataFrame(response.json()['results']['bindings'])

# Function to connect to MCP server
def fetch_mcp_data(mcp_url, query):
    response = requests.post(mcp_url, json={'query': query})
    return response.json()

# Streamlit application
st.title("Online Data Scientist")

# Sidebar for resource selection
resource_type = st.sidebar.selectbox("Select Resource Type", ["OData", "WFS", "GraphQL", "SPARQL", "MCP"])

# Input fields based on resource type
if resource_type == "OData":
    odata_url = st.sidebar.text_input("Enter OData URL")
    if st.sidebar.button("Fetch OData"):
        data = fetch_odata(odata_url)
        st.write(data)

elif resource_type == "WFS":
    wfs_url = st.sidebar.text_input("Enter WFS URL")
    if st.sidebar.button("Fetch WFS"):
        data = fetch_wfs(wfs_url)
        st.write(data)

elif resource_type == "GraphQL":
    graphql_url = st.sidebar.text_input("Enter GraphQL URL")
    graphql_query = st.sidebar.text_area("Enter GraphQL Query")
    if st.sidebar.button("Fetch GraphQL"):
        data = fetch_graphql(graphql_url, graphql_query)
        st.write(data)

elif resource_type == "SPARQL":
    sparql_endpoint = st.sidebar.text_input("Enter SPARQL Endpoint")
    sparql_query = st.sidebar.text_area("Enter SPARQL Query")
    if st.sidebar.button("Fetch SPARQL"):
        data = fetch_sparql(sparql_endpoint, sparql_query)
        st.write(data)

elif resource_type == "MCP":
    mcp_url = st.sidebar.text_input("Enter MCP URL")
    mcp_query = st.sidebar.text_area("Enter MCP Query")
    if st.sidebar.button("Fetch MCP Data"):
        mcp_data = fetch_mcp_data(mcp_url, mcp_query)
        st.write(mcp_data)

# Visualization options
if 'data' in locals():
    if st.sidebar.checkbox("Show Map"):
        map_data = folium.Map(location=[data['latitude'].mean(), data['longitude'].mean()], zoom_start=10)
        for _, row in data.iterrows():
            folium.Marker([row['latitude'], row['longitude']], popup=row['name']).add_to(map_data)
        folium_static(map_data)

    if st.sidebar.checkbox("Show Chart"):
        chart = alt.Chart(data).mark_bar().encode(
            x='category',
            y='value'
        )
        st.altair_chart(chart)

    if st.sidebar.checkbox("Show Table"):
        st.write(data)

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
altair
folium
streamlit-folium
"""

# Save Dockerfile and requirements.txt
with open("Dockerfile", "w") as f:
    f.write(dockerfile_content)

with open("requirements.txt", "w") as f:
    f.write(requirements_content)

st.sidebar.success("Dockerfile and requirements.txt created.")
```

This code creates a Streamlit application that allows users to fetch and analyze data from various online resources, including OData, WFS, GraphQL, SPARQL, and MCP. It also generates a Dockerfile and a requirements.txt file for deployment.