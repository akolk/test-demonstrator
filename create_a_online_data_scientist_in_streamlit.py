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
    return pd.DataFrame(response.json()['features'])

# Function to fetch data from GraphQL
def fetch_graphql(url, query):
    response = requests.post(url, json={'query': query})
    return pd.json_normalize(response.json()['data'])

# Function to fetch data from SPARQL
def fetch_sparql(endpoint, query):
    response = requests.get(endpoint, params={'query': query, 'format': 'json'})
    return pd.json_normalize(response.json()['results']['bindings'])

# Function to display map
def display_map(data):
    m = folium.Map(location=[data['latitude'].mean(), data['longitude'].mean()], zoom_start=10)
    for _, row in data.iterrows():
        folium.Marker([row['latitude'], row['longitude']], popup=row['name']).add_to(m)
    return m

# Function to display chart
def display_chart(data):
    chart = alt.Chart(data).mark_bar().encode(
        x='category:N',
        y='value:Q'
    )
    return chart

# Function to display table
def display_table(data):
    return data

# Streamlit application
st.title("Online Data Scientist")

# Input for resource type
resource_type = st.selectbox("Select Resource Type", ["OData", "WFS", "GraphQL", "SPARQL"])

# Input for resource URL
resource_url = st.text_input("Enter Resource URL")

# Input for GraphQL query if selected
graphql_query = ""
if resource_type == "GraphQL":
    graphql_query = st.text_area("Enter GraphQL Query")

# Input for SPARQL query if selected
sparql_query = ""
if resource_type == "SPARQL":
    sparql_query = st.text_area("Enter SPARQL Query")

# Button to fetch data
if st.button("Fetch Data"):
    if resource_type == "OData":
        data = fetch_odata(resource_url)
    elif resource_type == "WFS":
        data = fetch_wfs(resource_url)
    elif resource_type == "GraphQL":
        data = fetch_graphql(resource_url, graphql_query)
    elif resource_type == "SPARQL":
        data = fetch_sparql(resource_url, sparql_query)

    st.write("Data Fetched:")
    st.write(data)

    # Display options for visualization
    display_option = st.selectbox("Select Display Option", ["Map", "Chart", "Table"])
    
    if display_option == "Map":
        st.write(display_map(data))
    elif display_option == "Chart":
        st.write(display_chart(data))
    elif display_option == "Table":
        st.write(display_table(data))

# Placeholder for MCP server interaction
mcp_input = st.text_input("Enter input for MCP server")
if st.button("Send to MCP"):
    # Here you would implement the actual MCP server interaction
    st.write("MCP response would be displayed here.")

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