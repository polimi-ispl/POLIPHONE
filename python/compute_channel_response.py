"""
------------------------------------------------------------------------------
POLIPHONE Code

This code is provided in connection with the article:

  "POLIPHONE: A Dataset for Smartphone Model Identification from Audio Recordings"
  Davide Salvi, Daniele Ugo Leonzio, Antonio Giganti, Claudio Eutizi,
  Sara Mandelli, Paolo Bestagini, and Stefano Tubaro.
  IEEE Access, 2025. DOI: 10.1109/ACCESS.2025.3545152

Copyright (c) 2025 by the authors. All rights reserved.

Redistribution and use in source and binary forms, with or without 
modification, are permitted for non-commercial research purposes provided 
that the original authors and the source publication are credited appropriately.

For any commercial use, please contact the copyright holders.

This software is provided "as is" without any express or implied
warranty.
------------------------------------------------------------------------------
"""

import os
import numpy as np
import librosa
import matplotlib.pyplot as plt
from glob import glob
from tqdm import tqdm


def nan_helper(array):
    """
    Helper function to handle NaN values in a 1D numpy array.

    Args:
        array (numpy array): Input array with potential NaN values.

    Returns:
        numpy array: Array with NaN values interpolated.
    """
    nan_indices = np.isnan(array)
    not_nan_indices = ~nan_indices

    array[nan_indices] = np.interp(
        nan_indices.nonzero()[0],
        not_nan_indices.nonzero()[0],
        array[not_nan_indices]
    )

    return array


def normalize_audio(sig, rms_level=0):
    """
    Normalize the signal given a certain technique (peak or rms).
    Args:
        - rms_level (int) : rms level in dB.
    """

    # linear rms level and scaling factor
    r = 10**(rms_level / 10.0)
    a = np.sqrt((len(sig) * r**2) / np.sum(sig**2))

    # normalize
    y = sig * a

    return y


def compute_channel_responses(
        input_folder, output_folder,
        signal_duration=4.0, overlap_fraction=0.2, threshold=0, sample_rate=16000,
        n_fft=512, hop_length=256, win_length=512, rms_level=0, plot=False
):
    """
    Process a collection of audio signals to compute and save their channel responses.

    Args:
        input_folder (str): Path to input folder containing audio files.
        output_folder (str): Path to save computed channel responses.
        signal_duration (float): Sliding window duration in seconds (default: 4.0).
        overlap_fraction (float): Fractional overlap between consecutive windows (default: 0.2).
        threshold (float): Threshold to truncate log power spectrogram values (default: 0).
        sample_rate (int): Sample rate for audio files (default: 16000 Hz).
        n_fft (int): Number of FFT components (default: 512).
        hop_length (int): Hop length for STFT (default: 256).
        win_length (int): Window length for STFT (default: 512).
        rms_level (float): RMS level to normalize signals (default: 0 dB).
        plot (bool): Whether to plot individual spectrograms for debugging (default: False).

    Returns:
        None
    """
    # Get list of input audio paths
    signal_paths = glob(input_folder)

    for signal_path in tqdm(signal_paths, total=len(signal_paths)):
        # Load and preprocess the audio signal
        signal, _ = librosa.load(signal_path, sr=sample_rate, mono=True)
        signal = normalize_audio(signal, rms_level=rms_level)
        signal = librosa.effects.preemphasis(signal)

        # Calculate window parameters
        window_samples = int(signal_duration * sample_rate)
        overlap_samples = int(overlap_fraction * sample_rate)
        step_size = window_samples - overlap_samples

        num_windows = (len(signal) - overlap_samples) // step_size

        for window_idx in range(num_windows):
            # Extract the windowed segment
            start = window_idx * step_size
            end = start + window_samples
            windowed_signal = signal[start:end]

            # Compute the Short-Time Fourier Transform (STFT)
            stft_result = librosa.stft(
                windowed_signal,
                n_fft=n_fft,
                hop_length=hop_length,
                win_length=win_length,
                window='hamming'
            )

            # Compute the log-scaled spectrogram
            log_spectrogram = 20 * np.log10(1e-9 + np.abs(stft_result))

            # Apply the threshold
            log_spectrogram[log_spectrogram > threshold] = np.nan

            # Optional plotting
            if plot:
                plt.imshow(log_spectrogram, aspect='auto')
                plt.colorbar()
                plt.show()

            # Compute the mean channel response, ignoring NaNs
            channel_response = np.nanmean(log_spectrogram, axis=1)

            # Save the response with device and speaker-specific naming
            device = signal_path.split('/')[-3]
            speaker = os.path.basename(signal_path).split('.')[0]
            save_path = os.path.join(output_folder, f'{device}_{speaker}_win_{window_idx}.npy')
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            np.save(save_path, channel_response)


if __name__ == '__main__':

    input_audio_folder = '/path/to/input/audio/'
    output_folder = '/path/to/output/folder'

    compute_channel_responses(input_audio_folder, output_folder)
