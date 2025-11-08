# Yojana Mitra: Your Government Scheme AI Assistant

Yojana Mitra is an AI-powered assistant that helps citizens quickly access accurate and easy-to-understand information about Maharashtra Government schemes. The system uses semantic search and generative AI to interpret natural-language queries and return structured details such as eligibility, benefits, and application steps.

---

## ✅ Features
- Natural-language search for government schemes  
- AI-generated, structured responses  
- Semantic search using embeddings  
- Fast retrieval with FAISS  
- Clean Streamlit interface  
- Dataset of 85 Maharashtra Government schemes  
- Supports scheme-based, eligibility-based, and category-based queries  

---

## 🧠 How It Works
The system follows a **Retrieval-Augmented Generation (RAG)** workflow:

1. User enters any query.  
2. Query is converted into embeddings using Sentence Transformers.  
3. FAISS retrieves the most relevant scheme entries.  
4. Gemini API generates a structured and context-aware answer.  
5. Response is formatted in markdown.  
6. Streamlit displays the formatted result.

---

## 📂 Project Structure
```text
├── app.py                      # Streamlit UI
├── qa_logic.py                 # Response and prompt logic
├── vector_db.py                # FAISS semantic search
├── maharashtra_schemes.csv     # Dataset of 85 schemes
└── README.md                   # Documentation
```

---

## 🛠️ Technology Stack

### Frontend
- Streamlit  
- HTML/CSS  

### Backend
- Python  
- Google Gemini API  
- Sentence Transformers (all-MiniLM-L6-v2)  

### Search Layer
- FAISS (vector database)  
- Pandas  
- NumPy  

### Tools
- Jupyter Notebook  
- Caching for performance  

---

## 🚀 How to Run

1. **Clone the repository**
   ```bash
   git clone https://github.com/Renuka4443/Yojana-Mitra-Your-Smart-Assistant-for-Maharashtra-Government-Schemes
   cd Yojana-Mitra-Your-Smart-Assistant-for-Maharashtra-Government-Schemes
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Streamlit app**
   ```bash
   streamlit run app.py
   ```

---

## 📊 Results

The system was tested across multiple query types and performed accurately and consistently:

- Returned complete and relevant scheme details for direct queries
- Correctly handled eligibility-based and application-related questions
- Retrieved results within **2–6 seconds** using FAISS
- Displayed responses with clean markdown formatting
- Worked smoothly for category-based queries such as “Schemes for farmers” or “Schemes for students”

  ![WhatsApp Image 2025-11-04 at 20 58 59_33857c40](https://github.com/user-attachments/assets/e54fbe02-bb9a-41eb-8419-26ca8b5a8eb5)

  ![WhatsApp Image 2025-11-04 at 21 05 22_2a09f1db](https://github.com/user-attachments/assets/fc7184cb-4636-4d40-89fd-76f5acacbb86)

![WhatsApp Image 2025-11-04 at 21 04 05_61f2afe9](https://github.com/user-attachments/assets/d5507c9b-475c-45a2-be48-5e37647b074f)

![WhatsApp Image 2025-11-04 at 21 02 05_ee6b8e01](https://github.com/user-attachments/assets/430170d2-274c-46e6-ae2e-89f8e9ae7393)

---

## 🔮 Future Scope

- Add Marathi and Hindi support
- Enable voice-based input and output
- Introduce automated fact-checking
- Build a mobile application for wider accessibility
