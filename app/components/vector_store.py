from pathlib import Path

from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

from app.common.logger import get_logger
from app.common.custom_exception import CustomException
from app.components.embeddings import get_embedding_model
from app.config.config import VECTORSTORE_PATH


logger = get_logger(__name__)


def create_vector_store(
    text_chunks: list[Document]
) -> FAISS:
    """
    Create a FAISS vector store from document chunks.

    Args:
        text_chunks: List of LangChain Document objects.

    Returns:
        FAISS vector store.
    """

    try:
        if not text_chunks:
            raise CustomException(
                "No text chunks provided for vector store creation"
            )

        logger.info(
            f"Creating FAISS vector store from "
            f"{len(text_chunks)} text chunks"
        )

        embedding_model = get_embedding_model()

        vector_store = FAISS.from_documents(
            documents=text_chunks,
            embedding=embedding_model
        )

        logger.info(
            "FAISS vector store created successfully"
        )

        return vector_store

    except CustomException:
        raise

    except Exception as e:
        error_message = CustomException(
            "Failed to create FAISS vector store",
            e
        )

        logger.error(str(error_message))
        raise error_message


def save_vector_store(vector_store: FAISS) -> None:
    """
    Save the FAISS vector store locally.
    """

    try:
        if vector_store is None:
            raise CustomException(
                "Vector store is empty or None"
            )

        vectorstore_path = Path(VECTORSTORE_PATH)

        logger.info(
            f"Saving vector store to: {vectorstore_path}"
        )

        vectorstore_path.mkdir(
            parents=True,
            exist_ok=True
        )

        vector_store.save_local(
            str(vectorstore_path)
        )

        logger.info(
            "FAISS vector store saved successfully"
        )

    except CustomException:
        raise

    except Exception as e:
        error_message = CustomException(
            "Failed to save FAISS vector store",
            e
        )

        logger.error(str(error_message))
        raise error_message


def load_vector_store() -> FAISS:
    """
    Load the existing FAISS vector store.

    Returns:
        Loaded FAISS vector store.
    """

    try:
        vectorstore_path = Path(VECTORSTORE_PATH)

        if not vectorstore_path.exists():
            raise CustomException(
                f"Vector store directory does not exist: "
                f"{vectorstore_path}"
            )

        index_file = vectorstore_path / "index.faiss"
        metadata_file = vectorstore_path / "index.pkl"

        if not index_file.exists() or not metadata_file.exists():
            raise CustomException(
                "FAISS index files are missing"
            )

        logger.info(
            f"Loading FAISS vector store from: "
            f"{vectorstore_path}"
        )

        embedding_model = get_embedding_model()

        vector_store = FAISS.load_local(
            str(vectorstore_path),
            embedding_model,
            allow_dangerous_deserialization=True
        )

        logger.info(
            "FAISS vector store loaded successfully"
        )

        return vector_store

    except CustomException:
        raise

    except Exception as e:
        error_message = CustomException(
            "Failed to load FAISS vector store",
            e
        )

        logger.error(str(error_message))
        raise error_message


if __name__ == "__main__":

    try:
        from app.components.document_loader import load_documents
        from app.components.text_splitter import create_text_chunks

        # Step 1: Load PDF documents
        documents = load_documents()

        # Step 2: Create text chunks
        text_chunks = create_text_chunks(documents)

        # Step 3: Create FAISS vector store
        vector_store = create_vector_store(text_chunks)

        # Step 4: Save FAISS vector store
        save_vector_store(vector_store)

        print("\nFAISS Vector Store Created Successfully!")

        print(
            f"Total chunks stored: "
            f"{len(text_chunks)}"
        )

        print(
            f"Vector store location: "
            f"{VECTORSTORE_PATH}"
        )

    except Exception as e:
        print(f"\nError: {e}")