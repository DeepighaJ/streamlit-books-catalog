#!/usr/bin/env python3
"""
Web Scraping with BeautifulSoup - Day 2: Multi-Page Scraping with Pagination
Scrapes all 50 pages of books.toscrape.com, follows pagination automatically,
visits each book's detail page for richer fields (UPC, stock count, category,
description), and saves everything to a single CSV.

Console output matches the expected format from the project spec:
  {n}/{total}  {title}  £{price}  {availability}
  ({stock_count})  {category}
"""

import csv
import time
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

BASE_URL    = "https://books.toscrape.com/"
OUTPUT_FILE = "all_books.csv"
REQUEST_TIMEOUT = 10   # seconds per request
REQUEST_DELAY   = 0.2  # polite pause between every request (listing + detail)

# Set to a small number for a quick test; None = scrape all 50 pages.
MAX_PAGES: Optional[int] = None

RATING_MAP = {
    "Zero": 0, "One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5,
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Python Scraper - Daily Python Projects)"
}

# Nine-column output schema: listing fields + detail fields.
FIELDNAMES = [
    "title", "price", "rating", "availability",
    "stock_count", "category", "upc", "description", "url",
]


# ---------------------------------------------------------------------------
# DATA MODEL
# ---------------------------------------------------------------------------

@dataclass
class Book:
    """
    Listing fields (from the catalog page) are populated first.
    Detail fields are filled in by enrich_with_details() immediately after.
    Using a dataclass gives attribute access and a single schema definition.
    """
    # -- from listing page --
    title:        str
    price:        float
    rating:       int
    availability: str
    url:          str
    # -- from detail page (filled in after listing extraction) --
    stock_count:  Optional[int] = None
    category:     Optional[str] = None
    upc:          Optional[str] = None
    description:  Optional[str] = None


# ---------------------------------------------------------------------------
# HTTP SESSION
# ---------------------------------------------------------------------------

def build_session() -> requests.Session:
    """
    A shared Session gives us:
      - connection pooling (reuses the TCP connection across ~1,050 requests)
      - automatic retry on transient server errors (500/502/503/504)
      - a single place to set headers for every request
    """
    session = requests.Session()
    session.headers.update(HEADERS)
    retries = Retry(
        total=3,
        backoff_factor=0.5,
        status_forcelist=(500, 502, 503, 504),
    )
    adapter = HTTPAdapter(max_retries=retries)
    session.mount("https://", adapter)
    session.mount("http://",  adapter)
    return session


