import wave

with wave.open("saveyourtears.wav", "rb") as handle:
    params = handle.getparams()
    # only read the first 10 seconds of audio
    frames = handle.readframes(441000)
    print(handle.tell())

print(params)
params = list(params)
params[3] = len(frames)
print(params)

with wave.open("output_wavfile.wav", "wb") as handle:
    handle.setparams(params)
    handle.setnframes(441000)