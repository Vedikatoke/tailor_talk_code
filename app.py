import streamlit as st
import requests

st.set_page_config(page_title="TailorTalk")
st.title("TailorTalk: Your Calendar Assistant")
st.markdown("Chat with the assistant to schedule meetings on your Google Calendar ")

# Store messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display message history
for msg in st.session_state.messages:
    st.write(f"**{msg['role']}:** {msg['content']}")

# Chat input form
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("You:")
    submitted = st.form_submit_button("Send")

# Handle form submission
if submitted and user_input:
    print("Sending message to backend:", user_input)

    st.session_state.messages.append({"role": "User", "content": user_input})

    try:
        response = requests.post("http://localhost:8000/chat", json={"message": user_input})
        response.raise_for_status()
        result = response.json()
        agent_reply = result.get("response", " No response from backend.")
    except Exception as e:
        agent_reply = f" Error contacting backend: {e}"

    st.session_state.messages.append({"role": "Agent", "content": agent_reply})
