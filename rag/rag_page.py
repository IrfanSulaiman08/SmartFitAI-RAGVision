import streamlit as st
import json
import os
import time
from rag.ollama_engine import ask_rag

CHAT_FILE = "saved_chats/chats.json"

# =========================
# LOAD / SAVE
# =========================
def load_chats():
    if not os.path.exists(CHAT_FILE):
        return {}
    with open(CHAT_FILE, "r") as f:
        return json.load(f)

def save_chats(chats):
    with open(CHAT_FILE, "w") as f:
        json.dump(chats, f, indent=4)


# =========================
# AUTO CHAT NAME
# =========================
def generate_chat_name(text):
    text = text.lower()

    if any(w in text for w in ["diet", "food", "eat", "nutrition"]):
        return "Diet Chat"

    elif any(w in text for w in ["exercise", "fitness", "workout", "muscle"]):
        return "Fitness Chat"

    elif any(w in text for w in ["recovery", "pain", "injury"]):
        return "Recovery Chat"

    else:
        return text[:20]


# =========================
# MAIN PAGE
# =========================
def rag_page():

    # ===== STATE =====
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "current_chat" not in st.session_state:
        st.session_state.current_chat = "Chat 1"

    if "search" not in st.session_state:
        st.session_state.search = ""

    chats = load_chats()

    # =========================
    # CSS (COMPACT UI)
    # =========================
    st.markdown("""
    <style>

    section[data-testid="stSidebar"] {
        width: 240px !important;
        background-color: #0b1220;
    }

    .block-container {
        padding-top: 1rem;
    }

    .stButton {
        margin-bottom: 2px !important;
    }

    .stButton > button {
        width: 100%;
        font-size: 13px;
        padding: 6px;
        border-radius: 6px;
        text-align: left;
    }

    </style>
    """, unsafe_allow_html=True)

    # =========================
    # SIDEBAR
    # =========================
    with st.sidebar:

        # LOGO
        logo_path = os.path.join(os.getcwd(), "assets", "logo.png")
        st.image(logo_path, width=40)

        st.write("### SmartFit AI")

        # NEW CHAT
        if st.button("➕ New Chat"):
            st.session_state.messages = []
            st.session_state.current_chat = f"Chat {len(chats)+1}"

        # SEARCH
        st.session_state.search = st.text_input("🔍 Search chats")

        # SECTIONS
        st.radio("Sections", ["Diet", "Fitness", "Recovery"])

        # CHAT LIST
        st.write("### 📂 Chats")

        filtered_chats = {
            k: v for k, v in chats.items()
            if st.session_state.search.lower() in k.lower()
        }

        if len(filtered_chats) == 0:
            st.caption("No chats")

        for chat_name in filtered_chats.keys():

            col1, col2 = st.columns([8,1])

            # OPEN CHAT
            with col1:
                if st.button(chat_name, key=f"open_{chat_name}"):
                    st.session_state.messages = chats[chat_name]
                    st.session_state.current_chat = chat_name

            # DELETE ONLY IF ACTIVE
            with col2:
                if st.session_state.current_chat == chat_name:
                    if st.button("🗑️", key=f"del_{chat_name}"):
                        chats.pop(chat_name)
                        save_chats(chats)
                        st.session_state.messages = []
                        st.rerun()

        # CONTROLS
        st.write("### ⚙ Controls")

        if st.button("🧹 Clear"):
            st.session_state.messages = []

        if st.button("💾 Save"):
            if len(st.session_state.messages) > 0:
                first_msg = st.session_state.messages[0]["content"]
                chat_name = generate_chat_name(first_msg)

                chats[chat_name] = st.session_state.messages
                save_chats(chats)
                st.success("Saved")

        if st.button("⬅ Back"):
            st.session_state.page = "cv"

    # =========================
    # MAIN CHAT
    # =========================
    st.title("🤖 SmartFit AI - Advisor")
    st.caption("Ask about diet, fitness, recovery")

    # SHOW CHAT
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
    # INPUT
    user_input = st.chat_input("Ask your question...")

    if user_input:

    # USER MESSAGE
        st.session_state.messages.append({
            "role": "user",
            "content": user_input
        })

    # SHOW USER MESSAGE IMMEDIATELY
        with st.chat_message("user"):
            st.write(user_input)

    # =========================
    # LOADING + RESPONSE
    # =========================
        with st.chat_message("assistant"):

        # SPINNER WHILE WAITING
            with st.spinner("Thinking..."):
                full_text = ask_rag(user_input)

        # TYPING EFFECT
            placeholder = st.empty()
            temp = ""

            for word in full_text.split():
                temp += word + " "
                placeholder.markdown(temp)
                time.sleep(0.02)

    # SAVE BOT MESSAGE
        st.session_state.messages.append({
            "role": "assistant",
            "content": full_text
        })

        st.rerun()

    
