"""Book detail card component."""

import streamlit as st
import pandas as pd


def render_detail(filtered: pd.DataFrame):
    """Render book detail search and card."""
    st.divider()
    st.markdown("### 🔎 Book detail")

    # Search and select
    search_col, select_col = st.columns([1, 2])

    with search_col:
        book_search = st.text_input(
            "Type to search books",
            placeholder="e.g. sapiens, dark…",
            key="book_search",
            label_visibility="visible",
        )

    # Filter titles by search
    all_titles = sorted(filtered["title"].dropna().unique())
    if book_search:
        matched = [t for t in all_titles if book_search.lower() in t.lower()]
    else:
        matched = all_titles

    with select_col:
        if matched:
            selected_title = st.selectbox(
                f"Matching books ({len(matched)})",
                options=matched,
                key="book_select",
            )
        else:
            st.warning("No books match your search.")
            selected_title = None

    # Render book card
    if selected_title:
        book = filtered[filtered["title"] == selected_title].iloc[0]
        stars_html = f'<span class="star-gold">{"★" * int(book["rating"])}{"☆" * (5 - int(book["rating"]))}</span>'
        stock_val = (
            int(book["stock_count"]) if pd.notna(book.get("stock_count")) else "?"
        )
        url = book.get("url", "")
        upc = book.get("upc", "")
        desc = book.get("description", "")
        avail = book.get("availability", "")
        cat = book.get("category", "")

        st.markdown(
            f"""
        <div class="book-card">
            <div class="bc-title">{book['title']}</div>
            <span class="bc-cat">{cat}</span>
            <div class="bc-row">
                <div class="bc-stat">
                    <div class="bc-stat-label">Price</div>
                    <div class="bc-stat-value">£{book['price']:.2f}</div>
                </div>
                <div class="bc-stat">
                    <div class="bc-stat-label">Rating</div>
                    <div class="bc-stat-value">{stars_html}</div>
                </div>
                <div class="bc-stat">
                    <div class="bc-stat-label">In stock</div>
                    <div class="bc-stat-value">{stock_val}</div>
                </div>
            </div>
            <div class="bc-field"><b>Availability:</b> {avail}</div>
            <div class="bc-field"><b>UPC:</b> <span class="bc-upc">{upc}</span></div>
            <div class="bc-field"><b>URL:</b> <a href="{url}" target="_blank">{url}</a></div>
            {"<div class='bc-desc'>" + desc + "</div>" if pd.notna(desc) and desc else ""}
        </div>
        """,
            unsafe_allow_html=True,
        )
