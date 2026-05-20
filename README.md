# 📄 PDF RAG Chatbot AI

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-00a393.svg)
![React](https://img.shields.io/badge/React-18.x-61dafb.svg)
![LangChain](https://img.shields.io/badge/LangChain-Integration-green.svg)

A modern, full-stack **Retrieval-Augmented Generation (RAG)** chatbot. This application allows users to upload PDF documents and ask questions about their content. If the information is not found within the document, the AI seamlessly falls back to its general knowledge, clearly stating the source of its answer.

Built with a strict **Clean Architecture** approach to ensure maintainability, scalability, and separation of concerns.

---

## 🚀 Key Features

* **Intelligent Document Processing:** Extracts text from PDFs and splits it into optimized chunks with overlap for better context retention.
* **Hybrid RAG System:** * Prioritizes answering strictly from the uploaded PDF context.
  * Gracefully falls back to general AI knowledge if the specific info is missing (starting with: *"I could not find this information in the uploaded PDF, but..."*).
* **100% Free Open-Source Models:** Uses HuggingFace's Inference API (`Qwen/Qwen2.5-7B-Instruct` for generation).
* **Vector Database:** Integrates FAISS for lightning-fast similarity search and document retrieval.
* **Clean Architecture:** Strict separation between the API layer, business logic (Services), and abstractions (Core).
* **Modern SPA Frontend:** A clean, responsive React interface built with Vite.

---

## 📂 Detailed Project Structure

The project is divided into two main parts: the **Client** (Frontend) and the **Python Backend** (API & AI logic).

```text
📦 PDF_CHAT
├── 📁 client/                     # ⚛️ React Frontend Application (Vite)
│   ├── 📁 public/                 # Static assets (favicons, etc.)
│   ├── 📁 src/                    # Frontend source code
│   │   ├── 📄 App.jsx             # Main chat interface component & logic
│   │   ├── 📄 App.css             # UI styling & responsive design
│   │   └── 📄 main.jsx            # React DOM rendering entry point
│   ├── 📄 package.json            # Node.js dependencies & scripts
│   └── 📄 vite.config.js          # Vite bundler configuration
│
├── 📁 core/                       # 🏗️ Core Domain (Clean Architecture)
│   ├── 📄 __init__.py
│   └── 📄 interfaces.py           # Abstract Base Classes (IChatBot, IVectorStore) ensuring decoupling
│
├── 📁 services/                   # 🧠 Business Logic & AI Services
│   ├── 📄 __init__.py
│   ├── 📄 chat_service.py         # LLM orchestration, Prompts, and LangChain LCEL pipelines
│   ├── 📄 pdf_service.py          # PDF extraction logic (PyPDF2 integration)
│   └── 📄 vector_service.py       # Text splitting, Embeddings, and FAISS vector store management
│
├── 📄 .env                        # 🔒 Environment variables (Excluded from git)
├── 📄 .gitignore                  # Git ignored files configuration
├── 📄 main.py                     # ⚡ FastAPI entry point & API routes definition
├── 📄 README.md                   # Project documentation
└── 📄 requirements.txt            # Python dependencies (LangChain, FastAPI, FAISS, etc.)
```
## ⚙️ How It Works (The RAG Pipeline)

1. **Upload:** User uploads a PDF via the React UI.
2. **Extract & Chunk:** `pdf_service.py` extracts the text, and `vector_service.py` splits it into 1000-character chunks.
3. **Embed & Store:** Chunks are converted to numerical vectors using open-source embeddings and stored locally in a FAISS index.
4. **Query:** User asks a question. The system converts the question to a vector and retrieves the top most relevant PDF chunks.
5. **Generate:** `chat_service.py` constructs a strict prompt containing the chunks and the question, passing it to the HuggingFace LLM to generate an accurate response.

---

## 🛠️ Technology Stack

### Backend
* **Framework:** FastAPI, Uvicorn
* **AI & NLP:** LangChain (`langchain-core`, `langchain-huggingface`)
* **Vector Store:** FAISS (`langchain-community`)
* **PDF Processing:** PyPDF2
* **LLM Provider:** HuggingFace Hub Serverless API

### Frontend
* **Framework:** React.js
* **Build Tool:** Vite
* **HTTP Client:** Axios
* **Icons:** Lucide-React

---

## 💻 Installation & Setup

### Prerequisites
* Python 3.10+
* Node.js 18+
* A free HuggingFace account and Access Token.

### 1. Backend Setup

Clone the repository and navigate to the project root:
```bash
git clone [https://github.com/aitsmainabderrahim/local-pdf-assistant.git](https://github.com/aitsmainabderrahim/local-pdf-assistant.git)
cd pdf-rag-chatbot