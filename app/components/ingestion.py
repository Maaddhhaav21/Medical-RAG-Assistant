from app.common.logger import get_logger
from app.common.custom_exception import CustomException

from app.components.document_loader import load_documents
from app.components.text_splitter import create_text_chunks
from app.components.vector_store import (
    create_vector_store,
    save_vector_store,
)


logger = get_logger(__name__)


def run_ingestion_pipeline() -> None:
    """
    Run the complete document ingestion pipeline.

    Pipeline:
        PDF Documents
            ↓
        Document Loader
            ↓
        Text Splitter
            ↓
        Embedding Model
            ↓
        FAISS Vector Store
    """

    try:
        logger.info("=" * 60)
        logger.info("Starting document ingestion pipeline")
        logger.info("=" * 60)

        # Step 1: Load PDF documents
        logger.info("Step 1/4: Loading documents")

        documents = load_documents()

        logger.info(
            f"Successfully loaded {len(documents)} document pages"
        )

        # Step 2: Create text chunks
        logger.info("Step 2/4: Creating text chunks")

        text_chunks = create_text_chunks(documents)

        logger.info(
            f"Successfully created {len(text_chunks)} text chunks"
        )

        # Step 3: Create FAISS vector store
        logger.info("Step 3/4: Creating FAISS vector store")

        vector_store = create_vector_store(text_chunks)

        # Step 4: Save vector store
        logger.info("Step 4/4: Saving FAISS vector store")

        save_vector_store(vector_store)

        logger.info("=" * 60)
        logger.info("Document ingestion pipeline completed successfully")
        logger.info("=" * 60)

        print("\n" + "=" * 60)
        print("DOCUMENT INGESTION SUCCESSFUL!")
        print("=" * 60)

        print(f"\nDocument pages processed: {len(documents)}")
        print(f"Text chunks created: {len(text_chunks)}")

        print("\nFAISS vector store created and saved successfully!")

    except Exception as e:
        error_message = CustomException(
            "Document ingestion pipeline failed",
            e
        )

        logger.error(str(error_message))

        raise error_message


if __name__ == "__main__":

    try:
        run_ingestion_pipeline()

    except Exception as e:
        print(f"\nError: {e}")