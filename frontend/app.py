import streamlit as st
import requests
import time
import os
from dotenv import load_dotenv

load_dotenv()
backend_api = os.getenv("BACKEND_URL")


Page_title = "Orilearn RAG Agent"
Page_Icon = "@@"

st.set_page_config(page_title=Page_title,page_icon=Page_Icon,layout="wide")


st.markdown("""
<style>
    /* Main Header Styling */
    .main-header {
        font-size: 24px;
        font-weight: bold;
        color: #1E88E5; /* Blue */
        margin-bottom: 20px;
        border-bottom: 1px solid #ddd;
        padding-bottom: 10px;
    }
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #863E36;
        border-right: 1px solid #ddd;
    }
    /* Chat Bubble Tweaks */
    .stChatMessage {
        gap: 1rem;
    }
</style>
""", unsafe_allow_html=True)


with st.sidebar:
    st.header("Knowledge Base")

    try:
        if requests.get(f"{backend_api}/").status_code == 200:
            st.success("System Online")
        else:
            st.error("System Offline")
    except:
        st.error("Connection Failed")

    st.divider()

    st.markdown("Upload Document")
    uploaded_file = st.file_uploader(
        "Add a PDF, DOCX, or TXT",
        type=["pdf","docx","txt","md"],
        help="The AI will instantly read and index this file."
    )

    if uploaded_file:
        if st.button("Add File", type="primary"):
            with st.spinner("Uploading & Indexing..."):
                try:
                    files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
                    response = requests.post(f"{backend_api}/upload", files=files)
                    
                    if response.status_code == 200:
                        data = response.json()
                        st.toast(f"Successfully added {data['filename']}", icon="++")
                        st.success(f"Indexed {data['chunks_added']} chunks.")
                    else:
                        st.error(f"Upload Failed: {response.text}")
                
                except Exception as e:
                    st.error(f"Connection Error: {e}")

    st.divider()
    
    st.markdown("### Active Index")
    st.caption("Documents currently in the Knowledge Graph:")
    st.code("Backend manage updated files", language="text")


st.markdown(f'<div class="main-header>{Page_title}</div>',unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant", "content": "Welcome to Orbilearn! Please feel free to share your questions—I’m here to help you every step."
        }
    ]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


#handle user input

if prompt := st.chat_input("Type your question here..."):
    st.session_state.messages.append({"role":"user","content":prompt})
    with st.chat_message("user"):
        st.markdown(prompt)


    #response process 
    with st.chat_message("assistant"):
        msg_placeholder = st.empty()
        full_response =""

        with st.spinner("Analyzing documents..."):
            try:
                payload = {"query":prompt}
                response = requests.post(f"{backend_api}/chat",json=payload)

                if response.status_code == 200:
                    api_answer = response.json().get("answr","No response received.")

                    for chunk in api_answer.split():
                        full_response += chunk + " "
                        time.sleep(0.02)
                        msg_placeholder.markdown(full_response + " ")
                    msg_placeholder.markdown(full_response)

                else:
                    error_masg =f"server Error: {response.text}"
                    msg_placeholder.error(error_masg)
                    full_response = error_masg

            except requests.exceptions.ConnectionError:
                error_masg = "Connection refused, check backend status"
                msg_placeholder.error(error_masg)
                full_response = error_masg
            
            except Exception as e:
                error_masg = f"An error occurred:{str(e)}"
                msg_placeholder.error(error_masg)
                full_response = error_masg

        st.session_state.messages.append({"role": "assistant", "content": full_response})

