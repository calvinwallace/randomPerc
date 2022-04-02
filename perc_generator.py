import wavio
import numpy as np
import os

text = 'Deine Mutter'
file_name = 'perc_test'
bpm = 90
rate = 44100
res = 1 / 32
freq = 100
sample_dir = 'Hats'
dynamic_min = 0.7
dynamic_max = 0.8

text_bin = []
samples = []
length_beat = int(rate * 60 * 4 * res / bpm)
length_all = int(8 * length_beat * len(text))
pos = 0

wav_array = np.zeros(int(length_all))


def random_dyn():
    return dynamic_min + (dynamic_max - dynamic_min) * np.random.random()


def string_to_bytes():
    for char in text.encode():
        char_new = bin(char).split('b')[1]
        char_new = f'{char_new}0'
        text_bin.append(char_new)


def bytes_to_sound():
    global pos
    for char in text_bin:
        for bit in char:
            if bit == '0':
                append_sample()
            pos += length_beat


def append_sine():
    global wav_array
    t_signal = np.linspace(0, length_beat / rate, length_beat)
    wav_array[pos:pos + length_beat] = random_dyn() * np.sin(2 * np.pi * freq * t_signal)


def load_samples():
    for sample in os.listdir(sample_dir):
        if sample.endswith('.wav'):
            wav_data = wavio.read(f'{sample_dir}/{sample}')
            left_channel = wav_data.data.T[0]
            samples.append(left_channel)


def append_sample():
    global wav_array
    random_index = np.random.randint(len(samples))
    random_sample = samples[random_index]
    if len(random_sample) < length_beat:
        wav_array[pos:pos + len(random_sample)] = random_dyn() * random_sample
    else:
        wav_array[pos:pos + length_beat] = random_dyn() * random_sample[0:length_beat]


def export_wav_file():
    if not os.path.exists('wav'):
        os.mkdir('wav')
    wavio.write(f'wav/{file_name}.wav', wav_array, rate, sampwidth=3)


if __name__ == '__main__':
    load_samples()
    string_to_bytes()
    bytes_to_sound()
    export_wav_file()
