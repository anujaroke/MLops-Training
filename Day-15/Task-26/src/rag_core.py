import os
from pathlib import Path

from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# ===================== CONFIG =====================
DATA_FOLDER = "data"
CHROMA_DB = "chroma_db"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
LLM_MODEL = "llama3-70b-8192"
CHUNK_SIZE = 800
CHUNK_OVERLAP = 100
TOP_K = 4
# ==================================================


class RagEngine:
    def __init__(self):
        self.retriever = None
        self.chain = None

    def build(self):
        if not os.getenv("GROQ_API_KEY"):
            raise ValueError("Missing GROQ_API_KEY. Set it in your environment or .env file.")

        if not Path(DATA_FOLDER).exists():
            raise FileNotFoundError(
                f"Data folder '{DATA_FOLDER}' not found. Create it and add .txt files."
            )

        docs = self._load_documents(DATA_FOLDER)
        if not docs:
            raise ValueError("No documents found. Add .txt files to your data folder.")

        chunks = self._split_documents(docs)
        vectorstore = self._build_vectorstore(chunks)
        self.retriever = vectorstore.as_retriever(search_kwargs={"k": TOP_K})
        self.chain = self._build_chain()

    def answer(self, question: str):
        if not self.retriever or not self.chain:
            raise RuntimeError("RAG engine not initialized")

        docs = self.retriever.invoke(question)
        context = self._format_context(docs)
        response = self.chain.invoke({"context": context, "question": question})
        sources = self._unique_sources(docs)
        return response, sources

    def _load_documents(self, data_folder: str):
        loader = DirectoryLoader(
            data_folder,
            glob="**/*.txt",
            loader_cls=TextLoader,
            loader_kwargs={"encoding": "utf-8"},
        )
        return loader.load()

    def _split_documents(self, docs):
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
        )
        return splitter.split_documents(docs)

    def _build_vectorstore(self, chunks):
        embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
        vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory=CHROMA_DB,
        )
        try:
            vectorstore.persist()
        except Exception:
            pass
        return vectorstore

    def _build_chain(self):
        prompt = ChatPromptTemplate.from_template(
            """
You are OrgMind, an intelligent assistant for NexusTech Solutions.
Answer the question using only the provided context.
If you don't know the answer, say "I don't have enough information."

Context:
{context}

Question: {question}

Answer:
"""
        )
        llm = ChatGroq(
            model=LLM_MODEL,
            api_key=os.getenv("GROQ_API_KEY"),
            temperature=0.3,
        )
        return prompt | llm | StrOutputParser()

    def _format_context(self, docs):
        parts = []
        for i, doc in enumerate(docs, start=1):
            source = doc.metadata.get("source", "unknown")
            source_name = Path(source).name
            parts.append(f"[Doc {i} | {source_name}]\n{doc.page_content}")
        return "\n\n".join(parts)

    def _unique_sources(self, docs):
        seen = []
        for doc in docs:
            source = Path(doc.metadata.get("source", "unknown")).name
            if source not in seen:
                seen.append(source)
        return seen
