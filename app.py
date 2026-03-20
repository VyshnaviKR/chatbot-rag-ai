from utils.web_search import search_web
import streamlit as st
import time
import base64

from utils.rag import load_data, retrieve, load_uploaded_file
from models.llm import get_response

# ---------------- BACKGROUND ----------------
def set_bg(image_file):
    with open(image_file, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()

    st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{encoded}");
        background-size: cover;
        background-position: center;
    }}

    .stApp::before {{
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.65);
        z-index: 0;
    }}

    .stApp > div {{
        position: relative;
        z-index: 1;
    }}

    /* SIDEBAR */
    section[data-testid="stSidebar"] {{
        background: linear-gradient(180deg, #020617, #0f172a);
    }}

    section[data-testid="stSidebar"] * {{
        color: white !important;
        font-weight: 600;
    }}

    section[data-testid="stSidebar"] .stFileUploader {{
        background: rgba(255,255,255,0.1);
        padding: 10px;
        border-radius: 10px;
    }}

    section[data-testid="stSidebar"] button {{
        background-color: #22c55e;
        color: white;
        border-radius: 8px;
    }}

    /* CARD */
    .card {{
        background: rgba(0, 0, 0, 0.6);
        padding: 20px;
        border-radius: 15px;
        backdrop-filter: blur(10px);
        margin-top: 20px;
        text-align: center;
    }}

    /* INPUT */
    .stTextInput > div > div > input {{
        background-color: rgba(255,255,255,0.2);
        color: white;
        border-radius: 10px;
    }}

    h2 {{
        text-shadow: 0 0 10px #00f2ff;
    }}
    </style>
    """, unsafe_allow_html=True)

set_bg("assets/bg.jpg")

# ---------------- CHAT STATE ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.title("⚙️ Settings")

    mode = st.radio("Response Mode", ["Concise", "Detailed"])

    st.divider()

    uploaded_file = st.file_uploader("📂 Upload PDF", type="pdf")

    if uploaded_file:
        load_uploaded_file(uploaded_file)
        st.success("PDF loaded!")

    st.divider()

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []

# ---------------- MAIN UI ----------------
st.markdown('<div class="card">', unsafe_allow_html=True)

st.markdown("## 🛡️ AI Cybersecurity Chatbot")
st.markdown("### 🤖 RAG + AI Assistant")

query = st.text_input("💬 Ask something:")

st.markdown('</div>', unsafe_allow_html=True)

# Load data
load_data()

# ---------------- DISPLAY CHAT ----------------
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"""
        <div style='text-align:right; background:#2563eb; padding:10px; border-radius:10px; margin:5px; color:white;'>
        {msg["content"]}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style='text-align:left; background:#1e293b; padding:10px; border-radius:10px; margin:5px; color:white;'>
        {msg["content"]}
        </div>
        """, unsafe_allow_html=True)

# ---------------- TYPEWRITER ----------------
def typewriter(text):
    placeholder = st.empty()
    typed = ""
    for char in text:
        typed += char
        placeholder.markdown(typed + "▌")
        time.sleep(0.01)
    placeholder.markdown(typed)

# ---------------- BUTTON ----------------
if st.button("🚀 Send"):
    if query:
        st.session_state.messages.append({"role": "user", "content": query})

        # 🔹 RAG
        context = retrieve(query)

        # 🔹 Decide source
        if context:
            prompt = f"Answer based on:\n{context}\n\nQuestion: {query}"
        else:
            web_result = search_web(query)

            if web_result:
                prompt = f"Answer based on web results:\n{web_result}\n\nQuestion: {query}"
            else:
                prompt = query

        # 🔹 AI response
        with st.spinner("🧠 Thinking..."):
            answer = get_response(prompt)

        # 🔹 Mode
        if mode == "Concise":
            answer = answer[:150] + "..."

        # 🔹 Save + display
        st.session_state.messages.append({"role": "assistant", "content": answer})

        typewriter(answer)