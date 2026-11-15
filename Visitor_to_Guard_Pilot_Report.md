# Visitor-to-Guard Module — Initial Evidence and Pilot Results

**Project:** Multilingual Guard-Station Communication Assistant (NYU SPS Capstone)  
**Component:** Visitor-to-Guard (separate from the guard-to-visitor workflow)  
**Status:** Colab prototype working; multilingual evaluation ongoing  
**Evaluation recorded:** November 2026

## Objective

Accept a visitor's recorded speech, automatically identify its language, transcribe it, and translate it to English for the guard to read. Supported language codes in this prototype: Arabic (`ar`), Mandarin Chinese (`zh`), English (`en`), French (`fr`), Russian (`ru`), Spanish (`es`).

## Technical approach

1. **ASR and language detection:** Faster Whisper `small` with automatic language identification and `beam_size=5`.
2. **Machine translation:** `facebook/m2m100_418M` with target language forced to English. English input is passed through without machine translation.
3. **Output:** detected language, model confidence estimate, source transcription, English translation, ASR duration, translation duration and combined processing duration.
4. **Environment:** Google Colab with GPU (Tesla T4 in the recorded pilot). Initial prototype used CUDA float16 ASR and GPU translation. The standalone module supports CPU fallback.
5. **Batch workflow:** matches `<language>_<scenario>.m4a` (or `.wav` / `.mp3`) to evaluation rows and saves new results to CSV, skipping completed IDs.

The visitor pipeline does **not** currently connect to the teammate's guard-to-visitor user interface or implement a formal human-approval gate. The English text must be reviewed before operational decisions, especially for emergencies, access control, and accessibility.

## Evaluation design

- **90 planned scenarios** = 15 visitor-intent scenarios × 6 languages.
- Scenarios include event directions, check-in, appointments, building access, facilities, lost property, accessibility, deliveries, emergencies and clarification.
- English reference prompts and 75 proposed translations into the other five languages have been prepared. Non-English scripts are **AI-reviewed only** and require independent fluent-speaker verification.
- Source recordings and the evolving CSV data are kept outside the repository pending privacy/data review. The initial pilot used three Spanish recordings.

## Initial Spanish pilot (3 recordings)

| Test ID | Detected language | ASR result vs prepared script | English translation | End-to-end time |
|---|---|---|---|---:|
| es_01 | es | Exact script match | Where does the event take place? | 2.99 s |
| es_03 | es | Exact script match | I am here to visit a student. where should I register? | 1.77 s |
| es_08 | es | Exact script match | Is there a bathroom on this floor? | 1.53 s |

### Preliminary metrics

- Detected language correctly for **3/3** Spanish pilot recordings.
- **0.0% script-based WER** across the three clips. The reference transcripts were copied from prepared scripts; audio-to-reference confirmation is still needed before treating this as independently validated WER.
- **2.10 seconds** average measured processing time for the three clips (2.99, 1.77, 1.53 seconds), excluding setup/model load.
- English translations were assessed as preserving the intended request in **3/3** pilot cases in an initial qualitative review; this is **not** an independent fluent-speaker evaluation.

These preliminary results do not demonstrate six-language accuracy, performance with noise, reproducible latency across machines, or production readiness.

## Evidence and known risks

- Pilot outputs are preserved in the project's Google Drive `visitor_guard_evaluation.csv`; the 90-row template and script review sheet are also in Drive.
- Model quality may vary by language, dialect, accent, background noise and speaking style.
- Whisper can hallucinate on silence or noisy input. Automatic language identification and translation require validation.
- M2M100 can change context-specific meanings (e.g., check-in, restroom, access directions), as observed during preparation of multilingual draft scripts.
- The current code cancels on empty transcription or unsupported detected language; it does not implement robust acoustic silence detection, a confidence threshold, or escalation policy.
- No personal visitor recordings or credentials should be committed to the repository.

## Next steps

1. Verify reference scripts with fluent speakers and confirm pilot recording transcripts.
2. Record a small cross-language pilot (one each in Arabic, Mandarin, English, French and Russian) before scaling to 90 tests.
3. Calculate WER for word-segmented languages, CER for Mandarin, language-detection accuracy, intent correctness and latency distributions.
4. Include noisy, silence and ambiguous-input cases, and design a guard review/escalation workflow.
5. Integrate the visitor-to-guard output safely into the team interface only after review.

**Scope note:** This report documents visitor-to-guard work only; see `Week6_Evidence_Test_Report.md` for the teammate's separate guard-to-visitor tests.
