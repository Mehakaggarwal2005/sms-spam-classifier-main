# 🚀 SMS Spam Detector - Setup & Usage Guide

## Overview

Your SMS Spam Detector project now has **3 frontend options**:

1. **Streamlit** (Recommended) - Modern, interactive UI
2. **Flask** - Traditional web application with custom UI
3. **HTML/CSS** - Standalone frontend

---

## Option 1: Streamlit (⭐ Recommended)

### Why Streamlit?
- ✅ Easiest to set up and deploy
- ✅ Modern, responsive UI
- ✅ Great for data science projects
- ✅ Built-in caching for performance
- ✅ Real-time updates and feedback

### Installation & Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   python -m nltk.downloader punkt stopwords
   ```

2. **Run the application:**
   ```bash
   streamlit run app.py
   ```

3. **Access the app:**
   - Browser will auto-open at `http://localhost:8501`
   - If not, navigate to that URL manually

### Features
- 📨 Clean, professional interface
- 🎯 Real-time spam detection
- 📊 Confidence score display
- 📚 Example messages to try
- 💡 Tips for identifying spam
- 👁️ Responsive design

### Streamlit Commands
```bash
# Run the app
streamlit run app.py

# Run with custom port
streamlit run app.py --server.port 8502

# Run in headless mode (no browser)
streamlit run app.py --logger.level=debug --client.showErrorDetails=True
```

---

## Option 2: Flask Web Application

### Why Flask?
- ✅ Traditional web framework
- ✅ Custom HTML/CSS design
- ✅ RESTful API for integrations
- ✅ Better for production deployments
- ✅ Flexible and scalable

### Installation & Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   python -m nltk.downloader punkt stopwords
   ```

2. **Run the Flask application:**
   ```bash
   python flask_app.py
   ```

3. **Access the app:**
   - Open browser at `http://localhost:5000`
   - Server runs on `0.0.0.0:5000`

### Project Structure
```
templates/
├── index.html          # Flask HTML template
flask_app.py           # Flask backend with API
```

### API Endpoints

#### POST `/api/predict`
Predict if a message is spam

**Request:**
```json
{
  "message": "Your SMS message here"
}
```

**Response (Success):**
```json
{
  "prediction": "spam",
  "is_spam": true,
  "confidence": 92.45,
  "recommendation": "Do not click any links...",
  "message": "success"
}
```

**Response (Error):**
```json
{
  "error": "No message provided",
  "prediction": null,
  "confidence": null
}
```

#### GET `/api/health`
Health check endpoint

**Response:**
```json
{
  "status": "healthy",
  "service": "SMS Spam Detector",
  "version": "1.0"
}
```

### Flask Commands
```bash
# Run development server
python flask_app.py

# Run with specific port
python -c "from flask_app import app; app.run(port=5001)"

# Run in production mode
python -c "from flask_app import app; app.run(debug=False)"
```

---

## Option 3: Standalone HTML Frontend

### Why HTML?
- ✅ Lightest weight option
- ✅ No server required (can run locally)
- ✅ Great for testing UI/UX
- ✅ Easy to customize styling
- ✅ Works in any browser

### Setup

1. **Open the file:**
   - Double-click `index.html` in file explorer
   - Or right-click → Open with → Browser

2. **Features:**
   - ✅ Sample messages to try
   - ✅ Beautiful gradient design
   - ✅ Interactive buttons
   - ✅ Example spam/legitimate messages

⚠️ **Note:** The standalone HTML file doesn't connect to your model backend. 
To connect it, use the Flask option (Flask serves this same HTML file with API integration).

---

## Comparison Table

