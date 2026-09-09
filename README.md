# 🩺 Medical RAG Assistant

A production-ready Retrieval-Augmented Generation (RAG) application for answering medical questions using information retrieved from a medical knowledge base.

The application combines **FAISS**, **HuggingFace embeddings**, **LangChain**, **Groq LLMs**, **Flask**, **Docker**, **Jenkins**, and **Railway** to provide context-aware answers through an interactive web interface and REST API.

> ⚠️ **Disclaimer:** This project is intended for educational and research purposes only. It should not be considered a substitute for professional medical advice, diagnosis, or treatment.

## 🌐 Live Demo

**Railway:**  
https://medical-rag-assistant-production-b715.up.railway.app

---

## 📌 Overview

Large Language Models can sometimes generate inaccurate information or answer questions using knowledge outside a specific dataset.

This project addresses that problem using **Retrieval-Augmented Generation (RAG)**.

Instead of directly sending a user's question to the LLM, the system:

1. Receives a medical question from the user.
2. Searches a FAISS vector database for relevant medical information.
3. Retrieves the most relevant document chunks.
4. Combines the retrieved context with the user's question.
5. Sends the grounded prompt to the Groq-hosted LLM.
6. Generates and returns a context-aware answer.

The prompt is designed to keep the model grounded in the retrieved context and avoid unsupported information.

---

# 🧠 System Architecture

```text
                         ┌─────────────────────┐
                         │    User Question    │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │   Flask Web App     │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │     /api/ask        │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │     Retriever       │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │   FAISS Vector DB   │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │  Relevant Context   │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │   Prompt Template   │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │      Groq LLM       │
                         │    Qwen 3.6 27B     │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │     Final Answer    │
                         └─────────────────────┘
```

---

# ✨ Features

- Retrieval-Augmented Generation pipeline
- Medical document retrieval
- FAISS vector similarity search
- HuggingFace sentence embeddings
- LangChain-based RAG orchestration
- Groq-powered LLM inference
- Qwen 3.6 27B model
- Flask REST API
- Interactive medical chatbot interface
- Conversation history in the web UI
- Clear chat functionality
- Health-check endpoint
- Centralized logging
- Custom exception handling
- Environment-variable configuration
- Dockerized application
- Production serving with Gunicorn
- Jenkins CI pipeline
- Trivy container security scanning
- Railway deployment

---

# 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.12 | Core programming language |
| Flask | Backend web framework |
| LangChain | RAG pipeline orchestration |
| FAISS | Vector database and similarity search |
| HuggingFace | Text embedding generation |
| `all-MiniLM-L6-v2` | Embedding model |
| Groq | LLM inference |
| Qwen 3.6 27B | Language model |
| HTML / CSS | Frontend |
| JavaScript | Frontend interactions |
| Docker | Containerization |
| Gunicorn | Production WSGI server |
| Jenkins | Continuous integration |
| Trivy | Container security scanning |
| Railway | Cloud deployment |

---

# 📂 Project Structure

```text
Medical-RAG-Assistant/
│
├── app/
│   ├── common/
│   │   ├── custom_exception.py
│   │   └── logger.py
│   │
│   ├── components/
│   │   ├── document_loader.py
│   │   ├── embeddings.py
│   │   ├── ingestion.py
│   │   ├── llm.py
│   │   ├── rag_chain.py
│   │   ├── retriever.py
│   │   ├── text_splitter.py
│   │   └── vector_store.py
│   │
│   ├── config/
│   │   └── config.py
│   │
│   ├── routes/
│   │   └── api.py
│   │
│   ├── templates/
│   │   └── index.html
│   │
│   └── application.py
│
├── custom_jenkins/
│   └── Dockerfile
│
├── data/
│   └── raw/
│       └── anatomy_and_physiology.pdf
│
├── vectorstore/
│   └── faiss_index/
│       ├── index.faiss
│       └── index.pkl
│
├── logs/
│
├── .env
├── .gitignore
├── Dockerfile
├── Jenkinsfile
├── pyproject.toml
├── requirements.txt
├── uv.lock
└── README.md
```

---

# 🔄 How It Works

## 1. Document Processing

Medical documents are loaded and divided into smaller text chunks.

```text
Medical Documents
        ↓
Document Loading
        ↓
Text Splitting
        ↓
Document Chunks
```

Chunking allows the retriever to find more focused and relevant information.

---

## 2. Embedding Generation

Each document chunk is converted into a numerical vector using the HuggingFace embedding model:

```text
sentence-transformers/all-MiniLM-L6-v2
```

The embedding model produces **384-dimensional vectors**.

```text
Document Chunk
      ↓
Embedding Model
      ↓
Vector Representation
```

---

## 3. FAISS Vector Storage

The generated embeddings are stored in a FAISS vector index.

```text
Document Chunks
      ↓
Generate Embeddings
      ↓
FAISS Vector Store
```

The generated index is stored at:

```text
vectorstore/faiss_index/
├── index.faiss
└── index.pkl
```

---

## 4. User Question

The user enters a medical question through the web interface.

Example:

```text
What are the major functions of the heart?
```

The frontend sends the question to the Flask backend.

---

## 5. Document Retrieval

The retriever searches the FAISS vector store for the most relevant document chunks.

```text
User Question
      ↓
Similarity Search
      ↓
FAISS Vector Database
      ↓
Relevant Documents
```

---

## 6. Prompt Construction

The retrieved documents are combined with the user's question using the RAG prompt template.

```text
Retrieved Context
        +
User Question
        ↓
Prompt Template
```

The prompt instructs the model to answer using the supplied context and not reveal internal reasoning.

