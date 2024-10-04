#!/usr/bin/env python

import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import argparse


parser = argparse.ArgumentParser(description='Create mel-spectrogram, spectrogram, and extract sound characteristics from a WAV file')
parser.add_argument('input_file', type=str, help='Input WAV file')
args = parser.parse_args()


# Load audio file
audio, sr = librosa.load(args.input_file)

# Extract sound characteristics
duration = librosa.get_duration(y=audio, sr=sr)
tempo, beats = librosa.beat.beat_track(y=audio, sr=sr)
chroma_stft = librosa.feature.chroma_stft(y=audio, sr=sr)
rms = librosa.feature.rms(y=audio)
spectral_centroid = librosa.feature.spectral_centroid(y=audio, sr=sr)
spectral_bandwidth = librosa.feature.spectral_bandwidth(y=audio, sr=sr)
rolloff = librosa.feature.spectral_rolloff(y=audio, sr=sr)

# Create mel-spectrogram
mel_spectrogram = librosa.feature.melspectrogram(y=audio, sr=sr, n_mels=128)
log_mel_spectrogram = librosa.power_to_db(mel_spectrogram, ref=np.max)

# Create spectrogram
stft = np.abs(librosa.stft(audio))
db_stft = librosa.amplitude_to_db(stft, ref=np.max)

# Display mel-spectrogram and spectrogram
plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
librosa.display.specshow(log_mel_spectrogram, sr=sr, x_axis='time', y_axis='mel')
plt.title('Mel-Spectrogram')
plt.colorbar(format='%+2.0f dB')

plt.subplot(1, 2, 2)
librosa.display.specshow(db_stft, sr=sr, x_axis='time', y_axis='hz')
plt.title('Spectrogram')
plt.colorbar(format='%+2.0f dB')

plt.tight_layout()
plt.show()

# Print sound characteristics
print('Duration:', duration)
print('Tempo:', tempo)
print('Beats:', beats)
print('Chroma STFT:', chroma_stft.shape)
print('RMS:', rms.shape)
print('Spectral Centroid:', spectral_centroid.shape)
print('Spectral Bandwidth:', spectral_bandwidth.shape)
print('Spectral Rolloff:', rolloff.shape)
