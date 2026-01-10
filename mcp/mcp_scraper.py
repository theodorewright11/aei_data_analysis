import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

start = time.time()

BASE_URL = "https://mcp.so"
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; TeddyBot/1.0)"}
VERBOSE = False  # set True if you want to see failed URLs

def extract_section_text(soup, header_keywords):
    header = soup.find(
        lambda tag: tag.name in ["h2", "h3", "h4"]
        and any(k in tag.get_text(strip=True).lower() for k in header_keywords)
    )
    if not header:
        return None

    texts = []
    for sib in header.find_next_siblings():
        if sib.name in ["h2", "h3", "h4"]:
            break
        if sib.name in ["script", "style"]:
            continue
        txt = sib.get_text(" ", strip=True)
        if txt:
            texts.append(txt)

    return " ".join(texts) if texts else None


# ---------- Stage 1: collect all server cards across pages ----------
records = []
for page in tqdm(range(1, 279), desc="Collecting server links"):   # adjust to (1, 279) later
    url = f"{BASE_URL}/servers?page={page}"
    try:
        r = requests.get(url, headers=HEADERS)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        cards = soup.select("a[href^='/server/']")
        if not cards:
            print(f"No cards found on page {page}, stopping.")
            break
        for c in cards:
            title_elem = c.find(["h2", "h3", "h4"])
            desc_elem  = c.find("p")
            href = BASE_URL + c["href"]
            records.append({
                "title": title_elem.get_text(strip=True) if title_elem else None,
                "description": desc_elem.get_text(strip=True) if desc_elem else None,
                "url": href
            })
        time.sleep(0.15)  # polite delay between page requests
    except Exception as e:
        print(f"⚠️ failed page {page}: {e}")
        continue

df = pd.DataFrame(records).drop_duplicates(subset="url").reset_index(drop=True)
# df = df.drop_duplicates(subset="title").reset_index(drop=True)
print(f"Collected {len(df)} unique server listings")

# ---------- Stage 2: detail-page scraping (threaded) ----------
def scrape_detail(row):
    """Fetch and parse one server page."""
    rec = row.to_dict()
    try:
        r2 = requests.get(rec["url"], headers=HEADERS, timeout=10)
        r2.raise_for_status()
        s2 = BeautifulSoup(r2.text, "html.parser")

        # uploaded time
        time_div = s2.find(
            "div",
            class_="bg-secondary border-secondary text-secondary-foreground px-2 py-1 rounded-full text-xs truncate flex items-center gap-1",
        )
        rec["uploaded"] = time_div.get_text(strip=True) if time_div else None

        # use-cases section
        rec["use_cases"] = extract_section_text(
            s2, header_keywords=["use case"]
        )

        rec["key_features"] = extract_section_text(
            s2, header_keywords=["key feature"]
        )

    except Exception as e:
        rec["uploaded"] = None
        rec["use_cases"] = None
        rec["key_features"] = None
        if VERBOSE:
            print(f"⚠️ failed on {rec['url']}: {e}")

    return rec


# use 10 threads (adjust if connection stable; 5–15 is typical)
results = []
with ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(scrape_detail, row) for _, row in df.iterrows()]
    for f in tqdm(as_completed(futures), total=len(futures), desc="Scraping detail pages"):
        results.append(f.result())

df_out = pd.DataFrame(results)

# ---------- Save ----------
out_path = "mcp/data/mcp_desc_all_jan_5.csv"
df_out.to_csv(out_path, index=False)
print(f"✅ saved {len(df_out)} rows to {out_path}")
print("Elapsed:", round(time.time() - start, 2), "seconds")
