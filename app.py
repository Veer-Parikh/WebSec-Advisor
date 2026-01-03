import streamlit as st
import asyncio
from chatbot_modules.chatbot import OWASPChatbot

# 1. Page Configuration
st.set_page_config(
    page_title="OWASP Security Assistant",
    page_icon="🛡️",
    layout="wide"
)

# 2. Initialize Chatbot (Cached to prevent reloading on every interaction)
@st.cache_resource
def get_chatbot():
    chatbot = OWASPChatbot()
    # We must run the async init synchronously here
    asyncio.run(chatbot._async_init_components())
    return chatbot

try:
    bot = get_chatbot()
except Exception as e:
    st.error(f"Error initializing chatbot: {e}")
    st.stop()

# 3. Session State for Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. Sidebar options
with st.sidebar:
    st.title("⚙️ Controls")
    if st.button("Clear Chat History", type="primary"):
        st.session_state.messages = []
        st.rerun()
    
    st.divider()
    st.markdown("""
    ### About
    This is an **OWASP Security Assistant** powered by:
    - RAG (Retrieval Augmented Generation)
    - Semantic Search
    - OWASP Top 10 Knowledge Base
    """)

# 5. Main Chat Interface
st.title("🛡️ OWASP Security Assistant")
st.markdown("Ask me anything about web application security, vulnerabilities, or prevention methods.")

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. Chat Input & Processing
if prompt := st.chat_input("Ex: What is Broken Access Control?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        with st.spinner("Analyzing security context..."):
            try:
                # Run the async process_question method
                response_data = asyncio.run(bot.process_question(prompt))
                
                # Extract the clean text response
                full_response = response_data.get("response", "No response generated.")
                
                # Add context info if available (optional)
                if response_data.get("context_used"):
                    full_response += "\n\n--- \n*Sources were consulted for this answer.*"
                
                message_placeholder.markdown(full_response)
                
                # Add assistant response to chat history
                st.session_state.messages.append({"role": "assistant", "content": full_response})
                
            except Exception as e:
                error_msg = f"An error occurred: {str(e)}"
                message_placeholder.error(error_msg)