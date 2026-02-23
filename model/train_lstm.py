from prepare_data import prepare_data
from lstm_model import build_model
import numpy as np

X_train, X_test, y_train, y_test = prepare_data(
    "dataset/dataset_all_points.csv"
)

model = build_model(
    input_shape=(X_train.shape[1], X_train.shape[2]),
    num_classes=len(np.unique(y_train))
)

model.fit(
    X_train,
    y_train,
    epochs=20,
    batch_size=32,
    validation_data=(X_test, y_test)
)

model.save("model/lstm_exercise_model.h5")
print("✅ LSTM model trained and saved")
