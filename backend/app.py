from flask import Flask, request, jsonify
import joblib
import re

app = Flask(__name__)
model = joblib.load('phishing_model.pkl')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        url = data['url']        
        features = extract_features(url)
        prediction = model.predict([features])[0]
        result = {'prediction': 'Phishing' if prediction == 1 else 'Legitimate'}
        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/status', methods=['GET'])
def status():
    return jsonify({'status': 'Backend is running'}), 200

def extract_features(url):
    url_length = len(url)
    num_dots = url.count('.')
    has_https = 1 if 'https' in url else 0
    contains_ip = 1 if re.search(r'\d+\.\d+\.\d+\.\d+', url) else 0
    return [url_length, num_dots, has_https, contains_ip]

if __name__ == '__main__':
    app.run(debug=True)