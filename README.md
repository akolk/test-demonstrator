# DataFrame Viewer

This application consists of a backend built with Flask and a frontend built with Angular. The backend serves data stored in Pandas and GeoPandas DataFrames, while the frontend displays this data.

## Backend
- The backend is implemented using Flask.
- It exposes two API endpoints:
  - `/dataframes`: Returns a list of available DataFrames with their IDs and column names.
  - `/dataframe/<df_id>/columns`: Returns the data types of the columns in the specified DataFrame.

## Frontend
- The frontend is built using Angular.
- It fetches the list of DataFrames from the backend and displays them in a simple list format.

## Running the Application
1. Build and run the backend:
   ```bash
   docker build -t dataframe-viewer-backend .
   docker run -p 5000:5000 dataframe-viewer-backend
   ```
2. Navigate to the frontend directory and run:
   ```bash
   npm install
   ng serve
   ```
3. Open your browser and go to `http://localhost:4200` to view the application.