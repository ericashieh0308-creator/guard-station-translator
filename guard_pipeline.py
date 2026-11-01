
import whisper
import subprocess
import sys
from pathlib import Path
from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer

# Step 1: Check audio file
audio_file = Path("guard_test.wav")

if not audio_file.is_file():
    print("\nError: Audio file not found.")
    print("Translation cancelled. Please check the recording file.")
    sys.exit(1)

# Step 2: Load Whisper and recognize English speech
print("Loading Whisper model...")
whisper_model = whisper.load_model("tiny")

print("Recognizing English speech...")
result = whisper_model.transcribe(
    str(audio_file),
    language="en",
    fp16=False
)

english_text = result["text"].strip()

if not english_text:
    print("\nError: No English speech detected.")
    print("Translation cancelled. Please record audio again.")
    sys.exit(1)

print("\nRecognized English:")
print(english_text)

# Step 3: Select visitor language
languages = {
    "1": ("Chinese", "zh"),
    "2": ("Spanish", "es"),
    "3": ("French", "fr"),
    "4": ("Russian", "ru"),
    "5": ("Arabic", "ar")
}

print("\nSelect visitor language:")

for number, (name, code) in languages.items():
    print(f"{number}. {name}")

choice = input("Enter language number (1-5): ").strip()

if choice not in languages:
    print("\nInvalid language selection. Translation cancelled.")
    sys.exit(1)

language_name, target_language = languages[choice]
print(f"\nSelected language: {language_name}")

# Step 4: Load M2M100 translation model
print("\nLoading M2M100 translation model...")

model_name = "facebook/m2m100_418M"

try:
    tokenizer = M2M100Tokenizer.from_pretrained(model_name)
    translation_model = M2M100ForConditionalGeneration.from_pretrained(
        model_name
    )

    tokenizer.src_lang = "en"

    inputs = tokenizer(
        english_text,
        return_tensors="pt"
    )

    # Step 5: Translate to selected language
    translated_tokens = translation_model.generate(
        **inputs,
        forced_bos_token_id=tokenizer.get_lang_id(target_language),
        max_new_tokens=100
    )

    translated_text = tokenizer.batch_decode(
        translated_tokens,
        skip_special_tokens=True
    )[0].strip()

except Exception as error:
    print("\nError: Translation failed.")
    print("Translation cancelled. No message will be shown to the visitor.")
    print(f"Technical details: {type(error).__name__}")
    sys.exit(1)

if not translated_text:
    print("\nError: Translation returned empty text.")
    print("Translation cancelled.")
    sys.exit(1)

# Step 6: Guard reviews translation
print(f"\n{language_name} Translation (NOT YET APPROVED):")
print(translated_text)

print("\nGuard review required.")

approval = input("Approve translation? (yes/no): ").strip().lower()

if approval == "yes":
    approved_text = translated_text

elif approval == "no":
    print("\nTranslation NOT approved.")

    correction = input(
        f"Enter corrected {language_name} translation "
        "(or press Enter to cancel): "
    ).strip()

    if not correction:
        print("\nTranslation cancelled.")
        sys.exit(0)

    print("\nCorrected translation:")
    print(correction)

    confirm = input(
        "Approve corrected translation? (yes/no): "
    ).strip().lower()

    if confirm == "yes":
        approved_text = correction
    else:
        print("\nTranslation cancelled.")
        sys.exit(0)

else:
    print("\nInvalid response. Translation cancelled.")
    sys.exit(1)

# Step 7: Open Visitor Display only after approval
print("\nOpening Visitor Display...")

try:
    subprocess.run(
        [
            sys.executable,
            "visitor_display.py",
            approved_text,
            target_language
        ],
        check=True
    )

except (OSError, subprocess.CalledProcessError) as error:
    print("\nError: Visitor Display could not be opened.")
    print(f"Technical details: {type(error).__name__}")
    sys.exit(1)
