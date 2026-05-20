from abc import ABC, abstractmethod

class IPDFExtractor(ABC):
    @abstractmethod
    def extract_text(self, file_path_or_bytes) -> str:
        """Extracts text from a PDF file."""
        pass

class IVectorStore(ABC):
    @abstractmethod
    def create_vector_store(self, text: str):
        """Converts text into embeddings and stores them."""
        pass
    
    @abstractmethod
    def get_retriever(self):
        """Returns the retriever object for similarity search."""
        pass

class IChatBot(ABC):
    @abstractmethod
    def ask_question(self, question: str, retriever) -> str:
        """Generates an answer to the user's question based on the retrieved context."""
        pass