
import pandas as pd

from sqlalchemy import (
    MetaData,
    Table,
    Column,
    Integer,
    String,
    DateTime,
    func
)
from sqlalchemy.dialects.postgresql import insert

from src.database import engine


metadata = MetaData()

customers_table = Table(
    "customers",
    metadata,

    Column("customer_id", Integer, primary_key=True),
    Column("first_name", String(100), nullable=False),
    Column("last_name", String(100), nullable=False),
    Column("email", String(255), nullable=False),
    Column("phone", String(20), nullable=False),
    Column("city", String(100), nullable=False),
    Column(
        "created_at",
        DateTime,
        server_default=func.now()
    ),
    Column(
        "updated_at",
        DateTime,
        server_default=func.now()
    )
)


def load_customers(data: pd.DataFrame) -> int:
    """
    Insert new customers or update existing customers.

    Returns:
        Number of records processed.
    """

    if not data.empty:
        print("No valid records to load.")
        return 0

    records = data.to_dict(orient="records")

    metadata.create_all(engine)

    statement = insert(customers_table).values(records)

    update_values = {
        column: getattr(statement.excluded, column)
        for column in [
            "first_name",
            "last_name",
            "email",
            "phone",
            "city"
        ]
    }

    update_values["updated_at"] = func.now()

    statement = statement.on_conflict_do_update(
        index_elements=["customer_id"],
        set_=update_values
    )

    with engine.begin() as connection:
        connection.execute(statement)

    print(f"Successfully loaded {len(records)} customer records.")

    return len(records)


if __name__ == "__main__":
    from src.extract import extract_csv
    from src.transform import transform_customers
    from src.validate import validate_customers

    raw_data = extract_csv("data/raw/customers.csv")
    transformed_data = transform_customers(raw_data)

    valid_records, rejected_records = validate_customers(
        transformed_data
    )

    load_customers(valid_records)
