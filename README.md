# 🎯 Resume & JD Matcher

An AI-powered Retrieval-Augmented Generation (RAG) tool that matches candidate resumes to job descriptions and generates detailed gap analysis reports — built with Python, ChromaDB, Sentence Transformers, and Claude.

---

## 🚀 Features

- **Multi-resume upload** — supports PDF and DOCX formats
- **Vector similarity matching** — uses semantic embeddings to find the best-fit candidates, not just keyword matching
- **AI gap analysis** — Claude generates structured reports with strengths, gaps, fit scores, and actionable suggestions
- **Interactive UI** — clean Streamlit interface, no frontend experience needed
- **Fully local embeddings** — no cost for the embedding step, runs on your machine

---

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| UI | Streamlit |
| Document Parsing | PyMuPDF (PDF), python-docx (DOCX) |
| Embeddings | sentence-transformers (`all-MiniLM-L6-v2`) |
| Vector Database | ChromaDB |
| LLM / Analysis | Anthropic Claude (`claude-opus-4-5`) |

---

## 📁 Project Structure

```
resume_jd_matcher/
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python dependencies
├── utils/
│   ├── __init__.py
│   ├── parser.py           # PDF & DOCX text extraction + chunking
│   ├── embedder.py         # Embedding + ChromaDB vector store
│   └── analyzer.py         # Claude-powered gap analysis
└── data/
    ├── resumes/            # (optional) store sample resumes here
    └── jds/                # (optional) store sample JDs here
```

---

## ⚙️ Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/resume-jd-matcher.git
cd resume-jd-matcher
```

### 2. Create a virtual environment (recommended)
```bash
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Get your Anthropic API key
- Sign up at [console.anthropic.com](https://console.anthropic.com)
- Create an API key
- Add a small amount of credit (a few dollars is more than enough)

### 5. Run the app
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

---

## 🧑‍💻 How to Use

1. **Enter your Anthropic API key** in the sidebar
2. **Upload resumes** (PDF or DOCX) — you can upload multiple at once
3. **Paste or upload a Job Description**
4. **Choose how many top matches** you want to see
5. Click **Analyze Matches** — results appear with:
   - Vector similarity score
   - AI fit score (e.g. 7/10)
   - Recommendation (Strong Fit / Good Fit / Partial Fit / Weak Fit)
   - Strengths, Gaps, and Suggestions
   - Summary paragraph

---

## 🧠 How RAG Works in This Project

```
Resumes (PDF/DOCX)
       │
       ▼
  Text Extraction (PyMuPDF / python-docx)
       │
       ▼
  Chunking (400-word chunks, 50-word overlap)
       │
       ▼
  Embedding (sentence-transformers: all-MiniLM-L6-v2)
       │
       ▼
  Vector Store (ChromaDB — cosine similarity)
       │
  Job Description ──► Embed JD ──► Query Vector Store
       │
       ▼
  Top-K Matching Resumes (by cosine similarity)
       │
       ▼
  Claude API (Gap Analysis prompt + resume + JD)
       │
       ▼
  Structured JSON Report (strengths, gaps, suggestions)
```

---

## 📊 Sample Output

```
#1 — john_doe_resume.pdf  |  Similarity: 87.3%

Overall Fit:        8/10
Similarity Score:   87.3%
Recommendation:     Strong Fit

✅ Strengths
- 4 years of Python experience with FastAPI
- Hands-on Docker and Kubernetes deployment
- PostgreSQL and Redis database experience

⚠️ Gaps
- No mention of AWS cloud services (required in JD)
- Missing CI/CD pipeline experience (GitHub Actions)
- No leadership or team management experience

💡 Suggestions
- Add AWS certifications or projects to portfolio
- Contribute to open-source to demonstrate CI/CD usage

📝 Summary
John is a strong backend developer whose Python and 
containerization skills closely match the role. The 
primary gaps are cloud infrastructure and CI/CD, which 
could be addressed with targeted upskilling.
```

---

## 🔧 Configuration & Customization

- **Change embedding model**: Edit `model_name` in `utils/embedder.py`
- **Adjust chunk size**: Edit `chunk_size` and `overlap` in `utils/parser.py`
- **Change LLM model**: Edit `model` in `utils/analyzer.py`
- **Customize analysis prompt**: Edit `ANALYSIS_PROMPT` in `utils/analyzer.py`

---

## 📌 Future Improvements

- [ ] Export gap analysis reports as PDF
- [ ] Batch processing mode (analyze 100+ resumes via CLI)
- [ ] Ranking dashboard with sortable table view
- [ ] Support for LinkedIn profile URLs
- [ ] Fine-tuned embeddings on HR/tech domain data

---

## 🤝 Contributing

Pull requests welcome! Please open an issue first to discuss what you'd like to change.

---

## 📄 License

MIT License — free to use, modify, and distribute.

---

*Built with ❤️ using Python, ChromaDB, Sentence Transformers, and Anthropic Claude*
