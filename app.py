import streamlit as st
import os
import json
from utils.parser import parse_pdf, parse_docx
from utils.embedder import Embedder
from utils.analyzer import GapAnalyzer

st.set_page_config(
    page_title="Resume & JD Matcher",
    page_icon="🎯",
    layout="wide"
)

st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=Inter:wght@400;500;600&display=swap');

        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }

        .hero {
            background: linear-gradient(135deg, #1a1a2e, #16213e, #0f3460);
            border-radius: 20px;
            padding: 3rem 2.5rem;
            margin-bottom: 2rem;
            text-align: center;
            position: relative;
            overflow: hidden;
        }
        .hero::before {
            content: "";
            position: absolute;
            top: -50px; left: -50px;
            width: 200px; height: 200px;
            background: radial-gradient(circle, rgba(99,102,241,0.3), transparent 70%);
            border-radius: 50%;
        }
        .hero::after {
            content: "";
            position: absolute;
            bottom: -50px; right: -30px;
            width: 180px; height: 180px;
            background: radial-gradient(circle, rgba(236,72,153,0.25), transparent 70%);
            border-radius: 50%;
        }
        .hero-badge {
            display: inline-block;
            background: rgba(99,102,241,0.2);
            border: 1px solid rgba(99,102,241,0.5);
            color: #a5b4fc;
            font-size: 0.75rem;
            font-weight: 600;
            letter-spacing: 0.15em;
            text-transform: uppercase;
            padding: 0.3rem 1rem;
            border-radius: 999px;
            margin-bottom: 1.2rem;
        }
        .hero-title {
            font-size: 3rem;
            font-weight: 800;
            background: linear-gradient(90deg, #6366f1, #8b5cf6, #ec4899);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            line-height: 1.15;
            margin-bottom: 1rem;
        }
        .hero-sub {
            color: #9ca3af;
            font-size: 1.05rem;
            max-width: 540px;
            margin: 0 auto;
            line-height: 1.7;
        }

        /* Section headers */
        .section-header {
            font-size: 1.15rem;
            font-weight: 700;
            color: #6366f1;
            margin: 1rem 0 0.5rem 0;
            border-left: 4px solid #6366f1;
            padding-left: 0.6rem;
            display: flex;
            align-items: center;
            gap: 0.4rem;
        }

        /* Result cards */
        .rank-badge {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 28px; height: 28px;
            background: linear-gradient(135deg, #6366f1, #8b5cf6);
            color: white;
            border-radius: 50%;
            font-weight: 700;
            font-size: 0.85rem;
            margin-right: 0.5rem;
        }

        /* Sidebar styling */
        section[data-testid="stSidebar"] {
            background: #0f0c29 !important;
        }
        section[data-testid="stSidebar"] * {
            color: #e0e7ff !important;
        }
        section[data-testid="stSidebar"] .stTextInput input {
            background: rgba(99,102,241,0.1) !important;
            border: 1px solid rgba(99,102,241,0.4) !important;
            color: white !important;
            border-radius: 8px !important;
        }

        /* Analyze button */
        .stButton > button[kind="primary"] {
            background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
            border: none !important;
            border-radius: 12px !important;
            font-weight: 600 !important;
            font-size: 1rem !important;
            padding: 0.75rem !important;
            transition: opacity 0.2s !important;
        }
        .stButton > button[kind="primary"]:hover {
            opacity: 0.9 !important;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <div class="hero-badge">✦ AI-Powered Recruitment Tool</div>
    <div class="hero-title">🎯 Resume & JD Matcher</div>
    <div class="hero-sub">
        Upload resumes and a job description — instantly get semantic match scores,
        skill gap analysis, and AI-generated hiring insights.
    </div>
</div>
""", unsafe_allow_html=True)

# Init session state
if "embedder" not in st.session_state:
    st.session_state.embedder = Embedder()
if "resumes" not in st.session_state:
    st.session_state.resumes = {}

# Sidebar
with st.sidebar:
    st.markdown("### ⚙️ Configuration")
    api_key = st.text_input("Gemini API Key", type="password", help="Get yours free at aistudio.google.com")
    if api_key:
        os.environ["GEMINI_API_KEY"] = api_key
        st.success("API key set ✓")
    st.markdown("---")
    st.markdown("**How it works:**")
    st.markdown("1. 🔑 Paste your Gemini API key")
    st.markdown("2. 📄 Upload resumes (PDF/DOCX)")
    st.markdown("3. 💼 Paste a Job Description")
    st.markdown("4. 🚀 Click Analyze Matches")

col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown('<div class="section-header">📄 Upload Resumes</div>', unsafe_allow_html=True)
    uploaded_resumes = st.file_uploader(
        "Upload one or more resumes",
        type=["pdf", "docx"],
        accept_multiple_files=True,
        key="resume_uploader"
    )

    if uploaded_resumes:
        for file in uploaded_resumes:
            if file.name not in st.session_state.resumes:
                with st.spinner(f"Parsing {file.name}..."):
                    if file.name.endswith(".pdf"):
                        text = parse_pdf(file)
                    else:
                        text = parse_docx(file)
                    st.session_state.resumes[file.name] = text
                    st.session_state.embedder.add_resume(file.name, text)

        st.success(f"{len(st.session_state.resumes)} resume(s) loaded")
        for name in st.session_state.resumes:
            st.markdown(f"- ✅ `{name}`")

    if st.button("🗑️ Clear all resumes", use_container_width=True):
        st.session_state.resumes = {}
        st.session_state.embedder = Embedder()
        st.rerun()

with col2:
    st.markdown('<div class="section-header">💼 Job Description</div>', unsafe_allow_html=True)
    jd_input_method = st.radio("Input method", ["Paste text", "Upload file"], horizontal=True)

    jd_text = ""
    if jd_input_method == "Paste text":
        jd_text = st.text_area(
            "Paste the job description here",
            height=250,
            placeholder="e.g. We are looking for a Python developer with experience in FastAPI, Docker, and PostgreSQL..."
        )
    else:
        jd_file = st.file_uploader("Upload JD file", type=["pdf", "docx"], key="jd_uploader")
        if jd_file:
            if jd_file.name.endswith(".pdf"):
                jd_text = parse_pdf(jd_file)
            else:
                jd_text = parse_docx(jd_file)
            st.success("JD loaded ✓")

st.markdown("---")

num_resumes = max(2, len(st.session_state.resumes))
top_k = st.slider("Number of top matches to show", min_value=1, max_value=min(10, num_resumes), value=min(3, num_resumes))

analyze_btn = st.button("🚀 Analyze Matches", type="primary", use_container_width=True)

if analyze_btn:
    if not api_key:
        st.error("Please enter your Gemini API key in the sidebar.")
    elif not st.session_state.resumes:
        st.error("Please upload at least one resume.")
    elif not jd_text.strip():
        st.error("Please provide a job description.")
    else:
        with st.spinner("Finding best matches..."):
            matches = st.session_state.embedder.find_matches(jd_text, top_k=top_k)

        analyzer = GapAnalyzer(api_key)

        st.markdown("## 🏆 Top Matches")

        for i, (filename, score) in enumerate(matches):
            resume_text = st.session_state.resumes[filename]
            with st.expander(f"#{i+1} — {filename}  |  Similarity: {score:.2%}", expanded=(i == 0)):
                with st.spinner("Generating gap analysis..."):
                    analysis = analyzer.analyze(resume_text, jd_text, filename)

                col_a, col_b, col_c = st.columns(3)
                with col_a:
                    st.metric("Overall Fit", analysis.get("fit_score", "N/A"))
                with col_b:
                    st.metric("Vector Similarity", f"{score:.2%}")
                with col_c:
                    st.metric("Recommendation", analysis.get("recommendation", "N/A"))

                st.markdown("**✅ Strengths**")
                for s in analysis.get("strengths", []):
                    st.markdown(f"- {s}")

                st.markdown("**⚠️ Gaps / Missing Skills**")
                for g in analysis.get("gaps", []):
                    st.markdown(f"- {g}")

                st.markdown("**💡 Suggestions for Candidate**")
                for suggestion in analysis.get("suggestions", []):
                    st.markdown(f"- {suggestion}")

                st.markdown("**📝 Summary**")
                st.info(analysis.get("summary", ""))