
import pandas as pd
import pytest

from src.validate import validate_customers


def test_valid_customer():
    data = pd.DataFrame({
        "customer_id": [1],
        "first_name": ["John"],
        "last_name": ["Doe"],
        "email": ["john@example.com"],
        "phone": ["4031234567"],
        "city": ["Calgary"]
    })

    valid, rejected = validate_customers(data)

    assert len(valid) == 1
    assert len(rejected) == 0


def test_invalid_email():
    data = pd.DataFrame({
        "customer_id": [1],
        "first_name": ["John"],
        "last_name": ["Doe"],
        "email": ["invalid-email"],
        "phone": ["4031234567"],
        "city": ["Calgary"]
    })

    valid, rejected = validate_customers(data)

    assert len(valid) == 0
    assert len(rejected) == 1
    assert "email" in rejected.iloc[0]["error_reason"]


def test_invalid_phone():
    data = pd.DataFrame({
        "customer_id": [1],
        "first_name": ["John"],
        "last_name": ["Doe"],
        "email": ["john@example.com"],
        "phone": ["12345"],
        "city": ["Calgary"]
    })

    valid, rejected = validate_customers(data)

    assert len(valid) == 0
    assert len(rejected) == 1
    assert "phone" in rejected.iloc[0]["error_reason"]


def test_duplicate_customer_ids():
    data = pd.DataFrame({
        "customer_id": [1, 1],
        "first_name": ["John", "Jane"],
        "last_name": ["Doe", "Smith"],
        "email": ["john@example.com", "jane@example.com"],
        "phone": ["4031234567", "5871234567"],
        "city": ["Calgary", "Edmonton"]
    })

    valid, rejected = validate_customers(data)

    assert len(valid) == 0
    assert len(rejected) == 2
    assert all(
        "customer_id" in reason
        for reason in rejected["error_reason"]
    )


def test_missing_required_column():
    data = pd.DataFrame({
        "customer_id": [1],
        "first_name": ["John"]
    })

    with pytest.raises(ValueError):
        validate_customers(data)
