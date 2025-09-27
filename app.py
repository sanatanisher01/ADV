import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
@st.cache_data
def load_data():
    return pd.read_csv("Olympic_Games_Medal_Tally.csv")

df = load_data()

st.title("🏅 Olympic Games Medal Tally Dashboard")

# Show raw dataset
if st.checkbox("Show Raw Data"):
    st.dataframe(df)

# Sidebar menu
st.sidebar.title("📊 Select Visualization")
options = [
    "Top 10 Countries by Total Medals",
    "Top 5 Countries Medal Growth Over Time",
    "India Medal Breakdown",
    "Top 15 Countries (Misleading Pie Chart)",
    "Top 15 Countries (Corrected Bar Chart)",
    "USA vs India Medal Growth",
    "India Since 2000",
    "USA Medal Breakdown Over Time"
]
choice = st.sidebar.radio("Choose a chart:", options)

# ---------------- Chart 1 ----------------
if choice == "Top 10 Countries by Total Medals":
    grouped = df.groupby("country")["total"].sum().sort_values(ascending=False)
    top10 = grouped.head(10)

    fig, ax = plt.subplots(figsize=(10,6))
    ax.barh(top10.index, top10.values, color="orange")
    ax.set_title("Top 10 Countries by Total Olympic Medals")
    ax.set_xlabel("Total Medals")
    ax.set_ylabel("Country")
    st.pyplot(fig)

# ---------------- Chart 2 ----------------
elif choice == "Top 5 Countries Medal Growth Over Time":
    grouped = df.groupby("country")["total"].sum().sort_values(ascending=False)
    top5 = grouped.head(5)
    top5_countries = list(top5.index)
    df_top = df[df["country"].isin(top5_countries)]
    df_grouped = df_top.groupby(["year","country"])["total"].sum().reset_index()

    fig, ax = plt.subplots(figsize=(14,8))
    for country in top5_countries:
        country_data = df_grouped[df_grouped["country"] == country]
        ax.plot(country_data["year"], country_data["total"], marker="o", label=country)

    ax.set_title("Medals Over Time: Top 5 Countries")
    ax.set_xlabel("Year")
    ax.set_ylabel("Total Medals")
    ax.legend()
    st.pyplot(fig)

# ---------------- Chart 3 ----------------
elif choice == "India Medal Breakdown":
    india_data = df[df["country"] == "India"]
    india_group = india_data.groupby("year")[["gold","silver","bronze"]].sum().reset_index()

    fig, ax = plt.subplots(figsize=(14,8))
    ax.bar(india_group["year"], india_group["gold"], color="gold", label="Gold")
    ax.bar(india_group["year"], india_group["silver"], bottom=india_group["gold"], color="silver", label="Silver")
    ax.bar(india_group["year"], india_group["bronze"], bottom=india_group["gold"] + india_group["silver"], color="brown", label="Bronze")
    ax.set_title("India's Olympic Medal Breakdown")
    ax.set_xlabel("Year")
    ax.set_ylabel("Number of Medals")
    ax.legend()
    st.pyplot(fig)

# ---------------- Chart 4 ----------------
elif choice == "Top 15 Countries (Misleading Pie Chart)":
    grouped = df.groupby("country")["total"].sum().sort_values(ascending=False)
    top15 = grouped.head(15)

    fig, ax = plt.subplots(figsize=(10,10))
    ax.pie(top15, labels=top15.index, autopct="%1.1f%%", startangle=140)
    ax.set_title("Medal Distribution (Misleading Pie Chart)")
    st.pyplot(fig)

# ---------------- Chart 5 ----------------
elif choice == "Top 15 Countries (Corrected Bar Chart)":
    grouped = df.groupby("country")["total"].sum().sort_values(ascending=False)
    top15 = grouped.head(15)

    fig, ax = plt.subplots(figsize=(12,8))
    ax.barh(top15.index, top15.values, color="pink")
    ax.set_title("Top 15 Countries by Total Medals (Corrected View)")
    ax.set_xlabel("Total Medals")
    ax.set_ylabel("Country")
    st.pyplot(fig)

# ---------------- Chart 6 ----------------
elif choice == "USA vs India Medal Growth":
    story_data = df[df["country"].isin(["United States", "India"])]
    story_group = story_data.groupby(["year","country"])["total"].sum().reset_index()

    india_data = story_group[story_group["country"] == "India"]
    usa_data = story_group[story_group["country"] == "United States"]

    fig, ax = plt.subplots(figsize=(14,8))
    ax.plot(india_data["year"], india_data["total"], marker="o", label="India")
    ax.plot(usa_data["year"], usa_data["total"], marker="o", label="United States")
    ax.set_title("USA vs India: Medal Growth Over Time")
    ax.set_xlabel("Year")
    ax.set_ylabel("Total Medals")
    ax.legend()
    st.pyplot(fig)

# ---------------- Chart 7 ----------------
elif choice == "India Since 2000":
    india_recent = df[(df["country"]=="India") & (df["year"]>=2000)]

    fig, ax = plt.subplots(figsize=(10,5))
    sns.barplot(x="year", y="total", data=india_recent, color="royalblue", ax=ax)
    ax.set_title("India’s Olympic Medals Since 2000")
    ax.set_xlabel("Year")
    ax.set_ylabel("Total Medals")
    st.pyplot(fig)

# ---------------- Chart 8 ----------------
elif choice == "USA Medal Breakdown Over Time":
    usa_data = df[df["country"] == "United States"]
    usa_group = usa_data.groupby("year")[["gold","silver","bronze"]].sum().reset_index()

    fig, ax = plt.subplots(figsize=(14,8))
    ax.stackplot(usa_group["year"],
                usa_group["gold"],
                usa_group["silver"],
                usa_group["bronze"],
                labels=["Gold","Silver","Bronze"],
                colors=["gold","silver","brown"])
    ax.set_title("USA Olympic Medal Breakdown Over Time")
    ax.set_xlabel("Year")
    ax.set_ylabel("Number of Medals")
    ax.legend()
    st.pyplot(fig)
