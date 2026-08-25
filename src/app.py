import time

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from database_service import get_database_connection


# ============================================
# Page Configuration
# ============================================

st.set_page_config(
    page_title="Live Crypto Dashboard",
    page_icon="📈",
    layout="wide"
)


# ============================================
# Load Data
# ============================================

@st.cache_data(ttl=60)
def load_latest_crypto_data():
    connection = get_database_connection()

    query = """
        SELECT
            coin_id,
            symbol,
            name,
            current_price,
            market_cap,
            total_volume,
            high_24h,
            low_24h,
            price_change_percentage_24h,
            collected_at
        FROM latest_crypto_prices
        ORDER BY coin_id;
    """

    data_frame = pd.read_sql(query, connection)
    connection.close()

    data_frame["collected_at"] = pd.to_datetime(
        data_frame["collected_at"]
    )

    return data_frame


@st.cache_data(ttl=60)
def load_historical_crypto_data():
    connection = get_database_connection()

    query = """
        SELECT
            coin_id,
            symbol,
            name,
            current_price,
            market_cap,
            total_volume,
            high_24h,
            low_24h,
            price_change_percentage_24h,
            collected_at
        FROM crypto_market_data
        ORDER BY collected_at;
    """

    data_frame = pd.read_sql(query, connection)
    connection.close()

    data_frame["collected_at"] = pd.to_datetime(
        data_frame["collected_at"]
    )

    return data_frame


latest_data = load_latest_crypto_data()
historical_data = load_historical_crypto_data()


# ============================================
# Sidebar Controls
# ============================================

st.sidebar.title("Dashboard Controls")

coin_names = sorted(historical_data["name"].dropna().unique())

selected_coin = st.sidebar.selectbox(
    "Cryptocurrency",
    coin_names
)

time_range = st.sidebar.selectbox(
    "Time Range",
    [
        "All Data",
        "Last Hour",
        "Last 6 Hours",
        "Last 24 Hours"
    ]
)


if st.sidebar.button("Refresh Data"):
    st.cache_data.clear()
    st.rerun()


auto_refresh = st.sidebar.checkbox(
    "Auto Refresh"
)

refresh_seconds = st.sidebar.selectbox(
    "Refresh Interval",
    [30, 60, 300],
    index=1,
    disabled=not auto_refresh
)


st.sidebar.divider()

st.sidebar.caption("Data Source")
st.sidebar.write("CoinGecko API")

st.sidebar.caption("Storage")
st.sidebar.write("PostgreSQL")

st.sidebar.caption("Visualization")
st.sidebar.write("Streamlit + Plotly")


# ============================================
# Time Filter
# ============================================

filtered_data = historical_data.copy()

latest_timestamp = historical_data["collected_at"].max()


if time_range == "Last Hour":

    start_time = latest_timestamp - pd.Timedelta(hours=1)

    filtered_data = historical_data[
        historical_data["collected_at"] >= start_time
    ]


elif time_range == "Last 6 Hours":

    start_time = latest_timestamp - pd.Timedelta(hours=6)

    filtered_data = historical_data[
        historical_data["collected_at"] >= start_time
    ]


elif time_range == "Last 24 Hours":

    start_time = latest_timestamp - pd.Timedelta(hours=24)

    filtered_data = historical_data[
        historical_data["collected_at"] >= start_time
    ]


# ============================================
# Header
# ============================================

st.title("📈 Live Crypto Market Intelligence")

st.caption(
    "CoinGecko API → Python ETL → PostgreSQL → "
    "Streamlit → Plotly"
)


# ============================================
# Pipeline Status
# ============================================

status_column1, status_column2, status_column3 = st.columns(3)


with status_column1:
    st.metric(
        "Cryptocurrencies",
        latest_data["coin_id"].nunique()
    )


with status_column2:
    st.metric(
        "Database Records",
        len(historical_data)
    )


with status_column3:
    st.metric(
        "Latest Collection",
        latest_timestamp.strftime("%Y-%m-%d %H:%M")
    )


# ============================================
# Market Overview
# ============================================

st.divider()

st.subheader("💰 Market Overview")

columns = st.columns(len(latest_data))


for column, (_, coin) in zip(
    columns,
    latest_data.iterrows()
):

    with column:

        st.metric(
            label=(
                f"{coin['name']} "
                f"({coin['symbol'].upper()})"
            ),
            value=f"${coin['current_price']:,.2f}",
            delta=(
                f"{coin['price_change_percentage_24h']:.2f}%"
            )
        )


# ============================================
# Overall Market KPIs
# ============================================

st.subheader("🌎 Market Intelligence")

total_market_cap = latest_data["market_cap"].sum()
total_volume = latest_data["total_volume"].sum()

best_coin = latest_data.loc[
    latest_data[
        "price_change_percentage_24h"
    ].idxmax()
]

worst_coin = latest_data.loc[
    latest_data[
        "price_change_percentage_24h"
    ].idxmin()
]


kpi1, kpi2, kpi3, kpi4 = st.columns(4)


with kpi1:
    st.metric(
        "Combined Market Cap",
        f"${total_market_cap / 1_000_000_000:,.2f}B"
    )


