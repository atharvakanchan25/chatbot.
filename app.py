import streamlit as st
import pandas as pd
import PyPDF2
import docx
from langchain_ollama import ChatOllama
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from datetime import datetime

# -------------------
# Streamlit Page Config
# -------------------
st.set_page_config(
    page_title="AI Research Assistant",
    page_icon="🤖",
    layout="wide",
)

# -------------------
# Custom CSS Styling
# -------------------
st.markdown(
    """
    <style>
    /* Global background */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
        color: #e5e7eb;
        font-family: 'Inter', sans-serif;
    }

    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #111827 !important;
        padding: 20px;
        border-right: 1px solid rgba(255,255,255,0.1);
    }
    section[data-testid="stSidebar"] h1 {
        font-size: 20px !important;
        color: #f9fafb !important;
    }
    .sidebar-title {
        font-weight: 600;
        margin-bottom: 10px;
    }
    .stButton button, .stDownloadButton button, .stLinkButton button {
        background: #1e293b;
        color: #f9fafb;
        border: none;
        border-radius: 8px;
        padding: 8px 16px;
        transition: 0.2s;
    }
    .stButton button:hover, .stDownloadButton button:hover, .stLinkButton button:hover {
        background: #374151;
        transform: scale(1.02);
    }

    /* Chat bubbles */
    .chat-bubble {
        border-radius: 15px;
        padding: 12px 16px;
        margin: 6px 0;
        max-width: 75%;
        line-height: 1.5;
        font-size: 15px;
        animation: fadeIn 0.2s ease-in;
    }
    .user-bubble {
        background: rgba(56, 189, 248, 0.08);
        color: #e0f2fe;
        border: 1px solid rgba(56, 189, 248, 0.2);
        text-align: right;
    }
    .assistant-bubble {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255,255,255,0.1);
        color: #f3f4f6;
        text-align: left;
    }

    /* Timestamp */
    .timestamp {
        font-size: 11px;
        color: gray;
        margin-top: 2px;
    }

    /* Chat input */
    .stChatInput input {
        border-radius: 999px !important;
        background-color: #1e293b !important;
        color: #f9fafb !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        padding: 10px 16px !important;
    }

    /* Footer signature */
    .footer {
        text-align: center;
        font-size: 13px;
        color: #9ca3af;
        margin-top: 15px;
    }

    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(5px); }
        to { opacity: 1; transform: translateY(0); }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------
# Initialize Session State
# -------------------
if "messages" not in st.session_state:
    st.session_state["messages"] = []
if "memory" not in st.session_state:
    st.session_state["memory"] = ConversationBufferMemory()
if "answer_mode" not in st.session_state:
    st.session_state["answer_mode"] = "Detailed"

# -------------------
# Load Ollama Model
# -------------------
@st.cache_resource
def load_model():
    return ChatOllama(model="llama3:8b", temperature=0.6, streaming=True)

llm = load_model()
conversation = ConversationChain(llm=llm, memory=st.session_state["memory"])

# -------------------
# File Extractor
# -------------------
def extract_text(file):
    if file.name.endswith(".pdf"):
        reader = PyPDF2.PdfReader(file)
        return "".join([page.extract_text() for page in reader.pages if page.extract_text()])
    elif file.name.endswith(".docx"):
        doc = docx.Document(file)
        return " ".join([para.text for para in doc.paragraphs])
    elif file.name.endswith(".xlsx"):
        df = pd.read_excel(file)
        return df.to_string()
    elif file.name.endswith(".csv"):
        df = pd.read_csv(file)
        return df.to_string()
    elif file.name.endswith(".txt"):
        return file.read().decode("utf-8")
    return None

# -------------------
# Sidebar (Navigation + Settings + File Upload)
# -------------------
with st.sidebar:
    st.markdown("<h1>Research Assistant</h1>", unsafe_allow_html=True)

    # New Chat
    if st.button("➕ New Chat"):
        st.session_state["messages"] = []
        st.session_state["memory"].clear()
        st.rerun()

    st.divider()
    st.markdown("### 👤 Account", unsafe_allow_html=True)
    st.write("Not logged in")
    st.link_button("Login / Sign Up", "https://example.com")

    st.divider()
    st.markdown("### Conversations")
    st.write("Feature coming soon...")

    st.divider()
    st.markdown("### Settings")
    st.session_state["answer_mode"] = st.radio(
        "Answer Style",
        ["Concise", "Detailed", "Technical"],
        index=["Concise", "Detailed", "Technical"].index(st.session_state["answer_mode"])
    )

    if st.button("Clear Chat"):
        st.session_state["messages"] = []
        st.session_state["memory"].clear()
        st.rerun()

    st.divider()
    st.markdown("### Upload File")
    uploaded_file = st.file_uploader("Upload PDF, Word, Excel, or TXT", type=["pdf", "docx", "xlsx", "csv", "txt"])

    if uploaded_file:
        file_text = extract_text(uploaded_file)
        if file_text:
            # Save as user message
            st.session_state["messages"].append({
                "role": "user",
                "content": f"Uploaded file: **{uploaded_file.name}**\n\nSummarize this document.",
                "time": datetime.now().strftime("%H:%M"),
            })

            # Generate summary
            summary_prompt = f"Summarize the following document in {st.session_state['answer_mode']} mode:\n\n{file_text[:3000]}"
            summary = conversation.run(summary_prompt)

            st.session_state["messages"].append({
                "role": "assistant",
                "content": f"**Summary of {uploaded_file.name}:**\n\n{summary}",
                "time": datetime.now().strftime("%H:%M"),
            })

            st.rerun()

    st.markdown("<div class='footer'>Built with passion by <b>Atharva Kanchan</b></div>", unsafe_allow_html=True)

# -------------------
# Chat Header
# -------------------
st.markdown(
    """
    <div style='text-align: center;'>
        <h2 style='margin-bottom: 0;'>AI Research Assistant</h2>
        <p style='color: #9ca3af; margin-top: 0;'>Ask questions. Get research-grade answers.</p>
    </div>
    """,
    unsafe_allow_html=True,
)
st.divider()

# -------------------
# Chat Display
# -------------------
chat_container = st.container()

with chat_container:
    for msg in st.session_state["messages"]:
        role = msg["role"]
        content = msg["content"]
        timestamp = msg["time"]

        if role == "user":
            align = "right"
            bubble_class = "chat-bubble user-bubble"
        else:
            align = "left"
            bubble_class = "chat-bubble assistant-bubble"

        st.markdown(
            f"""
            <div style='text-align: {align}; margin: 8px;'>
                <div class='{bubble_class}'>
                    {content}
                </div>
                <div class='timestamp'>{timestamp}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

# -------------------
# Chat Input + Streaming Answer
# -------------------
st.divider()
user_input = st.chat_input("Type your research query...")

if user_input:
    st.session_state["messages"].append({
        "role": "user",
        "content": user_input,
        "time": datetime.now().strftime("%H:%M"),
    })

    placeholder = st.empty()
    placeholder.markdown("<p style='color: gray; font-size: 13px;'>🤔 Thinking...</p>", unsafe_allow_html=True)

    response_text = ""
    modified_input = f"Answer in {st.session_state['answer_mode']} mode:\n{user_input}"

    for chunk in conversation.llm.stream(modified_input):
        if hasattr(chunk, "content"):
            response_text += chunk.content
            placeholder.markdown(
                f"""
                <div style='text-align: left; margin: 8px;'>
                    <div class='chat-bubble assistant-bubble'>
                        {response_text}
                    </div>
                    <div class='timestamp'>{datetime.now().strftime("%H:%M")}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.session_state["messages"].append({
        "role": "assistant",
        "content": response_text,
        "time": datetime.now().strftime("%H:%M"),
    })

    st.rerun()

# -------------------
# Footer Signature
# -------------------
st.markdown(
    "<div class='footer'>✨ Crafted with ❤️ by <b>Atharva Kanchan</b> | 2025</div>",
    unsafe_allow_html=True,
)

