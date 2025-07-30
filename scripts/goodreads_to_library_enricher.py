import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import urllib3
import random

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def search_library_by_title_author(title, author):
    base_url = "https://dlc.lib.de.us/client/en_US/default/search/results"
    query = f"{title} {author}"
    params = {
        "qu": query,
        "te": "ERC_ST_DEFAULT"
    }
    headers = {
        "User-Agent": "GoodreadsLibraryChecker/1.0"
    }

    try:
        response = requests.get(base_url, params=params, headers=headers, timeout=10, verify=False)
        
        if response.status_code != 200:
            return "Not found", "Unknown", "Unknown"

        soup = BeautifulSoup(response.text, "html.parser")
        format_spans = soup.find_all("span", class_="navigatorName")

        formats = []
        for span in format_spans:
            a_tag = span.find("a", href=True)
            if a_tag and "qf=ERC_FORMAT" in a_tag["href"]:
                text = a_tag.text.strip()
                if text:
                    formats.append(text)

        return formats

    except Exception:
        return "Error", "Error", "Error"

# Load the cleaned CSV
df = pd.read_csv("files/cleaned_to_read_list.csv")

# Loop through books and enrich
for idx, row in df.iterrows():
    book = df.iloc[idx]
    title = book["Title"]
    author = book["Author"]

    formats = search_library_by_title_author(title, author)

    df.at[idx, 'Available Formats'] = str(formats)
    print(f"\n📚 Title: {title}")
    print(f"📦 Formats: {formats}")

    time.sleep(random.uniform(2, 4))

# Save the enriched file
output_file = "files/enriched_to_read_list.csv"
df.to_csv(output_file, index=False)
print(f"\n✅ Enriched CSV saved as: {output_file}")