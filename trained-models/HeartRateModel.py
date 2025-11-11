import numpy as np
import matplotlib.pyplot as plt
from keras.models import Sequential, load_model
from keras.layers import LSTM, Dense, Dropout
from keras.optimizers import Adam
from keras_tuner import RandomSearch
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.preprocessing import MinMaxScaler
from keras.callbacks import EarlyStopping

class HeartRateModel:
    def __init__(self):
        self.model = None

    # Function to build the model with hyperparameters
    def build_lstm_model(self, input_shape, hp=None):
        """
        Define and compile the LSTM model with hyperparameter tuning.
        """
        model = Sequential()

        # LSTM layers with hyperparameter tuning
        model.add(LSTM(units=hp.Int('units_1', min_value=32, max_value=256, step=32) if hp else 64,
                       return_sequences=True, input_shape=input_shape))
        model.add(Dropout(rate=hp.Float('dropout_1', min_value=0.0, max_value=0.5, step=0.1) if hp else 0.2))

        model.add(LSTM(units=hp.Int('units_2', min_value=32, max_value=256, step=32) if hp else 64, return_sequences=False))
        model.add(Dropout(rate=hp.Float('dropout_2', min_value=0.0, max_value=0.5, step=0.1) if hp else 0.2))

        # Dense layers
        model.add(Dense(units=hp.Int('dense_units', min_value=10, max_value=100, step=10) if hp else 50))
        model.add(Dense(1))

        # Compile the model
        model.compile(optimizer=Adam(learning_rate=hp.Float('learning_rate', min_value=1e-4, max_value=1e-2, sampling='LOG') if hp else 0.0001),
                      loss='mean_squared_error',
                      metrics=['mean_absolute_error'])

        print("LSTM model built and compiled with hyperparameters.")
        self.model = model
        return model

    # Function to train the model
    def train_model(self, X_train, y_train, epochs=15, batch_size=32):
        """
        Train the LSTM model.
        """
        history = self.model.fit(X_train, y_train,
                                 epochs=epochs,
                                 batch_size=batch_size,
                                 validation_split=0.2,
                                 callbacks=[EarlyStopping(monitor='val_loss', patience=5)])
        print("Model training completed.")
        return history

    # Function to evaluate the model
    def evaluate_model(self, X_test, y_test, scaler, num_samples=None):
        """
        Evaluate the model and print accuracy metrics.
        Plot actual vs predicted BPM with enhanced clarity.
        """
        # Predict
        predictions = self.model.predict(X_test)

        # Inverse transform to get actual bpm values
        predictions = scaler.inverse_transform(predictions)
        y_test_actual = scaler.inverse_transform(y_test.reshape(-1, 1))

        # Calculate metrics
        mse = mean_squared_error(y_test_actual, predictions)
        mae = mean_absolute_error(y_test_actual, predictions)
        print(f"Model Evaluation Metrics:\nMSE: {mse:.4f}\nMAE: {mae:.4f}")

        # Determine the number of samples to plot
        if num_samples is None or num_samples > len(y_test_actual):
            num_samples = len(y_test_actual)

        # Plot Actual vs Predicted
        plt.figure(figsize=(14, 6))
        plt.plot(y_test_actual[:num_samples], label='Actual BPM', color='blue', linewidth=2)
        plt.plot(predictions[:num_samples], label='Predicted BPM', color='orange', linestyle='--', linewidth=2)
        plt.title('Actual vs Predicted BPM', fontsize=12)
        plt.xlabel('Samples', fontsize=10)
        plt.ylabel('BPM', fontsize=12)
        plt.legend(fontsize=12)
        plt.grid(True)
        plt.show()

    # Hyperparameter tuning using Keras Tuner
    def tune_hyperparameters(self, X_train, y_train):
        """
        Perform hyperparameter tuning using Keras Tuner.
        """
        tuner = RandomSearch(
            lambda hp: self.build_lstm_model(input_shape=(X_train.shape[1], X_train.shape[2]), hp=hp),
            objective='val_mean_absolute_error',
            max_trials=10,  # Number of models to try
            executions_per_trial=1,  # Number of times to train the model for each trial
            directory='tuning_dir',
            project_name='heart_rate_prediction'
        )

        # Perform hyperparameter search
        tuner.search(X_train, y_train, epochs=15, validation_split=0.2)

        # Retrieve the best model
        best_model = tuner.get_best_models(num_models=1)[0]
        print("Best hyperparameters found and model retrieved.")

        self.model = best_model
        return best_model

    def prepare_lstm_data(self, df, sequence_length=10):
        """
        Prepare data for LSTM model training.
        """
        data = df['bpm'].values
        scaler = MinMaxScaler(feature_range=(-1, 1))
        data = scaler.fit_transform(data.reshape(-1, 1))

        X, y = [], []
        for i in range(sequence_length, len(data)):
            X.append(data[i-sequence_length:i, 0])
            y.append(data[i, 0])

        X, y = np.array(X), np.array(y)

        X = np.reshape(X, (X.shape[0], X.shape[1], 1))

        # Splitting data into training and testing sets
        split_index = int(len(X) * 0.8)
        X_train, X_test = X[:split_index], X[split_index:]
        y_train, y_test = y[:split_index], y[split_index:]

        return X_train, X_test, y_train, y_test, scaler

    
    def save_model(self, model_path):
        """
        Save the trained model to the specified path.
        """
        self.model.save(model_path)
        print(f"Model saved to {model_path}")

    def load_model(self, model_path):
        """
        Load a model from the specified path.
        """
        self.model = load_model(model_path)
        print(f"Model loaded from {model_path}")
