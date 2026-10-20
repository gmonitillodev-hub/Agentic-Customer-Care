import os
from pathlib import Path

from agentic_customer_care.providers.embedding_model_provider.embedding_provider import EmbeddingProviderFactory
from utils import get_project_root

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_chroma import Chroma
import markdown2
import json
from bs4 import BeautifulSoup

import re

def extract_documents_from_kb() -> list[Document]:
    """
    Extract documents from the knowledge base folder and return them as a list of Document objects.

    Returns:
        list[Document]: A list of Document objects containing the content and metadata of each document.
        
    Raises:
        FileNotFoundError: If the knowledge base folder does not exist or is not a directory
        
    """
    
    kd_folder = Path(get_project_root() / "knowledge_base" / "documents")
    
    print(f"\n    Extracting documents from knowledge base folder: {kd_folder}")
    
    documents = []
    
    if not kd_folder.exists() or not kd_folder.is_dir():
        raise FileNotFoundError(f"Knowledge base folder not found: {kd_folder}")
    
    for topic_folder in kd_folder.iterdir():
        if topic_folder.is_dir():
            for document_file in topic_folder.iterdir():
                if document_file.is_file():
                    with open(document_file, "r", encoding="utf-8") as f:
                        content = f.read()
                        splitted_topic = (topic_folder.name).split("/")
                        topic = (splitted_topic)[len(splitted_topic) - 1]
                        documents.append(
                            Document(
                                page_content=content,
                                metadata={
                                    "topic": str(topic), 
                                    "source": str(document_file)
                                    }
                                )
                            )
    
    print(f"    Number of documents extracted from knowledge base: {len(documents)}")
    
    return documents
     
def preprocess_documents(documents: list[Document]) -> list[Document]:
    """
    Preprocess the documents by cleaning and normalizing the text.

    Args:
        documents (list[Document]): A list of Document objects to be preprocessed.
    Returns:
        list[Document]: A list of preprocessed Document objects.
    """
    
    print(f"\n    Preprocessing {len(documents)} documents...")
    
    for doc in documents:
        
        """ Convert markdown to plain text and clean the content """
        html = markdown2.markdown(doc.page_content)

        soup = BeautifulSoup(html, "html.parser")
        doc.page_content = soup.get_text(separator="\n")
        
        # Remove extra whitespace and normalize the text
        doc.page_content = re.sub(r'\s+', ' ', doc.page_content).strip()
        
        # Remove any unwanted characters or patterns (e.g., special characters, HTML tags)
        doc.page_content = re.sub(r'<[^>]+>', '', doc.page_content)
        
        # Remove markdown titles (#, ##, ecc.)
        doc.page_content = re.sub(r'^#+\s*', '', doc.page_content, flags=re.MULTILINE)
        
    print(f"    Preprocessed documents: {len(documents)}")
        
    return documents
                          
def chunk_documents(documents: list[Document]) -> list[Document]:
    """
    Chunk the documents into smaller pieces for better processing.

    Args:
        documents (list[Document]): A list of Document objects to be chunked.
    """
    print(f"\n    Chunking {len(documents)} documents with RecursiveCharacterTextSplitter...")
    
    splitter = RecursiveCharacterTextSplitter(
           chunk_size=1000,        
           chunk_overlap=200,     
           separators=["\n\n", "\n", " ", ""],
        )
    chunks = splitter.split_documents(documents)
    
    output_dir = Path(get_project_root() / "knowledge_base" / "ingestion")
    os.makedirs(output_dir, exist_ok=True)  # crea la cartella se non esiste

    output_path = os.path.join(output_dir, "chunks.jsonl")
    with open(output_path, "w", encoding="utf-8") as f:
        for doc in chunks:
            d = {
            "page_content": doc.page_content,
            "metadata": doc.metadata
            }
            f.write(json.dumps(d, ensure_ascii=False) + "\n")
    
    print(f"    Number of chunks created: {len(chunks)}")
    return chunks
    
def create_vectorstore_from_chunks(chunks: list[Document]):
    
    """
    Create a vector store from the given chunks of documents using embeddings.
    
    Args:
        chunks (list[Document]): A list of Document objects to be indexed in the vector store.

    """
    
    PROVIDER_TYPE = os.getenv("EMBEDDING_PROVIDER", "huggingface")  # set in .env
    
    print(f"\n    Creating vectorstore from {len(chunks)} chunks using {PROVIDER_TYPE} embeddings... \n")
    
    embedding_provider = EmbeddingProviderFactory.get_embedding_provider(provider_type=PROVIDER_TYPE)

    clear_vectorstore = input(f"    Do you want to clear the existing vectorstore? (y/n): ")
    if clear_vectorstore.lower() == "y":
        vectorstore = Chroma(persist_directory=str(get_project_root() / "knowledge_base" / "vectorstore"), 
                         embedding_function=embedding_provider.get_embeddings_model())
        
        if vectorstore._collection.count() > 0:
            vectorstore.delete_collection()
            print(" \n   Existing vectorstore cleared. \n")
        
    try:
        # Embedding + Indexing — tutto in una riga
        vectorstore = Chroma.from_documents(
                documents=chunks,
                embedding=embedding_provider.get_embeddings_model(),
                persist_directory=str(get_project_root() / "knowledge_base" / "vectorstore")
            )
        indexed_vector_number = vectorstore._collection.count()  # Trigger indexing
        
        if indexed_vector_number <= 0:
            raise ValueError("No vectors were indexed. Please check the input documents and embeddings.")
        
        print(f"\n  Vectorstore created and persisted with {indexed_vector_number} vectors.")
        
    except Exception as e:
        print(f"Error creating vectorstore: {e}")
        raise e
    
def run_ingestion_pipeline():
    """
    Run the ingestion pipeline to extract, preprocess, and chunk documents from the knowledge base.
    
    Steps:
        1. Extract documents from the knowledge base folder.
        2. Preprocess the extracted documents.
        3. Chunk the preprocessed documents into smaller pieces.
        4. Create a vector store from the chunks using embeddings.
        
    """
    
    print("\n---------------------------------------------------------------")
    print("------------------------ Ingestion Pipeline ------------------- \n")
    print(" \n  Running ingestion pipeline...")
    
    extracted_documents = extract_documents_from_kb()
    documents = preprocess_documents(extracted_documents)
    
    chunks = chunk_documents(documents)    
    create_vectorstore_from_chunks(chunks)
    
    print("\n   Ingestion pipeline completed successfully.")
    print("---------------------------------------------------------------\n")
 
    
if __name__ == "__main__":
    
    run_ingestion_pipeline()