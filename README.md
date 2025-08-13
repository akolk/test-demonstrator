# DataFrame API

This is a simple backend application built with Flask that serves data from Pandas and GeoPandas DataFrames.

## Structure
- `app.py`: The main application file containing the Flask API.
- `requirements.txt`: Lists the required Python packages.
- `Dockerfile`: Contains instructions to build a Docker image for the application.

## How It Works
1. The application initializes with sample DataFrames.
2. It provides an API endpoint `/dataframes` to list all available DataFrames with their IDs and column names.
3. Another endpoint `/dataframes/<df_id>/columns` allows fetching the data types of the columns in a specified DataFrame.

## Running the Application
1. Build the Docker image:
   ```bash
   docker build -t dataframe-api .
   ```
2. Run the Docker container:
   ```bash
   docker run -p 5000:5000 dataframe-api
   ```
3. Access the API at `http://localhost:5000/dataframes` to see the list of DataFrames.