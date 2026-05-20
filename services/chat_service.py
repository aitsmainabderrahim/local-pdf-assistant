from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from core.interfaces import IChatBot

class LangChainChatBot(IChatBot):
    def __init__(self, hf_token: str):
        llm_endpoint = HuggingFaceEndpoint(
            repo_id="Qwen/Qwen2.5-7B-Instruct",
            max_new_tokens=512,
            temperature=0.3, 
            huggingfacehub_api_token=hf_token,
            timeout=120 
        )
        
        self.llm = ChatHuggingFace(llm=llm_endpoint)
        
        # English-only Prompt for better stability and encoding
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a helpful AI assistant. Follow these rules strictly:
            1. First, try to answer the user's question using ONLY the provided context.
            2. If the answer is found in the context, provide the answer directly based on the context.
            3. If the answer is NOT found in the context, you MUST start your response EXACTLY with this phrase:
            "I could not find this information in the uploaded PDF, but according to my general knowledge:"
            and then proceed to answer the question based on your own knowledge.
            """),
            ("human", "Context: \n{context}\n\nQuestion: {input}")
        ])

    def ask_question(self, question: str, retriever) -> str:
        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)

        rag_chain = (
            {"context": retriever | format_docs, "input": RunnablePassthrough()}
            | self.prompt
            | self.llm
            | StrOutputParser()
        )
        
        return rag_chain.invoke(question)