| Feature | Streamlit | Flask | HTML |
|---------|-----------|-------|------|
| **Setup Difficulty** | ⭐ Easy | ⭐⭐ Medium | ⭐ Easy|
| **Model Integration** | ✅ Built-in | ✅ API | ❌ No |
| **Customization** | Medium | ✅ High | ✅ Very High |
| **Performance** | ✅ Good | ✅ Excellent | ⭐⭐⭐ Fastest |
| **Deployment** | ✅ Very Easy | Easy | Very Easy |
| **API Endpoints** | Limited | ✅ Full REST API | N/A |
| **Mobile Friendly** | ✅ Yes | ✅ Yes | ✅ Yes |

**Recommendation:** Start with **Streamlit** for the best experience!

---

## Troubleshooting

### Common Issues

#### ⚠️ "model.pkl not found" error
**Solution:** Make sure `model.pkl` and `vectorizer.pkl` are in the same directory as your app files.

#### ⚠️ NLTK data errors
**Solution:** Run these commands:
```bash
python -m nltk.downloader punkt stopwords
```

#### ⚠️ Port already in use
**Streamlit:**
```bash
streamlit run app.py --server.port 8502
```

**Flask:**
```bash
python -c "from flask_app import app; app.run(port=5001)"
```

#### ⚠️ Module not found (nltk, sklearn, etc.)
**Solution:** Reinstall dependencies:
```bash
pip install --upgrade -r requirements.txt
```

#### ⚠️ Permission denied on Unix/Mac
**Solution:**
```bash
chmod +x app.py flask_app.py
python app.py  # or python flask_app.py
```

---

## Advanced Usage

### Running Multiple Instances

#### Streamlit + Flask (Simultaneously)
```bash
# Terminal 1 - Streamlit
streamlit run app.py --server.port 8501

# Terminal 2 - Flask (in a new terminal)
python flask_app.py --port 5000
```

### Deployment Options

#### Deploy Streamlit to Streamlit Cloud
1. Push code to GitHub
2. Go to https://streamlit.io/cloud
3. Click "New app" and select your repo
4. Done! App is live

#### Deploy Flask to Heroku
```bash
# Create Procfile (already included)
git push heroku main
```

#### Deploy Flask to Azure
```bash
# Using Azure CLI
az webapp up --name spam-detector --runtime python
```

#### Deploy with Docker
```bash
# Build image
docker build -t sms-spam-detector .

# Run container
docker run -p 8501:8501 sms-spam-detector  # Streamlit
docker run -p 5000:5000 sms-spam-detector  # Flask
```

---

## Performance Tips

### Streamlit Optimization
1. **Use `@st.cache_resource` for model loading** ✅ (Already done)
2. **Minimize widget creation in loops**
3. **Use `st.session_state` for data persistence**

### Flask Optimization
1. **Enable gzip compression** - Add to Flask app
2. **Use connection pooling** - For databases
3. **Cache predictions** - For identical messages
4. **Use gunicorn in production** - `pip install gunicorn`

### General Tips
1. ✅ Models are pre-loaded and cached
2. ✅ Predictions are fast (< 100ms)
3. ✅ NLTK data is downloaded once
4. ✅ No database queries needed

---

## API Integration Examples

### Python
```python
import requests

response = requests.post('http://localhost:5000/api/predict', 
    json={'message': 'Your SMS here'})
result = response.json()
print(result['prediction'])  # 'spam' or 'ham'
print(result['confidence'])  # 92.45
```

### JavaScript/Node.js
```javascript
const response = await fetch('/api/predict', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({message: 'Your SMS here'})
});
const data = await response.json();
console.log(data.prediction);  // 'spam' or 'ham'
```

### cURL
```bash
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{"message": "Your SMS here"}'
```

---

## Next Steps

1. ✅ **Try the app** - Run one of the three options
2. ✅ **Test with examples** - Use provided sample messages
3. ✅ **Fine-tune the model** - Retrain with more data if needed
4. ✅ **Deploy** - Choose deployment platform
5. ✅ **Share** - Get feedback from users

---

## Questions or Issues?

Check the main README.md for more information about the project, model details, and additional resources.

**Happy spam detecting! 🚀📨**
