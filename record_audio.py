import sounddevice as sd
import soundfile as sf

# Recording settings
sample_rate = 16000
duration = 8
filename = "guard_test.wav"

print("Recording will start now.")
print("Please speak English into your microphone.")

# Record audio
audio = sd.rec(
    int(duration * sample_rate),
    samplerate=sample_rate,
    channels=1,
    dtype="float32"
)

sd.wait()

# Save the recording
sf.write(filename, audio, sample_rate)

print("Recording completed!")
print("Saved as:", filename)