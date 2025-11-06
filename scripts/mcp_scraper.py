import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

BASE_URL = "https://mcp.so"
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; TeddyBot/1.0)"}

# ---------- Stage 1: list page ----------
r = requests.get(f"{BASE_URL}/servers", headers=HEADERS)
r.raise_for_status()
soup = BeautifulSoup(r.text, "html.parser")
cards = soup.select("a[href^='/server/']")

records = []
for c in cards[:10]:                     # limit for testing
    title_elem = c.find(["h2", "h3", "h4"])
    desc_elem  = c.find("p")
    records.append({
        "title": title_elem.get_text(strip=True) if title_elem else None,
        "description": desc_elem.get_text(strip=True) if desc_elem else None,
        "url": BASE_URL + c["href"]
    })

# ---------- Stage 2: detail pages ----------
for rec in records:
    try:
        r2 = requests.get(rec["url"], headers=HEADERS)
        r2.raise_for_status()
        s2 = BeautifulSoup(r2.text, "html.parser")

        # uploaded time
        time_div = s2.find("div", class_="bg-secondary border-secondary text-secondary-foreground px-2 py-1 rounded-full text-xs truncate flex items-center gap-1")
        rec["uploaded"] = time_div.get_text(strip=True) if time_div else None

        # use-cases section
        usecase_header = s2.find(string=lambda t: t and "Use cases" in t)
        if usecase_header:
            # collect text in the following siblings until next header
            texts = []
            for sib in usecase_header.parent.find_next_siblings():
                if sib.name in ["h2", "h3", "h4"]:
                    break
                texts.append(sib.get_text(" ", strip=True))
            rec["use_cases"] = " ".join(texts) if texts else None
        else:
            rec["use_cases"] = None

        time.sleep(1)  # polite delay
    except Exception as e:
        rec["uploaded"], rec["use_cases"] = None, None
        print(f"⚠️  failed on {rec['url']}: {e}")

# ---------- Save ----------
df = pd.DataFrame(records)
df.to_csv("mcp_servers_usecases.csv", index=False)
print(f"✅ saved {len(df)} rows")
print(df.head(3))
