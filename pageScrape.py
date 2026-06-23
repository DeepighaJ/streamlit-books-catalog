#!/usr/bin/env python3
"""
Web Scraping with BeautifulSoup - Day 1: Scrape a Single Page
Fetch the books.toscrape.com homepage, extract every book's title, price,
rating, and availability, and save the result to a CSV.
"""

import csv
from dataclasses import asdict, dataclass
from typing import List, Optional
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup, Tag  # type: ignore
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


# ---------------------------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------------------------

BASE_URL = "https://books.toscrape.com/"
OUTPUT_FILE = "books.csv"
REQUEST_TIMEOUT = 10  # seconds

# Star ratings on the site are written as words in the CSS class name.
RATING_MAP = {
    "Zero": 0,
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5,
}

# A polite, real-looking User-Agent so the server knows who's calling.
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Python Scraper - Daily Python Projects)"
}


@dataclass
class Book:
    """One scraped book. Using a dataclass instead of a dict gives us
    attribute access (book.price) and a single source of truth for the
    schema, instead of repeating field-name strings everywhere."""
    title: str
    price: float
    rating: int
    availability: str
    url: str


# ---------------------------------------------------------------------------
# FETCHING
# ---------------------------------------------------------------------------

def build_session() -> requests.Session:
    """Create a requests Session with sane defaults: shared headers and
    automatic retries on transient server/network errors."""
    session = requests.Session()
    session.headers.update(HEADERS)

    retries = Retry(
        total=3,
        backoff_factor=0.5,
        status_forcelist=(500, 502, 503, 504),
    )
    adapter = HTTPAdapter(max_retries=retries)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session


def fetch_page(session: requests.Session, url: str) -> Optional[str]:
    """Download the HTML at `url`, returning the response text or None."""
    print(f"Fetching: {url}")
    try:
        response = session.get(url, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"  \u2717 Request failed: {e}")
        return None

    size_kb = len(response.content) // 1024
    print(f"  \u2713 Status {response.status_code}, {size_kb}KB downloaded")
    return response.text


# ---------------------------------------------------------------------------
# EXTRACTION
# ---------------------------------------------------------------------------

def extract_rating(card: Tag) -> int:
    """Read the rating from <p class='star-rating X'>. We scan all classes
    for a known rating word rather than assuming it's always classes[1],
    so this keeps working even if the site adds another class."""
    rating_tag = card.find("p", class_="star-rating")
    classes = rating_tag.get("class", []) if rating_tag else []
    for cls in classes:
        if cls in RATING_MAP:
            return RATING_MAP[cls]
    return 0


def extract_book(card: Tag, base_url: str) -> Optional[Book]:
    """Extract every field for one book card; return a Book, or None if
    the card is missing an expected element (logged, not fatal)."""
    try:
        link = card.find("h3").find("a")
        price_text = card.find("p", class_="price_color").get_text()
        return Book(
            title=link["title"],
            price=float(price_text.replace("\u00A3", "").strip()),  # \u00A3 = £
            rating=extract_rating(card),
            availability=card.find("p", class_="availability").get_text(strip=True),
            url=urljoin(base_url, link["href"]),
        )
    except (AttributeError, KeyError, ValueError) as e:
        print(f"  \u2717 Skipped a malformed book card: {e}")
        return None


# ---------------------------------------------------------------------------
# DISPLAY
# ---------------------------------------------------------------------------

def stars(rating: int) -> str:
    """Render a rating as star characters for the console output."""
    return "\u2605" * rating + "\u2606" * (5 - rating)  # ★ filled, ☆ empty


def print_book_row(index: int, book: Book) -> None:
    """Print one book in a tidy aligned row."""
    title = book.title if len(book.title) <= 40 else book.title[:37] + "..."
    print(f"  {index:>2}. {title:<40}  \u00A3{book.price:>5.2f}  "
          f"{stars(book.rating)}   {book.availability}")


# ---------------------------------------------------------------------------
# SAVING
# ---------------------------------------------------------------------------

def save_to_csv(books: List[Book], path: str) -> None:
    """Write the list of books to a CSV file."""
    fieldnames = ["title", "price", "rating", "availability", "url"]
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(asdict(book) for book in books)


# ---------------------------------------------------------------------------
# SUMMARY
# ---------------------------------------------------------------------------

def print_summary(books: List[Book]) -> None:
    """Print a short summary of what was scraped."""
    if not books:
        return

    total = len(books)
    avg_price = sum(b.price for b in books) / total
    five_star = sum(1 for b in books if b.rating == 5)
    in_stock = sum(1 for b in books if "In stock" in b.availability)

    print()
    print("Summary:")
    print(f"  Books scraped:   {total}")
    print(f"  Average price:   \u00A3{avg_price:.2f}")
    print(f"  Highest rated:   {five_star} books with 5 stars")
    print(f"  All in stock:    {in_stock} books")


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

def main() -> None:
    print("=" * 80)
    print("BOOK SCRAPER \u2014 Day 1")
    print("=" * 80)
    print()

    # 1. Fetch the homepage.
    with build_session() as session:
        html = fetch_page(session, BASE_URL)
    if html is None:
        return

    # 2. Parse and find every book card.
    print("\nParsing HTML...")
    soup = BeautifulSoup(html, "lxml")
    book_cards = soup.find_all("article", class_="product_pod")
    print(f"  \u2713 Found {len(book_cards)} books on the page")

    if not book_cards:
        print("  \u2717 No books found \u2014 the page structure may have changed.")
        return

    # 3. Extract each book.
    print("\nExtracting book data...")
    books: List[Book] = []
    for card in book_cards:
        book = extract_book(card, BASE_URL)
        if book is None:
            continue
        books.append(book)
        print_book_row(len(books), book)

    if not books:
        print("  \u2717 Every card failed to parse \u2014 nothing to save.")
        return

    # 4. Save.
    print(f"\n\u2713 Scraped {len(books)} books")
    save_to_csv(books, OUTPUT_FILE)
    print(f"\u2713 Saved: {OUTPUT_FILE}")

    # 5. Summarize.
    print_summary(books)


if __name__ == "__main__":
    main()