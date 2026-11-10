
import pandas as pd

from src.transform import transform_customers


def test_transform_customer_data():
    data = pd.DataFrame({
        "customer_id": [1],
        "first_name": ["  JOHN  "],
        "last_name": [" doe "],
        "email": [" JOHN@EXAMPLE.COM "],
        "phone": ["403-123-4567"],
        "city": [" calgary "]
    })

    result = transform_customers(data)

    assert result.iloc[0]["first_name"] == "John"
    assert result.iloc[0]["last_name"] == "Doe"
    assert result.iloc[0]["email"] == "john@example.com"
    assert result.iloc[0]["phone"] == "4031234567"
    assert result.iloc[0]["city"] == "Calgary"


def test_transform_does_not_modify_original():
    data = pd.DataFrame({
        "customer_id": [1],
        "first_name": [" JOHN "],
        "last_name": [" DOE "],
        "email": [" JOHN@EXAMPLE.COM "],
        "phone": ["403-123-4567"],
        "city": [" calgary "]
    })

    original = data.copy()

    transform_customers(data)

    pd.testing.assert_frame_equal(data, original)
