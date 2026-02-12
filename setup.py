"""
Setup Script for SMS Spam Detector
Ensures all dependencies and data are properly installed
"""

import sys
import subprocess

def install_dependencies():
    """Install Python packages from requirements.txt"""
    print("📦 Installing Python dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully!\n")
        return True
    except Exception as e:
        print(f"❌ Error installing dependencies: {e}\n")
        return False


def download_nltk_data():
    """Download required NLTK data"""
    print("📚 Downloading NLTK data...")
    nltk_resources = ['punkt_tab', 'punkt', 'stopwords']
    
    try:
        import nltk
        for resource in nltk_resources:
            print(f"  ⏳ Downloading {resource}...", end=" ")
            nltk.download(resource, quiet=True)
            print("✅")
        print("✅ NLTK data downloaded successfully!\n")
        return True
    except Exception as e:
        print(f"❌ Error downloading NLTK data: {e}\n")
        return False


def verify_model_files():
    """Verify that model files exist"""
    import os
    
    print("🔍 Verifying model files...")
    required_files = ['model.pkl', 'vectorizer.pkl']
    
    all_exist = True
    for file in required_files:
        if os.path.exists(file):
            print(f"  ✅ {file} found")
        else:
            print(f"  ❌ {file} NOT found - Please ensure this file exists!")
            all_exist = False
    
    if all_exist:
        print("✅ All model files verified!\n")
    else:
        print("⚠️  Some model files are missing!\n")
        return False
    
    return all_exist


def test_imports():
    """Test that all required modules can be imported"""
    print("🧪 Testing imports...")
    required_modules = [
        ('streamlit', 'streamlit'),
        ('nltk', 'nltk'),
        ('sklearn', 'scikit-learn'),
        ('numpy', 'numpy'),
        ('flask', 'flask'),
    ]
    
    all_imports_ok = True
    for module, name in required_modules:
        try:
            __import__(module)
            print(f"  ✅ {name} imported successfully")
        except ImportError:
            print(f"  ❌ {name} import failed")
            all_imports_ok = False
    
    if all_imports_ok:
        print("✅ All imports successful!\n")
    else:
        print("❌ Some imports failed. Please run: pip install -r requirements.txt\n")
    
    return all_imports_ok


def main():
    """Run all setup steps"""
    print("""
    ╔════════════════════════════════════════════════════════════╗
    ║   SMS Spam Detector - Setup Script                         ║
    ║   This will verify and configure your environment          ║
    ╚════════════════════════════════════════════════════════════╝
    """)
    
    # Step 1: Install dependencies
    if not install_dependencies():
        print("⚠️  Please fix dependency installation and try again.")
        sys.exit(1)
    
    # Step 2: Download NLTK data
    if not download_nltk_data():
        print("⚠️  Please fix NLTK data download and try again.")
        sys.exit(1)
    
    # Step 3: Verify model files
    if not verify_model_files():
        print("⚠️  Please ensure model files exist in the current directory.")
        sys.exit(1)
    
    # Step 4: Test imports
    if not test_imports():
        print("⚠️  Please fix import errors and try again.")
        sys.exit(1)
    
    # Success!
    print("""
    ╔════════════════════════════════════════════════════════════╗
    ║   ✅ SETUP COMPLETE!                                       ║
    ║                                                            ║
    ║   Your SMS Spam Detector is ready to use!                 ║
    ║                                                            ║
    ║   Next Steps:                                             ║
    ║   1. Streamlit: streamlit run app.py                     ║
    ║   2. Flask:     python flask_app.py                      ║
    ║   3. HTML:      Open index.html in your browser          ║
    ║                                                            ║
    ║   Happy spam detecting! 🚀📨                              ║
    ╚════════════════════════════════════════════════════════════╝
    """)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Setup cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        sys.exit(1)
