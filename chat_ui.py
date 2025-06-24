import streamlit as st
import requests
import time
import uuid
import re

# ---------- CONFIG ---------- #
API_URL = "http://localhost:8000/generate"
st.set_page_config(page_title="Chat with Local LLM", layout="wide")

# ---------- SESSION INIT ---------- #
if "chat_sessions" not in st.session_state:
    st.session_state.chat_sessions = {}

if "active_chat_id" not in st.session_state:
    st.session_state.active_chat_id = str(uuid.uuid4())
    st.session_state.chat_sessions[st.session_state.active_chat_id] = []

# ---------- FUNCTIONS ---------- #
def generate_response(prompt):
    response = requests.post(API_URL, json={"prompt": prompt})
    response.raise_for_status()
    return response.json()["response"]

def start_new_chat():
    new_chat_id = str(uuid.uuid4())
    st.session_state.active_chat_id = new_chat_id
    st.session_state.chat_sessions[new_chat_id] = []

def beautify_response(text):
    lines = text.strip().split("\n")
    formatted = []
    inside_ol = False
    inside_ul = False

    for line in lines:
        line = line.strip()

        # Ordered list
        if re.match(r"^\d+\.", line):
            if not inside_ol:
                formatted.append("<ol style='margin-left:1.5em;'>")
                inside_ol = True
            formatted.append(f"<li>{line[3:].strip()}</li>")
            continue
        elif inside_ol:
            formatted.append("</ol>")
            inside_ol = False

        # Unordered list
        if line.startswith("- ") or line.startswith("* "):
            if not inside_ul:
                formatted.append("<ul style='margin-left:1.5em;'>")
                inside_ul = True
            formatted.append(f"<li>{line[2:].strip()}</li>")
            continue
        elif inside_ul:
            formatted.append("</ul>")
            inside_ul = False

        # Headings
        if line.startswith("### "):
            formatted.append(f"<h3>{line[4:]}</h3>")
        elif line.startswith("## "):
            formatted.append(f"<h2>{line[3:]}</h2>")
        elif line.startswith("# "):
            formatted.append(f"<h1>{line[2:]}</h1>")
        # Key-Value
        elif ":" in line and not line.startswith("http"):
            parts = line.split(":", 1)
            formatted.append(f"<p><b>{parts[0].strip()}:</b> {parts[1].strip()}</p>")
        # Normal paragraph
        elif line:
            formatted.append(f"<p>{line}</p>")

    if inside_ol:
        formatted.append("</ol>")
    if inside_ul:
        formatted.append("</ul>")

    return "\n".join(formatted)

# ---------- SIDEBAR ---------- #
st.sidebar.title("💬 Chat Sessions")
if st.sidebar.button("➕ New Chat"):
    start_new_chat()

for chat_id, messages in st.session_state.chat_sessions.items():
    label = messages[0]["content"][:30] + "..." if messages else "New Chat"
    if st.sidebar.button(label, key=chat_id):
        st.session_state.active_chat_id = chat_id

st.sidebar.markdown("---")
st.sidebar.caption("Powered by FastAPI + Ollama")

# ---------- MAIN UI ---------- #
chat_id = st.session_state.active_chat_id
messages = st.session_state.chat_sessions[chat_id]

st.markdown(
    "<h1 style='text-align:center;'>🧠 Chat L O K</h1><hr style='margin:0;'>",
    unsafe_allow_html=True
)

# ---------- DISPLAY MESSAGES ---------- #
for msg in messages:
    align = "flex-end" if msg["role"] == "user" else "flex-start"
    bg = "#e0f7fa" if msg["role"] == "user" else "#262626"
    color = "#000" if msg["role"] == "user" else "#fff"
    border = "18px 18px 0 18px" if msg["role"] == "user" else "18px 18px 18px 0"

    st.markdown(
        f"""
        <div style="display: flex; justify-content: {align}; margin: 10px 0;">
            <div style="
                background-color: {bg};
                color: {color};
                padding: 1em;
                border-radius: {border};
                max-width: 75%;
                font-size: 0.95rem;
                box-shadow: 0 2px 6px rgba(0,0,0,0.1);
                line-height: 1.6;
                overflow-wrap: break-word;
            ">
                {beautify_response(msg["content"])}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# ---------- CHAT INPUT ---------- #
if prompt := st.chat_input("Type your message..."):
    messages.append({"role": "user", "content": prompt})

    st.markdown(
        f"""
        <div style="display: flex; justify-content: flex-end; margin: 10px 0;">
            <div style="
                background-color: #e0f7fa;
                color: #000;
                padding: 1em;
                border-radius: 18px 18px 0 18px;
                max-width: 75%;
                font-size: 0.95rem;
                line-height: 1.6;
                box-shadow: 0 2px 6px rgba(0,0,0,0.05);
            ">
                {prompt}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    with st.spinner("Generating reply..."):
        placeholder = st.empty()
        full_response = ""
        try:
            response = generate_response(prompt)
            for word in response.split():
                full_response += word + " "
                time.sleep(0.01)
                placeholder.markdown(
                    f"""
                    <div style="display: flex; justify-content: flex-start; margin: 10px 0;">
                        <div style="
                            background-color: #262626;
                            color: white;
                            padding: 1em;
                            border-radius: 18px 18px 18px 0;
                            max-width: 75%;
                            font-size: 0.95rem;
                            line-height: 1.6;
                            overflow-wrap: break-word;
                        ">
                            {beautify_response(full_response)}▌
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            placeholder.markdown(
                f"""
                <div style="display: flex; justify-content: flex-start; margin: 10px 0;">
                    <div style="
                        background-color: #262626;
                        color: white;
                        padding: 1em;
                        border-radius: 18px 18px 18px 0;
                        max-width: 75%;
                        font-size: 0.95rem;
                        line-height: 1.6;
                        overflow-wrap: break-word;
                    ">
                        {beautify_response(full_response)}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
        except Exception:
            full_response = "⚠️ Backend error or FastAPI not running."
            st.error(full_response)

    messages.append({"role": "assistant", "content": full_response})
