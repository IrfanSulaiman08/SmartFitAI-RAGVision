import numpy as np
import pickle
from tensorflow.keras.models import load_model

model = load_model("model/lstm_exercise_model.h5", compile=False)

with open("model/label_encoder.pkl", "rb") as f:
    label_encoder = pickle.load(f)

def predict_exercise(sequence):

    sequence = np.array(sequence)

    if sequence.shape != (30, 132):
        return "Collecting..."

    sequence = sequence.reshape(1, 30, 132)

    pred = model.predict(sequence)
    label = label_encoder.inverse_transform([pred.argmax()])[0]

    return label
