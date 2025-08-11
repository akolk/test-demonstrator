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
    ).interactive()
    return chart

# Function to display data as a table
def display_table(data):
    return pd.DataFrame(data)

# Main application
st.title("Online Data Scientist")

# Input for data source
data_source = st.selectbox("Select Data Source", ["OData", "WFS", "GraphQL", "SPARQL"])
url = st.text_input("Enter the URL for the data source")

if data_source == "OData":
    if st.button("Fetch OData"):
        data = fetch_odata(url)
        st.write(data)

elif data_source == "WFS":
    if st.button("Fetch WFS"):
        data = fetch_wfs(url)
        st.write(data)

elif data_source == "GraphQL":
    query = st.text_area("Enter GraphQL Query")
    if st.button("Fetch GraphQL"):
        data = fetch_graphql(url, query)
        st.write(data)

elif data_source == "SPARQL":
    query = st.text_area("Enter SPARQL Query")
    if st.button("Fetch SPARQL"):
        data = fetch_sparql(url, query)
        st.write(data)

# Display options
if st.button("Display as Map"):
    if 'latitude' in data and 'longitude' in data:
        map_display = display_map(pd.DataFrame(data))
        st.write(map_display)

if st.button("Display as Chart"):
    chart_display = display_chart(pd.DataFrame(data))
    st.altair_chart(chart_display)

if st.button("Display as Table"):
    table_display = display_table(data)
    st.write(table_display)

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

# Save Dockerfile and requirements.txt
with open("Dockerfile", "w") as f:
    f.write(dockerfile_content)

with open("requirements.txt", "w") as f:
    f.write(requirements_content)

st.success("Dockerfile and requirements.txt created successfully.")