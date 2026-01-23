import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import os
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

# ---------- Configuration ----------
start = time.time()
BASE_URL = "https://mcp.so"
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; TeddyBot/1.0)"}
VERBOSE = False
IN_PATH = "mcp/data/mcp_desc_all_jan_5.csv"
OUT_PATH = "mcp/data/mcp_desc_all_jan_22.csv"
MAX_THREADS = 20  # Increased for faster scraping
DISCOVERY_THREADS = 10  # Threads for discovery phase

# Reusable session for connection pooling
session = requests.Session()
session.headers.update(HEADERS)

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

def scrape_detail(row):
    """Fetch and parse one server page."""
    rec = row.to_dict()
    try:
        r2 = session.get(rec["url"], timeout=10)
        r2.raise_for_status()
        s2 = BeautifulSoup(r2.text, "lxml")

        # uploaded time
        time_div = s2.find(
            "div",
            class_="bg-secondary border-secondary text-secondary-foreground px-2 py-1 rounded-full text-xs truncate flex items-center gap-1",
        )
        rec["uploaded"] = time_div.get_text(strip=True) if time_div else None

        # use-cases section
        rec["use_cases"] = extract_section_text(s2, header_keywords=["use case"])
        rec["key_features"] = extract_section_text(s2, header_keywords=["key feature"])

    except Exception as e:
        rec["uploaded"] = None
        rec["use_cases"] = None
        rec["key_features"] = None
        if VERBOSE:
            print(f"⚠️ failed on {rec['url']}: {e}")

    return rec

# ---------- Stage 0: Load Existing Data ----------
existing_df = pd.DataFrame()
existing_urls = set()

if os.path.exists(IN_PATH):
    existing_df = pd.read_csv(IN_PATH)
    existing_urls = set(existing_df['url'].unique())
    print(f"✅ Found {len(existing_urls)} existing records in {IN_PATH}")
else:
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    print("🆕 No existing data found. Starting fresh.")

# ---------- Stage 1: Collect Discovery Cards (Parallelized) ----------
def scrape_discovery_page(page_num):
    """Fetch one discovery page and return new server records."""
    url = f"{BASE_URL}/servers?page={page_num}"
    page_records = []
    try:
        r = session.get(url, timeout=10)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "lxml")
        cards = soup.select("a[href^='/server/']")

        for c in cards:
            href = BASE_URL + c["href"]
            if href in existing_urls:
                continue
            title_elem = c.find(["h2", "h3", "h4"])
            desc_elem = c.find("p")
            page_records.append({
                "title": title_elem.get_text(strip=True) if title_elem else None,
                "description": desc_elem.get_text(strip=True) if desc_elem else None,
                "url": href
            })
    except Exception as e:
        if VERBOSE:
            print(f"⚠️ failed page {page_num}: {e}")
    return page_records

records = []
with ThreadPoolExecutor(max_workers=DISCOVERY_THREADS) as executor:
    futures = [executor.submit(scrape_discovery_page, p) for p in range(1, 279)]
    for f in tqdm(as_completed(futures), total=len(futures), desc="Collecting server links"):
        records.extend(f.result())

df_new_links = pd.DataFrame(records).drop_duplicates(subset="url")
print(f"Found {len(df_new_links)} new server listings to scrape.")

# ---------- Stage 2: Detail-Page Scraping (Threaded) ----------
if not df_new_links.empty:
    new_results = []
    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        futures = [executor.submit(scrape_detail, row) for _, row in df_new_links.iterrows()]
        for f in tqdm(as_completed(futures), total=len(futures), desc="Scraping new detail pages"):
            new_results.append(f.result())

    # ---------- Stage 3: Merge and Save ----------
    df_new_data = pd.DataFrame(new_results)
    final_df = pd.concat([existing_df, df_new_data], ignore_index=True)
    
    # Final safety check: remove any duplicates that may have slipped through
    final_df = final_df.drop_duplicates(subset="url")
    
    final_df.to_csv(OUT_PATH, index=False)
    print(f"✅ Successfully appended {len(df_new_data)} new rows.")
else:
    print("🙌 Everything is already up to date!")

print(f"Total records now: {len(pd.read_csv(OUT_PATH))}")
print("Elapsed:", round(time.time() - start, 2), "seconds")