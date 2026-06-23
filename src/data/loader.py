"""
Data loading and preprocessing utilities.
"""

import pandas as pd
import streamlit as st


@st.cache_data
def load_data(path: str) -> pd.DataFrame:
    """Load and preprocess the books CSV data."""
    df = pd.read_csv(path)
    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
    df["stock_count"] = pd.to_numeric(df["stock_count"], errors="coerce")
    df["stars"] = df["rating"].apply(
        lambda r: "★" * int(r) + "☆" * (5 - int(r)) if pd.notna(r) else "N/A"
    )
    return df
