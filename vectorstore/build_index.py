from langchain_text_splitters.character import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

def build_vectorstore(text: str, filepath: str = "user_upload"):
    splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=20)
    chunks = splitter.split_text(text)
    
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    metadatas = [{"source": filepath, "chunk": i} for i in range(len(chunks))]
    store = Chroma.from_texts(
        texts=chunks,
        embedding=embeddings,
        metadatas=metadatas,
        persist_directory="./data/chroma_indexstore"
    )
    store.persist()
    return store


#test
# if __name__ == "__main__":
#     text = "This is a test document. It contains some text to be indexed."
#     filepath = "test_document.txt"
#     vectorstore = build_vectorstore(text, filepath)
#     print("Vectorstore built and saved successfully.")