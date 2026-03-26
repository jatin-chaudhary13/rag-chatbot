import streamlit as st
from app.chat import chat

def run_ui():
    st.set_page_config(page_title="AI Chatbot", layout="wide")

    # Session state
    if "chats" not in st.session_state:
        st.session_state.chats = {"Chat 1": []}
        st.session_state.current_chat = "Chat 1"

    # Sidebar (Chat switch)
    with st.sidebar:
        st.title("💬 Chats")

        if st.button("➕ New Chat"):
            new_chat = f"Chat {len(st.session_state.chats) + 1}"
            st.session_state.chats[new_chat] = []
            st.session_state.current_chat = new_chat

        for chat_name in st.session_state.chats.keys():
            if st.button(chat_name):
                st.session_state.current_chat = chat_name

    st.title("🤖 AI RAG Chatbot")

    chat_history = st.session_state.chats[st.session_state.current_chat]

    # Display history
    for q, a in chat_history:
        st.chat_message("user").write(q)
        st.chat_message("assistant").write(a)

    # Chat input (Enter to send)
    user_input = st.chat_input("Ask something...")

    if user_input:
        st.chat_message("user").write(user_input)

        with st.spinner("Thinking..."):
            response, sources, intent, suggestions, confidence = chat(user_input)

        full_response = f"""{response}

📌 Source: {sources}
🎯 Type: {intent}
📊 Confidence: {confidence}
"""

        st.chat_message("assistant").write(full_response)

        # Save chat
        chat_history.append((user_input, full_response))

        # Suggestions
        st.write("### 💡 Suggested Questions")
        for s in suggestions:
            st.write(f"- {s}")