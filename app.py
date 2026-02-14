import streamlit as st
import pandas as pd
import requests

# Page configuration
st.set_page_config(
    page_title="HBDB Banking Bot",
    page_icon="🏦",
    layout="wide"
)

st.title("🏦 HBDB Banking Bot")
st.markdown("---")

# Load FAQ data
@st.cache_resource
def load_faq_data():
    df = pd.read_csv("hbdb_banking_faqs (2) (1).csv")
    return df

# Create FAQ context
def get_faq_context(df):
    context = "HBDB Banking FAQs:\n\n"
    for _, row in df.iterrows():
        context += f"Q: {row['Question']}\nA: {row['Answer']}\n\n"
    return context

# Load data
faq_df = load_faq_data()
faq_context = get_faq_context(faq_df)

# Initialize session
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
user_input = st.chat_input("Ask about HBDB banking services...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    with st.chat_message("user"):
        st.markdown(user_input)
    
    system_prompt = f"""You are a helpful HBDB Banking Assistant.

{faq_context}

If the answer is in the FAQs, provide that information. Otherwise, suggest contacting HBDB customer service.
Be professional and helpful."""
    
    with st.chat_message("assistant"):
        placeholder = st.empty()
        
        try:
            headers = {
                "Authorization": f"Bearer i6gploMEoAqIM5Qu4zRYIkqwKcSrHFhY",
                "Content-Type": "application/json"
            }
            
            messages = [{"role": "system", "content": system_prompt}]
            for msg in st.session_state.messages[:-1]:
                messages.append(msg)
            
            response = requests.post(
                "https://api.mistral.ai/v1/chat/completions",
                headers=headers,
                json={
                    "model": "mistral-large-latest",
                    "messages": messages,
                    "temperature": 0.7,
                    "max_tokens": 1024
                },
                timeout=30
            )
            
            if response.status_code == 200:
                bot_response = response.json()["choices"][0]["message"]["content"]
            else:
                bot_response = f"Error: {response.status_code}"
            
            placeholder.markdown(bot_response)
            st.session_state.messages.append({"role": "assistant", "content": bot_response})
        
        except Exception as e:
            bot_response = f"Error: {str(e)}"
            placeholder.error(bot_response)
            st.session_state.messages.append({"role": "assistant", "content": bot_response})

# Sidebar
with st.sidebar:
    st.markdown("### About HBDB")
    st.markdown("Global banking services including accounts, cards, loans, and more.")
    
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()
