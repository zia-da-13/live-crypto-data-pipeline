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
# Data Functions
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
# Sidebar
# ============================================

st.sidebar.title("Dashboard Controls")

selected_coin = st.sidebar.selectbox(
    "Select Cryptocurrency",
    historical_data["name"].unique()
)

if st.sidebar.button("Refresh Data"):
    st.cache_data.clear()
    st.rerun()


st.sidebar.divider()

st.sidebar.write("Data Source")
st.sidebar.write("CoinGecko API")

st.sidebar.write("Database")
st.sidebar.write("PostgreSQL")

st.sidebar.write("Dashboard")
st.sidebar.write("Streamlit + Plotly")


# ============================================
# Header
# ============================================

st.title("📈 Live Crypto Market Intelligence Dashboard")

st.caption(
    "Real-time cryptocurrency analytics powered by "
    "CoinGecko, Python, PostgreSQL, Streamlit, and Plotly."
)


# ============================================
# Market Overview
# ============================================

st.subheader("Market Overview")

columns = st.columns(len(latest_data))

for column, (_, coin) in zip(columns, latest_data.iterrows()):
    with column:
        st.metric(
            label=f"{coin['name']} ({coin['symbol'].upper()})",
            value=f"${coin['current_price']:,.2f}",
            delta=f"{coin['price_change_percentage_24h']:.2f}%"
        )


st.divider()


# ============================================
# Relative Performance Comparison
# ============================================

st.subheader("Relative Price Performance")

comparison_data = historical_data.copy()

comparison_data = comparison_data.sort_values(
    ["coin_id", "collected_at"]
)

comparison_data["normalized_price"] = (
    comparison_data.groupby("coin_id")["current_price"]
    .transform(lambda prices: (prices / prices.iloc[0]) * 100)
)

relative_performance_chart = px.line(
    comparison_data,
    x="collected_at",
    y="normalized_price",
    color="name",
    title="BTC vs ETH vs SOL Relative Performance",
    labels={
        "collected_at": "Collection Time",
        "normalized_price": "Normalized Price",
        "name": "Cryptocurrency"
    }
)

relative_performance_chart.update_layout(
    hovermode="x unified",
    legend_title_text="Cryptocurrency"
)

st.plotly_chart(
    relative_performance_chart,
    use_container_width=True
)


# ============================================
# Market Cap and Volume Comparison
# ============================================

comparison_column1, comparison_column2 = st.columns(2)


with comparison_column1:

    market_cap_chart = px.bar(
        latest_data,
        x="name",
        y="market_cap",
        title="Market Capitalization",
        labels={
            "name": "Cryptocurrency",
            "market_cap": "Market Cap"
        },
        text_auto=".3s"
    )

    market_cap_chart.update_layout(
        yaxis_tickformat=".2s"
    )

    st.plotly_chart(
        market_cap_chart,
        use_container_width=True
    )


with comparison_column2:

    volume_chart = px.bar(
        latest_data,
        x="name",
        y="total_volume",
        title="24-Hour Trading Volume",
        labels={
            "name": "Cryptocurrency",
            "total_volume": "Trading Volume"
        },
        text_auto=".3s"
    )

    volume_chart.update_layout(
        yaxis_tickformat=".2s"
    )

    st.plotly_chart(
        volume_chart,
        use_container_width=True
    )


# ============================================
# 24-Hour Change Comparison
# ============================================

st.subheader("24-Hour Price Change")

change_chart = px.bar(
    latest_data,
    x="name",
    y="price_change_percentage_24h",
    title="Latest 24-Hour Percentage Change",
    labels={
        "name": "Cryptocurrency",
        "price_change_percentage_24h": "Price Change (%)"
    },
    text_auto=".2f"
)

change_chart.update_traces(
    texttemplate="%{y:.2f}%"
)

st.plotly_chart(
    change_chart,
    use_container_width=True
)


st.divider()


# ============================================
# Individual Cryptocurrency Analysis
# ============================================

st.subheader(f"{selected_coin} Analysis")

selected_data = historical_data[
    historical_data["name"] == selected_coin
].copy()

