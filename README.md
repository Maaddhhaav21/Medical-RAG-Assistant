# 🩺 Medical RAG Assistant

A Retrieval-Augmented Generation (RAG) application that answers medical questions using information retrieved from a medical knowledge base.

The application combines **FAISS**, **HuggingFace embeddings**, **LangChain**, **Groq LLMs**, and **Flask** to provide context-aware answers through an interactive web interface and REST API.

> ⚠️ **Disclaimer:** This project is intended for educational and research purposes only. It should not be considered a substitute for professional medical advice, diagnosis, or treatment.

---

## 📌 Overview

Large Language Models can sometimes generate inaccurate information or answer questions using knowledge outside a specific dataset.

This project addresses that problem using **Retrieval-Augmented Generation (RAG)**.

Instead of directly sending a user's question to the LLM, the system:

1. Receives a medical question from the user.
2. Searches a FAISS vector database for relevant medical information.
3. Retrieves the most relevant document chunks.
4. Passes the retrieved context and user question to the LLM.
5. Generates a context-aware response.

The application is instructed to answer using the retrieved context rather than relying solely on the model's general knowledge.

---

# 🧠 System Architecture

```text
                    ┌─────────────────┐
                    │   User Question │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Flask Web App   │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │   /api/ask      │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │    Retriever    │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ FAISS Vector DB │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Relevant Context│
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Prompt Template │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │    Groq LLM     │
                    │ Qwen 3.6 27B    │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │  Final Answer   │
                    └─────────────────┘
```

---

# ✨ Features

- Retrieval-Augmented Generation pipeline
- Medical document retrieval
- FAISS vector similarity search
- HuggingFace embeddings
- Groq-powered LLM inference
- LangChain-based RAG pipeline
- Flask REST API
- Interactive web interface
- Conversation history
- Clear chat functionality
- Health-check endpoint
- Centralized logging
- Custom exception handling
- Environment variable configuration

---

# 🛠️ Technology Stack

| Technology   | Purpose                               |
| ------------ | ------------------------------------- |
| Python       | Core programming language             |
| Flask        | Backend web framework                 |
| LangChain    | RAG pipeline orchestration            |
| FAISS        | Vector database and similarity search |
| HuggingFace  | Text embedding generation             |
| Groq         | High-speed LLM inference              |
| Qwen 3.6 27B | Large Language Model                  |
| HTML         | Frontend structure                    |
| CSS          | Frontend styling                      |
| JavaScript   | Frontend interactions                 |

---

# 📂 Project Structure

```text
Medical-RAG/
│
├── app/
│   │
│   ├── common/
│   │   ├── __init__.py
│   │   ├── custom_exception.py
│   │   └── logger.py
│   │
│   ├── components/
│   │   ├── __init__.py
│   │   ├── document_loader.py
│   │   ├── embedding.py
│   │   ├── llm.py
│   │   ├── rag_chain.py
│   │   ├── retriever.py
│   │   ├── text_splitter.py
│   │   └── vector_store.py
│   │
│   ├── config/
│   │   ├── __init__.py
│   │   └── config.py
│   │
│   ├── data/
│   │   └── medical_documents/
│   │
│   ├── database/
│   │   └── faiss_index/
│   │
│   ├── routes/
│   │   ├── __init__.py
│   │   └── api.py
│   │
│   ├── templates/
│   │   └── index.html
│   │
│   ├── __init__.py
│   └── application.py
│
├── logs/
├── .env
├── .gitignore
├── requirements.txt
├── Dockerfile
└── README.md
```

---

# 🔄 How It Works

## 1. Document Processing

Medical documents are loaded into the application and divided into smaller chunks.

```text
Medical Documents
        ↓
Document Loading
        ↓
Text Splitting
        ↓
Document Chunks
```

Splitting large documents into smaller chunks improves retrieval because the application can identify specific sections that are relevant to a user's question.

---

## 2. Embedding Generation

Each document chunk is converted into a numerical vector using a HuggingFace embedding model.

```text
Document Chunk
       ↓
Embedding Model
       ↓
Vector Representation
```

Embeddings capture the semantic meaning of text, allowing the application to compare a user's question with the stored medical information.

---

## 3. FAISS Vector Storage

The generated embeddings are stored in a FAISS vector database.

```text
Document Chunks
       ↓
Generate Embeddings
       ↓
FAISS Vector Store
```

FAISS enables efficient similarity searching across the medical knowledge base.

---

## 4. User Question

The user enters a question through the web interface.

Example:

```text
What are the symptoms of anemia?
```

The frontend sends the question to the Flask backend.

---

## 5. Document Retrieval

