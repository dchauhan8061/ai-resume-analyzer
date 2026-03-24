import streamlit as st
from pypdf import PdfReader
import google.generativeai as genai
import os
import re
from fpdf import FPDF

# 1. Page Config
st.set_page_config(page_title="getshortlisted.online", page_icon="📄")

# API Setup
my_key = os.environ.get("MY_API_KEY")
genai.configure(api_key=my_key)
model = genai.GenerativeModel('gemini-2.5-flash')

# 2. Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    target_job = st.text_input("🎯 Target Job Role", key="role_input")

# 3. Main UI
st.title("📄 AI Resume Analyzer")
uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"], key="resume_input")
jd_text = st.text_area("Paste JD here:", key="jd_input")

# 4. Buttons (Fix Indentation)
col1, col2 = st.columns(2)

with col1:
    analyze = st.button("🚀 Analyze Resume", use_container_width=True, key="btn_analyze")

with col2:
    if st.button("🧹 Clear All", use_container_width=True, key="btn_clear"):
        st.session_state["jd_input"] = ""
        st.session_state["role_input"] = ""
        if "resume_input" in st.session_state:
            st.session_state.pop("resume_input")
        st.rerun()

# 5. Logic
if analyze:
    if uploaded_file:
        with st.spinner("Analyzing..."):
            resume_text = ""
            reader = PdfReader(uploaded_file)
            for page in reader.pages:
                resume_text += page.extract_text()
            
            prompt = f"Role: {target_job}\nJD: {jd_text}\nResume: {resume_text}\nGive ATS Score/100."
            response = model.generate_content(prompt)
            st.write(response.text)
    else:
        st.warning("Please upload a resume first!")