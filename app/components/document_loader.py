from pathlib import Path

import fitz
from langchain_core.documents import Document

from app.common.logger import get_logger
from app.common.custom_exception import CustomException
from app.config.config import DATA_PATH

logger = get_logger(__name__)

def get_pdf_files() -> list[Path]:
    """
    Find all PDF files inside the data directory.
    """

    try:
        if not DATA_PATH.exists():
            raise CustomException(
                f"Data directory does not exist: {DATA_PATH}"
            )

        pdf_files = list(DATA_PATH.rglob("*.pdf"))

        if not pdf_files:
            logger.warning(
                f"No PDF files found in: {DATA_PATH}"
            )
            return []

        logger.info(
            f"Found {len(pdf_files)} PDF file(s)"
        )

        return pdf_files

    except Exception as e:
        if isinstance(e, CustomException):
            raise e

        error_message = CustomException(
            "Failed to find PDF files",
            e
        )

        logger.error(str(error_message))
        raise error_message


def load_single_pdf(pdf_path: Path) -> list[Document]:
    """
    Load a single PDF using PyMuPDF and convert its pages
    into LangChain Document objects.
    """

    try:
        logger.info(f"Loading PDF: {pdf_path.name}")
        pdf = fitz.open(pdf_path)
        documents = []
        for page_number, page in enumerate(pdf, start=1):
            text = page.get_text("text").strip()

            # Skip pages that do not contain readable text
            if not text:
                logger.warning(
                    f"Skipping empty page {page_number} "
                    f"from {pdf_path.name}"
                )
                continue

            document = Document(
                page_content=text,
                metadata={
                    "source": str(pdf_path),
                    "file_name": pdf_path.name,
                    "page": page_number
                }
            )

            documents.append(document)

        pdf.close()

        logger.info(
            f"Loaded {len(documents)} pages with readable text "
            f"from {pdf_path.name}"
        )

        return documents

    except Exception as e:
        error_message = CustomException(
            f"Failed to load PDF: {pdf_path.name}",
            e
        )

        logger.error(str(error_message))
        raise error_message


def load_documents() -> list[Document]:
    """
    Load all PDF documents from the configured data directory.
    """

    try:
        pdf_files = get_pdf_files()

        if not pdf_files:
            raise CustomException(
                "No PDF files available for processing"
            )

        all_documents = []

        for pdf_path in pdf_files:
            documents = load_single_pdf(pdf_path)
            all_documents.extend(documents)

        if not all_documents:
            raise CustomException(
                "PDF files were found, but no readable text could be extracted"
            )

        logger.info(
            f"Successfully loaded {len(all_documents)} "
            f"document pages in total"
        )

        return all_documents

    except Exception as e:
        if isinstance(e, CustomException):
            raise e

        error_message = CustomException(
            "Failed to load documents",
            e
        )

        logger.error(str(error_message))
        raise error_message


if __name__ == "__main__":
    try:
        documents = load_documents()

        print("\nDocument Loading Successful!")
        print(f"Total readable pages: {len(documents)}")

        print("\nFirst Document Metadata:")
        print(documents[0].metadata)

        print("\nFirst 500 Characters:")
        print(documents[0].page_content[:500])

    except Exception as e:
        print(f"\nError: {e}")