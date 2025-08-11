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
    headers = {'Accept': 'application/json'}
    response = requests.get(endpoint, headers=headers, params={'query': query})
    return response.json()

# Function to connect to MCP server
def connect_to_mcp(server_url, input_data):
    response = requests.post(server_url, json={'input': input_data})
    return response.json()

# Streamlit UI
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

    # Display data
    if isinstance(data, dict):
        st.json(data)
    elif isinstance(data, bytes):
        st.write(data)
    else:
        df = pd.DataFrame(data)
        st.dataframe(df)

# MCP input
mcp_server_url = st.text_input("Enter MCP Server URL")
mcp_input = st.text_input("Enter input for MCP")

if st.button("Send to MCP"):
    mcp_response = connect_to_mcp(mcp_server_url, mcp_input)
    st.json(mcp_response)

# Visualization options
if st.button("Visualize Data"):
    if isinstance(data, pd.DataFrame):
        if st.checkbox("Show as Map"):
            m = folium.Map(location=[data['latitude'].mean(), data['longitude'].mean()], zoom_start=10)
            for _, row in data.iterrows():
                folium.Marker([row['latitude'], row['longitude']], popup=row['name']).add_to(m)
            folium_static(m)
        elif st.checkbox("Show as Chart"):
            st.line_chart(data)
        elif st.checkbox("Show as Table"):
            st.dataframe(data)

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

if __name__ == "__main__":
    st.write("Dockerfile and requirements.txt have been created.")