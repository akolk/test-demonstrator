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
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to fetch OData.")
        return None

# Function to fetch data from WFS
def fetch_wfs(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.content
    else:
        st.error("Failed to fetch WFS.")
        return None

# Function to fetch data from GraphQL
def fetch_graphql(url, query):
    response = requests.post(url, json={'query': query})
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to fetch GraphQL.")
        return None

# Function to fetch data from SPARQL
def fetch_sparql(url, query):
    response = requests.get(url, params={'query': query, 'format': 'json'})
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to fetch SPARQL.")
        return None

# Function to connect to MCP server
def connect_to_mcp(server_url, input_data):
    response = requests.post(server_url, json={'input': input_data})
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to connect to MCP server.")
        return None

# Streamlit application
st.title("Online Data Scientist")

# Input for online resources
resource_type = st.selectbox("Select Resource Type", ["OData", "WFS", "GraphQL", "SPARQL"])
resource_url = st.text_input("Enter Resource URL")
query = st.text_area("Enter Query (if applicable)")

if st.button("Fetch Data"):
    if resource_type == "OData":
        data = fetch_odata(resource_url)
    elif resource_type == "WFS":
        data = fetch_wfs(resource_url)
    elif resource_type == "GraphQL":
        data = fetch_graphql(resource_url, query)
    elif resource_type == "SPARQL":
        data = fetch_sparql(resource_url, query)

    if data:
        st.write(data)

        # Display data as a table if it's a DataFrame
        if isinstance(data, dict) and 'value' in data:
            df = pd.DataFrame(data['value'])
            st.write(df)

            # Display chart
            if st.checkbox("Show Chart"):
                chart = alt.Chart(df).mark_bar().encode(
                    x=alt.X(df.columns[0]),
                    y=alt.Y(df.columns[1])
                )
                st.altair_chart(chart)

            # Display map if coordinates are available
            if 'latitude' in df.columns and 'longitude' in df.columns:
                m = folium.Map(location=[df['latitude'].mean(), df['longitude'].mean()], zoom_start=10)
                for _, row in df.iterrows():
                    folium.Marker([row['latitude'], row['longitude']], popup=row.to_json()).add_to(m)
                folium_static(m)

# Input for MCP server
mcp_server_url = st.text_input("Enter MCP Server URL")
mcp_input = st.text_area("Enter Input for MCP")

if st.button("Send to MCP"):
    if mcp_server_url and mcp_input:
        mcp_response = connect_to_mcp(mcp_server_url, mcp_input)
        if mcp_response:
            st.write(mcp_response)

# Keep track of resources
if 'resources' not in st.session_state:
    st.session_state.resources = []

if st.button("Save Resource"):
    if resource_url and resource_type:
        st.session_state.resources.append({'type': resource_type, 'url': resource_url})
        st.success("Resource saved!")

st.write("Saved Resources:")
st.write(st.session_state.resources)