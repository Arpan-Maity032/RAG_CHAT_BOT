import os
from langchain_community.document_loaders import PyPDFLoader, TextLoader, Docx2txtLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()

class RagService:
    def __init__(self):
        self.api_key = os.getenv("gemini_api_key")
        if not self.api_key:
            raise ValueError("gemini api_key missing");

        self.index_path = "faiss_index"
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model="models/gemini-embedding-001",
            google_api_key=self.api_key
        )
        self.vector_db = self._load_db()

    def _load_db(self):
        if os.path.exists(self.index_path):
            print("loading vectorDB Faiss")#for deburg perpose print
            return FAISS.load_local(
                self.index_path,
                self.embeddings,
                allow_dangerous_deserialization=True
            )
        return None
    
    def addFile(self,file_path:str,original_fileName:str):
        
        extention = os.path.splitext(original_fileName)[1].lower()

        if extention == ".pdf":
            loder = PyPDFLoader(file_path)
        elif extention == ".docx":
            loder = Docx2txtLoader(file_path)
        elif extention in [".txt",".md"]:
            loder = TextLoader(file_path)
        else:
            raise ValueError(f"{extention} is not supported")
        
        documents = loder.load();

        if not documents:
            return 0
        
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=900,chunk_overlap=200)
        chunks = text_splitter.split_documents(documents)

        #update vector Db
        if self.vector_db is None:
            self.vector_db = FAISS.from_documents(chunks,self.embeddings)
        else:
            self.vector_db.add_documents(chunks)

        self.vector_db.save_local(self.index_path)#save the dataBase localy
        return len(chunks)#return total no of token in your database
    

    def ask_question(self, query:str):
        if self.vector_db is None:
            return "The knowledge base is empty, Update database via admin side"
        
        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            temperature=0.3,
            google_api_key=self.google_api_key
        )

        retriever = self.vector_db.as_retriever(search_kwargs={"k":3})

        template = """Answer the question based strictly on the context below.
        Context: {context}
        Question: {question}
        Answer:"""

        prompt = PromptTemplate(template=template, input_variables=["context", "question"])

        qa_chain = RetrievalQA.from_chain_type(
            llm = llm,
            chain_type = "stuff",
            retriever = retriever,
            chain_type_kwargs = {"prompt":prompt}
        )

        result = qa_chain.invoke({"query":query})
        return result['result']
    
rag_model = RagService()