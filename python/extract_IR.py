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

import librosa
import matplotlib.pyplot as plt
import numpy as np
import scipy
import scipy.io


def normalize(signal, rms_level=0):
    """
    Normalize the signal to a specified RMS level.

    Args:
        signal (numpy array): Input signal.
        rms_level (float): RMS level in dB for normalization (default: 0 dB).

    Returns:
        numpy array: Normalized signal.
    """
    linear_rms = 10 ** (rms_level / 10.0)
    scaling_factor = np.sqrt((len(signal) * linear_rms ** 2) / np.sum(signal ** 2))
    return signal * scaling_factor


def extract_ir_sweep(sweep_response, inv_sweep_fft):
    """
    Extract the impulse response (IR) from a sweep response signal.

    Args:
        sweep_response (numpy array): Recorded device-specific sweep response.
        inv_sweep_fft (numpy array): FFT of the inverse sweep.

    Returns:
        tuple: Linear IR and Non-linear IR components.
    """
    if sweep_response.ndim > 1:
        sweep_response = sweep_response.T

    fft_size = inv_sweep_fft.shape[1]
    sweep_fft = scipy.fft.fft(sweep_response, fft_size)

    # Convolution in the frequency domain
    ir = np.real(scipy.fft.ifft(inv_sweep_fft * sweep_fft))
    ir = np.roll(ir.T, ir.shape[1] // 2)

    ir_lin = ir[len(ir) // 2:]
    ir_non_lin = ir[:len(ir) // 2]

    return ir_lin, ir_non_lin


def nmse_error(signal, reference_signal):
    """
    Calculate the Normalized Mean Squared Error (NMSE) for two signals.

    Args:
        signal (numpy array): Input signal for comparison.
        reference_signal (numpy array): Reference signal to compare against.

    Returns:
        float: Normalized mean squared error.
    """
    if len(signal) != len(reference_signal):
        return 0
    return np.mean((signal - reference_signal) ** 2) / np.mean((reference_signal - np.mean(reference_signal)) ** 2)


def process_device_signals(
        sweep_path,
        original_speech_path,
        device_speech_path,
        inv_sweep_fft,
        margin=0,
        sample_rate=None,
        window_duration=5,
        plot_results=False,
        save_output=False,
        output_ir_path=None,
        output_plot_path=None
):
    """
    Process a single device's sweep and speech signals to compute errors and IRs.

    Args:
        sweep_path (str): Path to the recorded sweep signal.
        original_speech_path (str): Path to the original clean speech signal.
        device_speech_path (str): Path to the device-specific speech signal.
        inv_sweep_fft (numpy array): FFT of the inverse sweep.
        margin (int): Margin to crop the speech signals (default: 0).
        sample_rate (int): Sample rate for audio signals (default: None).
        window_duration (int): Duration of windows for error analysis (default: 5 seconds).
        plot_results (bool): Whether to display plots of results (default: False).
        save_output (bool): Whether to save the IR and plots (default: False).
        output_ir_path (str): Path to save the computed impulse response (IR).
        output_plot_path (str): Path to save the error plots.

    Returns:
        tuple: Two lists - NMSE mean values and slope values for all analysis windows.
    """
    # Load recorded sweep and extract IR
    sweep_signal, fs = librosa.load(sweep_path, sr=sample_rate)
    ir_lin, _ = extract_ir_sweep(sweep_signal, inv_sweep_fft)

    # Load original speech and device-recorded speech
    speech_original, _ = librosa.load(original_speech_path, sr=sample_rate)
    speech_device, _ = librosa.load(device_speech_path, sr=sample_rate)

    # Convolve the original signal with the linear IR
    speech_reconstructed = np.convolve(speech_original, ir_lin[3000:6000, 0], mode='same')

    # Adjust device-reconstructed speech based on the given margin
    speech_device_mod = speech_device[margin:]
    speech_reconstructed_mod = speech_reconstructed[:-margin]

    # Analyze using sliding windows
    win_len = int(window_duration * fs)
    num_windows = len(speech_device_mod) // win_len
    err_min_all, err_pos_all = [], []

    for i in range(num_windows):
        start = i * win_len
        end = (i + 1) * win_len
        win_device = speech_device_mod[start:end]
        win_reconstructed = speech_reconstructed_mod[start:end]

        err_list, shifts = [], np.arange(-200, 200)

        # Compute error for shifted windows
        for shift in shifts:
            err = nmse_error(
                win_reconstructed[200 + shift: -200 + shift],
                win_device[200: -200]
            )
            err_list.append(err)

        # Find minimum error and optimal shift
        errors = 10 * np.log10(err_list)  # Convert to dB
        err_min_all.append(np.min(errors))
        err_pos_all.append(shifts[np.argmin(errors)])

    # Calculate slope for all shifts across windows
    slope = (err_pos_all[-1] - err_pos_all[0]) / len(err_pos_all)

    # (Optional) Save IR to file system
    if save_output and output_ir_path:
        np.save(output_ir_path, ir_lin[3000:6000, 0])

    # (Optional) Plot and save results
    if plot_results:
        plt.figure(figsize=(10, 6))
        plt.plot(err_min_all, label=f'NMSE VALUE [dB] - Mean: {np.mean(err_min_all):.2f}')
        plt.plot(err_pos_all, label=f'SHIFT VALUE - Slope: {slope:.2f}')
        plt.ylabel('Error and Shifts')
        plt.xlabel('Window Index')
        plt.legend()
        plt.title("Convolution Error Analysis")
        if save_output and output_plot_path:
            plt.savefig(output_plot_path, bbox_inches='tight')
        plt.show()

    return err_min_all, slope


if __name__ == "__main__":
    # Example of usage for a single device:
    # This is now a general-purpose script that can process any device or signal setup.

    # Load inverse sweep FFT
    inverse_sweep_path = 'invsweepfft.mat'
    mat = scipy.io.loadmat(inverse_sweep_path)
    inv_sweep_fft = mat['invsweepfft']

    # Paths of input and output files (replace with actual paths)
    sweep_path = '/path/to/device/sweep.wav'
    original_speech_path = '/path/to/original/speech.wav'
    device_speech_path = '/path/to/device/speech.wav'
    output_ir_path = '/path/to/output/ir.npy'
    output_plot_path = '/path/to/output/error_plot.pdf'

    # Run processing for a single configuration
    process_device_signals(
        sweep_path=sweep_path,
        original_speech_path=original_speech_path,
        device_speech_path=device_speech_path,
        inv_sweep_fft=inv_sweep_fft,
        margin=200,
        sample_rate=16000,
        window_duration=5,
        plot_results=True,
        save_output=True,
        output_ir_path=output_ir_path,
        output_plot_path=output_plot_path
    )
