from pathlib import Path

from utils import get_project_root

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma 
from langchain_core.documents import Document
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
    return documents
     
def preprocess_documents(documents: list[Document]) -> list[Document]:
    """
    Preprocess the documents by cleaning and normalizing the text.

    Args:
        documents (list[Document]): A list of Document objects to be preprocessed.
    Returns:
        list[Document]: A list of preprocessed Document objects.
    """
    
    for doc in documents:
        # Remove extra whitespace and normalize the text
        doc.page_content = re.sub(r'\s+', ' ', doc.page_content).strip()
        
        # Remove any unwanted characters or patterns (e.g., special characters, HTML tags)
        doc.page_content = re.sub(r'<[^>]+>', '', doc.page_content)
        
        # Remove markdown titles (#, ##, ecc.)
        doc.page_content = re.sub(r'^#+\s*', '', doc.page_content, flags=re.MULTILINE)
        
    return documents
                          
def chunk_documents(documents: list[Document]) -> list[Document]:
    """
    Chunk the documents into smaller pieces for better processing.

    Args:
        documents (list[Document]): A list of Document objects to be chunked.
    """
    
    splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50
        )
    chunks = splitter.split_documents(documents)
    
    return chunks
    
def create_vectorstore_from_chunks(chunks: list[Document]):
    
    """
    Create a vector store from the given chunks of documents using embeddings.
    
    Args:
        chunks (list[Document]): A list of Document objects to be indexed in the vector store.

    """
    # Embedding + Indexing — tutto in una riga
    vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=OpenAIEmbeddings(model="text-embedding-3-small")
        )
    
    print(f" Chunk indicizzati: {len(chunks)}") 

def run_ingestion_pipeline():
    """
    Run the ingestion pipeline to extract, preprocess, and chunk documents from the knowledge base.
    """
    
    extracted_documents = extract_documents_from_kb()
    documents = preprocess_documents(extracted_documents)
    
    print(f"Documenti estratti: {len(documents)}")
    chunks = chunk_documents(documents)
    print(f"Chunk creati: {len(chunks)}")
    print(f"Primo chunk: {chunks[0].page_content} , metadata: {chunks[0].metadata}")
 
    
if __name__ == "__main__":
    
    run_ingestion_pipeline()