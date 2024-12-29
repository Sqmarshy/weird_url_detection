from flask import Flask, request, jsonify
from flask_cors import CORS
from classifying import run_modal

app = Flask(__name__)
CORS(app)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        url = data['url']        
        prediction = run_modal(url)
        result = {'prediction': 'Phishing' if prediction == 1 else 'Safe'}
        print((result))
        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/status', methods=['GET'])
def status():
    return jsonify({'status': 'Backend is running'}), 200

if __name__ == '__main__':
    app.run(debug=True)