from scipy.io import wavfile
import os
import sounddevice
import numpy as np


class Tone(object):
    def __init__(self, wav_file_path):
        self.wav_file_path = wav_file_path
        self.frequency = float(wav_file_path[-15:-7])
        self.scientific_name = wav_file_path[-6:-4]

        # Set in read()
        self.rate, self.data = None, None
        self.num_total_samples = self.num_channels = None, None
        self.total_duration_sec = None

    def read(self):
        self.rate, self.data = wavfile.read(self.wav_file_path)
        self.num_total_samples, self.num_channels = self.data.shape
        self.total_duration_sec = self.num_total_samples / float(self.rate)

    def play(self):
        sounddevice.play(self.data, self.rate, blocking=True)

    def get_channel(self, channel):
        return self.data[:,channel]

    @property
    def time(self):
        return np.array(range(1, self.num_total_samples + 1))

    def __str__(self):
        return "Tone: %s (%.4f Hz)" \
               % (self.scientific_name, self.frequency)

    def __repr__(self):
        return "Tone: %s (%.4f Hz) at %d samples/second with %d channels with %d samples over %.2f seconds" \
               % (self.scientific_name, self.frequency, self.rate, self.num_channels, self.num_total_samples, self.total_duration_sec)


class ToneLibrary(object):
    def __init__(self, directory):
        self._tones = None
        self.directory = directory

    def populate(self):
        self._tones = []
        wav_file_names = sorted([file for file in os.listdir(self.directory) if file.endswith('.wav')])
        for wav_file_name in wav_file_names:
            wav_file_path = os.path.join(self.directory, wav_file_name)
            tone = Tone(wav_file_path)
            tone.read()
            self._tones.append(tone)

    def __getitem__(self, item):
        for tone in self._tones:
            if tone.scientific_name == item:
                return tone
        return None

    def __len__(self):
        return len(self._tones)

    def __iter__(self):
        return iter(self._tones)
