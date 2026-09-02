from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.common.logger import get_logger
from app.common.custom_exception import CustomException
from app.config.config import CHUNK_SIZE, CHUNK_OVERLAP


logger = get_logger(__name__)


def create_text_chunks(documents: list[Document]) -> list[Document]:
    """
    Split loaded documents into smaller text chunks.

    Args:
        documents: List of LangChain Document objects.

    Returns:
        List of smaller LangChain Document chunks.
    """

    try:
        if not documents:
            raise CustomException("No documents provided for text splitting")

        logger.info(
            f"Splitting {len(documents)} document pages into text chunks"
        )

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
            length_function=len,
            separators=[
                "\n\n",
                "\n",
                ". ",
                " ",
                ""
            ]
        )

        text_chunks = text_splitter.split_documents(documents)

        if not text_chunks:
            raise CustomException("No text chunks were created")

        # Remove chunks containing only whitespace
        text_chunks = [
            chunk
            for chunk in text_chunks
            if chunk.page_content and chunk.page_content.strip()
        ]

        if not text_chunks:
            raise CustomException(
                "All generated text chunks were empty"
            )

        logger.info(
            f"Successfully generated {len(text_chunks)} text chunks"
        )

        return text_chunks

    except CustomException:
        raise

    except Exception as e:
        error_message = CustomException(
            "Failed to generate text chunks",
            e
        )

        logger.error(str(error_message))
        raise error_message

if __name__ == "__main__":
    from app.components.document_loader import load_documents

    try:
        documents = load_documents()

        text_chunks = create_text_chunks(documents)

        print("\nText Chunking Successful!")
        print(f"Total document pages: {len(documents)}")
        print(f"Total text chunks: {len(text_chunks)}")

        print("\nFirst Chunk Metadata:")
        print(text_chunks[0].metadata)

        print("\nFirst Chunk Preview:")
        print(text_chunks[0].page_content[:500])

    except Exception as e:
        print(f"\nError: {e}")