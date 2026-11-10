
import pandas as pd
from unittest.mock import patch

from src.load import load_customers


def test_load_empty_dataframe():
    data = pd.DataFrame()

    result = load_customers(data)

    assert result == 0


@patch("src.load.engine.begin")
def test_load_customer_records(mock_begin):
    data = pd.DataFrame({
        "customer_id": [1, 2],
        "first_name": ["John", "Jane"],
        "last_name": ["Doe", "Smith"],
        "email": ["john@example.com", "jane@example.com"],
        "phone": ["4031234567", "5871234567"],
        "city": ["Calgary", "Edmonton"]
    })

    result = load_customers(data)

    assert result == 2
    assert mock_begin.call_count==2


@patch("src.load.engine.begin")
def test_load_single_customer(mock_begin):
    data = pd.DataFrame({
        "customer_id": [3],
        "first_name": ["Robert"],
        "last_name": ["Brown"],
        "email": ["robert@example.com"],
        "phone": ["7801234567"],
        "city": ["Lethbridge"]
    })

    result = load_customers(data)

    assert result == 1
    assert mock_begin.call_count == 2
