import streamlit as st
from chatbot import ChatBot

# 1. Page Configuration
st.set_page_config(page_title="Astra AI", page_icon="🤖")

# 2. Initialize the ChatBot (Stored in session state so it doesn't restart every click)
if "bot" not in st.session_state:
    try:
        st.session_state.bot = ChatBot()
        st.session_state.bot_status = "Connected"
    except Exception as e:
        st.session_state.bot_status = f"Error: {e}"

# 3. Sidebar for status and controls
with st.sidebar:
    st.title("Settings")
    st.write(f"Bot Status: {st.session_state.bot_status}")
    if st.button("Clear Conversation"):
        st.session_state.messages = []
        st.rerun()

# 4. Chat UI
st.title("🤖 Astra Friendly AI")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 5. User Input Logic
if prompt := st.chat_input("Say something..."):
    # Display user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("Astra is thinking..."):
            response = st.session_state.bot.get_response(prompt)
            st.markdown(response)
    
    st.session_state.messages.append({"role": "assistant", "content": response})