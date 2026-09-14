from __future__ import annotations

import os

import pandas as pd
import plotly.express as px
import streamlit as st
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("MONGO_DB", "dataset_zalupa")
COLLECTION_NAME = os.getenv("MONGO_COLLECTION", "customers")

st.set_page_config(
    page_title="Клиенты · MongoDB",
    page_icon="📊",
    layout="wide",
)


@st.cache_resource
def get_collection():
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=8000)
    client.admin.command("ping")
    return client[DB_NAME][COLLECTION_NAME]


@st.cache_data(ttl=60)
def load_customers() -> pd.DataFrame:
    collection = get_collection()
    docs = list(collection.find({}, {"_id": 0}))
    df = pd.DataFrame(docs)
    if df.empty:
        return df
    df["customer_age"] = pd.to_numeric(df["customer_age"], errors="coerce")
    df["customer_acquisition_cost"] = pd.to_numeric(
        df["customer_acquisition_cost"], errors="coerce"
    )
    return df


def apply_filters(df: pd.DataFrame) -> pd.DataFrame:
    st.sidebar.header("Фильтры")
    countries = sorted(df["customer_country"].dropna().unique())
    segments = sorted(df["customer_segment"].dropna().unique())
    regions = sorted(df["region"].dropna().unique())
    genders = sorted(df["gender"].dropna().unique())

    selected_countries = st.sidebar.multiselect("Страна", countries, default=countries)
    selected_segments = st.sidebar.multiselect("Сегмент", segments, default=segments)
    selected_regions = st.sidebar.multiselect("Регион", regions, default=regions)
    selected_genders = st.sidebar.multiselect("Пол", genders, default=genders)

    age_min, age_max = int(df["customer_age"].min()), int(df["customer_age"].max())
    age_range = st.sidebar.slider("Возраст", age_min, age_max, (age_min, age_max))

    filtered = df[
        df["customer_country"].isin(selected_countries)
        & df["customer_segment"].isin(selected_segments)
        & df["region"].isin(selected_regions)
        & df["gender"].isin(selected_genders)
        & df["customer_age"].between(age_range[0], age_range[1])
    ]
    return filtered


def kpi_row(df: pd.DataFrame) -> None:
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Клиентов", f"{len(df):,}".replace(",", " "))
    c2.metric("Средний возраст", f"{df['customer_age'].mean():.1f}")
    c3.metric("Средний CAC", f"${df['customer_acquisition_cost'].mean():.2f}")
    c4.metric("Суммарный CAC", f"${df['customer_acquisition_cost'].sum():,.0f}")


def main() -> None:
    st.title("Визуализация клиентского датасета")
    st.caption(f"Источник: MongoDB `{DB_NAME}.{COLLECTION_NAME}`")

    try:
        df = load_customers()
    except Exception as exc:
        st.error(
            "Не удалось подключиться к MongoDB. "
            "Запустите контейнер и скрипт загрузки (`load_to_mongo.py`)."
        )
        st.exception(exc)
        return

    if df.empty:
        st.warning("Коллекция пустая. Сначала выполните `python load_to_mongo.py`.")
        return

    filtered = apply_filters(df)
    if filtered.empty:
        st.info("Нет записей по выбранным фильтрам.")
        return

    kpi_row(filtered)
    st.divider()

    left, right = st.columns(2)
    with left:
        seg = (
            filtered.groupby("customer_segment", as_index=False)
            .size()
            .rename(columns={"size": "count"})
            .sort_values("count", ascending=False)
        )
        fig = px.bar(
            seg,
            x="customer_segment",
            y="count",
            color="customer_segment",
            title="Клиенты по сегментам",
        )
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

        gender = (
            filtered.groupby("gender", as_index=False)
            .size()
            .rename(columns={"size": "count"})
        )
        fig = px.pie(gender, names="gender", values="count", title="Пол")
        st.plotly_chart(fig, use_container_width=True)

    with right:
        country = (
            filtered.groupby("customer_country", as_index=False)
            .size()
            .rename(columns={"size": "count"})
            .sort_values("count", ascending=False)
        )
        fig = px.bar(
            country,
            x="customer_country",
            y="count",
            title="Клиенты по странам",
        )
        st.plotly_chart(fig, use_container_width=True)

        cac_seg = (
            filtered.groupby("customer_segment", as_index=False)[
                "customer_acquisition_cost"
            ]
            .mean()
            .sort_values("customer_acquisition_cost", ascending=False)
        )
        fig = px.bar(
            cac_seg,
            x="customer_segment",
            y="customer_acquisition_cost",
            title="Средний CAC по сегментам",
        )
        st.plotly_chart(fig, use_container_width=True)

    fig = px.histogram(
        filtered,
        x="customer_age",
        nbins=20,
        color="customer_segment",
        title="Распределение возраста",
    )
    st.plotly_chart(fig, use_container_width=True)

    region_country = (
        filtered.groupby(["region", "customer_country"], as_index=False)
        .size()
        .rename(columns={"size": "count"})
    )
    fig = px.treemap(
        region_country,
        path=["region", "customer_country"],
        values="count",
        title="Регион → страна",
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Таблица клиентов")
    st.dataframe(filtered, use_container_width=True, hide_index=True)


if __name__ == "__main__":
    main()
