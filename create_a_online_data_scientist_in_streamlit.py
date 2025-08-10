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

# Main application
def main():
    st.title("Online Data Scientist")

    resource_type = st.selectbox("Select Resource Type", ["OData", "WFS", "GraphQL", "SPARQL"])
    url = st.text_input("Enter the URL of the resource")
    
    if resource_type == "OData":
        data = fetch_odata(url)
    elif resource_type == "WFS":
        data = fetch_wfs(url)
    elif resource_type == "GraphQL":
        query = st.text_area("Enter GraphQL query")
        data = fetch_graphql(url, query)
    elif resource_type == "SPARQL":
        query = st.text_area("Enter SPARQL query")
        data = fetch_sparql(url, query)

    if 'data' in locals():
        display_option = st.selectbox("Select Display Option", ["Map", "Chart", "Table"])
        if display_option == "Map":
            display_map(data)
        elif display_option == "Chart":
            display_chart(data)
        elif display_option == "Table":
            display_table(data)

if __name__ == "__main__":
    main()
```

**Dockerfile**
```dockerfile
# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file into the container
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