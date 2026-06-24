import streamlit as st

from chat_logic import get_chat_response

# page config
st.set_page_config(page_title="LineMaker AI Support", page_icon="🏈", layout="centered")

st.title("💸 LineMaker AI Customer Support")
st.caption("Ask about betting rules, account transactions, active promotions, or responsible gaming limits.")

# session state init
if "messages" not in st.session_state:
    # We keep a user-facing list for the UI layout
    st.session_state.messages = []

if "backend_history" not in st.session_state:
    # We keep a separate history tailored explicitly for Gemini's API expectations
    st.session_state.backend_history = []

# render chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["text"])

# chat input & transaction loop
if user_input := st.chat_input("How can I help you with your account or a bet today?"):
    # 1. render user message instantly
    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append({"role": "user", "text": user_input})

    # 2. trigger the processing animation while generating the response
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        try:
            with st.spinner("Thinking..."):
                ai_response = get_chat_response(
                    user_message=user_input,
                    history=st.session_state.backend_history,
                )

            # render the response text
            response_placeholder.markdown(ai_response)

            # 3. commit the transaction to memory states
            st.session_state.messages.append({"role": "assistant", "text": ai_response})

            # gemini expectations: "user" for client inputs, "model" for AI responses
            st.session_state.backend_history.append({"role": "user", "text": user_input})
            st.session_state.backend_history.append({"role": "model", "text": ai_response})

        except Exception as e:
            response_placeholder.error(f"Error generating response: {e}")
