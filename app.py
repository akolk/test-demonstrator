from flask import Flask, jsonify
import pandas as pd
import geopandas as gpd

app = Flask(__name__)

# Sample dataframes
# Replace these with actual data loading logic

# Sample DataFrame 1

# Sample DataFrame 2

df1 = pd.DataFrame({
    'id': [1, 2, 3],
    'name': ['Alice', 'Bob', 'Charlie'],
    'age': [25, 30, 35]
})

df2 = gpd.GeoDataFrame({
    'id': [1, 2],
    'location': ['Point(1 1)', 'Point(2 2)'],
    'value': [100, 200]
})

dataframes = {
    'df1': df1,
    'df2': df2
}

@app.route('/dataframes', methods=['GET'])
def get_dataframes():
    result = []
    for key, df in dataframes.items():
        result.append({
            'id': key,
            'columns': df.columns.tolist()
        })
    return jsonify(result)

@app.route('/dataframes/<df_id>/columns', methods=['GET'])
def get_dataframe_columns(df_id):
    if df_id in dataframes:
        df = dataframes[df_id]
        types = {col: str(df[col].dtype) for col in df.columns}
        return jsonify(types)
    return jsonify({'error': 'DataFrame not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)