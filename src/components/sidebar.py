"""Sidebar filters component."""

import streamlit as st
import pandas as pd


class FilterState:
    """Manages all filter state."""

    def __init__(self, df: pd.DataFrame):
        self.df = df

    def render(self):
        """Render all sidebar filters."""
        with st.sidebar:
            st.markdown("## 🔍 Filter books")
            st.divider()

            # Category filter
            all_categories = sorted(self.df["category"].dropna().unique())
            selected_categories = st.multiselect(
                "Category",
                options=all_categories,
                default=all_categories,
            )

            st.divider()

            # Price filter
            min_price = float(self.df["price"].min())
            max_price = float(self.df["price"].max())
            price_range = st.slider(
                "Price range (£)",
                min_value=min_price,
                max_value=max_price,
                value=(min_price, max_price),
                step=0.5,
            )

            st.divider()

            # Rating filter
            min_rating = st.selectbox(
                "Minimum rating (stars)", [1, 2, 3, 4, 5], index=0
            )

            st.divider()

            # Stock filter
            in_stock_only = st.checkbox("In stock only", value=False)

            st.divider()

            # Keyword search
            keyword = st.text_input(
                "Search title or description", placeholder="e.g. love, dark…"
            )

        return {
            "categories": selected_categories,
            "price_range": price_range,
            "min_rating": min_rating,
            "in_stock_only": in_stock_only,
            "keyword": keyword,
        }

    @staticmethod
    def apply_filters(df: pd.DataFrame, filters: dict) -> pd.DataFrame:
        """Apply all filters to the dataframe."""
        filtered = df.copy()

        if filters["categories"]:
            filtered = filtered[filtered["category"].isin(filters["categories"])]

        filtered = filtered[
            (filtered["price"] >= filters["price_range"][0])
            & (filtered["price"] <= filters["price_range"][1])
        ]

        filtered = filtered[filtered["rating"] >= filters["min_rating"]]

        if filters["in_stock_only"]:
            filtered = filtered[
                filtered["availability"].str.contains("In stock", na=False)
            ]

        if filters["keyword"]:
            kw = filters["keyword"].lower()
            filtered = filtered[
                (filtered["title"].str.lower().str.contains(kw, na=False))
                | (
                    filtered["description"]
                    .fillna("")
                    .str.lower()
                    .str.contains(kw, na=False)
                )
            ]

        return filtered
