import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import pickle

def prepare_data(path):

    df = pd.read_csv(path)

    X = []
    y = []

    sequence_length = 30

    data = df.drop("class", axis=1).values
    labels = df["class"].values

    # group into sequences of 30 frames
    for i in range(0, len(data), sequence_length):

        if i + sequence_length <= len(data):

            seq = data[i:i+sequence_length]
            label = labels[i]

            X.append(seq)
            y.append(label)

    X = np.array(X)
    y = np.array(y)

    # encode labels
    le = LabelEncoder()
    y = le.fit_transform(y)

    # save encoder
    with open("model/label_encoder.pkl", "wb") as f:
        pickle.dump(le, f)

    return train_test_split(X, y, test_size=0.2)
