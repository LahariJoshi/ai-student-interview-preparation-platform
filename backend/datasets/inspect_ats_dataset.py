from datasets import load_dataset

DATASET_NAME = "0xnbk/resume-ats-score-v1-en"

dataset = load_dataset(DATASET_NAME)

print("\n========== DATASET INFO ==========")
print(dataset)

print("\n========== TRAIN FEATURES ==========")
print(dataset["train"].features)

print("\n========== DATASET INFO ==========")
print(dataset["train"].info)