with kpi2:
    st.metric(
        "Combined 24H Volume",
        f"${total_volume / 1_000_000_000:,.2f}B"
    )


with kpi3:
    st.metric(
        "Best 24H Performer",
        best_coin["name"],
        f"{best_coin['price_change_percentage_24h']:.2f}%"
    )


with kpi4:
    st.metric(
        "Lowest 24H Performer",
        worst_coin["name"],
        f"{worst_coin['price_change_percentage_24h']:.2f}%"
    )


# ============================================
# Normalized Performance
# ============================================

st.divider()

st.subheader("📈 Relative Market Performance")

comparison_data = filtered_data.copy()

comparison_data = comparison_data.sort_values(
    ["coin_id", "collected_at"]
)


comparison_data["normalized_price"] = (
    comparison_data
    .groupby("coin_id")["current_price"]
    .transform(
        lambda prices:
        (prices / prices.iloc[0]) * 100
    )
)


performance_chart = px.line(
    comparison_data,
    x="collected_at",
    y="normalized_price",
    color="name",
    title="BTC vs ETH vs SOL — Relative Performance",
    labels={
        "collected_at": "Time",
        "normalized_price": "Performance Index",
        "name": "Cryptocurrency"
    }
)


performance_chart.update_layout(
    hovermode="x unified"
)


st.plotly_chart(
    performance_chart,
    use_container_width=True
)


# ============================================
# Percentage Return
# ============================================

st.subheader("📊 Collected Price Returns")

return_data = filtered_data.sort_values(
    ["coin_id", "collected_at"]
).copy()


return_data["return_percentage"] = (
    return_data
    .groupby("coin_id")["current_price"]
    .pct_change(fill_method=None)
    * 100
)


return_data = return_data.dropna(
    subset=["return_percentage"]
)


return_chart = px.line(
    return_data,
    x="collected_at",
    y="return_percentage",
    color="name",
    title="Price Return Between Collection Periods",
    labels={
        "collected_at": "Time",
        "return_percentage": "Return (%)",
        "name": "Cryptocurrency"
    }
)


return_chart.update_layout(
    hovermode="x unified"
)


st.plotly_chart(
    return_chart,
    use_container_width=True
)


# ============================================
# Market Cap and Volume
# ============================================

chart_column1, chart_column2 = st.columns(2)


with chart_column1:

    market_cap_chart = px.bar(
        latest_data,
        x="name",
        y="market_cap",
        title="Market Capitalization",
        text_auto=".3s",
        labels={
            "name": "Cryptocurrency",
            "market_cap": "Market Cap"
        }
    )

    market_cap_chart.update_layout(
        yaxis_tickformat=".2s"
    )

    st.plotly_chart(
        market_cap_chart,
        use_container_width=True
    )


with chart_column2:

    volume_chart = px.bar(
        latest_data,
        x="name",
        y="total_volume",
        title="24-Hour Trading Volume",
        text_auto=".3s",
        labels={
            "name": "Cryptocurrency",
            "total_volume": "Volume"
        }
    )

    volume_chart.update_layout(
        yaxis_tickformat=".2s"
    )

    st.plotly_chart(
        volume_chart,
        use_container_width=True
    )


# ============================================
# 24-Hour Change
# ============================================

change_chart = px.bar(
    latest_data,
    x="name",
    y="price_change_percentage_24h",
    title="24-Hour Price Change",
    text_auto=".2f",
    labels={
        "name": "Cryptocurrency",
        "price_change_percentage_24h":
        "Price Change (%)"
    }
)


change_chart.update_traces(
    texttemplate="%{y:.2f}%"
)


st.plotly_chart(
    change_chart,
    use_container_width=True
)


# ============================================
# Correlation Analysis
# ============================================

st.divider()

st.subheader("🔗 Cryptocurrency Correlation")


price_pivot = filtered_data.pivot_table(
    index="collected_at",
    columns="name",
    values="current_price"
)


returns = price_pivot.pct_change(
    fill_method=None
).dropna()


if len(returns) >= 2:

    correlation_matrix = returns.corr()

    correlation_chart = px.imshow(
        correlation_matrix,
        text_auto=".2f",
        aspect="auto",
        title="Return Correlation Matrix",
        zmin=-1,
        zmax=1
    )

    st.plotly_chart(
        correlation_chart,
        use_container_width=True
    )

    st.caption(
        "Values near 1 indicate that the cryptocurrencies "
        "have tended to move in the same direction. "
        "Values near -1 indicate opposite movement."
    )

else:

    st.info(
        "More historical observations are needed "
        "for correlation analysis."
    )


# ============================================
# Individual Coin Analysis
# ============================================

st.divider()

st.subheader(
    f"🔎 {selected_coin} Analysis"
)


selected_data = filtered_data[
    filtered_data["name"] == selected_coin
].copy()


if selected_data.empty:

    st.warning(
        "No records are available for this cryptocurrency "
        "in the selected time range."
    )

