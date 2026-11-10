
from pathlib import Path
import pandas as pd


def extract_csv(file_path: str) -> pd.DataFrame:
    """
    Extract customer records from a CSV file.

    Args:
        file_path: Location of the source CSV file.

    Returns:
        DataFrame containing extracted records.
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Source file not found: {path}"
        )

    if path.suffix.lower() != ".csv":
        raise ValueError("Only CSV files are supported.")

    try:
        data = pd.read_csv(path)

        if data.empty:
            raise ValueError("Source CSV contains no records.")

        return data

    except pd.errors.EmptyDataError as error:
        raise ValueError("Source CSV is empty.") from error


if __name__ == "__main__":
    source = "data/raw/customers.csv"

    customers = extract_csv(source)

    print("Extraction successful!")
    print(f"Records extracted: {len(customers)}")
    print(customers)
