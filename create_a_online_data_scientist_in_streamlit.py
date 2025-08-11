import streamlit as st
import pandas as pd
import requests
import json
import folium
import altair as alt

# Function to fetch data from OData
def fetch_odata(url):
    response = requests.get(url)
    return pd.DataFrame(response.json()['value'])

# Function to fetch data from WFS
def fetch_wfs(url):
    response = requests.get(url)
    return pd.read_xml(response.content)

# Function to fetch data from GraphQL
def fetch_graphql(url, query):
    response = requests.post(url, json={'query': query})
    return pd.json_normalize(response.json()['data'])

# Function to fetch data from SPARQL
def fetch_sparql(endpoint, query):
    response = requests.get(endpoint, params={'query': query, 'format': 'json'})
    return pd.json_normalize(response.json()['results']['bindings'])

# Function to display data as a map
def display_map(data):
    m = folium.Map(location=[data['latitude'].mean(), data['longitude'].mean()], zoom_start=10)
    for _, row in data.iterrows():
        folium.Marker([row['latitude'], row['longitude']], popup=row['name']).add_to(m)
    st.write(m)

# Function to display data as a chart
def display_chart(data):
    chart = alt.Chart(data).mark_bar().encode(
        x='category:N',
        y='value:Q'
    )
    st.altair_chart(chart)

# Function to display data as a table
def display_table(data):
    st.write(data)

# Main Streamlit application
def main():
    st.title("Online Data Scientist")
    
    resource_type = st.selectbox("Select Resource Type", ["OData", "WFS", "GraphQL", "SPARQL"])
    
    if resource_type == "OData":
        url = st.text_input("Enter OData URL")
        if st.button("Fetch Data"):
            data = fetch_odata(url)
            st.write(data)
            display_map(data)
    
    elif resource_type == "WFS":
        url = st.text_input("Enter WFS URL")
        if st.button("Fetch Data"):
            data = fetch_wfs(url)
            st.write(data)
            display_map(data)
    
    elif resource_type == "GraphQL":
        url = st.text_input("Enter GraphQL URL")
        query = st.text_area("Enter GraphQL Query")
        if st.button("Fetch Data"):
            data = fetch_graphql(url, query)
            st.write(data)
            display_chart(data)
    
    elif resource_type == "SPARQL":
        endpoint = st.text_input("Enter SPARQL Endpoint")
        query = st.text_area("Enter SPARQL Query")
        if st.button("Fetch Data"):
            data = fetch_sparql(endpoint, query)
            st.write(data)
            display_table(data)

if __name__ == "__main__":
    main()
```

**Dockerfile**
```
# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Command to run the application
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

**requirements.txt**
```
streamlit
pandas
requests
folium
altair