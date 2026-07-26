from flask import Flask, request, jsonify
import joblib, json, os

app = Flask(__name__)

with open('model_metadata.json', 'r') as f:
    metadata = json.load(f)

LATEST_VERSION = list(metadata['versions'].keys())[-1]
latest_model = joblib.load(metadata['versions'][LATEST_VERSION]['joblib_file'])

@app.route('/models', methods=['GET'])
def get_models():
    return jsonify(metadata)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()

    if 'features' not in data:
        return jsonify({'error': "Request body must contain a 'features' key"}), 400

    features = data['features']  

    try:
        preds = latest_model.predict(features)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

    return jsonify({
        'model_version': LATEST_VERSION,
        'predictions': preds.tolist()
    })


if __name__ == '__main__':
    app.run(debug=True, port=5000)