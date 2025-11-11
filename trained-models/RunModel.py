import os
from DataPreprocessing import DataPreprocessing
from DataUnderstanding import DataUnderstanding
from HeartRateModel import HeartRateModel

def main(json_file_path, model_save_path):
    # Initialize classes
    data_prep = DataPreprocessing()
    data_understanding = DataUnderstanding()
    heart_rate_model = HeartRateModel()

    # Load and preprocess the data
    df = data_prep.load_data(json_file_path)
    df = data_prep.filter_by_confidence(df)
    df = data_prep.sort_data(df)
    df = data_prep.check_time_interval(df)
    df = data_prep.handle_missing_values(df)
    df = data_prep.remove_outliers(df)
    df = data_prep.remove_noise(df)
    df, scaler = data_prep.normalize_data(df)

    # Perform data understanding/visualization
    # data_understanding.descriptive_statistics(df)
    # data_understanding.distribution_analysis(df)
    # data_understanding.time_series_analysis(df)
    # data_understanding.correlation_analysis(df)
    # data_understanding.outlier_detection(df)
    # data_understanding.seasonal_trend_analysis(df)
    # data_understanding.missing_data_analysis(df)
    # data_understanding.confidence_level_analysis(df)

    # Prepare data for LSTM model
    X_train, X_test, y_train, y_test, scaler = heart_rate_model.prepare_lstm_data(df)

    # Hyperparameter tuning (optional)
    # Uncomment the following line to perform hyperparameter tuning
    best_model = heart_rate_model.tune_hyperparameters(X_train, y_train)

  # Check if the model file already exists
    if os.path.exists(model_save_path):
        print(f"Model already exists at {model_save_path}. Loading the model...")
        heart_rate_model.load_model(model_save_path)
    else:
        # Build and train the model if it doesn't exist
        heart_rate_model.build_lstm_model(input_shape=(X_train.shape[1], X_train.shape[2]))
        heart_rate_model.train_model(X_train, y_train)
        # Save the trained model
        heart_rate_model.save_model(model_save_path)
    # Evaluate the model
    heart_rate_model.evaluate_model(X_test, y_test, scaler)

if __name__ == "__main__":
    json_file_path = '../../datasets/hr/heartrate.json'  # Replace with your JSON file path
    model_save_path = 'saved_models/heart_rate_model.h5'  # Path where you want to save the model
    main(json_file_path, model_save_path)
