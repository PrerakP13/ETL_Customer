
from src.extract import extract_csv
from src.transform import transform_customers
from src.validate import validate_customers
from src.load import load_customers


def run_pipeline():

    print("\n========== ETL PIPELINE STARTED ==========\n")

    # 1. Extraction
    raw_data = extract_csv("data/raw/customers.csv")
    print(f"[EXTRACT] Records extracted: {len(raw_data)}")

    # 2. Transformation
    transformed_data = transform_customers(raw_data)
    print("[TRANSFORM] Data transformation completed.")

    # 3. Validation
    valid_records, rejected_records = validate_customers(
        transformed_data
    )

    print(f"[VALIDATE] Valid records: {len(valid_records)}")
    print(f"[VALIDATE] Rejected records: {len(rejected_records)}")

    # 4. Loading
    loaded_count = load_customers(valid_records)

    print("\n========== PIPELINE SUMMARY ==========")
    print(f"Total extracted: {len(raw_data)}")
    print(f"Total valid: {len(valid_records)}")
    print(f"Total rejected: {len(rejected_records)}")
    print(f"Total loaded: {loaded_count}")
    print("\n========== ETL PIPELINE COMPLETED ==========\n")


if __name__ == "__main__":
    run_pipeline()
