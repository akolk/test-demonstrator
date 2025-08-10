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
def connect_to_mcp(server_url, input_data):
    response = requests.post(server_url, json={'input': input_data})
    return response.json()

# Streamlit application
st.title("Online Data Scientist")

# Sidebar for resource selection
resource_type = st.sidebar.selectbox("Select Resource Type", ["OData", "WFS", "GraphQL", "SPARQL", "MCP"])

if resource_type == "OData":
    odata_url = st.text_input("Enter OData URL")
    if st.button("Fetch OData"):
        data = fetch_odata(odata_url)
        st.write(data)

elif resource_type == "WFS":
    wfs_url = st.text_input("Enter WFS URL")
    if st.button("Fetch WFS"):
        data = fetch_wfs(wfs_url)
        st.write(data)

elif resource_type == "GraphQL":
    graphql_url = st.text_input("Enter GraphQL URL")
    graphql_query = st.text_area("Enter GraphQL Query")
    if st.button("Fetch GraphQL"):
        data = fetch_graphql(graphql_url, graphql_query)
        st.write(data)

elif resource_type == "SPARQL":
    sparql_endpoint = st.text_input("Enter SPARQL Endpoint")
    sparql_query = st.text_area("Enter SPARQL Query")
    if st.button("Fetch SPARQL"):
        data = fetch_sparql(sparql_endpoint, sparql_query)
        st.write(data)

elif resource_type == "MCP":
    mcp_server_url = st.text_input("Enter MCP Server URL")
    mcp_input = st.text_input("Enter Input for MCP")
    if st.button("Connect to MCP"):
        data = connect_to_mcp(mcp_server_url, mcp_input)
        st.write(data)

# Displaying data as Map, Chart, or Table
if 'data' in locals():
    if isinstance(data, dict):
        st.json(data)
    elif isinstance(data, bytes):
        st.write(data.decode())
    else:
        df = pd.DataFrame(data)
        if st.checkbox("Show Data as Table"):
            st.write(df)
        if st.checkbox("Show Data as Chart"):
            chart = alt.Chart(df).mark_bar().encode(
                x='column_x',
                y='column_y'
            )
            st.altair_chart(chart, use_container_width=True)
        if st.checkbox("Show Data on Map"):
            map_center = [df['latitude'].mean(), df['longitude'].mean()]
            m = folium.Map(location=map_center, zoom_start=10)
            for _, row in df.iterrows():
                folium.Marker([row['latitude'], row['longitude']], popup=row['name']).add_to(m)
            st.write(m)

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
altair
"""

# Save Dockerfile and requirements.txt
with open("Dockerfile", "w") as f:
    f.write(dockerfile_content.strip())

with open("requirements.txt", "w") as f:
    f.write(requirements_content.strip())

st.success("Dockerfile and requirements.txt created successfully.")
```

This script creates a Streamlit application that can fetch data from various online resources and display it in different formats. It also generates a Dockerfile and a requirements.txt file for deployment.