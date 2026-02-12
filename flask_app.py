"""
Flask Backend for SMS Spam Detector
Serves HTML frontend and provides API endpoints for spam detection
"""

from flask import Flask, render_template, request, jsonify
import pickle
import string
from nltk.corpus import stopwords
import nltk
from nltk.stem.porter import PorterStemmer
import os

# Download required NLTK data if not already present
try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        print("⏳ Downloading required language data...")
        nltk.download('punkt_tab', quiet=True)
        nltk.download('punkt', quiet=True)

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    print("⏳ Downloading stopwords data...")
    nltk.download('stopwords', quiet=True)

app = Flask(__name__)
ps = PorterStemmer()

# Load models at startup
try:
    tfidf = pickle.load(open('vectorizer.pkl', 'rb'))
    model = pickle.load(open('model.pkl', 'rb'))
    print("✓ Models loaded successfully")
except FileNotFoundError:
    print("❌ Error: model.pkl or vectorizer.pkl not found!")
    raise


def transform_text(text):
    """Preprocess and transform text"""
    text = text.lower()
    text = nltk.word_tokenize(text)

    y = []
    for i in text:
        if i.isalnum():
            y.append(i)

    text = y[:]
    y.clear()

    for i in text:
        if i not in stopwords.words('english') and i not in string.punctuation:
            y.append(i)

    text = y[:]
    y.clear()

    for i in text:
        y.append(ps.stem(i))

    return " ".join(y)


@app.route('/')
def home():
    """Serve the main HTML page"""
    return render_template('index.html')


@app.route('/api/predict', methods=['POST'])
def predict():
    """
    API endpoint for spam prediction
    Expects JSON: {"message": "your message here"}
    Returns: {"prediction": "spam/ham", "confidence": 0.95, "message": "success"}
    """
    try:
        data = request.get_json()
        message = data.get('message', '').strip()

        if not message:
            return jsonify({
                'error': 'No message provided',
                'prediction': None,
                'confidence': None
            }), 400

        # Preprocess
        transformed_message = transform_text(message)

        # Vectorize
        vector_input = tfidf.transform([transformed_message])

        # Predict
        prediction = model.predict(vector_input)[0]

        # Get confidence
        try:
            confidence_array = model.predict_proba(vector_input)[0]
            confidence = float(max(confidence_array) * 100)
        except:
            confidence = None

        # Ensure prediction is converted to int/string for JSON serialization
        prediction_int = int(prediction)
        
        # Return result
        result = {
            'prediction': 'spam' if prediction_int == 1 else 'ham',
            'is_spam': bool(prediction_int == 1),
            'confidence': round(confidence, 2) if confidence else None,
            'message': 'success',
            'recommendation': (
                'Do not click any links or respond to this message. '
                'Consider reporting it to your carrier.'
            ) if prediction_int == 1 else (
                'This message is safe to read and respond to.'
            )
        }

        return jsonify(result), 200

    except Exception as e:
        return jsonify({
            'error': str(e),
            'prediction': None,
            'confidence': None
        }), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'SMS Spam Detector',
        'version': '1.0'
    }), 200


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)

    print("""
    ╔══════════════════════════════════════════╗
    ║   SMS Spam Detector - Flask Backend      ║
    ║   Starting server...                     ║
    ╚══════════════════════════════════════════╝
    """)

    # Run the Flask app
    app.run(
        debug=True,
        host='0.0.0.0',
        port=5000,
        use_reloader=True
    )
