from flask import Flask, jsonify
import pandas as pd
import geopandas as gpd

app = Flask(__name__)

# Sample dataframes
# In a real application, you would load your data from files or a database

df1 = pd.DataFrame({'id': [1, 2], 'name': ['A', 'B'], 'value': [10.5, 20.3]})
df2 = gpd.GeoDataFrame({'id': [1, 2], 'geometry': [None, None]})

dataframes = {'df1': df1, 'df2': df2}

@app.route('/dataframes', methods=['GET'])
def get_dataframes():
    result = []
    for name, df in dataframes.items():
        result.append({'id': name, 'columns': df.columns.tolist()})
    return jsonify(result)

@app.route('/dataframe/<name>/columns', methods=['GET'])
def get_dataframe_columns(name):
    df = dataframes.get(name)
    if df is not None:
        columns_info = {col: str(df[col].dtype) for col in df.columns}
        return jsonify(columns_info)
    return jsonify({'error': 'DataFrame not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)