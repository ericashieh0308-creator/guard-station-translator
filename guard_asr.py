import whisper

# Load the Whisper model locally
print("Loading Whisper model...")
model = whisper.load_model("tiny")

# Transcribe an English audio file
print("Transcribing audio...")
result = model.transcribe("guard_test.wav", language="en")

# Display the result
print("Recognized text:")
print(result["text"])