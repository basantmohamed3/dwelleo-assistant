import os
from dotenv import load_dotenv

# Replaced slow UnstructuredMarkdownLoader with lightweight, highly efficient native loader
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

load_dotenv()

KNOWLEDGE_BASE_DIR = "knowledge_base"
CHROMA_DIR = "chroma_db"


def build_vectorstore():
    """Parses local knowledge assets, runs chunk segmenting, and builds vector store."""
    # Using generic TextLoader assuming files are cleanly parsed markdown text strings
    loader = DirectoryLoader(
        KNOWLEDGE_BASE_DIR,
        glob="**/*.md",
        loader_cls=TextLoader
    )
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    chunks = splitter.split_documents(documents)

    embeddings = OpenAIEmbeddings()
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_DIR
    )
    # Note: Explicit vectorstore.persist() removed here as it is handled automatically 
    # natively within modern Chroma instances during compilation.
    print(f"Built vectorstore with {len(chunks)} chunks")
    return vectorstore


def load_vectorstore():
    """Initializes existing persistent Chroma engine storage index."""
    embeddings = OpenAIEmbeddings()
    return Chroma(
        persist_directory=CHROMA_DIR,
        embedding_function=embeddings
    )


def get_retriever():
    if not os.path.exists(CHROMA_DIR):
        vectorstore = build_vectorstore()
    else:
        vectorstore = load_vectorstore()
        
    return vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 6}
    )