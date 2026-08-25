# ============================================
# Market Comparison
# ============================================

st.divider()

st.subheader("🌎 Market Comparison")

st.write(
    "Compare Bitcoin, Ethereum, and Solana across price performance, "
    "market capitalization, trading volume, and 24-hour movement."
)


# ============================================
# Normalize Price Performance
# ============================================

comparison_data = historical_data.copy()

comparison_data = comparison_data.sort_values(
    ["coin_id", "collected_at"]
)

comparison_data["normalized_price"] = (
    comparison_data.groupby("coin_id")["current_price"]
    .transform(lambda prices: (prices / prices.iloc[0]) * 100)
)


normalized_chart = comparison_data.pivot_table(
    index="collected_at",
    columns="name",
    values="normalized_price"
)


st.subheader("📈 Relative Price Performance")

st.caption(
    "Each cryptocurrency starts at 100 so their performance "
    "can be compared on the same scale."
)

st.line_chart(
    normalized_chart,
    use_container_width=True
)


# ============================================
# Market Comparison Charts
# ============================================

comparison_column1, comparison_column2 = st.columns(2)


# --------------------------------------------
# Market Capitalization
# --------------------------------------------

with comparison_column1:

    st.subheader("🏦 Market Capitalization")

    market_cap_comparison = latest_data[
        [
            "name",
            "market_cap"
        ]
    ].set_index("name")

    st.bar_chart(
        market_cap_comparison,
        use_container_width=True
    )


# --------------------------------------------
# Trading Volume
# --------------------------------------------

with comparison_column2:

    st.subheader("📊 24H Trading Volume")

    volume_comparison = latest_data[
        [
            "name",
            "total_volume"
        ]
    ].set_index("name")

    st.bar_chart(
        volume_comparison,
        use_container_width=True
    )


# ============================================
# Price Change Comparison
# ============================================

st.subheader("⚡ 24-Hour Price Change")

price_change_comparison = latest_data[
    [
        "name",
        "price_change_percentage_24h"
    ]
].set_index("name")


st.bar_chart(
    price_change_comparison,
    use_container_width=True
)