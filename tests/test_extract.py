
import pytest
import pandas as pd

from src.extract import extract_csv


def test_extract_valid_csv(tmp_path):
    file = tmp_path / "customers.csv"

    file.write_text(
        "customer_id,first_name,email\n"
        "1,John,john@example.com\n"
        "2,Jane,jane@example.com\n"
    )

    result = extract_csv(str(file))

    assert len(result) == 2
    assert result.iloc[0]["first_name"] == "John"


def test_extract_missing_file():
    with pytest.raises(FileNotFoundError):
        extract_csv("missing.csv")


def test_extract_invalid_extension(tmp_path):
    file = tmp_path / "customers.txt"
    file.write_text("some data")

    with pytest.raises(ValueError):
        extract_csv(str(file))


def test_extract_empty_csv(tmp_path):
    file = tmp_path / "empty.csv"
    file.write_text("")

    with pytest.raises(ValueError):
        extract_csv(str(file))


def test_extract_csv_with_headers_only(tmp_path):
    file = tmp_path / "headers.csv"
    file.write_text("customer_id,first_name,email\n")

    with pytest.raises(ValueError):
        extract_csv(str(file))
