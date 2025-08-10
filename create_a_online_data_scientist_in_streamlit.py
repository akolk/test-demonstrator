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

# Function to display data as a map
def display_map(data):
    m = folium.Map(location=[data['latitude'].mean(), data['longitude'].mean()], zoom_start=10)
    for _, row in data.iterrows():
        folium.Marker([row['latitude'], row['longitude']], popup=row['name']).add_to(m)
    return m

# Function to display data as a chart
def display_chart(data):
    chart = alt.Chart(data).mark_bar().encode(
        x='category:N',
        y='value:Q'
    )
    return chart

# Function to display data as a table
def display_table(data):
    return data

# Streamlit application
st.title("Online Data Scientist")

# Input for resource URL
resource_type = st.selectbox("Select Resource Type", ["OData", "WFS", "GraphQL", "SPARQL"])
resource_url = st.text_input("Enter Resource URL")

if resource_type == "GraphQL":
    query = st.text_area("Enter GraphQL Query")
else:
    query = ""

if st.button("Fetch Data"):
    if resource_type == "OData":
        data = fetch_odata(resource_url)
        df = pd.DataFrame(data)
    elif resource_type == "WFS":
        data = fetch_wfs(resource_url)
        st.write(data)  # WFS usually returns XML or GeoJSON
        df = pd.DataFrame()  # Placeholder for WFS data processing
    elif resource_type == "GraphQL":
        data = fetch_graphql(resource_url, query)
        df = pd.DataFrame(data['data'])  # Adjust according to the GraphQL response structure
    elif resource_type == "SPARQL":
        data = fetch_sparql(resource_url, query)
        df = pd.DataFrame(data['results']['bindings'])  # Adjust according to SPARQL response structure

    st.write("Data Fetched:")
    st.write(df)

    if not df.empty:
        if 'latitude' in df.columns and 'longitude' in df.columns:
            st.subheader("Map View")
            map_display = display_map(df)
            st_folium(map_display, width=700, height=500)
        else:
            st.subheader("Chart View")
            chart_display = display_chart(df)
            st.altair_chart(chart_display, use_container_width=True)

        st.subheader("Table View")
        table_display = display_table(df)
        st.write(table_display)

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
altair
"""

# Write Dockerfile and requirements.txt
with open("Dockerfile", "w") as f:
    f.write(dockerfile_content)

with open("requirements.txt", "w") as f:
    f.write(requirements_content)

if __name__ == "__main__":
    st.write("Run this app using Streamlit.")
```

This code creates a Streamlit application that can fetch and display data from various online resources, including OData, WFS, GraphQL, and SPARQL. It also generates a Dockerfile and a requirements.txt file for deployment.