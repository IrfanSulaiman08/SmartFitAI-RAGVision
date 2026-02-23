import numpy as np
import pandas as pd
import os

# create dataset folder if not exists
if not os.path.exists("dataset"):
    os.makedirs("dataset")

classes = ["pushup", "squat", "plank", "bicep_curl"]

data = []

for cls in classes:
    for _ in range(1000):   # 1000 samples per exercise

        sequence = np.random.rand(30, 132)

        for frame in sequence:
            row = [cls] + frame.tolist()
            data.append(row)

# columns
columns = ["class"]
for i in range(132):
    columns.append(f"f{i}")

df = pd.DataFrame(data, columns=columns)

df.to_csv("dataset/dataset_all_points.csv", index=False)

print("✅ Dataset created successfully!")
