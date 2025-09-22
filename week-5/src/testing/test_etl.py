import pandas as pd
import os
import uuid
from src.utils.etl import *
import unittest

def make_sample_df():
    """Create a sample dataframe similar to your CSV input."""
    data = {
        "Drink": ["Latte, 2, £4.50", "Espresso, 1, £2.50"],
        "Branch": ["BranchA", "BranchB"],
        "Payment Type": ["Card", "Cash"],
        "Customer Name": ["Alice", "Bob"],
        "Card Number": ["1234", "5678"],
        "Date/Time": ["01/01/2024 10:00", "02/01/2024 15:30"]
    }
    return pd.DataFrame(data)

# ----------------------------
# UNIT TESTS
# ----------------------------

def test_extract():
    df = etl.extract()
    assert isinstance(df, pd.DataFrame)
    assert not df.empty

def test_remove_pii():
    df = make_sample_df()
    cleaned = etl.remove_pii(df.copy())
    assert "Customer Name" not in cleaned.columns
    assert "Card Number" not in cleaned.columns

def test_fix_df_structure():
    df = make_sample_df()
    fixed = etl.fix_df_structure(df.copy())
    # Payment Type column replaced
    assert "Payment Type" in fixed.columns
    assert "Branch" in fixed.columns

def test_split_items():
    df = make_sample_df()
    df = etl.fix_df_structure(df)
    df = etl.split_items(df)
    assert "Qty" in df.columns
    assert "Price" in df.columns
    assert df["Qty"].dtype == int
    assert df["Price"].dtype == float

def test_split_datetime():
    df = make_sample_df()
    df = etl.split_datetime(df.copy())
    assert "Date" in df.columns
    assert "Time" in df.columns
    assert all(df["Date"].str.match(r"\d{4}-\d{2}-\d{2}"))

def test_check_and_fill_missing():
    df = make_sample_df()
    df = etl.remove_pii(df)
    df["Drink"] = None  # force a missing value
    df, missing = etl.check_for_missing_vals(df)
    assert "Drink" in missing
    df_filled = etl.fill_missing_vals(df, missing)
    assert df_filled["Drink"].iloc[0] == "Unknown"

def test_generate_guid():
    guid1 = etl.generate_guid("test", "123")
    guid2 = etl.generate_guid("test", "123")
    guid3 = etl.generate_guid("different", "123")
    assert guid1 == guid2  # deterministic
    assert guid1 != guid3

def test_normalisation():
    df = make_sample_df()
    df = etl.fix_df_structure(df)
    df = etl.split_items(df)
    df = etl.split_datetime(df)
    df = etl.remove_pii(df)

    branches, transactions, products = etl.normalisation(df)
    assert isinstance(branches, list)
    assert isinstance(transactions, list)
    assert isinstance(products, list)
    assert "branch_id" in branches[0]
    assert "transaction_id" in transactions[0]
    assert "product_id" in products[0]

# ----------------------------
# INTEGRATION TEST (end-to-end)
# ----------------------------

def test_transform_pipeline():
    df = make_sample_df()
    df = etl.transform(df)
    assert "Date" in df.columns
    assert "Time" in df.columns
    assert "Qty" in df.columns
    assert "Price" in df.columns
    assert "Branch" in df.columns