def fetch_page(session: requests.Session, url: str) -> Optional[str]:
    """
    Download and return the HTML at `url`, or None on failure.
    We force UTF-8 decoding because requests guesses Latin-1 for this site,
    which turns the £ sign into the garbage string 'Â' and breaks float().
    """
    try:
        response = session.get(url, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        response.encoding = "utf-8"   # fix: don't let requests guess the encoding
        return response.text
    except requests.RequestException:
        return None


# ---------------------------------------------------------------------------
# PAGINATION
# ---------------------------------------------------------------------------

def find_next_url(soup: BeautifulSoup, current_url: str) -> Optional[str]:
    """
    Return the absolute URL of the next catalog page, or None on the last page.

    The site puts this at the bottom of every page (except the last):
        <li class="next"><a href="page-2.html">next</a></li>

    We read it from the page itself rather than hardcoding page-1 through
    page-50, so this works even if the catalog grows beyond 50 pages.

    urljoin() is essential here: pages 2-50 use relative hrefs like
    "page-3.html", which must be resolved against the *current* page's URL
    (not BASE_URL) to produce a correct absolute URL.
    """
    next_li = soup.find("li", class_="next")
    if next_li is None:
        return None   # we've reached the last page
    next_href = next_li.find("a")["href"]
    return urljoin(current_url, next_href)


def extract_total_pages(soup: BeautifulSoup) -> Optional[int]:
    """Read 'Page 1 of 50' from the pager for progress display."""
    pager = soup.find("li", class_="current")
    if pager is None:
        return None
    parts = pager.get_text(strip=True).split()
    # parts looks like ["Page", "1", "of", "50"]
    if len(parts) >= 4 and parts[2].lower() == "of":
        try:
            return int(parts[3])
        except ValueError:
            return None
    return None


# ---------------------------------------------------------------------------
# LISTING PAGE EXTRACTION
# ---------------------------------------------------------------------------

def extract_rating(card: Tag) -> int:
    """
    The star rating is encoded as a word in the CSS class, e.g.:
        <p class="star-rating Three">
    We scan all classes for a known rating word rather than assuming it is
    always classes[1], so this survives the site adding another class later.
    """
    rating_tag = card.find("p", class_="star-rating")
    classes = rating_tag.get("class", []) if rating_tag else []
    for cls in classes:
        if cls in RATING_MAP:
            return RATING_MAP[cls]
    return 0


def extract_book_from_card(card: Tag, page_url: str) -> Optional[Book]:
    """
    Pull listing-level fields from one <article class="product_pod"> card.

    We pass `page_url` (not BASE_URL) as the resolution base for relative
    hrefs because catalog pages 2-50 live at a different path than page 1,
    and their relative links resolve differently.
    """
    try:
        link       = card.find("h3").find("a")
        price_text = card.find("p", class_="price_color").get_text()
        return Book(
            title        = link["title"],
            # Strip the £ symbol before converting to float.
            # \u00A3 is the Unicode code point for £.
            price        = float(price_text.replace("\u00A3", "").strip()),
            rating       = extract_rating(card),
            availability = card.find("p", class_="availability").get_text(strip=True),
            url          = urljoin(page_url, link["href"]),
        )
    except (AttributeError, KeyError, ValueError) as exc:
        print(f"    \u2717 Skipped a malformed book card: {exc}")
        return None


# ---------------------------------------------------------------------------
# DETAIL PAGE EXTRACTION
# ---------------------------------------------------------------------------

def extract_upc(soup: BeautifulSoup) -> Optional[str]:
    """The UPC lives in a <table> row where the header cell says 'UPC'."""
    upc_th = soup.find("th", string="UPC")
    if upc_th is None:
        return None
    td = upc_th.find_next_sibling("td")
    return td.get_text(strip=True) if td else None


def extract_stock_count(soup: BeautifulSoup) -> Optional[int]:
    """
    The availability paragraph on the detail page reads:
        'In stock (22 available)'
    We pull out every digit from that text to get just the number.
    """
    avail = soup.find("p", class_="availability")
    if avail is None:
        return None
    digits = "".join(ch for ch in avail.get_text() if ch.isdigit())
    return int(digits) if digits else None


def extract_category(soup: BeautifulSoup) -> Optional[str]:
    """
    The breadcrumb trail is:  Home > Category > Book title
    The category is always the second-to-last breadcrumb item,
    regardless of how many levels deep the trail goes.
    """
    breadcrumb = soup.find("ul", class_="breadcrumb")
    if breadcrumb is None:
        return None
    crumbs = breadcrumb.find_all("li")
    return crumbs[-2].get_text(strip=True) if len(crumbs) >= 3 else None


def extract_description(soup: BeautifulSoup) -> Optional[str]:
    """
    The description has no class of its own. It is the <p> tag that
    immediately follows the <div id="product_description"> header.

    find_next_sibling("p") is the move for 'give me the next paragraph
    after this element' -- a pattern that comes up constantly in scraping
    when related content lives in separate sibling tags.
    """
    header = soup.find("div", id="product_description")
    if header is None:
        return None
    desc_p = header.find_next_sibling("p")
    return desc_p.get_text(strip=True) if desc_p else None


def enrich_with_details(session: requests.Session, book: Book) -> bool:
    """
    Fetch the book's own detail page and populate the four extra fields
    directly on the Book object.  Returns True on success, False on failure.

    On failure the book keeps its listing-level data (title, price, etc.)
    with the detail fields left as None, and the run continues -- one bad
    detail page should not abort the whole catalog scrape.
    """
    html = fetch_page(session, book.url)
    if html is None:
        return False
    soup = BeautifulSoup(html, "html.parser")
    book.upc         = extract_upc(soup)
    book.stock_count = extract_stock_count(soup)
    book.category    = extract_category(soup)
    book.description = extract_description(soup)
    return True


# ---------------------------------------------------------------------------
# DISPLAY  (matches the expected console output in the project spec)
# ---------------------------------------------------------------------------

def print_book_row(index: int, total: int, book: Book) -> None:
    """
    Two-line console output per book:
      {n}/{total}  {title:<50}  £{price:.2f}   {availability}
      ({stock_count})  {category}
    """
    title = book.title if len(book.title) <= 50 else book.title[:47] + "..."
    print(f"  {index}/{total}  {title:<50}  \u00A3{book.price:.2f}   {book.availability}")
    stock_label = f"({book.stock_count})" if book.stock_count is not None else "(?)"
    print(f"  {stock_label:<6}  {book.category or 'Unknown'}")


# ---------------------------------------------------------------------------
# SAVING
# ---------------------------------------------------------------------------

def save_to_csv(books: List[Book], path: str) -> None:
    """Write all books to a CSV.  asdict() converts each dataclass to a
    plain dict so DictWriter can align the columns automatically."""
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(asdict(b) for b in books)


# ---------------------------------------------------------------------------
# SUMMARY
# ---------------------------------------------------------------------------

def print_summary(books: List[Book], pages: int,
                  failures: int, elapsed: float) -> None:
    if not books:
        print("No books scraped.")
        return

    total      = len(books)
    avg_price  = sum(b.price for b in books) / total
    five_star  = sum(1 for b in books if b.rating == 5)
    in_stock   = sum(1 for b in books if "In stock" in b.availability)
    categories = {b.category for b in books if b.category}

    print()
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"  Pages scraped:          {pages}")
    print(f"  Books scraped:          {total}")
    print(f"  Detail fetch failures:  {failures}")
    print(f"  Average price:          \u00A3{avg_price:.2f}")
    print(f"  5-star books:           {five_star}")
    print(f"  In stock:               {in_stock}")
    print(f"  Distinct categories:    {len(categories)}")
    print(f"  Total time:             {elapsed / 60:.1f} min")


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

