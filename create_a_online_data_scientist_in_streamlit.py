import streamlit as st
import pandas as pd
import requests
import json
import folium
from streamlit_folium import folium_static

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
    folium_static(m)

# Function to display data as a chart
def display_chart(data):
    st.line_chart(data)

# Function to display data as a table
def display_table(data):
    st.write(data)

# Main application
def main():
    st.title("Online Data Scientist")

    resource_type = st.selectbox("Select Resource Type", ["OData", "WFS", "GraphQL", "SPARQL"])
    
    if resource_type == "OData":
        url = st.text_input("Enter OData URL")
        if st.button("Fetch Data"):
            data = fetch_odata(url)
            df = pd.DataFrame(data)
            display_table(df)

    elif resource_type == "WFS":
        url = st.text_input("Enter WFS URL")
        if st.button("Fetch Data"):
            data = fetch_wfs(url)
            st.write(data)

    elif resource_type == "GraphQL":
        url = st.text_input("Enter GraphQL URL")
        query = st.text_area("Enter GraphQL Query")
        if st.button("Fetch Data"):
            data = fetch_graphql(url, query)
            df = pd.DataFrame(data['data'])
            display_table(df)

    elif resource_type == "SPARQL":
        endpoint = st.text_input("Enter SPARQL Endpoint")
        query = st.text_area("Enter SPARQL Query")
        if st.button("Fetch Data"):
            data = fetch_sparql(endpoint, query)
            df = pd.DataFrame(data['results']['bindings'])
            display_table(df)

    # Placeholder for MCP server connection and chatbot input
    mcp_input = st.text_input("Enter input for MCP server")
    if st.button("Send to MCP"):
        # Simulate MCP server response
        st.write(f"Response from MCP for input '{mcp_input}': [Simulated Response]")

if __name__ == "__main__":
    main()
```

### Dockerfile
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

### requirements.txt
```
streamlit
pandas
requests
folium
streamlit-folium