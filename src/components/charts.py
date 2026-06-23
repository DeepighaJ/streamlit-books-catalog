"""Charts component."""

import streamlit as st
import plotly.express as px
import pandas as pd
from src.config import CHART_CFG, HOVER_LABEL, RATING_COLORS


def render_price_and_rating_charts(filtered: pd.DataFrame):
    """Render price distribution and rating breakdown charts."""
    col_l, col_r = st.columns(2)

    with col_l:
        st.markdown("### Price distribution")
        fig = px.histogram(
            filtered,
            x="price",
            nbins=30,
            labels={"price": "Price (£)", "count": "Books"},
            color_discrete_sequence=["#6366f1"],
        )
        fig.update_traces(
            hovertemplate="<b>£%{x:.2f}</b><br>%{y} books<extra></extra>",
        )
        fig.update_layout(
            margin=dict(t=8, b=8, l=8, r=8),
            plot_bgcolor="#ffffff",
            paper_bgcolor="#ffffff",
            bargap=0.05,
            hoverlabel=HOVER_LABEL,
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor="#f0f0f5"),
        )
        st.plotly_chart(fig, use_container_width=True, config=CHART_CFG)

    with col_r:
        st.markdown("### Rating breakdown")
        rc = filtered["rating"].value_counts().sort_index().reset_index()
        rc.columns = ["rating", "count"]
        rc["label"] = rc["rating"].apply(lambda r: "★" * int(r))
        rc["color"] = rc["rating"].map(RATING_COLORS)
        fig = px.bar(
            rc,
            x="label",
            y="count",
            labels={"label": "Stars", "count": "Books"},
            color="rating",
            color_discrete_map={k: v for k, v in RATING_COLORS.items()},
        )
        fig.update_traces(
            hovertemplate="<b>%{x}</b><br>%{y} books<extra></extra>",
        )
        fig.update_layout(
            margin=dict(t=8, b=8, l=8, r=8),
            plot_bgcolor="#ffffff",
            paper_bgcolor="#ffffff",
            showlegend=False,
            hoverlabel=HOVER_LABEL,
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor="#f0f0f5"),
        )
        st.plotly_chart(fig, use_container_width=True, config=CHART_CFG)


def render_category_charts(filtered: pd.DataFrame):
    """Render category and price analysis charts."""
    col_l2, col_r2 = st.columns(2)

    with col_l2:
        st.markdown("### Books per category")
        cat_counts = filtered["category"].value_counts().reset_index()
        cat_counts.columns = ["category", "count"]
        fig = px.bar(
            cat_counts.head(15),
            x="count",
            y="category",
            orientation="h",
            labels={"count": "Number of books", "category": ""},
            color="count",
            color_continuous_scale=[[0, "#c7d2fe"], [1, "#4f46e5"]],
        )
        fig.update_traces(
            hovertemplate="<b>%{y}</b><br>%{x} books<extra></extra>",
        )
        fig.update_layout(
            margin=dict(t=8, b=8, l=8, r=8),
            plot_bgcolor="#ffffff",
            paper_bgcolor="#ffffff",
            coloraxis_showscale=False,
            yaxis=dict(categoryorder="total ascending", showgrid=False),
            xaxis=dict(showgrid=True, gridcolor="#f0f0f5"),
            hoverlabel=HOVER_LABEL,
            height=380,
        )
        st.plotly_chart(fig, use_container_width=True, config=CHART_CFG)

    with col_r2:
        st.markdown("### Average price by category")
        avg_p = (
            filtered.groupby("category")["price"]
            .mean()
            .sort_values(ascending=False)
            .head(15)
            .reset_index()
        )
        avg_p.columns = ["category", "avg_price"]
        fig = px.bar(
            avg_p,
            x="avg_price",
            y="category",
            orientation="h",
            labels={"avg_price": "Avg price (£)", "category": ""},
            color="avg_price",
            color_continuous_scale=[[0, "#fed7aa"], [1, "#ea580c"]],
        )
        fig.update_traces(
            hovertemplate="<b>%{y}</b><br>Avg: £%{x:.2f}<extra></extra>",
        )
        fig.update_layout(
            margin=dict(t=8, b=8, l=8, r=8),
            plot_bgcolor="#ffffff",
            paper_bgcolor="#ffffff",
            coloraxis_showscale=False,
            yaxis=dict(categoryorder="total ascending", showgrid=False),
            xaxis=dict(showgrid=True, gridcolor="#f0f0f5"),
            hoverlabel=HOVER_LABEL,
            height=380,
        )
        st.plotly_chart(fig, use_container_width=True, config=CHART_CFG)


