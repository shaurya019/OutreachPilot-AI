import re
from typing import Dict, List
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup


MAX_CHARS = 12000


def clean_text(text: str) -> str:
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def is_internal_link(base_url: str, link: str) -> bool:
    base_domain = urlparse(base_url).netloc.replace("www.", "")
    link_domain = urlparse(link).netloc.replace("www.", "")

    return not link_domain or base_domain == link_domain


def fetch_page_text(url: str) -> Dict[str, str | None]:
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 OutreachPilotAI/1.0"
        }

        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        for tag in soup(["script", "style", "noscript", "svg"]):
            tag.decompose()

        title = soup.title.string.strip() if soup.title and soup.title.string else ""
        text = clean_text(soup.get_text(separator=" "))

        return {
            "url": url,
            "title": title,
            "text": text[:MAX_CHARS],
            "error": None,
        }

    except Exception as exc:
        return {
            "url": url,
            "title": "",
            "text": "",
            "error": str(exc),
        }


def discover_important_links(base_url: str, limit: int = 5) -> List[str]:
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 OutreachPilotAI/1.0"
        }

        response = requests.get(base_url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        priority_keywords = [
            "about",
            "product",
            "products",
            "platform",
            "career",
            "careers",
            "blog",
            "engineering",
            "docs",
            "solutions",
        ]

        links: List[str] = []

        for anchor in soup.find_all("a", href=True):
            href = anchor["href"]
            full_url = urljoin(base_url, href)

            if not is_internal_link(base_url, full_url):
                continue

            lower_url = full_url.lower()

            if any(keyword in lower_url for keyword in priority_keywords):
                normalized = full_url.split("#")[0]

                if normalized not in links:
                    links.append(normalized)

            if len(links) >= limit:
                break

        return links

    except Exception:
        return []


def extract_company_website_context(company_website: str) -> Dict[str, object]:
    homepage = fetch_page_text(company_website)
    important_links = discover_important_links(company_website, limit=4)

    pages = [homepage]

    for link in important_links:
        if link != company_website:
            pages.append(fetch_page_text(link))

    combined_text_parts = []

    for page in pages:
        if page.get("text"):
            combined_text_parts.append(
                f"URL: {page['url']}\nTITLE: {page['title']}\nTEXT: {page['text']}"
            )

    combined_text = "\n\n---\n\n".join(combined_text_parts)

    return {
        "pages": pages,
        "important_pages": [page["url"] for page in pages],
        "combined_text": combined_text[:MAX_CHARS],
        "errors": [page["error"] for page in pages if page.get("error")],
    }