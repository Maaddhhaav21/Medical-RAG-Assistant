import re

from flask import Blueprint, jsonify, request

from app.common.logger import get_logger
from app.components.rag_chain import create_rag_chain


logger = get_logger(__name__)


api = Blueprint("api", __name__)


# --------------------------------------------------
# LOAD RAG CHAIN
# --------------------------------------------------

logger.info("Initializing RAG chain")

rag_chain = create_rag_chain(k=4)

logger.info("RAG chain initialized successfully")


# --------------------------------------------------
# CLEAN LLM RESPONSE
# --------------------------------------------------

def clean_llm_response(response_text: str) -> str:
    """
    Remove reasoning, thinking tags, and other unwanted
    internal model output before sending the answer to the user.
    """

    if not response_text:
        return ""

    cleaned_text = response_text.strip()

    # Remove complete <think>...</think> blocks
    cleaned_text = re.sub(
        r"<think>.*?</think>",
        "",
        cleaned_text,
        flags=re.DOTALL | re.IGNORECASE
    )

    # Remove everything before </think> if present
    if "</think>" in cleaned_text.lower():
        parts = re.split(
            r"</think>",
            cleaned_text,
            flags=re.IGNORECASE,
            maxsplit=1
        )

        cleaned_text = parts[-1]

    # Remove common reasoning labels
    unwanted_patterns = [
        r"<analysis>.*?</analysis>",
        r"<reasoning>.*?</reasoning>",
        r"<reflection>.*?</reflection>",
    ]

    for pattern in unwanted_patterns:
        cleaned_text = re.sub(
            pattern,
            "",
            cleaned_text,
            flags=re.DOTALL | re.IGNORECASE
        )

    # Remove any remaining opening/closing think tags
    cleaned_text = re.sub(
        r"</?think>",
        "",
        cleaned_text,
        flags=re.IGNORECASE
    )

    return cleaned_text.strip()


# --------------------------------------------------
# HEALTH CHECK
# --------------------------------------------------

@api.route("/health", methods=["GET"])
def health_check():
    """
    Check whether the API is running.
    """

    return jsonify(
        {
            "status": "success",
            "message": "Medical RAG API is running"
        }
    ), 200


# --------------------------------------------------
# ASK QUESTION
# --------------------------------------------------

@api.route("/ask", methods=["POST"])
def ask_question():
    """
    Ask a medical question.
    """

    try:

        data = request.get_json()

        if not data:
            return jsonify(
                {
                    "status": "error",
                    "message": "Request body must contain JSON data"
                }
            ), 400

        question = data.get("question", "").strip()

        if not question:
            return jsonify(
                {
                    "status": "error",
                    "message": "Question cannot be empty"
                }
            ), 400

        logger.info(
            f"Received question: {question}"
        )

        # Invoke RAG chain
        response = rag_chain.invoke(question)

        # Get raw response
        raw_answer = response.content

        logger.info(
            f"Raw LLM response received: {len(raw_answer)} characters"
        )

        # Clean reasoning / thinking output
        answer = clean_llm_response(raw_answer)

        logger.info(
            "Answer generated and cleaned successfully"
        )

        return jsonify(
            {
                "status": "success",
                "question": question,
                "answer": answer
            }
        ), 200

    except Exception as e:

        logger.exception(
            f"Failed to process question: {str(e)}"
        )

        return jsonify(
            {
                "status": "error",
                "message": "Failed to generate an answer"
            }
        ), 500