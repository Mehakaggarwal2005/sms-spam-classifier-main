import streamlit as st
import pickle
import string
from nltk.corpus import stopwords
import nltk
from nltk.stem.porter import PorterStemmer
import numpy as np
import os

# Download required NLTK data if not already present
try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        with st.spinner('Downloading required language data...'):
            nltk.download('punkt_tab', quiet=True)
            nltk.download('punkt', quiet=True)

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    with st.spinner('Downloading stopwords data...'):
        nltk.download('stopwords', quiet=True)

# Page configuration
st.set_page_config(
    page_title="SMS Spam Detector",
    page_icon="📨",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stTextArea textarea {
        font-size: 16px;
    }
    .result-spam {
        padding: 20px;
        border-radius: 10px;
        background-color: #ff6b6b;
        color: white;
        text-align: center;
        font-size: 24px;
        font-weight: bold;
        margin: 20px 0;
    }
    .result-ham {
        padding: 20px;
        border-radius: 10px;
        background-color: #51cf66;
        color: white;
        text-align: center;
        font-size: 24px;
        font-weight: bold;
        margin: 20px 0;
    }
    </style>
""", unsafe_allow_html=True)

ps = PorterStemmer()

@st.cache_resource
def load_models():
    """Load and cache the model and vectorizer"""
    tfidf = pickle.load(open('vectorizer.pkl','rb'))
    model = pickle.load(open('model.pkl','rb'))
    return tfidf, model

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

# Load models
tfidf, model = load_models()

# Header
st.markdown("# 📨 SMS Spam Detector")
st.markdown("*Powered by Machine Learning | Detect spam messages instantly*")
st.markdown("---")

# Two column layout
col1, col2 = st.columns([2, 1], gap="large")

with col1:
    st.subheader("🔍 Check Your Message")
    input_sms = st.text_area(
        "Paste or type your SMS message here:",
        placeholder="Enter the message you want to check...",
        height=150,
        label_visibility="collapsed"
    )

with col2:
    st.subheader("📚 Quick Tips")
    st.info("""
    **Spam Messages Often Contain:**
    - Urgent requests
    - Links and URLs
    - Special offers
    - Free prizes/money
    - Requests for personal info
    """)

st.markdown("---")

# Check button
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    check_button = st.button('🚀 Check Message', use_container_width=True, type="primary")

if check_button:
    if not input_sms.strip():
        st.warning("⚠️ Please enter a message to check!")
    else:
        with st.spinner('Analyzing message...'):
            # 1. preprocess
            transformed_sms = transform_text(input_sms)
            # 2. vectorize
            vector_input = tfidf.transform([transformed_sms])
            # 3. predict
            result = model.predict(vector_input)[0]
            
            # Get confidence score if available
            try:
                confidence = model.predict_proba(vector_input)[0]
                confidence_score = max(confidence) * 100
            except:
                confidence_score = None
        
        st.markdown("---")
        st.markdown("### 📊 Result")
        
        # 4. Display with enhanced styling
        if result == 1:
            st.markdown('<div class="result-spam">🚨 SPAM DETECTED</div>', unsafe_allow_html=True)
            st.error("⚠️ This message appears to be **SPAM**")
            if confidence_score:
                st.metric("Confidence Level", f"{confidence_score:.1f}%", delta="High Risk")
            st.warning("**Recommendation:** Do not click any links or respond to this message. Consider reporting it to your carrier.")
        else:
            st.markdown('<div class="result-ham">✅ LEGITIMATE MESSAGE</div>', unsafe_allow_html=True)
            st.success("✓ This message appears to be **LEGITIMATE**")
            if confidence_score:
                st.metric("Confidence Level", f"{confidence_score:.1f}%", delta="Safe")

# Footer with example messages
with st.expander("📝 Try Example Messages"):
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Example Spam Messages:")
        spam_examples = [
            "Congratulations! You won a FREE iPhone. Click here: bit.ly/winner",
            "URGENT: Your account has been suspended. Verify now: malicious-site.com",
            "Claim your FREE £50 voucher NOW! Limited offer!"
        ]
        for example in spam_examples:
            if st.button(f"Try: {example[:40]}...", key=f"spam_{example}"):
                st.session_state.example_input = example
    
    with col2:
        st.subheader("Example Legitimate Messages:")
        ham_examples = [
            "Hi, are you available for lunch tomorrow?",
            "Your package has been delivered. Thank you for shopping!",
            "Meeting is scheduled for 2 PM. See you then!"
        ]
        for example in ham_examples:
            if st.button(f"Try: {example[:40]}...", key=f"ham_{example}"):
                st.session_state.example_input = example

# Sidebar information
with st.sidebar:
    st.markdown("## 📌 About This App")
    st.info("""
    This SMS Spam Detector uses **Machine Learning** to classify messages as spam or legitimate.
    
    **How it works:**
    1. Your message is preprocessed and cleaned
    2. Text is converted into numerical features
    3. Our trained model analyzes the features
    4. Result is displayed instantly
    
    **Accuracy:** State-of-the-art classification model
    **Privacy:** Messages are NOT stored or logged
    """)
    
    st.markdown("## ⚙️ Technical Details")
    st.markdown("""
    - **Model Type:** Machine Learning Classifier
    - **Vectorization:** TF-IDF
    - **Text Processing:** NLTK
    - **Framework:** Streamlit
    """)
    
    st.markdown("---")
    st.markdown("*Made with ❤️ for spam detection*")
