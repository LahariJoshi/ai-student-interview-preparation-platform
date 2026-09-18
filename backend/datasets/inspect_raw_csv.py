import csv

CSV_PATH = r"C:\Users\JOSHI KRISHNA LAHARI\.cache\huggingface\hub\datasets--0xnbk--resume-ats-score-v1-en\snapshots\836a2db5ac95094bd423904c2b1a0d06f1b2a505\train.csv"

with open(CSV_PATH, "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    print("\n========== CSV COLUMNS ==========")
    print(reader.fieldnames)

    print("\n========== FIRST ROW ==========")

    row = next(reader)

    for column, value in row.items():
        print(f"\n--- {column} ---")
        print(value[:2000] if value else None)