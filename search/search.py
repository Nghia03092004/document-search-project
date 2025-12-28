import os
import pickle
import faiss
from sentence_transformers import SentenceTransformer

# ===== 1. Đường dẫn =====
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FAISS_DIR = os.path.join(BASE_DIR, "../faiss_index")

FAISS_PATH = os.path.join(FAISS_DIR, "index.faiss")
CHUNKS_PATH = os.path.join(FAISS_DIR, "chunks.pkl")

# ===== 2. Load index và data =====
if not os.path.exists(FAISS_PATH) or not os.path.exists(CHUNKS_PATH):
    raise FileNotFoundError("Chưa có index. Chạy build_index.py trước.")

index = faiss.read_index(FAISS_PATH)

with open(CHUNKS_PATH, "rb") as f:
    chunks = pickle.load(f)

print(f"Loaded FAISS index with {index.ntotal} vectors.")

# ===== 3. Load model =====
model = SentenceTransformer(
    "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)

# ===== 4. Hàm search =====
def search(query, top_k=5, threshold=0.35):
    """
    Semantic search đơn giản
    - query: câu hỏi
    - top_k: số kết quả lấy ra
    - threshold: điểm similarity tối thiểu
    """

    query_emb = model.encode(
        [query],
        normalize_embeddings=True
    )

    scores, indices = index.search(query_emb, top_k)

    results = []
    for score, idx in zip(scores[0], indices[0]):
        if score < threshold:
            continue
        results.append((chunks[idx], float(score)))

    return results

# ===== 5. Test trực tiếp =====
if __name__ == "__main__":
    print("Nhập query (gõ 'exit' để thoát)")
    while True:
        q = input("Query> ").strip()
        if q.lower() in ["exit", "quit"]:
            break

        results = search(q)

        if not results:
            print("❌ Không tìm thấy nội dung phù hợp.")
            print("=" * 60)
            continue

        print("\nTop results:")
        for i, (text, score) in enumerate(results, 1):
            preview = text[:200].replace("\n", " ")
            print(f"{i}. ({score:.4f}) {preview}...")

        print("=" * 60)
