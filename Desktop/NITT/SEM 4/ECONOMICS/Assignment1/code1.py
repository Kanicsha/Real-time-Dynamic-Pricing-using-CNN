import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.sequence import pad_sequences
import tensorflow as tf
from tensorflow.keras import layers, models

# Load and preprocess the data
df = pd.read_csv('dataset.csv')
df['Date'] = pd.to_datetime(df['Date'])
df = df.sort_values(by='Date')

# Prepare the sequences (7-day window)
window_size = 7
X, y = [], []

for i in range(len(df) - window_size):
    X.append(df[['amazon_price', 'in_store_price']].iloc[i:i+window_size].values)  # 7-day sequence
    y.append(df['amazon_price'].iloc[i + window_size])  # Target price for the next day

X = np.array(X)  # Shape: (samples, timesteps, features)
y = np.array(y)  # Shape: (samples,)

# Option 1: Padding Sequences (If the sequences are shorter than desired)
X = pad_sequences(X, maxlen=7, padding='post')

# Rescale the features
scaler = MinMaxScaler()
X = scaler.fit_transform(X.reshape(-1, X.shape[-1])).reshape(X.shape)

# Rescale the target variable
scaler_y = MinMaxScaler()
y = scaler_y.fit_transform(y.reshape(-1, 1))

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Build the CNN model
model = models.Sequential()

# 1D Convolutional Layer with a smaller kernel size
model.add(layers.Conv1D(filters=64, kernel_size=2, activation='relu', input_shape=(X_train.shape[1], X_train.shape[2])))

# MaxPooling Layer
model.add(layers.MaxPooling1D(pool_size=2))

# Second Convolutional Layer
model.add(layers.Conv1D(filters=128, kernel_size=2, activation='relu'))

# Second MaxPooling Layer
model.add(layers.MaxPooling1D(pool_size=2))

# Flatten the 3D output to 1D
model.add(layers.Flatten())

# Fully Connected Layer
model.add(layers.Dense(64, activation='relu'))

# Output Layer (for predicting the next day's price)
model.add(layers.Dense(1, activation='linear'))

# Compile the model
model.compile(optimizer='adam', loss='mean_squared_error')

# Train the model
model.fit(X_train, y_train, epochs=20, batch_size=32, validation_data=(X_test, y_test))

# Evaluate and make predictions
test_loss = model.evaluate(X_test, y_test)
print(f"Test Loss: {test_loss}")

predictions = model.predict(X_test)

# Inverse transform the predicted prices
predictions_rescaled = scaler_y.inverse_transform(predictions)

# Inverse transform the actual values from y_test
y_test_rescaled = scaler_y.inverse_transform(y_test)

# Compare predicted vs actual prices
for i in range(10):
    print(f"Predicted: {predictions_rescaled[i][0]}, Actual: {y_test_rescaled[i][0]}")