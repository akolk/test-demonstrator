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
    response = requests.get(endpoint, params={'query': query, 'format': 'json'})
    return response.json()

# Function to display data as a map
def display_map(data):
    m = folium.Map(location=[data['latitude'].mean(), data['longitude'].mean()], zoom_start=10)
    for _, row in data.iterrows():
        folium.Marker([row['latitude'], row['longitude']], popup=row['name']).add_to(m)
    return m

# Function to display data as a chart
def display_chart(data):
    chart = alt.Chart(data).mark_bar().encode(
        x='category',
        y='value'
    )
    return chart

# Function to display data as a table
def display_table(data):
    return pd.DataFrame(data)

# Streamlit application
st.title("Online Data Scientist")

# Input for resource URLs
odata_url = st.text_input("OData URL")
wfs_url = st.text_input("WFS URL")
graphql_url = st.text_input("GraphQL URL")
sparql_url = st.text_input("SPARQL Endpoint")

# Input for GraphQL query
graphql_query = st.text_area("GraphQL Query")

# Fetch and display data
if st.button("Fetch OData"):
    odata_result = fetch_odata(odata_url)
    st.write(display_table(odata_result))

if st.button("Fetch WFS"):
    wfs_result = fetch_wfs(wfs_url)
    st.write(wfs_result)

if st.button("Fetch GraphQL"):
    graphql_result = fetch_graphql(graphql_url, graphql_query)
    st.write(display_table(graphql_result))

if st.button("Fetch SPARQL"):
    sparql_query = st.text_area("SPARQL Query")
    sparql_result = fetch_sparql(sparql_url, sparql_query)
    st.write(display_table(sparql_result))

# Display results as map, chart, or table
if st.button("Display Map"):
    if 'latitude' in odata_result and 'longitude' in odata_result:
        map_data = pd.DataFrame(odata_result)
        st.write(display_map(map_data))

if st.button("Display Chart"):
    if 'category' in odata_result and 'value' in odata_result:
        chart_data = pd.DataFrame(odata_result)
        st.altair_chart(display_chart(chart_data))

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

# Copy the rest of the application code
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

# Write Dockerfile
with open("Dockerfile", "w") as f:
    f.write(dockerfile_content)

# Write requirements.txt
with open("requirements.txt", "w") as f:
    f.write(requirements_content)

st.success("Dockerfile and requirements.txt have been created.")