from collections import Counter
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

start = time.time()

BASE_URL = "https://mcp.so"
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; TeddyBot/1.0)"}
VERBOSE = False

# ---------- Stage 1: collect all server cards across pages ----------
records = []
seen_urls = set()
page_counts = []

for page in tqdm(range(1, 273), desc="Collecting server links"):
    url = f"{BASE_URL}/servers?page={page}"
    try:
        r = requests.get(url, headers=HEADERS)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        cards = soup.select("a[href^='/server/']")
        if not cards:
            print(f"⚠️ No cards found on page {page}, stopping.")
            break

        new_urls = 0
        for c in cards:
            title_elem = c.find(["h2", "h3", "h4"])
            desc_elem  = c.find("p")
            href = BASE_URL + c["href"]
            if href not in seen_urls:
                seen_urls.add(href)
                records.append({
                    "page": page,
                    "title": title_elem.get_text(strip=True) if title_elem else None,
                    "description": desc_elem.get_text(strip=True) if desc_elem else None,
                    "url": href
                })
                new_urls += 1

        page_counts.append((page, len(cards), new_urls))
        if page % 25 == 0:
            print(f"Page {page}: {len(cards)} cards, {new_urls} new, total unique so far {len(seen_urls)}")
        time.sleep(0.15)

    except Exception as e:
        print(f"⚠️ failed page {page}: {e}")
        continue

df = pd.DataFrame(records)
print(f"\n✅ Collected {len(df)} unique URLs after deduping.")
print(f"Total pages scraped: {len(page_counts)}")

# Optional: check if new URLs dry up
no_new = [p for p, cards, new in page_counts if new == 0]
if no_new:
    print(f"⚠️ Pages with zero new URLs: {no_new[:10]} ...")

# Optional: show distribution of URLs per page
print("\nTop 10 pages by # of new URLs:")
for p, cards, new in sorted(page_counts, key=lambda x: -x[2])[:10]:
    print(f"  Page {p}: {new} new / {cards} total cards")

# ---------- Continue with detail scraping ----------
def scrape_detail(row):
    rec = row.to_dict()
    try:
        r2 = requests.get(rec["url"], headers=HEADERS, timeout=10)
        r2.raise_for_status()
        s2 = BeautifulSoup(r2.text, "html.parser")

        time_div = s2.find(
            "div",
            class_="bg-secondary border-secondary text-secondary-foreground px-2 py-1 rounded-full text-xs truncate flex items-center gap-1",
        )
        rec["uploaded"] = time_div.get_text(strip=True) if time_div else None

        usecase_header = s2.find(
            lambda tag: tag.name in ["h2", "h3", "h4"]
            and "use case" in tag.get_text(strip=True).lower()
        )
        if usecase_header:
            texts = []
            for sib in usecase_header.find_next_siblings():
                if sib.name in ["h2", "h3", "h4"]:
                    break
                if sib.name in ["script", "style"]:
                    continue
                txt = sib.get_text(" ", strip=True)
                if txt:
                    texts.append(txt)
            rec["use_cases"] = " ".join(texts) if texts else None
        else:
            rec["use_cases"] = None
    except Exception as e:
        rec["uploaded"], rec["use_cases"] = None, None
        if VERBOSE:
            print(f"⚠️ failed on {rec['url']}: {e}")
    return rec

results = []
with ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(scrape_detail, row) for _, row in df.iterrows()]
    for f in tqdm(as_completed(futures), total=len(futures), desc="Scraping detail pages"):
        results.append(f.result())

df_out = pd.DataFrame(results)
out_path = "mcp/data/mcp_desc_all_nov_7_debug.csv"
df_out.to_csv(out_path, index=False)
print(f"\n✅ saved {len(df_out)} rows to {out_path}")
print("Elapsed:", round(time.time() - start, 2), "seconds")
