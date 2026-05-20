import PyPDF2
from core.interfaces import IPDFExtractor

class PyPDFExtractor(IPDFExtractor):
    def extract_text(self, file_bytes) -> str:
        text = ""
        pdf_reader = PyPDF2.PdfReader(file_bytes)
        for page in pdf_reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"
        return text