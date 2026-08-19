import streamlit as st
from chatbot import chatbot_response


# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="AI Registration Assistant",
    page_icon="🤖",
    layout="centered"
)


# -----------------------------
# Custom Styling
# -----------------------------
st.markdown(
    """
    <style>
    .main {
        max-width: 900px;
        margin: auto;
    }

    .title {
        text-align: center;
        font-size: 38px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        font-size: 17px;
        margin-bottom: 25px;
    }

    .info-box {
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 20px;
    }

    .stButton > button {
    border-radius: 10px;
    padding: 10px;
    font-weight: 600;
    }

.stChatMessage {
    border-radius: 12px;
    }

div[data-testid="stChatInput"] {
    border-radius: 12px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# -----------------------------
# Header
# -----------------------------
st.markdown(
    '<div class="title">🤖 AI Registration Assistant</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Your AI-powered internship registration companion'
    '</div>',
    unsafe_allow_html=True
)

st.info(
    "I can help you with internship registration, "
    "answer basic questions, and guide you through the process."
)

# -----------------------------
# FAQ Quick Questions
# -----------------------------
st.markdown("### Frequently Asked Questions")

faq_questions = [
    "What is this internship?",
    "What technologies are used?",
    "What information is required?",
    "What fields are available?"
]

cols = st.columns(2)

for i, question in enumerate(faq_questions):
    with cols[i % 2]:
        if st.button(question, use_container_width=True):
            st.session_state.messages.append(
                {
                    "role": "user",
                    "content": question
                }
            )

            response = chatbot_response(question)

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": response
                }
            )

            st.rerun()


# -----------------------------
# Initialize Chat
# -----------------------------
if "messages" not in st.session_state:

    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Hello! I am the AI Registration Assistant. "
                "How can I help you today?"
            )
        }
    ]


# -----------------------------
# Display Chat History
# -----------------------------
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.write(message["content"])


# -----------------------------
# User Input
# -----------------------------
user_input = st.chat_input(
    "Type your message here..."
)


# -----------------------------
# Process Message
# -----------------------------
if user_input:

    # Add user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    # Display user message
    with st.chat_message("user"):
        st.write(user_input)

    # Get chatbot response
    response = chatbot_response(user_input)

    # Add bot response
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response
        }
    )

    # Display bot response
    with st.chat_message("assistant"):
        st.write(response)