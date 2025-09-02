import streamlit as st
from chatbot import chatbot

def main():
    st.title("💬 Chatbot")
    st.write("Welcome to the chatbot. Please type a message and press Enter to start the conversation.")

    # Chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # User input
    user_input = st.text_input("You:", key="user_input")

    if user_input:
        response = chatbot(user_input)

        # Save conversation
        st.session_state.messages.append(("You", user_input))
        st.session_state.messages.append(("Bot", response))

        # Exit if goodbye
        if response.lower() in ['goodbye', 'bye']:
            st.markdown("<p style='color:blue;'>🤖 Thank you for chatting with me. Have a great day! 👋</p>", unsafe_allow_html=True)
            st.stop()

    # Display messages with colors
    for sender, msg in st.session_state.messages:
        if sender == "You":
            st.markdown(f"<p style='color:green;'><b>🧑 You:</b> {msg}</p>", unsafe_allow_html=True)
        else:
            st.markdown(f"<p style='color:purple;'><b>🤖 Bot:</b> {msg}</p>", unsafe_allow_html=True)

if __name__ == '__main__':
    main()
