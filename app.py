import streamlit as st
import pandas as pd
import plotly.express as px


# ---------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------

st.set_page_config(
    page_title="Amazon Bestselling Books",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ---------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------

st.markdown("""
<style>

    .main {
        background-color: #f8f9fa;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    .dashboard-title {
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .dashboard-subtitle {
        font-size: 18px;
        color: #666666;
        margin-bottom: 30px;
    }

    .section-title {
        font-size: 25px;
        font-weight: 600;
        margin-top: 25px;
        margin-bottom: 15px;
    }

</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------

@st.cache_data
def load_data():
    df = pd.read_csv("books.csv")
    df.columns = df.columns.str.strip()
    return df


df = load_data()


# ---------------------------------------------------
# CHECK REQUIRED COLUMNS
# ---------------------------------------------------

required_columns = [
    "Name",
    "Author",
    "User Rating",
    "Reviews",
    "Price",
    "Year",
    "Genre"
]

missing_columns = [
    column for column in required_columns
    if column not in df.columns
]

if missing_columns:
    st.error(
        f"Missing columns in books.csv: {missing_columns}"
    )
    st.write("Available columns:", df.columns.tolist())
    st.stop()


# ---------------------------------------------------
# HEADER
# ---------------------------------------------------

st.markdown(
    '<div class="dashboard-title">📚 Amazon Bestselling Books</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="dashboard-subtitle">'
    'Interactive dashboard for exploring Amazon bestselling books'
    '</div>',
    unsafe_allow_html=True
)


# ---------------------------------------------------
# SIDEBAR FILTERS
# ---------------------------------------------------

st.sidebar.title("🔎 Dashboard Filters")

st.sidebar.markdown(
    "Use the filters below to explore the dataset."
)


# Genre filter
genres = sorted(df["Genre"].dropna().unique())

selected_genres = st.sidebar.multiselect(
    "📚 Select Genre",
    options=genres,
    default=genres
)


# Year filter
min_year = int(df["Year"].min())
max_year = int(df["Year"].max())

selected_years = st.sidebar.slider(
    "📅 Select Year Range",
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year)
)


# Rating filter
min_rating = float(df["User Rating"].min())
max_rating = float(df["User Rating"].max())

selected_rating = st.sidebar.slider(
    "⭐ User Rating",
    min_value=min_rating,
    max_value=max_rating,
    value=(min_rating, max_rating),
    step=0.1
)


# Price filter
min_price = float(df["Price"].min())
max_price = float(df["Price"].max())

selected_price = st.sidebar.slider(
    "💰 Maximum Price",
    min_value=min_price,
    max_value=max_price,
    value=max_price,
    step=1.0
)


# ---------------------------------------------------
# APPLY FILTERS
# ---------------------------------------------------

filtered_df = df[
    (df["Genre"].isin(selected_genres)) &
    (df["Year"].between(selected_years[0], selected_years[1])) &
    (df["User Rating"].between(selected_rating[0], selected_rating[1])) &
    (df["Price"] <= selected_price)
].copy()


# ---------------------------------------------------
# NO DATA MESSAGE
# ---------------------------------------------------

if filtered_df.empty:

    st.warning(
        "⚠️ No books match the selected filters. "
        "Please adjust the filters."
    )

    st.stop()


# ---------------------------------------------------
# KPI SECTION
# ---------------------------------------------------

st.markdown(
    '<div class="section-title">📊 Key Statistics</div>',
    unsafe_allow_html=True
)

col1, col2, col3, col4 = st.columns(4)


with col1:
    st.metric(
        "📚 Total Books",
        f"{len(filtered_df):,}"
    )


with col2:
    st.metric(
        "⭐ Average Rating",
        f"{filtered_df['User Rating'].mean():.2f}"
    )


with col3:
    st.metric(
        "💰 Average Price",
        f"${filtered_df['Price'].mean():.2f}"
    )


with col4:
    st.metric(
        "💬 Total Reviews",
        f"{filtered_df['Reviews'].sum():,.0f}"
    )


# ---------------------------------------------------
# CHART 1 — BOOKS BY YEAR
# ---------------------------------------------------

st.markdown(
    '<div class="section-title">📈 Books Published by Year</div>',
    unsafe_allow_html=True
)

books_by_year = (
    filtered_df
    .groupby("Year")
    .size()
    .reset_index(name="Books")
)

fig_year = px.line(
    books_by_year,
    x="Year",
    y="Books",
    markers=True,
    title="Number of Bestselling Books by Year"
)

fig_year.update_layout(
    xaxis_title="Year",
    yaxis_title="Number of Books",
    hovermode="x unified"
)

st.plotly_chart(
    fig_year,
    use_container_width=True
)


# ---------------------------------------------------
# TWO COLUMN CHART SECTION
# ---------------------------------------------------

col1, col2 = st.columns(2)


# ---------------------------------------------------
# CHART 2 — AVERAGE RATING BY GENRE
# ---------------------------------------------------

with col1:

    st.subheader("⭐ Average Rating by Genre")

    rating_by_genre = (
        filtered_df
        .groupby("Genre")["User Rating"]
        .mean()
        .reset_index()
        .sort_values("User Rating", ascending=False)
    )

    fig_rating = px.bar(
        rating_by_genre,
        x="Genre",
        y="User Rating",
        title="Average User Rating by Genre",
        text_auto=".2f"
    )

    fig_rating.update_layout(
        xaxis_title="Genre",
        yaxis_title="Average Rating"
    )

    st.plotly_chart(
        fig_rating,
        use_container_width=True
    )


# ---------------------------------------------------
# CHART 3 — AVERAGE PRICE BY GENRE
# ---------------------------------------------------

with col2:

    st.subheader("💰 Average Price by Genre")

    price_by_genre = (
        filtered_df
        .groupby("Genre")["Price"]
        .mean()
        .reset_index()
        .sort_values("Price", ascending=False)
    )

    fig_price = px.bar(
        price_by_genre,
        x="Genre",
        y="Price",
        title="Average Book Price by Genre",
        text_auto=".2f"
    )

    fig_price.update_layout(
        xaxis_title="Genre",
        yaxis_title="Average Price ($)"
    )

    st.plotly_chart(
        fig_price,
        use_container_width=True
    )


# ---------------------------------------------------
# CHART 4 — RATING VS REVIEWS
# ---------------------------------------------------

st.markdown(
    '<div class="section-title">🔍 Rating vs Reviews</div>',
    unsafe_allow_html=True
)

fig_scatter = px.scatter(
    filtered_df,
    x="User Rating",
    y="Reviews",
    size="Reviews",
    hover_name="Name",
    hover_data=[
        "Author",
        "Price",
        "Year",
        "Genre"
    ],
    title="Relationship Between User Rating and Reviews"
)

fig_scatter.update_layout(
    xaxis_title="User Rating",
    yaxis_title="Number of Reviews"
)

st.plotly_chart(
    fig_scatter,
    use_container_width=True
)


# ---------------------------------------------------
# TOP AUTHORS
# ---------------------------------------------------

st.markdown(
    '<div class="section-title">🏆 Top Authors</div>',
    unsafe_allow_html=True
)

top_authors = (
    filtered_df
    .groupby("Author")
    .size()
    .reset_index(name="Bestseller Appearances")
    .sort_values(
        "Bestseller Appearances",
        ascending=False
    )
    .head(10)
)

fig_authors = px.bar(
    top_authors.sort_values("Bestseller Appearances"),
    x="Bestseller Appearances",
    y="Author",
    orientation="h",
    title="Top 10 Authors by Bestseller Appearances",
    text_auto=True
)

fig_authors.update_layout(
    xaxis_title="Bestseller Appearances",
    yaxis_title="Author"
)

st.plotly_chart(
    fig_authors,
    use_container_width=True
)


# ---------------------------------------------------
# TOP BOOKS
# ---------------------------------------------------

st.markdown(
    '<div class="section-title">📖 Most Reviewed Books</div>',
    unsafe_allow_html=True
)

top_books = (
    filtered_df[
        [
            "Name",
            "Author",
            "User Rating",
            "Reviews",
            "Price",
            "Year",
            "Genre"
        ]
    ]
    .sort_values("Reviews", ascending=False)
    .head(10)
)

st.dataframe(
    top_books,
    use_container_width=True,
    hide_index=True
)


# ---------------------------------------------------
# RAW DATASET
# ---------------------------------------------------

st.markdown(
    '<div class="section-title">📄 Dataset</div>',
    unsafe_allow_html=True
)

with st.expander("View Raw Dataset"):

    st.write(
        f"Showing {len(filtered_df):,} books after applying filters."
    )

    st.dataframe(
        filtered_df,
        use_container_width=True,
        hide_index=True
    )


# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------

st.markdown("---")

st.caption(
    "📚 Amazon Bestselling Books EDA Dashboard | "
    "Built with Python, Pandas, Plotly and Streamlit"
)