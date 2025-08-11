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
    return data

# Main application
def main():
    st.title("Online Data Scientist")
    
    # Input for online resources
    resource_type = st.selectbox("Select Resource Type", ["OData", "WFS", "GraphQL", "SPARQL"])
    resource_url = st.text_input("Enter Resource URL")
    
    if resource_type == "GraphQL":
        query = st.text_area("Enter GraphQL Query")
    else:
        query = None

    if st.button("Fetch Data"):
        if resource_type == "OData":
            data = fetch_odata(resource_url)
            df = pd.DataFrame(data)
        elif resource_type == "WFS":
            data = fetch_wfs(resource_url)
            df = pd.DataFrame(data)  # Assuming data can be converted to DataFrame
        elif resource_type == "GraphQL":
            data = fetch_graphql(resource_url, query)
            df = pd.DataFrame(data['data'])  # Adjust based on actual response structure
        elif resource_type == "SPARQL":
            data = fetch_sparql(resource_url, query)
            df = pd.DataFrame(data['results']['bindings'])  # Adjust based on actual response structure

        st.write("Data Fetched:")
        st.write(display_table(df))

        if st.checkbox("Show Map"):
            st.write(display_map(df))
        
        if st.checkbox("Show Chart"):
            st.write(display_chart(df))

# Run the application
if __name__ == "__main__":
    main()
```

### Dockerfile
```dockerfile
# Use the official Python image from the Docker Hub
FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the port the app runs on
EXPOSE 8501

# Command to run the application
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### requirements.txt
```
streamlit
pandas
requests
folium
matplotlib
altair