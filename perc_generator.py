import wavio
import numpy as np
import os
from datetime import datetime


class Generator:
    def __init__(self, text: str, bpm: int, res: float, dynamic_min: float, dynamic_max: float, date=True):
        self.text = text
        self.file_name = 'perc'
        self.bpm = bpm
        self.rate = 44100
        self.sample_dir = 'Samples'
        self.res = res
        self.dynamic_min = dynamic_min
        self.dynamic_max = dynamic_max
        self.date = date

        self.text_bin = []
        self.samples = []
        self.date_time = datetime.now().strftime("%d_%m_%H_%M_%S")
        self.length_beat = int(self.rate * 60 * 4 * res / bpm)
        length_all = int(8 * self.length_beat * len(text))
        self.pos = 0

        self.wav_array = np.zeros(int(length_all))

    @property
    def random_dyn(self):
        return self.dynamic_min + (self.dynamic_max - self.dynamic_min) * np.random.random()

    def string_to_bytes(self):
        for char in self.text.encode():
            char_new = bin(char).split('b')[1]
            char_new = f'{char_new}0'
            self.text_bin.append(char_new)

    def bytes_to_sound(self):
        for char in self.text_bin:
            for bit in char:
                if bit == '0':
                    self.append_sample()
                self.pos += self.length_beat

    def append_sine(self):
        t_signal = np.linspace(0, self.length_beat / self.rate, self.length_beat)
        self.wav_array[self.pos:self.pos + self.length_beat] = self.random_dyn * np.sin(
            2 * np.pi * self.freq * t_signal)

    def load_samples(self):
        for sample in os.listdir(self.sample_dir):
            if sample.endswith('.wav'):
                wav_data = wavio.read(f'{self.sample_dir}/{sample}')
                left_channel = wav_data.data.T[0]
                self.samples.append(left_channel)

    def append_sample(self):
        random_index = np.random.randint(len(self.samples))
        random_sample = self.samples[random_index]
        if len(random_sample) < self.length_beat:
            self.wav_array[self.pos:self.pos + len(random_sample)] = self.random_dyn * random_sample
        else:
            self.wav_array[self.pos:self.pos + self.length_beat] = self.random_dyn * random_sample[0:self.length_beat]

    def export_wav_file(self):
        if not os.path.exists('Exports'):
            os.mkdir('Exports')
        if self.date:
            self.file_name = f'{self.file_name}_{self.date_time}'
        wavio.write(f'Exports/{self.file_name}.wav', self.wav_array, self.rate, sampwidth=3)

    def export(self):
        self.load_samples()
        self.string_to_bytes()
        self.bytes_to_sound()
        self.export_wav_file()


if __name__ == '__main__':
    g = Generator('A', 90, 1 / 32, 0.5, 1, date=False)
    g.export()