else:

    selected_latest = selected_data.iloc[-1]


    metric1, metric2, metric3, metric4 = st.columns(4)


    with metric1:

        st.metric(
            "Current Price",
            f"${selected_latest['current_price']:,.2f}"
        )


    with metric2:

        st.metric(
            "24H High",
            f"${selected_latest['high_24h']:,.2f}"
        )


    with metric3:

        st.metric(
            "24H Low",
            f"${selected_latest['low_24h']:,.2f}"
        )


    with metric4:

        st.metric(
            "24H Change",
            (
                f"{selected_latest['price_change_percentage_24h']:.2f}%"
            )
        )


    # ========================================
    # Historical Price
    # ========================================

    price_chart = px.line(
        selected_data,
        x="collected_at",
        y="current_price",
        title=f"{selected_coin} Price History",
        labels={
            "collected_at": "Time",
            "current_price": "Price (USD)"
        }
    )


    price_chart.update_layout(
        hovermode="x unified"
    )


    st.plotly_chart(
        price_chart,
        use_container_width=True
    )


    # ========================================
    # High / Low
    # ========================================

    high_low_chart = go.Figure()


    high_low_chart.add_trace(
        go.Scatter(
            x=selected_data["collected_at"],
            y=selected_data["high_24h"],
            mode="lines",
            name="24H High"
        )
    )


    high_low_chart.add_trace(
        go.Scatter(
            x=selected_data["collected_at"],
            y=selected_data["low_24h"],
            mode="lines",
            name="24H Low"
        )
    )


    high_low_chart.update_layout(
        title=f"{selected_coin} 24-Hour High vs Low",
        xaxis_title="Time",
        yaxis_title="Price (USD)",
        hovermode="x unified"
    )


    st.plotly_chart(
        high_low_chart,
        use_container_width=True
    )


    # ========================================
    # Volume / Market Cap Trends
    # ========================================

    trend1, trend2 = st.columns(2)


    with trend1:

        selected_volume_chart = px.line(
            selected_data,
            x="collected_at",
            y="total_volume",
            title="Trading Volume Trend",
            labels={
                "collected_at": "Time",
                "total_volume": "Volume"
            }
        )

        selected_volume_chart.update_layout(
            yaxis_tickformat=".2s"
        )

        st.plotly_chart(
            selected_volume_chart,
            use_container_width=True
        )


    with trend2:

        selected_market_cap_chart = px.line(
            selected_data,
            x="collected_at",
            y="market_cap",
            title="Market Cap Trend",
            labels={
                "collected_at": "Time",
                "market_cap": "Market Cap"
            }
        )

        selected_market_cap_chart.update_layout(
            yaxis_tickformat=".2s"
        )

        st.plotly_chart(
            selected_market_cap_chart,
            use_container_width=True
        )


    # ========================================
    # Statistics
    # ========================================

    st.subheader("📌 Collected Statistics")


    average_price = selected_data[
        "current_price"
    ].mean()

    highest_price = selected_data[
        "current_price"
    ].max()

    lowest_price = selected_data[
        "current_price"
    ].min()


    stat1, stat2, stat3, stat4 = st.columns(4)


    with stat1:

        st.metric(
            "Average Price",
            f"${average_price:,.2f}"
        )


    with stat2:

        st.metric(
            "Highest Price",
            f"${highest_price:,.2f}"
        )


    with stat3:

        st.metric(
            "Lowest Price",
            f"${lowest_price:,.2f}"
        )


    with stat4:

        st.metric(
            "Records",
            len(selected_data)
        )


# ============================================
# Latest Market Table
# ============================================

st.divider()

st.subheader("🪙 Latest Market Snapshot")


display_data = latest_data.copy()

display_data["symbol"] = (
    display_data["symbol"].str.upper()
)


display_data = display_data[
    [
        "name",
        "symbol",
        "current_price",
        "market_cap",
        "total_volume",
        "high_24h",
        "low_24h",
        "price_change_percentage_24h",
        "collected_at"
    ]
]


display_data = display_data.rename(
    columns={
        "name": "Cryptocurrency",
        "symbol": "Symbol",
        "current_price": "Current Price",
        "market_cap": "Market Cap",
        "total_volume": "24H Volume",
        "high_24h": "24H High",
        "low_24h": "24H Low",
        "price_change_percentage_24h":
        "24H Change %",
        "collected_at": "Collected At"
    }
)


st.dataframe(
    display_data,
    use_container_width=True,
    hide_index=True
)


# ============================================
# Raw Historical Data
# ============================================

with st.expander(
    "📂 View Historical Database Records"
):

    st.dataframe(
        filtered_data.sort_values(
            "collected_at",
            ascending=False
        ),
        use_container_width=True,
        hide_index=True
    )


# ============================================
# Auto Refresh
# ============================================

if auto_refresh:

    st.caption(
        f"Dashboard will refresh every "
        f"{refresh_seconds} seconds."
    )

    time.sleep(refresh_seconds)

    st.cache_data.clear()

    st.rerun()


# ============================================
# Footer
# ============================================

st.divider()

st.caption(
    "Live Crypto Data Engineering Project | "
    "CoinGecko API → Python → PostgreSQL → "
    "Streamlit → Plotly"
)