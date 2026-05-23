"""
app.py — Streamlit ChatGPT-style UI using Groq API (no local LLM needed).

Run with:  streamlit run app.py
"""

import os
from pathlib import Path
import streamlit as st

from retrieve import retrieve
from generate import generate, MODEL


# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="RAG Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS: Light theme + high contrast dark text & chat bubbles ─────────────────
st.markdown("""
<style>
/* Main app styling: light background, dark text */
.stApp { background-color: #ffffff; color: #1f2328; }

/* Sidebar styling: subtle light-gray background with a clean border */
section[data-testid="stSidebar"] { background-color: #f6f8fa; border-right: 1px solid #d0d7de; }
section[data-testid="stSidebar"] * { color: #24292f !important; }

/* Captions and subtexts in sidebar */
.stMarkdown p { color: #1f2328; }
.stCaption { color: #57606a !important; }

/* User chat bubble: distinct blue with white text for clarity */
.user-bubble {
    background: #0969da;
    color: #ffffff !important;
    padding: 10px 16px;
    border-radius: 18px 18px 4px 18px;
    margin: 6px 0 6px 80px;
    font-size: 15px; line-height: 1.6;
}

/* Bot chat bubble: light gray box with solid dark text */
.bot-bubble {
    background: #f6f8fa;
    color: #1f2328 !important;
    padding: 10px 16px;
    border-radius: 18px 18px 18px 4px;
    margin: 6px 80px 6px 0;
    font-size: 15px; line-height: 1.6;
    border: 1px solid #d0d7de;
}

/* Source document chips: clean white background, dark text */
.source-chip {
    display: inline-block;
    background: #ffffff;
    border: 1px solid #d0d7de;
    color: #57606a !important;
    font-size: 12px;
    padding: 2px 10px;
    border-radius: 12px;
    margin: 3px 4px 3px 0;
}

/* Section labels in the sidebar */
.sidebar-label {
    font-size: 11px; font-weight: 600; color: #57606a !important;
    text-transform: uppercase; letter-spacing: .08em;
    margin: 14px 0 6px 0;
}

/* Main chat input field */
.stTextInput > div > div > input {
    background: #ffffff !important; color: #1f2328 !important;
    border: 1px solid #d0d7de !important; border-radius: 8px !important;
}

/* Main Action Buttons (e.g., Send, New Chat) */
.stButton > button {
    background: #1f883d; color: #ffffff !important; border: none;
    border-radius: 8px; padding: 8px 20px; font-weight: 500;
}
.stButton > button:hover { background: #1a7f37; color: #ffffff !important; }

/* Navigation buttons for previous chats in sidebar */
div[data-testid="stSidebar"] .stButton > button {
    background: #ffffff; color: #24292f !important; border: 1px solid #d0d7de;
}
div[data-testid="stSidebar"] .stButton > button:hover {
    background: #f3f4f6; border-color: #8c959f;
}
</style>
""", unsafe_allow_html=True)


# ── Session state ─────────────────────────────────────────────────────────────
if "chats" not in st.session_state:
    st.session_state.chats = [{"title": "New chat", "messages": []}]
if "active_chat" not in st.session_state:
    st.session_state.active_chat = 0
if "groq_key" not in st.session_state:
    st.session_state.groq_key = os.getenv("GROQ_API_KEY", "")


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🤖 RAG Chatbot")
    st.caption(f"Model: `{MODEL}` via Groq")
    st.divider()

    # ── API key input ──
    st.markdown('<div class="sidebar-label">Groq API Key</div>', unsafe_allow_html=True)
    key_input = st.text_input(
        "groq_key_input",
        value=st.session_state.groq_key,
        placeholder="gsk_...",
        type="password",
        label_visibility="collapsed",
    )
    if key_input:
        st.session_state.groq_key = key_input
        st.success("Key saved ✓")
    else:
        st.warning("Paste your key above")
        st.markdown("[Get free key →](https://console.groq.com)", unsafe_allow_html=False)

    st.divider()

    # ── New chat ──
    if st.button("＋  New Chat", use_container_width=True):
        st.session_state.chats.append({"title": "New chat", "messages": []})
        st.session_state.active_chat = len(st.session_state.chats) - 1
        st.rerun()

    # ── Chat history ──
    st.markdown('<div class="sidebar-label">Previous Chats</div>', unsafe_allow_html=True)
    for i, chat in enumerate(st.session_state.chats):
        label = chat["title"][:32] + ("…" if len(chat["title"]) > 32 else "")
        if st.button(label, key=f"chat_{i}", use_container_width=True):
            st.session_state.active_chat = i
            st.rerun()

    # ── PDFs list ──
    st.markdown('<div class="sidebar-label">PDF Files</div>', unsafe_allow_html=True)
    docs = list(Path("docs").glob("*.pdf")) if Path("docs").exists() else []
    if docs:
        for pdf in docs:
            st.markdown(f"📄 {pdf.name}")
    else:
        st.caption("No PDFs — add to docs/")

    # ── Index status ──
    st.divider()
    if Path("faiss.index").exists():
        st.success("Index ready ✓")
    else:
        st.error("Run `python ingest.py` first")


# ── Main chat area ────────────────────────────────────────────────────────────
chat = st.session_state.chats[st.session_state.active_chat]

st.markdown(f"### {chat['title']}")
st.divider()

# Render message history
for msg in chat["messages"]:
    if msg["role"] == "user":
        st.markdown(f'<div class="user-bubble">{msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="bot-bubble">{msg["content"]}</div>', unsafe_allow_html=True)
        if msg.get("sources"):
            chips = "".join(
                f'<span class="source-chip">📄 {s["source"]} · chunk {s["chunk_index"]}</span>'
                for s in msg["sources"]
            )
            st.markdown(f'<div style="margin:4px 0 16px 0">{chips}</div>', unsafe_allow_html=True)

# ── Input bar ─────────────────────────────────────────────────────────────────
st.divider()
col1, col2 = st.columns([8, 1])
with col1:
    query = st.text_input(
        "msg", placeholder="Ask anything about your documents…",
        label_visibility="collapsed", key="query_input",
    )
with col2:
    send = st.button("Send", use_container_width=True)


# ── Handle send ───────────────────────────────────────────────────────────────
if send and query.strip():
    if not Path("faiss.index").exists():
        st.error("No index. Add PDFs to docs/ then run:  python ingest.py")
        st.stop()

    if not st.session_state.groq_key:
        st.error("Paste your Groq API key in the sidebar first.")
        st.stop()

    # Set chat title from first message
    if not chat["messages"]:
        chat["title"] = query[:40]

    chat["messages"].append({"role": "user", "content": query})

    with st.spinner("Thinking…"):
        chunks = retrieve(query, top_k=3)
        answer = generate(query, chunks, api_key=st.session_state.groq_key)

    chat["messages"].append({
        "role": "bot",
        "content": answer,
        "sources": chunks,
    })

    st.rerun()

elif send and not query.strip():
    st.warning("Type a question first.")


# ── Empty state ───────────────────────────────────────────────────────────────
if not chat["messages"]:
    st.markdown("""
<div style="text-align:center; margin-top:80px; color:#57606a;">
  <div style="font-size:48px">🤖</div>
  <div style="font-size:20px; margin:12px 0 6px 0; color:#1f2328;">Ask your documents anything</div>
  <div style="font-size:14px;">Add PDFs to <code>docs/</code> · run <code>python ingest.py</code> · ask away</div>
</div>
""", unsafe_allow_html=True)