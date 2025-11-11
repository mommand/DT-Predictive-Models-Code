import numpy as np
import tensorflow as tf
from DataPreprocessing import DataPreprocessing
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import LSTM, Dense, Input, Reshape, Flatten, LeakyReLU
from tensorflow.keras.optimizers import Adam

def build_generator(seq_length):
    model = Sequential()
    model.add(LSTM(50, return_sequences=True, input_shape=(seq_length, 1)))
    model.add(LSTM(50, return_sequences=False))
    model.add(Dense(25))
    model.add(Dense(1))
    model.add(Reshape((seq_length, 1)))  # Ensure this shape is correct
    return model

def build_discriminator(seq_length):
    model = Sequential()
    model.add(LSTM(50, return_sequences=True, input_shape=(seq_length, 1)))
    model.add(LSTM(50, return_sequences=False))
    model.add(Dense(25))
    model.add(LeakyReLU(alpha=0.2))
    model.add(Dense(1, activation='sigmoid'))
    return model
def build_gan(generator, discriminator):
    """
    Combines the generator and discriminator into a GAN model.
    """
    discriminator.trainable = False
    
    # GAN input: The noise vector or the input for generator
    gan_input = Input(shape=(seq_length, 1))
    
    # Generator output
    generated_sequence = generator(gan_input)
    
    # Ensure the output shape of the generator matches the input shape expected by the discriminator
    # This step depends on how the generator and discriminator are defined
    # If the generator already outputs the correct shape, this reshape may not be needed
    # gan_output = discriminator(Reshape((seq_length, 1))(generated_sequence))
    
    gan_output = discriminator(generated_sequence)
    
    gan = Model(gan_input, gan_output)
    gan.compile(loss='binary_crossentropy', optimizer=Adam())
    return gan

def train_gan(df, scaler, epochs=1000, batch_size=32, seq_length=10):
    # Training the GAN model
    def create_sequences(data, seq_length):
        X = []
        for i in range(len(data) - seq_length):
            X.append(data[i:i + seq_length])
        return np.array(X)

    real_data = create_sequences(df['bpm'].values, seq_length)
    real_data = real_data.reshape((real_data.shape[0], seq_length, 1))

    generator = build_generator(seq_length)
    discriminator = build_discriminator(seq_length)
    discriminator.compile(loss='binary_crossentropy', optimizer=Adam(), metrics=['accuracy'])
    gan = build_gan(generator, discriminator)

    real_labels = np.ones((batch_size, 1))
    fake_labels = np.zeros((batch_size, 1))

    for epoch in range(epochs):
        idx = np.random.randint(0, real_data.shape[0], batch_size)
        real_samples = real_data[idx]
        noise = np.random.normal(0, 1, (batch_size, seq_length, 1))
        fake_samples = generator.predict(noise)
        d_loss_real = discriminator.train_on_batch(real_samples, real_labels)
        d_loss_fake = discriminator.train_on_batch(fake_samples, fake_labels)
        d_loss = 0.5 * np.add(d_loss_real, d_loss_fake)
        noise = np.random.normal(0, 1, (batch_size, seq_length, 1))
        g_loss = gan.train_on_batch(noise, real_labels)

        if epoch % 100 == 0:
            print(f"Epoch: {epoch}, D Loss: {d_loss[0]}, D Acc: {d_loss[1]}, G Loss: {g_loss}")

    return generator

def predict_next_heart_rate(generator, df, scaler, seq_length=10):
    # Ensure that last_sequence has the correct shape
    last_sequence = df['bpm'].values[-seq_length:]
    
    if len(last_sequence) != seq_length:
        raise ValueError(f"The length of last_sequence ({len(last_sequence)}) does not match the expected sequence length ({seq_length}).")
    
    # Reshape the sequence to (1, seq_length, 1)
    last_sequence = last_sequence.reshape((1, seq_length, 1))

    # Generate the next bpm value using the generator
    predicted_bpm = generator.predict(last_sequence)

    # Inverse scaling to get the bpm value back to original scale
    predicted_bpm = scaler.inverse_transform(predicted_bpm)
    
    return predicted_bpm[0][0]

# Example usage
seq_length = 10
data_prep = DataPreprocessing()
json_file_path='../../datasets/hr/heartrate.json'
df = data_prep.load_data(json_file_path, date_format='%m/%d/%y %H:%M:%S')
df = data_prep.filter_by_confidence(df)
df = data_prep.sort_data(df)
df = data_prep.check_time_interval(df)
df = data_prep.handle_missing_values(df)
df = data_prep.remove_outliers(df)
df = data_prep.remove_noise(df)
df, scaler = data_prep.normalize_data(df)

generator = train_gan(df, scaler, seq_length=seq_length)

predicted_bpm = predict_next_heart_rate(generator, df, scaler, seq_length=seq_length)
print(f"Predicted next heart rate value: {predicted_bpm}")