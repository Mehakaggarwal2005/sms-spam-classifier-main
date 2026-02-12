"""
SMS Spam Classifier - Model Training Script
Trains the spam detection model from spam.csv and saves model.pkl & vectorizer.pkl
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import pickle
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import warnings

warnings.filterwarnings('ignore')

# Download required NLTK data
print("📚 Downloading NLTK data...")
try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('punkt_tab', quiet=True)
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)

print("✅ NLTK data ready\n")

# Initialize
ps = PorterStemmer()
stop_words = set(stopwords.words('english'))

print("📖 Loading spam.csv...")
df = pd.read_csv('spam.csv', encoding='latin-1')

# Display dataset info
print(f"Dataset loaded: {len(df)} messages")
print(f"Columns: {df.columns.tolist()}")

# Get the correct columns
if 'v1' in df.columns and 'v2' in df.columns:
    df = df[['v1', 'v2']]
    df.columns = ['label', 'text']
elif 'Label' in df.columns and 'Message' in df.columns:
    df = df[['Label', 'Message']]
    df.columns = ['label', 'text']
elif 'label' in df.columns and 'text' in df.columns:
    pass  # Already correct
else:
    print("⚠️  Column names not recognized. Using first two columns...")
    df.columns = ['label', 'text']

print(f"✅ Using columns: label & text")
print(f"   Labels: {df['label'].unique()}")
print()

# Text preprocessing function
def preprocess_text(text):
    """Preprocess and clean text"""
    # Convert to lowercase
    text = str(text).lower()
    
    # Tokenize
    tokens = nltk.word_tokenize(text)
    
    # Remove non-alphanumeric characters
    tokens = [token for token in tokens if token.isalnum()]
    
    # Remove stopwords and punctuation
    tokens = [token for token in tokens if token not in stop_words and token not in string.punctuation]
    
    # Stemming
    tokens = [ps.stem(token) for token in tokens]
    
    return ' '.join(tokens)

print("🔄 Preprocessing text...")
df['processed_text'] = df['text'].apply(preprocess_text)
print("✅ Text preprocessed\n")

# Convert labels to numeric
df['label_encoded'] = (df['label'] == 'spam').astype(int)

print(f"Label distribution:")
print(f"  Spam:     {(df['label_encoded'] == 1).sum()} messages")
print(f"  Legitimate: {(df['label_encoded'] == 0).sum()} messages")
print()

# Split data
print("📊 Splitting data (80-20)...")
X_train, X_test, y_train, y_test = train_test_split(
    df['processed_text'],
    df['label_encoded'],
    test_size=0.2,
    random_state=42,
    stratify=df['label_encoded']
)
print(f"✅ Training set: {len(X_train)}, Test set: {len(X_test)}\n")

# Vectorization
print("🔢 Creating TF-IDF vectorizer...")
vectorizer = TfidfVectorizer(max_features=3000)
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)
print(f"✅ Vectorizer created ({len(vectorizer.get_feature_names_out())} features)\n")

# Train model
print("🤖 Training Naive Bayes classifier...")
model = MultinomialNB()
model.fit(X_train_vec, y_train)
print("✅ Model trained\n")

# Evaluate
print("📈 Evaluating model...")
y_pred = model.predict(X_test_vec)

accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)

print(f"Accuracy:  {accuracy:.4f} ({accuracy*100:.2f}%)")
print(f"Precision: {precision:.4f}")
print(f"Recall:    {recall:.4f}")
print(f"F1 Score:  {f1:.4f}")
print()

# Confusion Matrix
cm = confusion_matrix(y_test, y_pred)
print("Confusion Matrix:")
print(f"  True Negatives:  {cm[0][0]}")
print(f"  False Positives: {cm[0][1]}")
print(f"  False Negatives: {cm[1][0]}")
print(f"  True Positives:  {cm[1][1]}")
print()

# Save models
print("💾 Saving models...")
pickle.dump(vectorizer, open('vectorizer.pkl', 'wb'))
pickle.dump(model, open('model.pkl', 'wb'))
print("✅ Models saved successfully!")
print()

print("=" * 60)
print("✅ TRAINING COMPLETE!")
print("=" * 60)
print()
print("Model files saved:")
print("  ✓ vectorizer.pkl - TF-IDF vectorizer")
print("  ✓ model.pkl - Trained Naive Bayes model")
print()
print("You can now use these files with:")
print("  • app.py (Streamlit)")
print("  • flask_app.py (Flask)")
print()
print("Next steps:")
print("  1. Run: streamlit run app.py")
print("  2. Or: python flask_app.py")
print()
