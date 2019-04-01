import numpy as np

def fft(signal, rate):
    """
    Helper function to make use of numpy's FFT functionality.
    Based on https://plot.ly/matplotlib/fft/
    :return: A tuple of the freqencies and corresponding amplitudes in the Frequency vs. Amplitude domain.
    """
    n = len(signal)

    k = np.arange(n)
    T = n / rate
    # two-sided frequency range:
    freq = k / T
    # one-sided frequency range:
    freq = freq[range(int(n / 2))]

    # FFT + Normalization
    y = np.fft.fft(signal) / n
    y = y[range(int(n / 2))]
    y = abs(y)

    return freq, y

def sample_tone(tone, sample_ratio):
    num_samples = int(tone.num_total_samples * sample_ratio)
    return tone.time[:num_samples], tone.get_channel(1)[:num_samples]

def estimate_peak_freq(signal, rate):
    fft_freq, fft_y = fft(signal, rate)
    max_fft_y_index = np.argmax(fft_y)
    return fft_freq[max_fft_y_index]
