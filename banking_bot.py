import streamlit as st
import pandas as pd
import requests
import json

# Set page configuration
st.set_page_config(
    page_title="HBDB Banking Bot",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Mistral API details
api_key = "i6gploMEoAqIM5Qu4zRYIkqwKcSrHFhY"
api_base_url = "https://api.mistral.ai/v1"

# Load FAQ data
@st.cache_resource
def load_faq_data():
    csv_path = r"c:\Banking Project AAK Bank\hbdb_banking_faqs (2) (1).csv"
    df = pd.read_csv(csv_path)
    return df

# Create context from FAQ
def create_faq_context(df):
    context = "HBDB Banking FAQs:\n\n"
    for idx, row in df.iterrows():
        context += f"Q: {row['Question']}\nA: {row['Answer']}\n\n"
    return context

# Main app
st.title("🏦 HBDB Banking Bot")
st.markdown("---")
st.markdown("Welcome to the HBDB Banking Assistant! Ask any questions about our banking services.")

# Load FAQ data
faq_df = load_faq_data()
faq_context = create_faq_context(faq_df)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
user_input = st.chat_input("Ask your banking question...")

if user_input:
    # Add user message to chat
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # Prepare system prompt with FAQ context
    system_prompt = f"""You are a helpful HBDB Banking Assistant. You provide accurate information about HBDB banking services.
    
Use the following FAQ data to answer customer questions accurately:

{faq_context}

If a question is not covered in the FAQs, provide helpful general banking advice but note that the customer should contact HBDB customer service for specific details.

Always be professional, friendly, and helpful."""
    
    # Get response from Mistral AI
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        try:
            # Prepare headers and request body
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            
            # Build messages list
            messages = [{"role": "system", "content": system_prompt}]
            for msg in st.session_state.messages[:-1]:
                messages.append({"role": msg["role"], "content": msg["content"]})
            
            # Make API request
            response = requests.post(
                f"{api_base_url}/chat/completions",
                headers=headers,
                json={
                    "model": "mistral-large-latest",
                    "messages": messages,
                    "temperature": 0.7,
                    "max_tokens": 1024
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                full_response = result["choices"][0]["message"]["content"]
                message_placeholder.markdown(full_response)
            else:
                error_msg = f"API Error: {response.status_code} - {response.text}"
                message_placeholder.error(error_msg)
                full_response = error_msg
        
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            message_placeholder.error(error_msg)
            full_response = error_msg
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})

# Sidebar with information
with st.sidebar:
    st.markdown("### 📋 About HBDB")
    st.markdown("HBDB is a global banking institution offering:")
    st.markdown("""
    - 💰 Savings and Checking Accounts
    - 💳 Credit Cards
    - 🏠 Mortgages
    - 🚗 Auto Loans
    - 📱 Mobile Banking
    - 🌍 Global Transfers
    - 💼 Business Accounts
    """)
    
    st.markdown("---")
    st.markdown("### ⚙️ How to Use")
    st.markdown("""
    1. Type your banking question in the chat box
    2. The bot will respond with relevant information
    3. For complex issues, contact HBDB customer service
    """)
    
    st.markdown("---")
    st.markdown("### 📞 Contact HBDB")
    st.markdown("""
    - Visit: www.hbdb.com
    - Call: Check website for country-specific numbers
    - Email: Check website for support
    """)

# Sidebar with information
with st.sidebar:
    st.markdown("### 📋 About HBDB")
    st.markdown("HBDB is a global banking institution offering:")
    st.markdown("""
    - 💰 Savings and Checking Accounts
    - 💳 Credit Cards
    - 🏠 Mortgages
    - 🚗 Auto Loans
    - 📱 Mobile Banking
    - 🌍 Global Transfers
    - 💼 Business Accounts
    """)
    
    st.markdown("---")
    st.markdown("### ⚙️ How to Use")
    st.markdown("""
    1. Type your banking question in the chat box
    2. The bot will respond with relevant information
    3. For complex issues, contact HBDB customer service
    """)
    
    st.markdown("---")
    st.markdown("### 📞 Contact HBDB")
    st.markdown("""
    - Visit: www.hbdb.com
    - Call: Check website for country-specific numbers
    - Email: Check website for support
    """)
