<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/a544c763-e9bb-47ef-b5bf-3bea9b7f6334" />
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/cdf77859-e8b5-4ab0-9e05-275acc680736" />
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/2abe5fb3-df22-4f48-ad70-ac1661b00505" />

<div align="center">
  <h1 align="center">🛡️ OWASP Security Assistant (RAG)</h1>
  <h3 align="center">Retrieval-Augmented Generation Chatbot for Web Security</h3>
  
  <p align="center">
    <a href="#features">Features</a> •
    <a href="#architecture">Architecture</a> •
    <a href="#installation">Installation</a> •
    <a href="#usage">Usage</a>
  </p>
  
  <p align="center">
    <img alt="Python" src="https://img.shields.io/badge/Python-3.9%2B-blue.svg">
    <img alt="Streamlit" src="https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white">
    <img alt="Gemini" src="https://img.shields.io/badge/Google%20Gemini-8E75B2?style=flat&logo=google&logoColor=white">
    <img alt="Pinecone" src="https://img.shields.io/badge/Pinecone-Vector_DB-green">
  </p>
</div>

A specialized cybersecurity chatbot that combines **Google's Gemini 1.5 Flash** model with a **Retrieval-Augmented Generation (RAG)** engine. Unlike standard AI models, this tool can ingest your specific security documents (PDFs, text files, OWASP guides) into a **Pinecone vector database** to provide accurate, source-cited answers about vulnerabilities, remediation, and company-specific policies.

---

<a id="features"></a>
## 🚀 Key Features

<table>
  <tr>
    <td width="50%">
      <h3>🧠 RAG Intelligence</h3>
      <ul>
        <li><b>Custom Knowledge Base:</b> Ingest your own .txt files (policies, cheat sheets) so the bot knows <i>your</i> context.</li>
        <li><b>Vector Search:</b> Uses <code>all-MiniLM-L6-v2</code> embeddings and Pinecone for high-accuracy retrieval.</li>
        <li><b>Source Citing:</b> The bot tells you exactly which document it used to answer the question.</li>
      </ul>
    </td>
    <td width="50%">
      <h3>🤖 Powerful LLM Backend</h3>
      <ul>
        <li><b>Gemini 1.5 Flash:</b> High-speed, large context window (8k+ tokens) for detailed explanations.</li>
        <li><b>Safety Filter Bypass:</b> Configured to allow "Dangerous Content" discussions (essential for explaining attacks like SQLi/XSS).</li>
        <li><b>Context Aware:</b> Remembers previous turns in the conversation.</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td>
      <h3>💻 Interactive UI</h3>
      <ul>
        <li><b>Streamlit Interface:</b> Clean, web-based chat interface.</li>
        <li><b>Real-time formatting:</b> Renders code blocks, markdown, and security alerts beautifully.</li>
        <li><b>Session Management:</b> Clear history and restart sessions easily.</li>
      </ul>
    </td>
    <td>
      <h3>🛡️ Security Specialized</h3>
      <ul>
        <li><b>OWASP Knowledge:</b> Pre-prompted with specific instructions for OWASP Top 10 categories.</li>
        <li><b>Dynamic Guidance:</b> Automatically adjusts advice based on the vulnerability type (e.g., specific Python code for SQLi).</li>
      </ul>
    </td>
  </tr>
</table>

---

<a id="architecture"></a>
## 🏗️ Architecture

The system moves away from purely local models to a hybrid cloud approach for performance and scalability:

1.  **Ingestion:** Python script (`ingest.py`) reads text files -> Converts to Vectors (SentenceTransformers) -> Uploads to Pinecone.
2.  **Retrieval:** User asks a question -> System finds top 5 relevant chunks from Pinecone.
3.  **Generation:** Relevant chunks + User Question are sent to Gemini 1.5 Flash to generate a unified, accurate answer.

---

## 📁 Project Structure

```text
OWASP_BERT/
├── app.py                  # Main Streamlit Web Application
├── ingest.py               # Script to upload your documents to Pinecone
├── chatbot_modules/        # Core Logic
│   ├── chatbot.py          # Orchestrator
│   ├── components.py       # Initializes Pinecone/Models
│   ├── retrieval.py        # RAG Logic (Search & Rerank)
│   ├── llm_service.py      # Google Gemini API Handler
│   ├── config.py           # Settings (API Keys, Paths)
│   └── ...
├── data/                   # Folder where you put your .txt files to be ingested
├── Prompt_Templates/       # System prompts for the LLM
└── legacy_code/            # (Optional) Old notebooks/BERT experiments
```
<a id="installation"></a>
## ⚙️ Installation

### 1. Prerequisites
* Python 3.9+
* A **Google Gemini API Key** (Free tier available at [aistudio.google.com](https://aistudio.google.com/))
* A **Pinecone API Key** (Free tier available at [pinecone.io](https://www.pinecone.io/))

### 2. Setup

Clone the repository and install dependencies:

```bash
# Install required packages
pip install -r requirements.txt
# Ensure Pinecone and Streamlit are installed
pip install pinecone streamlit google-generativeai sentence-transformers python-dotenv
```

### 3. Environment Variables

Create a `.env` file in the root directory:

```ini
GEMINI_API_KEY=your_gemini_key_here
PINECONE_API_KEY=your_pinecone_key_here
PINECONE_ENVIRONMENT=us-east-1
```

---

<a id="usage"></a>
## 🎯 Usage Workflow

### Step 1: Add Knowledge (Ingestion)
The bot starts with an empty brain. You must feed it data.

1.  Create a folder named `data` in the root directory.
2.  Add `.txt` files containing security info (e.g., `OWASP_Top_10.txt`, `Company_Policy.txt`).
3.  Run the ingestion script:

```bash
python ingest.py
```
*Output: "✅ Ingestion Complete! Your bot now has knowledge."*

### Step 2: Run the Chatbot
Launch the web interface:

```bash
python -m streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`.

---

## 🔧 Configuration (`config.py`)

You can tweak the bot's behavior in `chatbot_modules/config.py`:

```python
CONFIG = {
    "USE_PINECONE": True,           # Enable RAG
    "USE_LOCAL_LLM": False,         # Keep False (We are using Gemini)
    "EMBEDDING_MODEL_PATH": "all-MiniLM-L6-v2",
    "MAX_CONTEXT_TOKENS": 2500,     # How much text to read from documents
    "TEMPERATURE": 0.7,             # Creativity (0.0 = Strict, 1.0 = Creative)
}
```

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request
