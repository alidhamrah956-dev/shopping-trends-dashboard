import pandas as pd
import plotly.express as px
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Customer Shopping Trends Dashboard",
    page_icon="🛍️",
    layout="wide",
)

# Load Data


@st.cache_data
def load_data():
  return pd.read_csv("shopping_trends_updated.csv")


df = load_data()

# Sidebar Filters
st.sidebar.header("🔍 Dashboard Filters")

selected_gender = st.sidebar.multiselect(
    "Select Gender",
    options=df["Gender"].unique(),
    default=df["Gender"].unique(),
)
selected_category = st.sidebar.multiselect(
    "Select Category",
    options=df["Category"].unique(),
    default=df["Category"].unique(),
)
selected_season = st.sidebar.multiselect(
    "Select Season",
    options=df["Season"].unique(),
    default=df["Season"].unique(),
)

# Filter Data
filtered_df = df[
    df["Gender"].isin(selected_gender)
    & df["Category"].isin(selected_category)
    & df["Season"].isin(selected_season)
]

# Main Dashboard Title
st.title("🛍️ Customer Shopping Trends & Analytics Dashboard")
st.markdown(
    "Interactive dashboard analyzing customer demographics, purchasing"
    " behaviors, and seasonal trends."
)
st.markdown("---")

# Top KPI Summary Cards
col1, col2, col3, col4 = st.columns(4)

total_cust = filtered_df["Customer ID"].nunique()
total_rev = filtered_df["Purchase Amount (USD)"].sum()
avg_purchase = (
    filtered_df["Purchase Amount (USD)"].mean() if total_cust > 0 else 0
)
avg_rating = (
    filtered_df["Review Rating"].mean() if total_cust > 0 else 0
)

col1.metric("Total Transactions", f"{total_cust:,}")
col2.metric("Total Revenue", f"${total_rev:,.2f}")
col3.metric("Average Purchase", f"${avg_purchase:.2f}")
col4.metric("Average Review Rating", f"{avg_rating:.2f} / 5.0")

st.markdown("---")

# Row 1: Charts
row1_col1, row1_col2 = st.columns(2)

with row1_col1:
  st.subheader("📦 Purchases by Product Category")
  cat_df = (
      filtered_df.groupby("Category")["Purchase Amount (USD)"]
      .agg(["count", "mean"])
      .reset_index()
  )
  fig_cat = px.bar(
      cat_df,
      x="Category",
      y="count",
      text="count",
      color="Category",
      labels={"count": "Transaction Count", "Category": "Product Category"},
      title="Transaction Volume per Category",
  )
  st.plotly_chart(fig_cat, use_container_width=True)

with row1_col2:
  st.subheader("🌦️ Purchase Amount by Season")
  season_df = (
      filtered_df.groupby("Season")["Purchase Amount (USD)"]
      .mean()
      .reset_index()
  )
  fig_season = px.bar(
      season_df,
      x="Season",
      y="Purchase Amount (USD)",
      color="Season",
      text_auto=".2f",
      labels={
          "Purchase Amount (USD)": "Average Purchase ($)",
          "Season": "Season",
      },
      title="Average Spending Across Seasons",
  )
  st.plotly_chart(fig_season, use_container_width=True)

# Row 2: Demographics & Payment
row2_col1, row2_col2 = st.columns(2)

with row2_col1:
  st.subheader("👥 Customer Gender Distribution")
  gender_df = filtered_df["Gender"].value_counts().reset_index()
  gender_df.columns = ["Gender", "Count"]
  fig_gender = px.pie(
      gender_df,
      names="Gender",
      values="Count",
      hole=0.4,
      title="Gender Breakdown",
  )
  st.plotly_chart(fig_gender, use_container_width=True)

with row2_col2:
  st.subheader("💳 Preferred Payment Methods")
  pay_df = filtered_df["Payment Method"].value_counts().reset_index()
  pay_df.columns = ["Payment Method", "Count"]
  fig_pay = px.bar(
      pay_df,
      x="Payment Method",
      y="Count",
      color="Payment Method",
      title="Transactions by Payment Method",
  )
  st.plotly_chart(fig_pay, use_container_width=True)

# Row 3: Age & Subscriptions
row3_col1, row3_col2 = st.columns(2)

with row3_col1:
  st.subheader("👤 Customer Age Distribution")
  fig_age = px.histogram(
      filtered_df,
      x="Age",
      nbins=20,
      title="Age Spread of Shoppers",
      labels={"Age": "Customer Age", "count": "Number of Customers"},
  )
  st.plotly_chart(fig_age, use_container_width=True)

with row3_col2:
  st.subheader("⭐ Subscription Status")
  sub_df = filtered_df["Subscription Status"].value_counts().reset_index()
  sub_df.columns = ["Subscription Status", "Count"]
  fig_sub = px.pie(
      sub_df,
      names="Subscription Status",
      values="Count",
      title="Active Subscribers vs Non-Subscribers",
      color_discrete_sequence=px.colors.qualitative.Pastel,
  )
  st.plotly_chart(fig_sub, use_container_width=True)

# Raw Data Preview
with st.expander("🔍 View Filtered Raw Data Table"):
  st.dataframe(filtered_df)