def render_scatter_chart(filtered: pd.DataFrame):
    """Render price vs rating scatter chart."""
    st.markdown("### Price vs rating")
    fig = px.scatter(
        filtered,
        x="price",
        y="rating",
        color="category",
        hover_data={"title": True, "stock_count": True, "category": False},
        labels={"price": "Price (£)", "rating": "Stars", "category": "Category"},
        opacity=0.75,
    )
    fig.update_traces(
        hovertemplate=(
            "<b>%{customdata[0]}</b><br>"
            "Price: £%{x:.2f}<br>"
            "Rating: %{y} ★<br>"
            "In stock: %{customdata[1]}<extra></extra>"
        ),
        marker_size=8,
    )
    fig.update_layout(
        margin=dict(t=8, b=8, l=8, r=8),
        plot_bgcolor="#ffffff",
        paper_bgcolor="#ffffff",
        hoverlabel=HOVER_LABEL,
        legend_title="Category",
        xaxis=dict(showgrid=True, gridcolor="#f0f0f5"),
        yaxis=dict(showgrid=True, gridcolor="#f0f0f5", dtick=1),
        height=380,
    )
    st.plotly_chart(fig, use_container_width=True, config=CHART_CFG)


def render_stock_availability(filtered: pd.DataFrame):
    """Render stock availability donut chart and stats."""
    st.markdown("### Stock availability")
    donut_col, stats_col = st.columns([2, 1])

    with donut_col:
        avail_counts = filtered["availability"].value_counts().reset_index()
        avail_counts.columns = ["availability", "count"]

        fig = px.pie(
            avail_counts,
            names="availability",
            values="count",
            hole=0.55,
            color_discrete_sequence=["#4f46e5", "#e0e7ff", "#6366f1"],
        )
        fig.update_traces(
            textinfo="label+percent",
            textposition="outside",
            hovertemplate="<b>%{label}</b><br>%{value} books (%{percent})<extra></extra>",
            pull=[0.03] * len(avail_counts),
        )
        fig.update_layout(
            margin=dict(t=20, b=20, l=20, r=20),
            paper_bgcolor="#ffffff",
            showlegend=False,
            hoverlabel=HOVER_LABEL,
            height=320,
        )
        st.plotly_chart(fig, use_container_width=True, config=CHART_CFG)

    with stats_col:
        st.markdown("<div style='height:40px'></div>", unsafe_allow_html=True)
        total = len(filtered)
        for _, row in avail_counts.iterrows():
            pct = row["count"] / total * 100 if total else 0
            st.markdown(
                f"""
            <div style="background:#ffffff;border:1px solid #e8eaf0;border-radius:10px;
                        padding:14px 18px;margin-bottom:10px;">
                <div style="font-size:11px;color:#9ca3af;font-weight:600;
                            text-transform:uppercase;letter-spacing:0.04em;margin-bottom:4px;">
                    {row['availability']}
                </div>
                <div style="font-size:22px;font-weight:700;color:#1a1a2e;">{row['count']:,}</div>
                <div style="font-size:12px;color:#6b7280;margin-top:2px;">{pct:.1f}% of shown books</div>
            </div>
            """,
                unsafe_allow_html=True,
            )
