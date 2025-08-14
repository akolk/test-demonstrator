from flask import Flask, jsonify
from flask_cors import CORS
import pandas as pd
import geopandas as gpd

app = Flask(__name__)
CORS(app)

# Sample DataFrames
# Replace with actual data loading logic
sample_df1 = pd.DataFrame({'id': [1, 2], 'name': ['A', 'B'], 'value': [10.5, 20.3]})
sample_df2 = gpd.GeoDataFrame({'id': [1, 2], 'geometry': [None, None]})

dataframes = {
    'df1': sample_df1,
    'df2': sample_df2
}

@app.route('/dataframes', methods=['GET'])
def get_dataframes():
    df_info = []
    for df_id, df in dataframes.items():
        df_info.append({'id': df_id, 'columns': df.columns.tolist()})
    return jsonify(df_info)

@app.route('/dataframe/<df_id>/columns', methods=['GET'])
def get_dataframe_columns(df_id):
    if df_id in dataframes:
        df = dataframes[df_id]
        column_types = {col: str(df[col].dtype) for col in df.columns}
        return jsonify(column_types)
    return jsonify({'error': 'DataFrame not found'}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)