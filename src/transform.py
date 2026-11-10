
import pandas as pd


def transform_customers(data: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and standardize customer records.
    """

    transformed = data.copy()

    # Standardize names
    for column in ["first_name", "last_name"]:
        transformed[column] = (
            transformed[column]
            .astype("string")
            .str.strip()
            .str.title()
        )

    # Normalize email addresses
    transformed["email"] = (
        transformed["email"]
        .astype("string")
        .str.strip()
        .str.lower()
    )

    # Standardize phone numbers
    transformed["phone"] = (
        transformed["phone"]
        .astype("string")
        .str.replace(r"\D", "", regex=True)
    )

    # Standardize city names
    transformed["city"] = (
        transformed["city"]
        .astype("string")
        .str.strip()
        .str.title()
    )

    return transformed


if __name__ == "__main__":
    from src.extract import extract_csv

    customers = extract_csv("data/raw/customers.csv")
    cleaned = transform_customers(customers)

    print("Transformation successful!")
    print(cleaned.to_string(index=False))
