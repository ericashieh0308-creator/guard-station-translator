# Visitor-to-Guard (prototype)

This folder-level module complements the existing `guard_pipeline.py` **guard-to-visitor** workflow without modifying it.

## What it does

An audio file from a visitor is processed by Faster Whisper `small` for speech recognition and automatic language identification, then by Meta M2M100 `facebook/m2m100_418M` to produce English text for a guard. For detected English, translation is skipped.

Supported languages: `ar`, `zh`, `en`, `fr`, `ru`, `es`.

## Files

- `visitor_to_guard.py`: reusable Python module with command-line interface
- `visitor_batch_evaluate.py`: resumable CSV-based batch evaluator
- `Visitor_to_Guard_Pilot_Report.md`: evaluation design, initial results, limitations
- `visitor_to_guard_requirements.txt`: Python dependencies

## Install

Tested prototype: Google Colab on a Tesla T4 GPU. Standalone CPU fallback is provided but can be slower. PyTorch/CUDA compatibility depends on your machine.

```bash
python -m pip install -r visitor_to_guard_requirements.txt
```

For some GPU environments, CTranslate2/faster-whisper also needs appropriate NVIDIA CUDA and cuDNN libraries. In Colab, the original prototype installed `nvidia-cublas-cu12` and `nvidia-cudnn-cu12` and loaded these libraries prior to initializing Whisper.

## Transcribe and translate a recording

```bash
python visitor_to_guard.py path/to/es_01.m4a --device auto
```

Returns a JSON object with language, language probability, transcription, English translation and processing times.

## Run batch evaluation

The local evaluation CSV must already exist and have a unique `test_id` column and the result columns documented in the report.

```bash
python visitor_batch_evaluate.py \
  --evaluation-csv /path/to/visitor_guard_evaluation.csv \
  --audio-root /path/to/audio_recordings \
  --device auto
```

Use audio filenames such as `es/es_01.m4a` under the audio root. This script skips rows already containing an ASR transcription. Save audio, reference transcripts, and any sensitive data outside GitHub. The evaluator **does not assign correctness scores automatically**; WER and semantic correctness need independently checked references.

## Current validation

The first pilot processed 3 Spanish recordings: 3/3 language IDs matched Spanish, 0% transcription WER **against prepared scripts**, and mean processing time 2.10s. These are preliminary results and do not indicate performance across all six languages. See `Visitor_to_Guard_Pilot_Report.md`.

## Integration note

The current module only returns English output; there is no guard-facing production interface or formal guard approval workflow. Treat translations as unverified, especially for safety or access-related messages. The existing guard-to-visitor interface remains unchanged.
