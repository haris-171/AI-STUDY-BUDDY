import streamlit as st
from google import genai
import PyPDF2

st.set_page_config(page_title="AI Study Buddy", page_icon="🤖")

st.title("🤖 AI Study Buddy")
st.write("Upload your notes. Get AI-powered Summary, Quiz & Answers.")
st.divider()

# --- Sidebar ---
with st.sidebar:
    st.header("🔑 Configuration")
    api_key = st.text_input("Enter Gemini API Key", type="password", placeholder="Paste your API key here")
    st.info("Get your free API key from Google AI Studio")
    st.markdown("---")
    st.caption("Developed by Haris | COMSATS University")

if not api_key:
    st.warning("Please enter your Gemini API Key in the sidebar to continue.")
    st.stop()

client = genai.Client(api_key=api_key)

def ask_ai(prompt):
    response = client.models.generate_content(
model="gemini-3.8-flash",
        contents=prompt
    )
    return response.text

# --- File Upload ---
uploaded_file = st.file_uploader("📄 Upload Your Notes / Chapter (PDF)", type="pdf")

if uploaded_file:
    reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    
    st.success(f"PDF Uploaded Successfully | Pages: {len(reader.pages)} | Words: {len(text.split())}")
    text_short = text[:12000]

    tab1, tab2, tab3 = st.tabs(["📝 Summary", "🎯 Quiz Generator", "💬 Ask AI"])

    with tab1:
        st.subheader("Chapter Summary")
        if st.button("Generate Summary", use_container_width=True):
            with st.spinner("Generating summary..."):
                prompt = f"Summarize this study material in simple English for a university student. Use bullet points, clear headings, and highlight important definitions. Material:\n\n{text_short}"
                st.write(ask_ai(prompt))

    with tab2:
        st.subheader("MCQs Quiz Generator")
        if st.button("Generate 5 MCQs", use_container_width=True):
            with st.spinner("Generating quiz..."):
                prompt = f"Create 5 MCQs from this study material. Format: Q1: Question? A) ... B) ... C) ... D) ... Correct Answer: X. Material:\n\n{text_short}"
                st.write(ask_ai(prompt))
                st.balloons()

    with tab3:
        st.subheader("Ask Anything From Your Notes")
        question = st.text_input("Your Question", placeholder="e.g. What is OOP? Explain in simple words")
        if st.button("Ask AI"):
            if question:
                with st.spinner("Thinking..."):
                    prompt = f"Answer this question based on the study material. If answer is not in material, explain from your own knowledge in simple English. Material: {text_short}\n\nQuestion: {question}"
                    st.write(ask_ai(prompt))
else:
    st.info("Upload a PDF file above to get started.")

st.divider()
st.caption("AI Study Buddy | Haris Portfolio | Powered by Gemini AI")