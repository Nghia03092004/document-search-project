# Document Search Project (Vietnamese News)

A high-performance document search engine designed to crawl, process, and index Vietnamese articles from VNExpress. This project utilizes **Sentence Embeddings** and **FAISS** (Facebook AI Similarity Search) to provide semantic search capabilities, accessible via a Streamlit web interface or a REST API.

---

## 🚀 Features

- **Web Crawling:** Automated extraction of articles from VNExpress by category.
- **Text Preprocessing:** Cleaning and chunking Vietnamese text for optimal indexing.
- **Semantic Search:** Uses `sentence-transformers` to understand query intent beyond simple keywords.
- **Vector Database:** High-speed similarity search powered by FAISS.
- **Interactive UI:** A user-friendly Streamlit dashboard for real-time searching.
- **Extensible API:** Flask-based backend for easy integration with other services.

---

## 📂 Project Structure

```text
document-search-project/
├─ crawl/
│  └─ crawl_vnexpress.py   # Web crawler script
├─ data/
│  ├─ crawl/               # Raw data (articles.csv)
│  └─ processed/           # Processed text chunks (chunks.csv)
├─ preprocess/
│  └─ clean_text.py        # Text cleaning and normalization
├─ search/
│  ├─ build_index.py       # FAISS index generation
│  └─ search.py            # Search logic and CLI interface
├─ api/
│  └─ app.py               # Optional Flask API
├─ app/
│  └─ streamlit_app.py     # Streamlit web application
├─ requirements.txt        # Project dependencies
└─ README.md               # Project documentation
```

🛠️ Installation
Clone the repository:

```bash
git clone <your-repo-url>
cd document-search-project
```

Set up a Virtual Environment:

```bash
python -m venv venv
```
### Windows
```bash
venv\Scripts\activate
```
### Linux/Mac
```bash
venv/bin/activate
```
#### Install Dependencies:
```bash
pip install -r requirements.txt
```

## 📖 Usage Guide
1. Crawl Data
Extract the latest news from VNExpress. You can modify the CATEGORY_URL within the script.
```bash
python crawl/crawl_vnexpress.py
```
2. Preprocess Text
Clean the raw HTML/text and split documents into manageable chunks.
```bash
python preprocess/clean_text.py
```
3. Build Vector Index
Generate the FAISS index. This step converts text chunks into high-dimensional vectors.
```bash
python search/build_index.py
```
4. Search Documents
```bash
python search/search.py
```
#### Via Web Interface:
```bash
streamlit run app/streamlit_app.py
```
## 🛠️ Tech Stack
Data: Requests, BeautifulSoup4, Pandas

NLP: Sentence-Transformers (Vietnamese-supported models)

Vector Engine: FAISS (CPU)

Frontend: Streamlit

Backend: Flask (Optional)

## 📝 Notes

Ensure the data/crawl/ directory exists before running the crawler.

The search quality depends heavily on the embedding model used in build_index.py.

This project can be easily upgraded to a RAG (Retrieval-Augmented Generation) pipeline by connecting it to an LLM like GPT-4 or Gemini.

## 📄 License
This project is licensed under the MIT License.
