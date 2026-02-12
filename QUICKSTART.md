# ⚡ Quick Start Guide

## 30-Second Setup

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
python -m nltk.downloader punkt stopwords
```

### Step 2: Choose Your Frontend & Run

#### 🌟 Option A: Streamlit (Recommended)
```bash
streamlit run app.py
```
✅ Opens automatically in your browser at http://localhost:8501

#### Option B: Flask
```bash
python flask_app.py
```
✅ Open browser at http://localhost:5000

#### Option C: HTML Standalone
✅ Double-click `index.html` to open in browser

---

## That's It! 🎉

Your SMS Spam Detector is now running!

### Try These:
- **Test Message:** "Congratulations! You won FREE money. Click here http://bit.ly/winner"
- **Expected Result:** SPAM (red alert)

- **Test Message:** "Hi, are you free for lunch tomorrow?"
- **Expected Result:** Legitimate (green checkmark)

---

## File Structure

```
├── app.py                    # Streamlit app ⭐ Use this!
├── flask_app.py             # Flask alternative
├── templates/
│   └── index.html          # Web UI (for Flask)
├── index.html              # Standalone version
├── model.pkl               # Your trained model
├── vectorizer.pkl          # TF-IDF vectorizer
├── requirements.txt        # Dependencies
├── README.md               # Full documentation
├── SETUP_GUIDE.md          # Detailed setup
└── spam.csv               # Training data
```

---

## Common Commands

```bash
# Install all dependencies
pip install -r requirements.txt

# Download NLTK data (required once)
python -m nltk.downloader punkt stopwords

# Run Streamlit (recommended)
streamlit run app.py

# Run Flask
python flask_app.py

# Run on different port
streamlit run app.py --server.port 8502
```

---

## Features Your Users Get

✅ **Simple Interface** - Just paste SMS and click "Check"
✅ **Instant Results** - Predictions in < 1 second
✅ **Confidence Scores** - Shows how sure the model is
✅ **Example Messages** - Try pre-made spam/legitimate examples
✅ **Visual Feedback** - Red for spam, green for legitimate
✅ **Tips & Guidance** - Learn what makes a message spam
✅ **Mobile Friendly** - Works on phones and tablets

---

## Deploy Your App

### Free Option: Streamlit Cloud ⭐
1. Push your repo to GitHub
2. Go to https://streamlit.io/cloud
3. Click "Deploy" and select your repo
4. ✅ Your app is live!

### Other Options:
- **Heroku** (Flask) - Procfile already included
- **Azure** - Just push with Azure CLI
- **Docker** - Using your model.pkl and vectorizer.pkl

---

## Next: Read the Detailed Guides

- 📖 **README.md** - Full project documentation
- 📖 **SETUP_GUIDE.md** - Comprehensive setup & troubleshooting
- 📖 **DEPLOYMENT.md** - How to deploy to servers/cloud

---

## Need Help?

1. Check **SETUP_GUIDE.md** for troubleshooting
2. Ensure `model.pkl` and `vectorizer.pkl` exist
3. Run NLTK downloader: `python -m nltk.downloader punkt stopwords`
4. Try a different port if getting "address already in use"

---

**You're all set! Enjoy your SMS Spam Detector! 🚀📨**
