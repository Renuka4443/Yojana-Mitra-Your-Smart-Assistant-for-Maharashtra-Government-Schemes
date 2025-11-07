# Installation Guide - VS Code में Project Run करने के लिए

## Step-by-Step Installation Instructions

### 1. Python Install करें (जरूरी)

- **Python 3.7 या उससे नया version** download करें
- **Recommended:** Python 3.10, 3.11, या 3.12 (सबसे stable और compatible)
- **Python 3.13.5 भी काम करेगा** (लेकिन कुछ packages में compatibility issues हो सकते हैं)
- Download link: https://www.python.org/downloads/
- Installation के समय **"Add Python to PATH"** checkbox को check करें (बहुत जरूरी!)
- Installation complete होने के बाद terminal में check करें:
  ```bash
  python --version
  ```
  या
  ```bash
  python3 --version
  ```

**Note:** Python 3.13.5 (या कोई भी 3.13 version) use कर सकते हैं, लेकिन अगर `faiss-cpu` install करने में problem आए, तो:
- Python 3.11 या 3.12 use करें (most stable)
- या `faiss-cpu` install करते समय `--no-cache-dir` flag use करें

---

### 2. VS Code में Project Folder खोलें

- VS Code open करें
- File → Open Folder से project folder select करें
- या terminal में:
  ```bash
  cd "E:\NEW GEN AI PROJECT"
  code .
  ```

---

### 3. Terminal खोलें (VS Code में)

- VS Code में `Ctrl + ~` (tilde key) दबाएं
- या Terminal → New Terminal से terminal खोलें
- Terminal project folder में ही होना चाहिए

---

### 4. Python Packages Install करें

Terminal में यह command run करें:

```bash
pip install -r requirements.txt
```

**अगर `pip` command काम नहीं करे, तो:**
```bash
python -m pip install -r requirements.txt
```

या
```bash
python3 -m pip install -r requirements.txt
```

**Important Notes:**
- इसमें 2-5 minutes लग सकते हैं
- `faiss-cpu` install करने में थोड़ा time लग सकता है
- `sentence-transformers` पहली बार model files download करेगा (लगभग 80-100 MB)
- Internet connection होना चाहिए

**अगर किसी package में error आए, तो manually install करें:**
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

---

### 5. .env File बनाएं (API Key के लिए)

Project folder में एक **`.env`** file बनाएं:

**VS Code में:**
- File → New File → `.env` नाम से save करें
- या terminal में:
  ```bash
  echo GEMINI_API_KEY=your_api_key_here > .env
  ```

**.env file में यह content add करें:**
```
GEMINI_API_KEY=your_api_key_here
```

**Google Gemini API Key कैसे प्राप्त करें:**
1. https://makersuite.google.com/app/apikey पर जाएं
2. Google account से login करें
3. "Create API Key" button पर click करें
4. API key को copy करें
5. `.env` file में `your_api_key_here` की जगह paste करें

---

### 6. Required Files Check करें

Project folder में ये files होनी चाहिए:
- ✅ `app.py` (Main application file)
- ✅ `vector_db.py`
- ✅ `qa_logic.py`
- ✅ `requirements.txt`
- ✅ `maharashtra_schemes.csv` (बहुत जरूरी!)
- ✅ `.env` (आपको बनानी होगी)
- ✅ `LOGO.png` (Optional - अगर नहीं है तो default icon use होगा)

---

### 7. Streamlit Run करें

Terminal में यह command run करें:

```bash
streamlit run app.py
```

**अगर `streamlit` command काम नहीं करे, तो:**
```bash
python -m streamlit run app.py
```

या
```bash
python3 -m streamlit run app.py
```

**Success होने पर:**
- Browser automatically खुल जाएगा
- Application `http://localhost:8501` पर run होगा
- अगर browser automatically नहीं खुले, तो manually `http://localhost:8501` पर जाएं

---

### 8. First Time Setup (Important)

पहली बार run करने पर:
- Vector database automatically create होगी (`cache` folder में)
- Model files download होंगी (इसमें 2-5 minutes लग सकते हैं)
- Internet connection होना चाहिए

**अगर CSV file में changes हों तो:**
- `cache` folder delete करें
- फिर से `streamlit run app.py` run करें
- नई database create होगी

---

