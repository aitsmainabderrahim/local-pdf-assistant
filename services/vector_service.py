from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from core.interfaces import IVectorStore

class FAISSVectorStore(IVectorStore):
    def __init__(self, api_key: str = None):
        # We don't need OpenAI API key anymore. Using a free, lightweight open-source model.
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.vector_store = None

    def create_vector_store(self, text: str):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        chunks = text_splitter.split_text(text)
        self.vector_store = FAISS.from_texts(chunks, self.embeddings)

    def get_retriever(self):
        if not self.vector_store:
            raise ValueError("Vector store is not initialized. Please load a PDF first.")
        return self.vector_store.as_retriever()