selected_latest = selected_data.iloc[-1]


metric_column1, metric_column2, metric_column3, metric_column4 = st.columns(4)


with metric_column1:
    st.metric(
        "Current Price",
        f"${selected_latest['current_price']:,.2f}"
    )


with metric_column2:
    st.metric(
        "24H High",
        f"${selected_latest['high_24h']:,.2f}"
    )


with metric_column3:
    st.metric(
        "24H Low",
        f"${selected_latest['low_24h']:,.2f}"
    )


with metric_column4:
    st.metric(
        "24H Change",
        f"{selected_latest['price_change_percentage_24h']:.2f}%"
    )


# ============================================
# Historical Price Chart
# ============================================

price_chart = px.line(
    selected_data,
    x="collected_at",
    y="current_price",
    title=f"{selected_coin} Historical Price",
    labels={
        "collected_at": "Collection Time",
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


# ============================================
# High / Low Range
# ============================================

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
    xaxis_title="Collection Time",
    yaxis_title="Price (USD)",
    hovermode="x unified"
)

st.plotly_chart(
    high_low_chart,
    use_container_width=True
)


# ============================================
# Volume and Market Cap Trends
# ============================================

trend_column1, trend_column2 = st.columns(2)


with trend_column1:

    historical_volume_chart = px.line(
        selected_data,
        x="collected_at",
        y="total_volume",
        title=f"{selected_coin} Trading Volume Trend",
        labels={
            "collected_at": "Collection Time",
            "total_volume": "Trading Volume"
        }
    )

    historical_volume_chart.update_layout(
        yaxis_tickformat=".2s",
        hovermode="x unified"
    )

    st.plotly_chart(
        historical_volume_chart,
        use_container_width=True
    )


with trend_column2:

    historical_market_cap_chart = px.line(
        selected_data,
        x="collected_at",
        y="market_cap",
        title=f"{selected_coin} Market Cap Trend",
        labels={
            "collected_at": "Collection Time",
            "market_cap": "Market Cap"
        }
    )

    historical_market_cap_chart.update_layout(
        yaxis_tickformat=".2s",
        hovermode="x unified"
    )

    st.plotly_chart(
        historical_market_cap_chart,
        use_container_width=True
    )


# ============================================
# Collected Statistics
# ============================================

st.subheader("Collected Price Statistics")

average_price = selected_data["current_price"].mean()
highest_price = selected_data["current_price"].max()
lowest_price = selected_data["current_price"].min()
total_records = len(selected_data)

stat_column1, stat_column2, stat_column3, stat_column4 = st.columns(4)


with stat_column1:
    st.metric(
        "Average Price",
        f"${average_price:,.2f}"
    )


with stat_column2:
    st.metric(
        "Highest Price",
        f"${highest_price:,.2f}"
    )


with stat_column3:
    st.metric(
        "Lowest Price",
        f"${lowest_price:,.2f}"
    )


with stat_column4:
    st.metric(
        "Historical Records",
        total_records
    )


st.divider()


# ============================================
# Latest Market Table
# ============================================

st.subheader("Latest Market Snapshot")

display_data = latest_data[
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
].copy()

display_data["symbol"] = display_data["symbol"].str.upper()

display_data = display_data.rename(
    columns={
        "name": "Cryptocurrency",
        "symbol": "Symbol",
        "current_price": "Current Price",
        "market_cap": "Market Cap",
        "total_volume": "24H Volume",
        "high_24h": "24H High",
        "low_24h": "24H Low",
        "price_change_percentage_24h": "24H Change %",
        "collected_at": "Collected At"
    }
)

st.dataframe(
    display_data,
    use_container_width=True,
    hide_index=True
)


# ============================================
# Historical Data
# ============================================

with st.expander("View Historical Database Records"):

    st.dataframe(
        selected_data.sort_values(
            "collected_at",
            ascending=False
        ),
        use_container_width=True,
        hide_index=True
    )


# ============================================
# Footer
# ============================================

st.divider()

st.caption(
    "Live Crypto Data Engineering Project | "
    "CoinGecko API → Python ETL → PostgreSQL → Streamlit → Plotly"
)