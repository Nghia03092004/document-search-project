from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

import numpy as np
import faiss
import pickle
import math
from sentence_transformers import SentenceTransformer

app = FastAPI()

# Load model + index
model = SentenceTransformer(
    "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)

index = faiss.read_index("data/faiss.index")

with open("data/chunks.pkl", "rb") as f:
    chunks = pickle.load(f)


class QueryRequest(BaseModel):
    query: str
    top_k: int = 3


@app.post("/query")
def query_docs(req: QueryRequest):
    print("👉 Received query:", req.query, "top_k:", req.top_k)

    # Encode query
    q_emb = model.encode([req.query])
    q_emb = np.array(q_emb, dtype="float32")

    # Search
    scores, ids = index.search(q_emb, req.top_k)

    results = []

    for i in range(len(ids[0])):
        idx = int(ids[0][i])
        score = float(scores[0][i])

        if math.isnan(score) or math.isinf(score):
            score = 0.0

        text = chunks[idx]

        if not isinstance(text, str):
            text = str(text)

        results.append({
            "id": idx,
            "score": score,
            "text": text
        })

    payload = {
        "query": req.query,
        "results": results
    }

    payload = jsonable_encoder(payload)

    return JSONResponse(content=payload)
