import pandas as pd
import numpy as np
import faiss
import pickle
from sentence_transformers import SentenceTransformer
from pathlib import Path

CHUNKS_PATH = "data/processed/chunks.csv"
INDEX_PATH = "data/faiss.index"
META_PATH = "data/chunks.pkl"

Path("data").mkdir(exist_ok=True)

print("Loading chunks...")
df = pd.read_csv(CHUNKS_PATH)

texts = df["text"].astype(str).tolist()

print("Total chunks:", len(texts))

model = SentenceTransformer(
    "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)

print("Encoding...")
embeddings = model.encode(
    texts,
    batch_size=32,
    show_progress_bar=True
)

embeddings = np.array(embeddings).astype("float32")

dim = embeddings.shape[1]
index = faiss.IndexFlatL2(dim)

print("Building FAISS index...")
index.add(embeddings)

faiss.write_index(index, INDEX_PATH)

meta = df[["url", "title", "category", "text"]].to_dict(orient="records")

with open(META_PATH, "wb") as f:
    pickle.dump(meta, f)

print("DONE")
