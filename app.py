import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader

# -------------------------------------------------------------------------
# 1. Page Configuration
# -------------------------------------------------------------------------
st.set_page_config(
    page_title="Lecture Buddy AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------------------------------------------------
# 2. CSS Styling (The UI Upgrade)
# -------------------------------------------------------------------------
st.markdown("""
<style>
    /* 1. Main Background - Dark VS Code Theme */
    .stApp {
        background-color: #0e1117;
        color: #FAFAFA;
    }
    
    /* 2. Sidebar - Slightly lighter dark */
    [data-testid="stSidebar"] {
        background-color: #161b22;
        border-right: 1px solid #30363d;
    }

    /* 3. Glassmorphism for Containers */
    .stTextArea, .stSelectbox, .stSlider, .stTextInput {
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        padding: 10px;
        backdrop-filter: blur(10px);
    }

    /* 4. Gradient Button (Purple-to-Blue) for Primary Actions */
    div.stButton > button[kind="primary"] {
        background: linear-gradient(90deg, #6b2cf5 0%, #3a86ff 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 1.5rem;
        font-weight: bold;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(107, 44, 245, 0.3);
    }
    div.stButton > button[kind="primary"]:hover {
        transform: scale(1.02);
        box-shadow: 0 6px 20px rgba(107, 44, 245, 0.5);
    }

    /* 5. Custom Title Styling */
    .custom-title {
        font-size: 3rem;
        font-weight: 800;
        background: -webkit-linear-gradient(45deg, #a78bfa, #3b82f6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
    }
    .custom-subtitle {
        font-size: 1.2rem;
        color: #8b949e;
        margin-bottom: 2rem;
    }

    /* 6. Clean Look - Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* 7. Card Styling for Results */
    .result-card {
        background-color: #161b22;
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #30363d;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------------------
# 3. Helper Functions (Logic)
# -------------------------------------------------------------------------

def get_gemini_response(prompt_text, api_key):
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(prompt_text)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

def extract_text_from_pdf(uploaded_file):
    try:
        pdf_reader = PdfReader(uploaded_file)
        text = ""
        for page in pdf_reader.pages:
            content = page.extract_text()
            if content:
                text += content
        return text
    except Exception as e:
        return f"Error reading PDF: {str(e)}"

# -------------------------------------------------------------------------
# 4. Sidebar: Configuration
# -------------------------------------------------------------------------
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712035.png", width=50)
    st.title("Settings")
    
    st.markdown("### 🔑 API Access")
    api_key = st.text_input("Gemini API Key", type="password", placeholder="Paste key here...")
    st.caption("[Get Free API Key](https://aistudio.google.com/app/apikey)")
    
    st.divider()
    
    st.markdown("### ⚙️ Quiz Config")
    quiz_level = st.selectbox("Difficulty", ["Easy", "Medium", "Hard"])
    num_questions = st.slider("Questions", 3, 10, 3)
    
    st.divider()
    
    if st.button("🗑️ Clear History", use_container_width=True):
        st.session_state.summary = None
        st.session_state.quiz = None
        st.rerun()

    st.markdown("---")
    st.markdown("Made with 💜 by **Jann Elijah Limpiado**")

# -------------------------------------------------------------------------
# 5. Main Content UI
# -------------------------------------------------------------------------

# Custom Header using HTML
st.markdown('<div class="custom-title">Lecture Buddy AI 🧠</div>', unsafe_allow_html=True)
st.markdown('<div class="custom-subtitle">Turn your chaotic lecture slides into clear summaries and quizzes instantly.</div>', unsafe_allow_html=True)

# Input Section
col1, col2 = st.columns([1, 2])
with col1:
    st.markdown("### 📂 Source Material")
    input_method = st.radio("Select Input:", ["Upload PDF", "Paste Text"], horizontal=True)

user_content = ""

if input_method == "Upload PDF":
    uploaded_file = st.file_uploader("Drop your PDF here", type=['pdf'])
    if uploaded_file is not None:
        with st.spinner("📄 Extracting text..."):
            user_content = extract_text_from_pdf(uploaded_file)
            if len(user_content) < 50:
                st.warning("⚠️ Text too short. Is this a scanned image?")
            else:
                st.success(f"✅ Loaded {len(user_content)} characters.")
else:
    user_content = st.text_area("Paste text here...", height=250, placeholder="Copy and paste your lecture notes here...")

# -------------------------------------------------------------------------
# 6. Logic & Processing
# -------------------------------------------------------------------------

# Initialize Session State
if "summary" not in st.session_state:
    st.session_state.summary = None
if "quiz" not in st.session_state:
    st.session_state.quiz = None

st.divider()

# The Big Gradient Button
if st.button("✨ Generate Study Material", type="primary", use_container_width=True):
    if not api_key:
        st.error("🔒 Please enter your Gemini API Key in the sidebar.")
    elif not user_content:
        st.warning("📂 Please provide some content first.")
    else:
        with st.spinner("🤖 AI is thinking... (Summary & Quiz)"):
            
            # A. Generate Summary
            summary_prompt = f"""
            You are an expert tutor. Summarize the following text into concise bullet points.
            Highlight the key concepts, definitions, and important dates.
            Use Markdown formatting for headings and bold text.
            
            Text:
            {user_content}
            """
            st.session_state.summary = get_gemini_response(summary_prompt, api_key)
            
            # B. Generate Quiz
            quiz_prompt = f"""
            Generate {num_questions} multiple-choice questions based on the text.
            Difficulty Level: {quiz_level}.
            
            Strictly follow this format for every question:
            
            **Question X:** [Question text]
            - A) [Option]
            - B) [Option]
            - C) [Option]
            - D) [Option]
            
            ---
            **Answer Key:**
            1. [Correct Letter] - [Brief Explanation]
            (etc...)
            
            Text:
            {user_content}
            """
            st.session_state.quiz = get_gemini_response(quiz_prompt, api_key)

# -------------------------------------------------------------------------
# 7. Results Display
# -------------------------------------------------------------------------

if st.session_state.summary and st.session_state.quiz:
    
    # We use tabs for a clean UI
    tab_summary, tab_quiz = st.tabs(["📝 Smart Summary", "❓ Knowledge Quiz"])
    
    with tab_summary:
        st.markdown('<div class="result-card">', unsafe_allow_html=True)
        st.markdown(st.session_state.summary)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.download_button(
            label="📥 Download Summary",
            data=st.session_state.summary,
            file_name="lecture_notes.txt",
            mime="text/plain"
        )
        
    with tab_quiz:
        st.markdown('<div class="result-card">', unsafe_allow_html=True)
        
        # --- ROBUST SPLITTING LOGIC START ---
        # This fixes the "too many values to unpack" error
        if "---" in st.session_state.quiz:
            # We split by '---'
            parts = st.session_state.quiz.split("---")
            
            # If there are 2 parts, it's perfect (Questions --- Key)
            if len(parts) == 2:
                quiz_content = parts[0]
                answer_key = parts[1]
            
            # If there are MORE than 2 parts, the AI added extra lines. 
            # We assume the LAST part is the Key, and join everything else as questions.
            else:
                answer_key = parts[-1] # The last item is the Key
                quiz_content = "---".join(parts[:-1]) # Join the rest back together
            
            st.markdown(quiz_content)
            st.divider()
            with st.expander("👀 Click to Reveal Answers"):
                st.markdown(answer_key)
        else:
            # Fallback if no separator found at all
            st.markdown(st.session_state.quiz)
        # --- ROBUST SPLITTING LOGIC END ---
            
        st.markdown('</div>', unsafe_allow_html=True)