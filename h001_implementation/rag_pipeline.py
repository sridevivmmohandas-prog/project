import re, json
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import Ollama
from langchain.chains import RetrievalQA

class CustomerAgent:
    def __init__(self):
        self.load_data()
        self.setup_rag()
    
    def load_data(self):
        loader = PyPDFLoader("data/customer_john.pdf")
        docs = loader.load()
        self.docs = [re.sub(r'\b\d{3}-\d{3}-\d{4}\b', '[PHONE]', doc.page_content) for doc in docs]
    
    def setup_rag(self):
        splitter = RecursiveCharacterTextSplitter(chunk_size=500)
        chunks = splitter.split_documents(self.docs)
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        self.vectorstore = FAISS.from_documents(chunks, embeddings)
        self.llm = Ollama(model="llama3.1")
        self.qa_chain = RetrievalQA.from_chain_type(self.llm, retriever=self.vectorstore.as_retriever())
    
    def chat(self, query):
        return self.qa_chain({"query": f"{query} Use customer history and nearby stores."})['result']
