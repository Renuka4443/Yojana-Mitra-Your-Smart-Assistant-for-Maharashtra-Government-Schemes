# Yojana Mitra - Maharashtra Government Schemes AI Assistant

## Installation Guide (Setup Instructions)

यह project दूसरे laptop पर run करने के लिए निम्नलिखित चीजें install करनी होंगी:

### 1. Python Installation (Required)

- **Python 3.7 या उससे नया version** install करें
- Download: https://www.python.org/downloads/
- Installation के समय **"Add Python to PATH"** option को check करें

### 2. Required Python Packages (Install करें)

Project folder में terminal/command prompt खोलें और निम्न command run करें:

```bash
pip install -r requirements.txt
```

या फिर manually install करें:

```bash
pip install streamlit>=1.28.0
pip install pandas>=2.0.0
pip install sentence-transformers>=2.2.0
pip install faiss-cpu>=1.7.4
pip install google-generativeai>=0.3.0
pip install python-dotenv>=1.0.0
pip install numpy>=1.23.0
pip install Pillow
```

**Note:** 
- `faiss-cpu` install करने में थोड़ा time लग सकता है
- `sentence-transformers` first time download करेगा model files (लगभग 80-100 MB)

### 3. Environment Variables Setup (API Key)

Project folder में एक `.env` file बनाएं और अपना Google Gemini API key add करें:

```bash
GEMINI_API_KEY=your_api_key_here
```

**Google Gemini API Key कैसे प्राप्त करें:**
1. https://makersuite.google.com/app/apikey पर जाएं
2. Google account से login करें
3. "Create API Key" button पर click करें
4. API key को copy करें और `.env` file में paste करें

### 4. Required Files Check

निम्नलिखित files project folder में होनी चाहिए:

- ✅ `maharashtra_schemes.csv` - Schemes का database (Required)
- ✅ `app.py` - Main application file (Required)
- ✅ `vector_db.py` - Vector database module (Required)
- ✅ `qa_logic.py` - QA system module (Required)
- ✅ `requirements.txt` - Dependencies list (Required)
- ✅ `LOGO.png` - Logo file (Optional - अगर नहीं है तो default icon use होगा)

### 5. Project को Run करना

Terminal/Command Prompt में project folder में जाएं और निम्न command run करें:

```bash
streamlit run app.py
```

या

```bash
python -m streamlit run app.py
```

Browser automatically खुल जाएगा और application `http://localhost:8501` पर run होगा।

### 6. First Time Setup (Important)

पहली बार run करने पर:
- Vector database automatically create होगी (cache folder में save होगी)
- Model files download होंगी (इसमें 2-5 minutes लग सकते हैं)
- अगर CSV file में changes हों तो cache folder delete करें ताकि नई database create हो

### Troubleshooting (समस्याएं और समाधान)

#### Problem: `pip` command not found
**Solution:** Python को properly install करें और PATH में add करें

#### Problem: `streamlit` command not found
**Solution:** 
```bash
pip install streamlit
```

#### Problem: API Key error
**Solution:** `.env` file बनाएं और सही API key add करें

#### Problem: Module not found error
**Solution:** 
```bash
pip install -r requirements.txt
```

#### Problem: CSV file not found
**Solution:** `maharashtra_schemes.csv` file project folder में होनी चाहिए

#### Problem: FAISS installation error (Windows)
**Solution:** 
```bash
pip install faiss-cpu --no-cache-dir
```

या Visual C++ Build Tools install करें

### System Requirements

- **OS:** Windows 10/11, macOS, या Linux
- **Python:** 3.7 या उससे नया
- **RAM:** कम से कम 4GB (8GB recommended)
- **Disk Space:** कम से कम 500MB (models और cache के लिए)
- **Internet:** First time setup के लिए (model downloads)

### Project Structure

```
NEW GEN AI PROJECT/
├── app.py                    # Main Streamlit application
├── vector_db.py              # Vector database module
├── qa_logic.py               # Question answering logic
├── requirements.txt          # Python dependencies
├── maharashtra_schemes.csv   # Schemes database (Required)
├── LOGO.png                  # Logo file (Optional)
├── .env                      # Environment variables (Create this)
├── cache/                    # Auto-generated cache folder
└── README.md                 # This file
```

### Quick Start (जल्दी शुरू करने के लिए)

1. Python install करें
2. Project folder में terminal खोलें
3. `pip install -r requirements.txt` run करें
4. `.env` file बनाएं और API key add करें
5. `streamlit run app.py` run करें
6. Browser में application खुल जाएगा

### Notes

- First run में model download होगा, इसलिए internet connection होना चाहिए
- Vector database cache folder में save होती है, इसलिए दूसरी बार run करने पर fast होगा
- अगर CSV file update हो तो cache folder delete करें

---

**For any issues or questions, check the error messages in terminal/command prompt for detailed information.**



