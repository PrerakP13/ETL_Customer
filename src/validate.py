
import pandas as pd


REQUIRED_COLUMNS = [
    "customer_id",
    "first_name",
    "last_name",
    "email",
    "phone",
    "city"
]


def validate_customers(data: pd.DataFrame):
    """
    Validate customer records.

    Returns:
        valid_records: Records that pass validation.
        rejected_records: Records that fail validation.
    """

    valid = data.copy()

    # Check required columns
    missing_columns = [
        column for column in REQUIRED_COLUMNS
        if column not in valid.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    # Build validation conditions
    checks = pd.DataFrame(index=valid.index)

    for column in REQUIRED_COLUMNS:
        checks[column] = (
            valid[column].notna() &
            valid[column].astype("string").str.strip().ne("")
        )

    checks["email"] = (
        checks["email"] &
        valid["email"].str.match(
            r"^[^@\s]+@[^@\s]+\.[^@\s]+$",
            na=False
        )
    )

    checks["phone"] = (
        checks["phone"] &
        valid["phone"].str.match(r"^\d{10}$", na=False)
    )

    checks["customer_id"] = (
        checks["customer_id"] &
        ~valid["customer_id"].duplicated(keep=False)
    )

    # Identify valid and rejected records
    is_valid = checks.all(axis=1)

    valid_records = valid[is_valid].copy()
    rejected_records = valid[~is_valid].copy()

    # Explain why records were rejected
    rejected_records["error_reason"] = checks.loc[
        ~is_valid
    ].apply(
        lambda row: ", ".join(
            column for column, passed in row.items()
            if not passed
        ),
        axis=1
    )

    return valid_records, rejected_records


if __name__ == "__main__":
    from src.extract import extract_csv
    from src.transform import transform_customers

    customers = extract_csv("data/raw/customers.csv")
    cleaned = transform_customers(customers)

    valid, rejected = validate_customers(cleaned)

    print(f"Valid records: {len(valid)}")
    print(f"Rejected records: {len(rejected)}")

    if not rejected.empty:
        print(rejected.to_string(index=False))
