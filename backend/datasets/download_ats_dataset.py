from datasets import load_dataset

DATASET_NAME = "0xnbk/resume-ats-score-v1-en"

print("Downloading dataset...")

dataset = load_dataset(DATASET_NAME)

print("\nDataset downloaded successfully!")
print(dataset)

for split in dataset:
    print(f"{split}: {len(dataset[split])} rows")