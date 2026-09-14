#!/usr/bin/env python3
"""Загрузка customer_master.csv в MongoDB."""

from __future__ import annotations

import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("MONGO_DB", "dataset_zalupa")
COLLECTION_NAME = os.getenv("MONGO_COLLECTION", "customers")
CSV_PATH = Path(__file__).parent / "customer_master.csv"


def main() -> None:
    if not CSV_PATH.exists():
        raise FileNotFoundError(f"Не найден файл: {CSV_PATH}")

    df = pd.read_csv(CSV_PATH)
    df["customer_age"] = pd.to_numeric(df["customer_age"], errors="coerce")
    df["customer_acquisition_cost"] = pd.to_numeric(
        df["customer_acquisition_cost"], errors="coerce"
    )
    df["customer_postal_code"] = df["customer_postal_code"].astype(str)
    records = df.to_dict(orient="records")

    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=8000)
    client.admin.command("ping")
    collection = client[DB_NAME][COLLECTION_NAME]
    collection.drop()
    collection.insert_many(records)
    collection.create_index("customer_id", unique=True)
    collection.create_index("customer_country")
    collection.create_index("customer_segment")
    collection.create_index("region")

    print(
        f"Загружено {collection.count_documents({})} документов "
        f"в {DB_NAME}.{COLLECTION_NAME}"
    )
    client.close()


if __name__ == "__main__":
    main()
