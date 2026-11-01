import numpy as np
import soundfile as sf

# Create 5 seconds of silent audio
sample_rate = 16000
duration = 5

silent_audio = np.zeros(
    sample_rate * duration,
    dtype=np.float32
)

sf.write(
    "guard_silent_test.wav",
    silent_audio,
    sample_rate
)

print("Silent test audio created successfully.")