## Quick Installation Checklist

Install करने से पहले यह checklist follow करें:

- [ ] Python 3.7+ installed है (3.10-3.12 recommended, 3.13.5 भी OK)
- [ ] Python PATH में add है (terminal में `python --version` check करें)
- [ ] VS Code में project folder open है
- [ ] Terminal VS Code में open है
- [ ] `pip install -r requirements.txt` run किया है (successfully)
- [ ] `.env` file बनाई है और API key add किया है
- [ ] `maharashtra_schemes.csv` file project folder में है
- [ ] `streamlit run app.py` command run किया है

---

## Common Problems और Solutions

### Problem 1: `pip` command not found
**Solution:**
```bash
python -m pip install -r requirements.txt
```

### Problem 2: `streamlit` command not found
**Solution:**
```bash
python -m streamlit run app.py
```

### Problem 3: Module not found error
**Solution:**
```bash
pip install -r requirements.txt
```
या specific package install करें:
```bash
pip install streamlit pandas sentence-transformers faiss-cpu google-generativeai python-dotenv numpy Pillow
```

### Problem 4: API Key error
**Solution:**
- `.env` file बनाएं
- `GEMINI_API_KEY=your_actual_api_key` add करें
- API key में quotes नहीं होने चाहिए

### Problem 5: CSV file not found
**Solution:**
- `maharashtra_schemes.csv` file project folder में होनी चाहिए
- File name exactly यही होना चाहिए

### Problem 6: FAISS installation error (Windows या Python 3.13)
**Solution:**
```bash
pip install faiss-cpu --no-cache-dir
```

**अगर Python 3.13 में `faiss-cpu` install नहीं हो रहा:**
- Python 3.11 या 3.12 install करें (recommended)
- या `faiss-cpu` की जगह alternative package try करें
- या pre-built wheel manually download करें

### Problem 8: Python 3.13 compatibility issues
**Solution:**
- Python 3.13.5 generally काम करेगा, लेकिन अगर packages install नहीं हो रहे:
- **Best solution:** Python 3.11 या 3.12 install करें (सबसे stable)
- Download: https://www.python.org/downloads/
- Python 3.10, 3.11, 3.12 - सभी perfectly compatible हैं

### Problem 7: Port already in use (8501)
**Solution:**
```bash
streamlit run app.py --server.port 8502
```

### Problem 9: "WARNING: Ignoring invalid distribution ~ip" warning
**Status:** यह warning है, error नहीं - **Safe to ignore!**

**क्या करें:**
- **कुछ नहीं करना है** - Installation continue करें
- यह warning pip cache corruption की वजह से आती है
- Packages फिर भी properly install होंगी
- Application बिना किसी problem के run होगी

**अगर warning bother कर रही है, तो fix करें:**
```bash
# Pip cache clean करें
pip cache purge

# या broken packages remove करें
pip uninstall -y ~ip

# फिर से install करें
pip install -r requirements.txt
```

**Note:** यह warning Python 3.13 में common है, लेकिन कोई problem नहीं है।

---

## System Requirements

- **OS:** Windows 10/11, macOS, या Linux
- **Python:** 3.7 या उससे नया
  - **Recommended:** Python 3.10, 3.11, या 3.12 (सबसे stable)
  - **Python 3.13.5 भी काम करेगा** (लेकिन कुछ packages में issues हो सकते हैं)
- **RAM:** कम से कम 4GB (8GB recommended)
- **Disk Space:** कम से कम 500MB (models और cache के लिए)
- **Internet:** First time setup के लिए (model downloads)

---

## VS Code Extensions (Optional but Recommended)

VS Code में ये extensions install कर सकते हैं:
- **Python** (Microsoft) - Python support के लिए
- **Python Indent** - Code formatting के लिए
- **autoDocstring** - Documentation के लिए

---

## Summary - एक नजर में

1. **Python install करें** (PATH में add करें)
2. **VS Code में project folder खोलें**
3. **Terminal खोलें** (VS Code में)
4. **`pip install -r requirements.txt`** run करें
5. **`.env` file बनाएं** और API key add करें
6. **`streamlit run app.py`** run करें
7. **Browser में application खुल जाएगा**

---

**अगर कोई problem हो तो terminal में error message check करें और उसके according solution try करें!**

