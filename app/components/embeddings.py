from langchain_huggingface import HuggingFaceEmbeddings

from app.common.logger import get_logger
from app.common.custom_exception import CustomException
from app.config.config import EMBEDDING_MODEL


logger = get_logger(__name__)


def get_embedding_model():
    """
    Load and return the Hugging Face embedding model.
    """

    try:
        logger.info(
            f"Loading embedding model: {EMBEDDING_MODEL}"
        )

        embedding_model = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL,
            model_kwargs={
                "device": "cpu"
            },
            encode_kwargs={
                "normalize_embeddings": True
            }
        )

        logger.info(
            "Embedding model loaded successfully"
        )

        return embedding_model

    except Exception as e:
        error_message = CustomException(
            "Failed to load embedding model",
            e
        )

        logger.error(str(error_message))
        raise error_message


if __name__ == "__main__":

    try:
        embedding_model = get_embedding_model()

        # Test embedding
        test_text = (
            "The heart pumps blood throughout "
            "the human body."
        )

        logger.info(
            "Testing embedding model"
        )

        embedding = embedding_model.embed_query(
            test_text
        )

        print("\nEmbedding Model Test Successful!")
        print(f"Model: {EMBEDDING_MODEL}")
        print(f"Embedding dimensions: {len(embedding)}")

        print("\nFirst 10 values:")
        print(embedding[:10])

    except Exception as e:
        print(f"\nError: {e}")