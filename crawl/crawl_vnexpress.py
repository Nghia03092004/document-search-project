import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm
import time
import os

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

CATEGORIES = {
    "suc-khoe": "https://vnexpress.net/suc-khoe",
    "kinh-doanh": "https://vnexpress.net/kinh-doanh",
    "giao-duc": "https://vnexpress.net/giao-duc",
    "khoa-hoc": "https://vnexpress.net/khoa-hoc",
    "cong-nghe": "https://vnexpress.net/so-hoa",
    "thoi-su": "https://vnexpress.net/thoi-su",
    "the-thao": "https://vnexpress.net/the-thao",
}

SAVE_PATH = "data/raw/articles.csv"
MAX_ARTICLES = 50000
DELAY = 0.5


def get_article_links(category_url, max_pages=200):
    links = set()

    for page in range(1, max_pages + 1):
        url = f"{category_url}-p{page}"
        try:
            res = requests.get(url, headers=HEADERS, timeout=10)
            soup = BeautifulSoup(res.text, "lxml")

            for a in soup.find_all("a", href=True):
                href = a["href"]
                if (
                    href.startswith("https://vnexpress.net")
                    and href.endswith(".html")
                    and "video" not in href
                ):
                    links.add(href)

            time.sleep(DELAY)
        except Exception:
            continue

    return links


def crawl_article(url):
    res = requests.get(url, headers=HEADERS, timeout=10)
    soup = BeautifulSoup(res.text, "lxml")

    title_tag = soup.find("h1")
    title = title_tag.text.strip() if title_tag else ""

    paragraphs = soup.select("article p")
    content = " ".join(p.text.strip() for p in paragraphs)

    return title, content


def main():
    os.makedirs("data/raw", exist_ok=True)

    all_links = []
    link_category = {}

    print("Collecting links")
    for cat, cat_url in CATEGORIES.items():
        links = get_article_links(cat_url)
        print(f"  {cat}: {len(links)} links")

        for link in links:
            link_category[link] = cat
        all_links.extend(links)

    all_links = list(set(all_links))
    print(f"Total unique links: {len(all_links)}")

    data = []
    for url in tqdm(all_links[:MAX_ARTICLES]):
        try:
            title, content = crawl_article(url)
            if len(content) > 300:
                data.append({
                    "url": url,
                    "title": title,
                    "content": content,
                    "category": link_category.get(url, "unknown")
                })
            time.sleep(DELAY)
        except Exception:
            continue

    df = pd.DataFrame(data)
    df.to_csv(SAVE_PATH, index=False, encoding="utf-8-sig")
    print(f"FINISH: saved {len(df)} articles to {SAVE_PATH}")


if __name__ == "__main__":
    main()
