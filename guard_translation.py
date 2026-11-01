from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer

# Load the local translation model
print("Loading translation model...")

model_name = "facebook/m2m100_418M"

tokenizer = M2M100Tokenizer.from_pretrained(model_name)
model = M2M100ForConditionalGeneration.from_pretrained(model_name)

# Guard's English response
english_text = "I'm not sure which room your meeting is in. Please wait while I check the building directory."
# Translate English to Chinese
tokenizer.src_lang = "en"

inputs = tokenizer(
    english_text,
    return_tensors="pt"
)

translated_tokens = model.generate(
    **inputs,
    forced_bos_token_id=tokenizer.get_lang_id("zh"),
    max_new_tokens=100
)

chinese_text = tokenizer.batch_decode(
    translated_tokens,
    skip_special_tokens=True
)[0]

print("\nOriginal English:")
print(english_text)

print("\nTranslated Chinese:")
print(chinese_text)