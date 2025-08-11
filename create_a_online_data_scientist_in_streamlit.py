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

# Function to display data on a map
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
    ).interactive()
    return chart

# Function to display data as a table
def display_table(data):
    return pd.DataFrame(data)

# Streamlit application
st.title("Online Data Scientist")

# Input for data source
data_source = st.selectbox("Select Data Source", ["OData", "WFS", "GraphQL", "SPARQL"])
url = st.text_input("Enter URL")
query = st.text_area("Enter Query (if applicable)")

if st.button("Fetch Data"):
    if data_source == "OData":
        data = fetch_odata(url)
    elif data_source == "WFS":
        data = fetch_wfs(url)
    elif data_source == "GraphQL":
        data = fetch_graphql(url, query)
    elif data_source == "SPARQL":
        data = fetch_sparql(url, query)
    
    st.write("Data Fetched:")
    st.json(data)

    # Display options
    display_option = st.selectbox("Display As", ["Map", "Chart", "Table"])
    
    if display_option == "Map":
        if 'latitude' in data and 'longitude' in data:
            map_data = pd.DataFrame(data)
            st.write(display_map(map_data).get_root().render())
        else:
            st.error("Data must contain 'latitude' and 'longitude' for map display.")
    
    elif display_option == "Chart":
        chart_data = pd.DataFrame(data)
        st.altair_chart(display_chart(chart_data))
    
    elif display_option == "Table":
        table_data = pd.DataFrame(data)
        st.write(display_table(table_data))

# Dockerfile content
dockerfile_content = """
FROM python:3.9-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

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