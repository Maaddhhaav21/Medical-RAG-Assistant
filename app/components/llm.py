from langchain_groq import ChatGroq

from app.common.logger import get_logger
from app.common.custom_exception import CustomException
from app.config.config import GROQ_API_KEY


logger = get_logger(__name__)


def load_llm():
    """
    Load the Groq LLM.

    Returns:
        Configured ChatGroq model.
    """

    try:
        if not GROQ_API_KEY:
            raise CustomException(
                "GROQ_API_KEY is missing"
            )

        logger.info("Loading Groq LLM")

        llm = ChatGroq(
            model="llama-3.1-8b-instant",
            temperature=0.2,
            max_tokens=512,
            groq_api_key=GROQ_API_KEY,
        )

        logger.info(
            "Groq LLM loaded successfully"
        )

        return llm

    except CustomException:
        raise

    except Exception as e:
        error_message = CustomException(
            "Failed to load Groq LLM",
            e
        )

        logger.error(str(error_message))
        raise error_message


if __name__ == "__main__":

    try:
        llm = load_llm()

        test_question = (
            "Explain the function of the heart "
            "in simple terms."
        )

        logger.info("Testing LLM")

        response = llm.invoke(
            test_question
        )

        print("\n" + "=" * 60)
        print("LLM TEST SUCCESSFUL")
        print("=" * 60)

        print("\nResponse:")
        print(response.content)

    except Exception as e:
        print(f"\nError: {e}")