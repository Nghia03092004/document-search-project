import pandas as pd
import re
from tqdm import tqdm
from pathlib import Path

INPUT_PATH = "data/raw/articles.csv"
OUTPUT_PATH = "data/processed/chunks.csv"

CHUNK_SIZE = 300

Path("data/processed").mkdir(parents=True, exist_ok=True)

def clean_text(text):
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    text = re.sub(
        r"[^\w\sàáạảãâầấậẩẫăằắặẳẵ"
        r"èéẹẻẽêềếệểễ"
        r"ìíịỉĩ"
        r"òóọỏõôồốộổỗơờớợởỡ"
        r"ùúụủũưừứựửữ"
        r"ỳýỵỷỹđ]",
        " ",
        text
    )
    return text.strip()

def chunk_text(text, size):
    words = text.split()
    chunks = []

    for i in range(0, len(words), size):
        chunk = " ".join(words[i:i+size])
        if len(chunk) > 50:
            chunks.append(chunk)

    return chunks

def main():
    df = pd.read_csv(INPUT_PATH)
    all_chunks = []

    for _, row in tqdm(df.iterrows(), total=len(df)):
        content = clean_text(str(row["content"]))
        chunks = chunk_text(content, CHUNK_SIZE)

        for chunk in chunks:
            all_chunks.append({
                "url": row["url"],
                "title": row["title"],
                "category": row["category"],
                "text": chunk
            })

    out_df = pd.DataFrame(all_chunks)
    out_df.to_csv(OUTPUT_PATH, index=False, encoding="utf-8-sig")

    print("Chunks saved:", OUTPUT_PATH)
    print("Total chunks:", len(out_df))

if __name__ == "__main__":
    main()