The retriever searches the FAISS vector database for the most relevant document chunks.

```text
User Question
      ↓
Similarity Search
      ↓
FAISS Vector Database
      ↓
Relevant Documents
```

The application retrieves the top relevant documents before generating an answer.

---

## 6. Prompt Construction

The retrieved documents are combined with the user's question using a prompt template.

```text
Retrieved Context
        +
User Question
        ↓
Prompt Template
```

The prompt instructs the LLM to answer based on the provided context.

---

## 7. Answer Generation

The final prompt is sent to the Groq-hosted language model.

```text
Context + Question
        ↓
      Groq LLM
        ↓
    Final Answer
```

The generated answer is returned to the Flask backend and displayed in the web interface.

---

# 🧠 RAG Chain

The core RAG pipeline follows this flow:

```text
User Question
      │
      ▼
┌───────────────┐
│   Retriever   │
└───────┬───────┘
        │
        ▼
┌───────────────┐
│ FAISS Search  │
└───────┬───────┘
        │
        ▼
Relevant Documents
        │
        ▼
┌───────────────┐
│ Format Context│
└───────┬───────┘
        │
        ▼
┌───────────────┐
│ Prompt Template│
└───────┬───────┘
        │
        ▼
┌───────────────┐
│   Groq LLM    │
└───────┬───────┘
        │
        ▼
    Final Answer
```

The RAG chain retrieves relevant documents and formats them before passing the context to the language model.

---

# 🔌 API Endpoints

## Health Check

### Endpoint

```text
GET /api/health
```

### Example Response

```json
{
  "status": "success",
  "message": "Medical RAG API is running"
}
```

---

## Ask a Medical Question

### Endpoint

```text
POST /api/ask
```

### Request Body

```json
{
  "question": "What are the symptoms of anemia?"
}
```

### Successful Response

```json
{
  "status": "success",
  "question": "What are the symptoms of anemia?",
  "answer": "..."
}
```

### Empty Question Response

```json
{
  "status": "error",
  "message": "Question cannot be empty"
}
```

---

# ⚙️ Installation

## 1. Clone the Repository

```bash
git clone <your-repository-url>
```

Navigate into the project directory:

```bash
cd Medical-RAG
```

---

## 2. Create a Virtual Environment

```bash
python -m venv .venv
```

### macOS/Linux

```bash
source .venv/bin/activate
```

### Windows

```bash
.venv\Scripts\activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔐 Environment Variables

Create a `.env` file in the root directory of the project.

```env
GROQ_API_KEY=your_groq_api_key_here
```

Do not upload your API key to GitHub.

Your `.gitignore` should include:

```text
.env
.venv/
__pycache__/
*.pyc
logs/
```

---

# ▶️ Running the Application

Start the Flask application:

```bash
python app/application.py
```

The application will run on:

```text
http://127.0.0.1:5001
```

Open this address in your browser to access the Medical RAG Assistant.

---

# 🧪 Testing the RAG Pipeline

The RAG chain can be tested directly using the test block in `rag_chain.py`.

Example:

```python
test_question = "What are the major functions of the heart?"

response = rag_chain.invoke(test_question)

print(response.content)
```

This retrieves relevant documents from the vector store and generates an answer using the configured LLM.

---

# 🤖 LLM Configuration

The application uses Groq for LLM inference.

The model is configured in `app/components/llm.py`.

```python
llm = ChatGroq(
    model="qwen/qwen3.6-27b",
    temperature=0.2,
    max_tokens=512,
    groq_api_key=GROQ_API_KEY
)
```

The lower temperature value helps generate more consistent and focused responses.

---

# 🛡️ Error Handling

The application includes error handling for common scenarios such as:

- Missing JSON request data
- Empty user questions
- Missing API keys
- RAG pipeline failures
- LLM loading errors
- Vector store errors

Errors are logged using the application's centralized logging system.

---

# 📊 Future Improvements

Potential improvements for the project include:

- Source citations for generated answers
- Streaming LLM responses
- User authentication
- Chat history persistence
- PostgreSQL database integration
- Docker Compose deployment
- CI/CD pipeline
- Kubernetes deployment
- Evaluation metrics for RAG responses
- Reranking retrieved documents
- Hybrid search
- Redis caching
- User feedback collection
- Monitoring and observability
- Automated RAG evaluation

---

# 🐳 Docker

The project can be containerized using Docker.

Build the Docker image:

```bash
docker build -t medical-rag .
```

Run the container:

```bash
docker run -p 5001:5001 --env-file .env medical-rag
```

The application should then be accessible on:

```text
http://localhost:5001
```

---

# 👨‍💻 Author

**Madhav Manoj**

---
