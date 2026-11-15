"""Batch-process visitor recordings into an existing evaluation CSV.

The evaluation CSV is stored locally (often on Google Drive) and is not committed.
Only rows with missing ASR outputs are processed. Scores are NOT assigned here:
ground-truth transcription and intent review must be independently verified.
"""

import argparse
from pathlib import Path

import pandas as pd

from visitor_to_guard import VisitorToGuard

LANGUAGES = ("ar", "zh", "en", "fr", "ru", "es")
EXTENSIONS = {".m4a", ".mp3", ".wav"}
TEXT_COLUMNS = (
    "audio_file", "detected_language", "asr_transcription",
    "english_translation",
)


def process_batch(evaluation_csv: Path, audio_root: Path, device: str = "auto"):
    df = pd.read_csv(evaluation_csv)
    required = {"test_id", "asr_transcription", *TEXT_COLUMNS}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing CSV columns: {sorted(missing)}")
    if df["test_id"].duplicated().any():
        raise ValueError("Duplicate test_id values in evaluation CSV")

    for column in TEXT_COLUMNS:
        df[column] = df[column].astype("string")

    pending = []
    skipped = 0
    for language in LANGUAGES:
        folder = audio_root / language
        if not folder.is_dir():
            continue
        for path in sorted(folder.iterdir()):
            if path.suffix.lower() not in EXTENSIONS:
                continue
            test_id = path.stem
            if not test_id.startswith(f"{language}_"):
                print(f"Skipping mismatched folder/filename: {path}")
                continue
            rows = df.index[df["test_id"] == test_id].tolist()
            if len(rows) != 1:
                print(f"Skipping unknown test ID: {test_id}")
                continue
            index = rows[0]
            current = df.at[index, "asr_transcription"]
            if pd.notna(current) and str(current).strip():
                skipped += 1
                continue
            pending.append((index, path))

    if not pending:
        print(f"No new files. Previously completed: {skipped}")
        return

    pipeline = VisitorToGuard(device=device)
    completed = 0
    failed = 0

    for index, audio_path in pending:
        print(f"Processing {audio_path.stem} ...")
        try:
            result = pipeline.process(str(audio_path))
            updates = {
                "audio_file": str(audio_path),
                "detected_language": result["detected_language"],
                "language_probability": result["language_probability"],
                "asr_transcription": result["transcription"],
                "english_translation": result["english_translation"],
                "asr_seconds": result["asr_seconds"],
                "translation_seconds": result["translation_seconds"],
                "total_seconds": result["total_seconds"],
            }
            for column, value in updates.items():
                df.at[index, column] = value
            completed += 1
        except Exception as exc:
            failed += 1
            print(f"Failed {audio_path.stem}: {type(exc).__name__}: {exc}")
        finally:
            # Retain successfully processed rows if a subsequent recording fails.
            df.to_csv(evaluation_csv, index=False, encoding="utf-8-sig")

    print(f"Newly processed: {completed}; skipped: {skipped}; failed: {failed}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evaluation-csv", type=Path, required=True)
    parser.add_argument("--audio-root", type=Path, required=True)
    parser.add_argument("--device", choices=["auto", "cpu", "cuda"], default="auto")
    args = parser.parse_args()
    process_batch(args.evaluation_csv, args.audio_root, args.device)
