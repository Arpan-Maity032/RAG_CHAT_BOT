# RAG_CHAT_BOT

[![FAISS](https://img.shields.io/badge/FAISS-CPU-blue.svg)](https://github.com/facebookresearch/faiss)
[![Python-Dotenv](https://img.shields.io/badge/python--dotenv-1.0.1-green.svg)](https://pypi.org/project/python-dotenv/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110.0-teal.svg)](https://fastapi.tiangolo.com/)
[![Uvicorn](https://img.shields.io/badge/Uvicorn-0.29.0-purple.svg)](https://www.uvicorn.org/)
[![Python-Multipart](https://img.shields.io/badge/python--multipart-0.0.9-orange.svg)](https://pypi.org/project/python-multipart/)

[![LangChain](https://img.shields.io/badge/LangChain-0.1.20-yellow.svg)](https://www.langchain.com/)
[![LangChain-Google-GenAI](https://img.shields.io/badge/LangChain--Google--GenAI-1.0.3-red.svg)](https://pypi.org/project/langchain-google-genai/)
[![LangChain-Community](https://img.shields.io/badge/LangChain--Community-0.0.38-lightgrey.svg)](https://pypi.org/project/langchain-community/)

[![PyPDF](https://img.shields.io/badge/PyPDF-4.0.2-blueviolet.svg)](https://pypi.org/project/pypdf/)
[![Docx2Txt](https://img.shields.io/badge/docx2txt-0.8-brightgreen.svg)](https://pypi.org/project/docx2txt/)
[![Tiktoken](https://img.shields.io/badge/Tiktoken-0.6.0-black.svg)](https://pypi.org/project/tiktoken/)


A powerful, privacy-focused **Retrieval-Augmented Generation (RAG)** chatbot. This system allows users to chat with their internal documents (PDFs, Word docs, text files) using gemini 1.5 flash model via geamini-api. No data leaves your network.

The project runs on a modern client-server architecture, separating the Streamlit frontend from the FastAPI backend.

The High-Level Design (HLD) follows a robust Client-Server Architecture decoupling the interface from logic.

Frontend (Streamlit): A lightweight UI for user chat and file uploads, communicating strictly via REST APIs.

Backend (FastAPI): The central orchestrator handling business logic, serving as a "Shared Service" for data processing.

Dual Ingestion Strategy: The system uniquely supports two data entry points:

User Path: Real-time uploads via the Frontend API.

Admin Path: Bulk ingestion via a backend script.
Both paths converge on a unified Ingestion Engine, ensuring consistent processing (chunking/embedding) into the FAISS VectorDB and gemini model.

---

![Demo Image](Image/HLD%20design_RAG_CHATBOT.png)

---

# BACKEND
```File Structure

backend/
├── documents_to_add/     # for bulk document upload (Admin side)
├── temp_upload/          # upload documents via /upload API
├── add_bulk.py           # add bulk documents (Admin side)
├── main.py               # FastAPI routes
├── ragservice.py         # RAG implementation
└── requirements.txt      # All required packages
|__ .env                  # define gemini_api_key =


## Installation

First, install all required packages using:

bash
pip install -r requirements.txt


Run Project
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Before run Backend make sure put the gemini api key in .env file gemini_api_key =(your API key)

# You can add documents in backend admin side vis "http://127.0.0.1:8000/update" or "http://127.0.0.1:8000/docs"
---
![Demo Image](Image/HLD%20design_RAG_CHATBOT.png)
---

# FRONTEND

---
The Frontend is built with Streamlit, serving as a lightweight Client-Side interface. It handles user interactions—specifically chatting and file uploads—and forwards them to the backend via REST API calls. It contains no business logic, acting purely as a presentation layer to visualize the RAG system's responses.

run the backend using bellow comand
'''
streamlit run app.py
'''

---
![Demo Image](Image/frontend_UI_Chatbot.jpeg)
---

```File Structure

backend/
├── .env     # BACKEND_URL = "http://127.0.0.1:8000" take backend API
├── app.py    # all streamlit code

```
# NOTE:
  Make sure always check backend run which port and define this in .env file in frontned
  make sure after running faiss_index created automaticaly don`t need to create file( for more look at .gitignore)
