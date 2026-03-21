import streamlit as st
from pypdf import PdfReader
import google.generativeai as genai
import os
from fpdf import FPDF

my_key = os.environ.get("MY_API_KEY")

model = genai.GenerativeModel('gemini-2.5-flash')

st.set_page_config(page_title="AI Resume Analyzer", page_icon="📄", layout="centered")

def create_pdf(text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    clean_text = text.encode('latin-1', 'ignore').decode('latin-1')
    pdf.multi_cell(0, 10, txt=clean_text)
    return pdf.output(dest='S').encode('latin-1')

st.markdown("""
<style>

/* FORCE full app background */
html, body, [class*="css"]  {
    background-color: #0E1117 !important;
}

/* Main container */
[data-testid="stAppViewContainer"] {
    background-color: #0E1117 !important;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #262730 !important;
}

</style>
""", unsafe_allow_html=True)
st.markdown("""
<style>
.stButton>button {
    background: linear-gradient(90deg, #4CAF50, #00C9A7);
    color: white;
    border: none;
    border-radius: 12px;
    height: 3em;
    font-weight: bold;
    transition: 0.3s;
}

.stButton>button:hover {
    transform: scale(1.05);
    background: linear-gradient(90deg, #00C9A7, #4CAF50);
}
</style>
""", unsafe_allow_html=True)

st.title("📄 AI Resume Analyzer")

uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"], key="resume_uploader")

jd_text = st.text_area("Paste the Job Description (JD) here:", help="Jis job ke liye aap apply kar rahe hain, uska description yahan paste karein.")

st.set_page_config(page_title="AI Resume Analyzer", page_icon="📄", layout="centered")

with st.sidebar:

    st.header("⚙️ Settings")
    target_job = st.text_input("🎯 Target Job Role", placeholder="e.g. Data Scientist")
    
    st.markdown("---")
    st.caption("💡 Tip: Adding a job role improves analysis accuracy")

resume_text = ""

if uploaded_file:
    reader = PdfReader(uploaded_file)
    for page in reader.pages:
        text = page.extract_text()
        if text:
            resume_text += text

# Buttons

col1, col2 = st.columns(2)

with col1:
    analyze = st.button("🚀 Analyze Resume", use_container_width=True)

with col2:
    clear = st.button("🧹 Clear", use_container_width=True)

# Clear logic
if clear:
    st.session_state.clear()
    st.rerun()

# Analyze logic
if analyze:
    if resume_text:
        with st.spinner("Analyzing..."):
            prompt = f"""
You are a senior HR manager and ATS expert.

Target Job Role: {target_job if target_job else "General Role"}

Analyze the resume specifically for this role.

Give:
1. ATS Score (out of 100) based on this role
2. Role-specific strengths
3. Role-specific weaknesses
4. Missing keywords for this role
5. Improvements to match this role better

Resume:
{resume_text}
"""
            response = model.generate_content(prompt)

            st.subheader("Result")
            if response and response.text:
                st.markdown(response.text)
                
                pdf_bytes = create_pdf(response.text)
                
                st.download_button(
                    label="📥 Download Analysis Report",
                    data=pdf_bytes,
                    file_name="Analysis_Report.pdf",
                    mime="application/pdf"
                )
            else:
                st.error("No response")
    else:
        st.warning("Upload resume first!")