# fetch_products.py

# SHL Product Catalog Scraper

# This script crawls the SHL product catalog page, collects individual
# assessment pages and extracts:
#   - title
#   - description
#   - URL
#   - inferred test_type (K or P)
#
# Test Type Detection Logic:
#   1. Check for an explicit "Test Type" tag on the page.
#   2. If not found, scan page text for relevant keywords.
#   3. Assign "K" (Knowledge & Skills) or "P" (Personality & Behavior)

import requests
import time
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd

base_url = "https://www.shl.com"
catalog_url = "https://www.shl.com/solutions/products/product-catalog/"
out_put = "shl_catalog.csv"


def get_catalog_page_links():
    """Fetch all individual product page URLs from SHL catalog."""
    print("Fetching product catalog page links...")
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(catalog_url, headers=headers, timeout=15)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    found_links = set()
    for a_tag in soup.select("a[href]"):
        href = a_tag.get("href") or ""
        if href.startswith("/") and "/products/" in href:
            full_url = urljoin(base_url, href)
            found_links.add(full_url)

    found_links = sorted(found_links)
    print(f" Found {len(found_links)} candidate product URLs.")
    return found_links


def extract_product_details(page_url):
    """
    Extract title, description, and test type from a single product page.
    Uses both explicit and inferred detection for test_type.
    """
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(page_url, headers=headers, timeout=15)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")

        # --- Title ---
        title_el = soup.select_one("h1")
        title = title_el.get_text(strip=True) if title_el else ""

        # --- Description ---
        desc_block = soup.select_one(".product-description, .entry-content, .content")
        description = desc_block.get_text(" ", strip=True) if desc_block else soup.get_text(" ", strip=True)[:600]

        # --- Test Type Detection ---
        test_type = ""

        # (1) Explicit label check: "Test Type" mentioned on page
        for el in soup.find_all(string=True):
            text = el.strip().lower()
            if "test type" in text:
                if "personality" in text or "behavior" in text or "behaviour" in text:
                    test_type = "P"
                elif "knowledge" in text or "skill" in text:
                    test_type = "K"
                break

        # (2) Keyword inference from entire text (if not explicitly mentioned)
        if not test_type:
            page_text = soup.get_text(" ", strip=True).lower()
            if any(word in page_text for word in ["knowledge", "skill", "technical", "ability", "aptitude", "problem-solving", "cognitive", "numerical", "verbal"]):
                test_type = "K"
            elif any(word in page_text for word in ["personality", "behavior", "behaviour", "motivation", "traits", "values", "interpersonal", "emotional", "leadership"]):
                test_type = "P"

        # (3) Default fallback (still empty)
        if not test_type:
            test_type = ""

        return {
            "title": title,
            "url": page_url,
            "description": description,
            "test_type": test_type,
        }

    except Exception as e:
        print(f" Failed to parse {page_url}: {e}")
        return None


def scrape_and_export_file(output_path=out_put):
    """Scrape all catalog product pages and export to CSV."""
    links = get_catalog_page_links()
    product_rows = []

    for i, link in enumerate(links, start=1):
        data = extract_product_details(link)
        if not data:
            continue

        # Skip job solution pages
        combined_text = (data["title"] + " " + data["description"]).lower()
        if "pre-packaged" in combined_text or "job solution" in combined_text:
            continue

        product_rows.append(data)
        print(f"[{i}/{len(links)}] Scraped: {data['title'][:60]}...")
        time.sleep(0.4)  # be kind to SHL servers

    df = pd.DataFrame(product_rows)
    df.to_csv(output_path, index=False)
    print(f"\n Saved {len(df)} product rows to {output_path}\n")
    return df


if __name__ == "__main__":
    scrape_and_export_file()
