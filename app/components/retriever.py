from langchain_core.documents import Document

from app.common.logger import get_logger
from app.common.custom_exception import CustomException
from app.components.vector_store import load_vector_store


logger = get_logger(__name__)


def get_retriever(k: int = 4):
    """
    Load the FAISS vector store and create a retriever.

    Args:
        k: Number of relevant document chunks to retrieve.

    Returns:
        A LangChain retriever object.
    """

    try:
        if k < 1:
            raise CustomException(
                "The value of k must be at least 1"
            )

        logger.info("Loading FAISS vector store")

        vector_store = load_vector_store()

        if vector_store is None:
            raise CustomException(
                "Vector store could not be loaded"
            )

        retriever = vector_store.as_retriever(
            search_type="similarity",
            search_kwargs={
                "k": k
            }
        )

        logger.info(
            f"Retriever created successfully with k={k}"
        )

        return retriever

    except CustomException:
        raise

    except Exception as e:
        error_message = CustomException(
            "Failed to create retriever",
            e
        )

        logger.error(str(error_message))
        raise error_message


def retrieve_documents(
    query: str,
    k: int = 4
) -> list[Document]:
    """
    Retrieve relevant documents for a given query.

    Args:
        query: User's question.
        k: Number of relevant chunks to retrieve.

    Returns:
        List of relevant LangChain Document objects.
    """

    try:
        if not query or not query.strip():
            raise CustomException(
                "Query cannot be empty"
            )

        logger.info(
            f"Retrieving documents for query: {query}"
        )

        retriever = get_retriever(k=k)

        relevant_documents = retriever.invoke(query)

        if not relevant_documents:
            logger.warning(
                "No relevant documents were found"
            )
            return []

        logger.info(
            f"Retrieved {len(relevant_documents)} relevant documents"
        )

        return relevant_documents

    except CustomException:
        raise

    except Exception as e:
        error_message = CustomException(
            "Failed to retrieve relevant documents",
            e
        )

        logger.error(str(error_message))
        raise error_message


if __name__ == "__main__":

    try:
        test_query = "What is the function of the heart?"

        documents = retrieve_documents(
            query=test_query,
            k=3
        )

        print("\n" + "=" * 60)
        print("RETRIEVER TEST SUCCESSFUL")
        print("=" * 60)

        print(f"\nQuery: {test_query}")
        print(f"Documents retrieved: {len(documents)}")

        for index, document in enumerate(
            documents,
            start=1
        ):
            print("\n" + "-" * 60)
            print(f"RESULT {index}")

            print("\nMetadata:")
            print(document.metadata)

            print("\nContent:")
            print(document.page_content[:500])

    except Exception as e:
        print(f"\nError: {e}")