---

## 7. Answer Generation

The final prompt is sent to the Groq-hosted Qwen model.

```text
Context + Question
        ↓
     Groq LLM
        ↓
   Final Answer
```

The answer is returned by the Flask API and rendered in the web interface.

---

# 🧠 RAG Chain

The complete RAG pipeline follows this flow:

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
│  FAISS Search │
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
┌────────────────┐
│ Prompt Template│
└───────┬────────┘
        │
        ▼
┌───────────────┐
│   Groq LLM    │
└───────┬───────┘
        │
        ▼
   Final Answer
```

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
git clone https://github.com/Maaddhhaav21/Medical-RAG-Assistant.git
cd Medical-RAG-Assistant
```

---

## 2. Create a Virtual Environment

Using `uv`:

```bash
uv venv
source .venv/bin/activate
```

On Windows:

```bash
.venv\Scripts\activate
```

Alternatively, using Python directly:

```bash
python -m venv .venv
```

---

## 3. Install Dependencies

Using `uv`:

```bash
uv sync
```

Or using pip:

```bash
pip install -r requirements.txt
```

---

# 🔐 Environment Variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
```

Never commit your API key to GitHub.

The `.gitignore` should contain entries such as:

```text
.env
.venv/
__pycache__/
*.pyc
logs/
```

---

# ▶️ Running Locally

Start the Flask application:

```bash
python app/application.py
```

The application runs on:

```text
http://127.0.0.1:5001
```

Open the address in your browser to access the Medical RAG Assistant.

---

# 🧪 Testing the RAG Pipeline

The RAG chain can be tested directly through the application components.

Example:

```python
test_question = "What are the major functions of the heart?"

response = rag_chain.invoke(test_question)

print(response.content)
```

This retrieves relevant documents from FAISS and generates an answer using the configured LLM.

---

# 🤖 LLM Configuration

The application uses Groq for LLM inference.

The model is configured in:

```text
app/components/llm.py
```

Current model:

```text
qwen/qwen3.6-27b
```

The application uses a low temperature for focused responses and disables exposed reasoning output.

Example configuration:

```python
llm = ChatGroq(
    model="qwen/qwen3.6-27b",
    temperature=0.2,
    max_tokens=1024,
    reasoning_effort="none",
    reasoning_format="hidden",
    groq_api_key=GROQ_API_KEY,
)
```

---

# 🛡️ Error Handling

The application includes handling for common scenarios such as:

- Missing JSON request data
- Empty user questions
- Missing API keys
- RAG pipeline failures
- LLM loading failures
- Vector store failures

Errors are logged through the application's centralized logging system.

---

# 🐳 Docker

The application includes a production Dockerfile and runs using Gunicorn.

## Build the Image

```bash
docker build -t medical-rag .
```

## Run the Container

```bash
docker run -p 5001:5001 --env-file .env medical-rag
```

The application will be available at:

```text
http://localhost:5001
```

The container starts the Flask application with:

```text
gunicorn --bind 0.0.0.0:5001 app.application:app
```

---

# 🔄 CI/CD with Jenkins

The project includes a Jenkins pipeline for continuous integration.

The Jenkins pipeline performs steps such as:

```text
GitHub Checkout
      ↓
Environment Check
      ↓
Install Dependencies
      ↓
Run Tests
      ↓
Build Docker Image
      ↓
Trivy Security Scan
```

The pipeline configuration is stored in:

```text
Jenkinsfile
```

Jenkins is run using a custom Docker image defined in:

```text
custom_jenkins/Dockerfile
```

---

# 🔒 Container Security

Trivy is used to scan the Docker image for vulnerabilities.

Example:

```bash
trivy image --severity HIGH,CRITICAL medical-rag-app:latest
```

This helps identify high- and critical-severity vulnerabilities in the container image.

---

# ☁️ Railway Deployment

The application is deployed to Railway using the GitHub repository.

## Production URL

```text
https://medical-rag-assistant-production-b715.up.railway.app
```

The Railway service runs the Dockerized application using Gunicorn.

The required production environment variable is:

```text
GROQ_API_KEY
```

Railway deploys the application from the `main` branch.

---

# 🔁 Deployment Architecture

```text
                 GitHub
                   │
                   ├──────────────► Railway
                   │                  │
                   │                  ▼
                   │             Docker Build
                   │                  │
                   │                  ▼
                   │          Gunicorn + Flask
                   │                  │
                   │                  ▼
                   │          Public RAG App
                   │
                   ▼
                Jenkins
                   │
                   ├── Tests
                   ├── Docker Build
                   └── Trivy Scan
```

---

# 📊 Current Project Details

The current knowledge base contains the medical content used to build the FAISS index.

The ingestion pipeline produced:

```text
Readable document pages: 1345
Text chunks:              6217
Embedding dimension:       384
Embedding model:           all-MiniLM-L6-v2
```

The stored vector index is located at:

```text
vectorstore/faiss_index/
```

---

# 🚀 Future Improvements

- Source citations for generated answers
- Streaming LLM responses
- User authentication
- Persistent chat history
- PostgreSQL integration
- Reranking retrieved documents
- Hybrid search
- Redis caching
- User feedback collection
- RAG evaluation metrics
- Automated RAG evaluation
- Monitoring and observability
- Kubernetes deployment

---

# 👨‍💻 Author

**Madhav Manoj**

---

## ⚠️ Disclaimer

This application is a technical demonstration of a Retrieval-Augmented Generation system for educational and research purposes. It is not a medical diagnostic tool and should not replace advice from qualified healthcare professionals.