def main() -> None:
    print("=" * 70)
    print("BOOK SCRAPER \u2014 Day 2: Multi-Page Scraping with Pagination")
    if MAX_PAGES:
        print(f"(TEST MODE: capped at {MAX_PAGES} page(s))")
    print("=" * 70)
    print()

    start_time = time.time()
    all_books:     List[Book] = []
    pages_scraped: int        = 0
    detail_failures: int      = 0

    with build_session() as session:

        # ----------------------------------------------------------------
        # Phase 1 + 2 combined: for each listing page, extract books and
        # immediately enrich each one from its detail page before moving on.
        # This mirrors the two-level pattern from the project spec and gives
        # real-time per-book progress in the console.
        # ----------------------------------------------------------------

        url: Optional[str] = BASE_URL
        total_pages: Optional[int] = None

        while url:
            pages_scraped += 1
            page_label = f"of {total_pages}" if total_pages else "of -50"
            print(f"\nPage {pages_scraped} {page_label}: {url}")

            html = fetch_page(session, url)
            if html is None:
                print(f"  \u2717 Could not fetch page {pages_scraped} -- stopping pagination.")
                break

            soup = BeautifulSoup(html, "html.parser")

            # Discover total page count from the first page's pager widget.
            if total_pages is None:
                total_pages = extract_total_pages(soup)

            # Extract every book card on this listing page.
            cards = soup.find_all("article", class_="product_pod")
            page_books: List[Book] = []
            for card in cards:
                book = extract_book_from_card(card, url)
                if book is not None:
                    page_books.append(book)

            print(f"  \u2713 {len(page_books)} books found")

            # Visit each book's detail page and print the two-line row.
            for i, book in enumerate(page_books, 1):
                ok = enrich_with_details(session, book)
                if not ok:
                    detail_failures += 1
                print_book_row(i, len(page_books), book)
                all_books.append(book)
                time.sleep(REQUEST_DELAY)

            if MAX_PAGES and pages_scraped >= MAX_PAGES:
                print(f"\n  Reached MAX_PAGES={MAX_PAGES} -- stopping early.")
                break

            url = find_next_url(soup, url)
            time.sleep(REQUEST_DELAY)

    if not all_books:
        print("\nNothing to save. Exiting.")
        return

    # Save everything to one CSV.
    save_to_csv(all_books, OUTPUT_FILE)
    print(f"\n\u2713 Saved {len(all_books)} books to {OUTPUT_FILE}")

    elapsed = time.time() - start_time
    print_summary(all_books, pages_scraped, detail_failures, elapsed)


if __name__ == "__main__":
    main()