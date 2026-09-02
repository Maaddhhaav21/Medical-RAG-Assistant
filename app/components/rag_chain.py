from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough

from app.common.logger import get_logger
from app.common.custom_exception import CustomException

from app.components.llm import load_llm
from app.components.retriever import get_retriever


logger = get_logger(__name__)


CUSTOM_PROMPT_TEMPLATE = """
You are a Medical RAG Assistant.

Answer the user's question using ONLY the information provided in the context.

IMPORTANT RULES:
1. Use ONLY the provided context.
2. Do not use outside knowledge.
3. Do not invent or assume information that is not present in the context.
4. Do not reveal your internal reasoning process.
5. Do not output <think> or </think> tags.
6. Do not provide step-by-step internal reasoning.
7. Provide a detailed and well-explained answer when sufficient information is available.
8. Do not give an unnecessarily short answer.
9. Organize the answer into clear paragraphs.
10. Explain important concepts mentioned in the context when they are relevant to the user's question.

If the answer cannot be found in the provided context, say exactly:

"I could not find enough information in the provided documents to answer this question."

Context:
{context}

Question:
{question}

Answer:
"""


def get_prompt_template() -> PromptTemplate:
    """
    Create and return the RAG prompt template.
    """

    return PromptTemplate(
        template=CUSTOM_PROMPT_TEMPLATE,
        input_variables=[
            "context",
            "question"
        ]
    )


def format_documents(documents) -> str:
    """
    Combine retrieved documents into a single context string.
    """

    if not documents:
        return ""

    return "\n\n".join(
        document.page_content
        for document in documents
    )


def create_rag_chain(k: int = 8):

    try:

        logger.info(
            "Creating RAG chain"
        )

        # Load retriever
        retriever = get_retriever(k=k)

        # Load LLM
        llm = load_llm()

        # Create prompt
        prompt = get_prompt_template()

        # Create RAG chain
        rag_chain = (
            {
                "context": retriever | format_documents,
                "question": RunnablePassthrough()
            }
            | prompt
            | llm
        )

        logger.info(
            "RAG chain created successfully"
        )

        return rag_chain

    except CustomException:
        raise

    except Exception as e:

        error_message = CustomException(
            "Failed to create RAG chain",
            e
        )

        logger.error(
            str(error_message)
        )

        raise error_message


if __name__ == "__main__":

    try:

        rag_chain = create_rag_chain(k=4)

        test_question = (
            "What are the major functions of the heart?"
        )

        logger.info(
            f"Testing RAG chain with question: "
            f"{test_question}"
        )

        response = rag_chain.invoke(
            test_question
        )

        print("\n" + "=" * 60)
        print("RAG CHAIN TEST SUCCESSFUL")
        print("=" * 60)

        print("\nQuestion:")
        print(test_question)

        print("\nAnswer:")
        print(response.content)

    except Exception as e:

        print(
            f"\nError: {e}"
        )