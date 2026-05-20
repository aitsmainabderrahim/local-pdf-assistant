from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import io
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Importing our existing Clean Architecture services!
from services.pdf_service import PyPDFExtractor
from services.vector_service import FAISSVectorStore
from services.chat_service import LangChainChatBot

app = FastAPI(title="PDF Chat API")

# Enable CORS so React (running on a different port) can talk to this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration: Fetching the token from the .env file safely
HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN")

# Raise an error early if the token is missing from the .env file
if not HUGGINGFACE_TOKEN:
    raise ValueError("HUGGINGFACE_TOKEN is not set in the .env file.")

# Dependency Injection - Global instances
pdf_extractor = PyPDFExtractor()
vector_store = FAISSVectorStore()
chat_bot = LangChainChatBot(hf_token=HUGGINGFACE_TOKEN)

class QuestionRequest(BaseModel):
    question: str

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="File must be a PDF")
    
    try:
        file_bytes = await file.read()
        # Using io.BytesIO to simulate a file object for PyPDF2
        pdf_file_obj = io.BytesIO(file_bytes)
        
        text = pdf_extractor.extract_text(pdf_file_obj)
        if not text.strip():
            raise HTTPException(status_code=400, detail="PDF is empty or unreadable.")
            
        vector_store.create_vector_store(text)
        return {"message": "Document processed successfully. You can now ask questions."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat")
async def chat(request: QuestionRequest):
    try:
        retriever = vector_store.get_retriever()
        answer = chat_bot.ask_question(request.question, retriever)
        return {"answer": answer}
    except ValueError as e:
        # Happens if vector store is not initialized (no PDF uploaded)
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))