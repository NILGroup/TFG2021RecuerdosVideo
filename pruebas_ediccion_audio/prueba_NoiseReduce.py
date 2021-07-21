import noisereduce as nr


# load data
from scipy.io import wavfile


rate, data = wavfile.read("../GH010191.wav")
# select section of data that is noise
noisy_part = data[10000:15000]
# perform noise reduction
reduced_noise = nr.reduce_noise(audio_clip=data, noise_clip=noisy_part, verbose=True)