"""Visitor-to-guard prototype: multilingual visitor speech -> English for guard.

Extracted from the team's Colab prototype (Faster Whisper small + M2M100 418M).
This is intentionally separate from guard_pipeline.py (guard -> visitor).
Models are loaded lazily; weights are downloaded at first use.
"""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import torch
from faster_whisper import WhisperModel
from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer

SUPPORTED_LANGUAGES = {"ar", "zh", "en", "fr", "ru", "es"}
MODEL_ID = "facebook/m2m100_418M"


class VisitorToGuard:
    """Run automatic language detection, speech recognition, then English MT."""

    def __init__(self, device: str = "auto"):
        if device == "auto":
            device = "cuda" if torch.cuda.is_available() else "cpu"
        if device not in {"cpu", "cuda"}:
            raise ValueError("device must be auto, cpu or cuda")
        if device == "cuda" and not torch.cuda.is_available():
            raise RuntimeError("CUDA requested but not available")

        self.device = device
        self.asr = WhisperModel(
            "small",
            device=device,
            compute_type="float16" if device == "cuda" else "int8",
        )
        self.tokenizer = M2M100Tokenizer.from_pretrained(MODEL_ID)
        self.mt_model = M2M100ForConditionalGeneration.from_pretrained(
            MODEL_ID
        ).to(device)
        self.mt_model.eval()

    def translate_to_english(self, text: str, language: str) -> str:
        if language not in SUPPORTED_LANGUAGES:
            raise ValueError(f"Unsupported detected language: {language}")
        if not text.strip():
            raise ValueError("No speech recognized; translation cancelled")
        if language == "en":
            return text

        self.tokenizer.src_lang = language
        inputs = self.tokenizer(
            text, return_tensors="pt", truncation=True
        ).to(self.device)
        with torch.inference_mode():
            tokens = self.mt_model.generate(
                **inputs,
                forced_bos_token_id=self.tokenizer.get_lang_id("en"),
                max_new_tokens=100,
                num_beams=4,
            )
        return self.tokenizer.batch_decode(
            tokens, skip_special_tokens=True
        )[0].strip()

    def process(self, audio_path: str) -> dict:
        path = Path(audio_path)
        if not path.is_file():
            raise FileNotFoundError(f"Audio file not found: {path}")

        start = time.perf_counter()
        segments, info = self.asr.transcribe(str(path), beam_size=5)
        transcript = " ".join(
            segment.text.strip() for segment in segments
        ).strip()
        asr_seconds = time.perf_counter() - start

        start = time.perf_counter()
        english = self.translate_to_english(transcript, info.language)
        translation_seconds = time.perf_counter() - start

        return {
            "detected_language": info.language,
            "language_probability": round(info.language_probability, 3),
            "transcription": transcript,
            "english_translation": english,
            "asr_seconds": round(asr_seconds, 2),
            "translation_seconds": round(translation_seconds, 2),
            "total_seconds": round(asr_seconds + translation_seconds, 2),
        }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("audio_path", help="Path to .wav, .mp3, or .m4a recording")
    parser.add_argument("--device", choices=["auto", "cpu", "cuda"], default="auto")
    args = parser.parse_args()
    result = VisitorToGuard(device=args.device).process(args.audio_path)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
