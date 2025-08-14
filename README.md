# Backend Application

This is a simple backend application built with Flask that serves data stored in Pandas and GeoPandas DataFrames. The application exposes APIs to interact with the data, allowing an Angular frontend to query the available DataFrames and their columns.

## Structure
- `app.py`: The main application file containing the Flask API.
- `requirements.txt`: Lists the dependencies required to run the application.
- `Dockerfile`: Contains instructions to build a Docker image for the application.

## How It Works
1. The application initializes with sample data stored in Pandas and GeoPandas DataFrames.
2. It exposes two API endpoints:
   - `GET /dataframes`: Returns a list of available DataFrames with their IDs and column names.
   - `GET /dataframe/<name>/columns`: Returns the data types of the columns for the specified DataFrame.
3. The Angular frontend can call these endpoints to retrieve and display the data.

## Running the Application
1. Build the Docker image:
   ```bash
   docker build -t my-backend-app .
   ```
2. Run the Docker container:
   ```bash
   docker run -p 5000:5000 my-backend-app
   ```
3. Access the API at `http://localhost:5000`.