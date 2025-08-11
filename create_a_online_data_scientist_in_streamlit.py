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
def connect_mcp(server_url, input_text):
    response = requests.post(server_url, json={'input': input_text})
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

    # Display data as a table
    st.subheader("Data Table")
    st.dataframe(data)

    # Display data as a chart
    if st.checkbox("Show Chart"):
        chart_type = st.selectbox("Select Chart Type", ["Line", "Bar", "Area"])
        if chart_type == "Line":
            chart = alt.Chart(data).mark_line().encode(x=data.columns[0], y=data.columns[1])
        elif chart_type == "Bar":
            chart = alt.Chart(data).mark_bar().encode(x=data.columns[0], y=data.columns[1])
        else:
            chart = alt.Chart(data).mark_area().encode(x=data.columns[0], y=data.columns[1])
        st.altair_chart(chart)

    # Display data on a map if applicable
    if 'latitude' in data.columns and 'longitude' in data.columns:
        st.subheader("Map")
        m = folium.Map(location=[data['latitude'].mean(), data['longitude'].mean()], zoom_start=10)
        for idx, row in data.iterrows():
            folium.Marker([row['latitude'], row['longitude']], popup=row.to_json()).add_to(m)
        st.map(m)

# Input for MCP server
mcp_server_url = st.text_input("Enter MCP Server URL")
mcp_input = st.text_area("Enter Input for MCP")

if st.button("Send to MCP"):
    mcp_response = connect_mcp(mcp_server_url, mcp_input)
    st.write(mcp_response)

# Dockerfile
dockerfile_content = """
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
"""

# requirements.txt
requirements_content = """
streamlit
pandas
requests
folium
matplotlib
altair
"""

# Save Dockerfile and requirements.txt
with open("Dockerfile", "w") as f:
    f.write(dockerfile_content)

with open("requirements.txt", "w") as f:
    f.write(requirements_content)

if __name__ == "__main__":
    st.write("Run this app using Streamlit!")