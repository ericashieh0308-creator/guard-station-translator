
# Week 6 Evidence Test Report
## Multilingual Guard-Station Communication Assistant

**Component:** Guard-to-Visitor Workflow  
**Testing Period:** Week 6, Fall 2026  
**Test Environment:** Windows, Python 3.12, PyCharm  
**Technologies:** Whisper Tiny, M2M100, Tkinter  
**Supported Languages:** Chinese, Spanish, French, Russian, Arabic

---

## 1. Testing Objective

The objective of Week 6 testing was to evaluate the functional reliability, multilingual display behavior, error handling, and human approval controls of the Guard-to-Visitor communication workflow.

The workflow uses Whisper for English speech recognition, M2M100 for multilingual translation, a guard review and approval step, and a Tkinter interface for displaying approved messages to visitors.

The tests focused on verifying that translations are not displayed to visitors before guard approval.

## 2. Test Scope

The following components were evaluated:

- English speech recognition using Whisper Tiny
- Translation into five visitor languages using M2M100
- Guard approval, rejection, and manual correction
- Visitor Display rendering and text wrapping
- Arabic right-to-left (RTL) presentation
- Invalid inputs and simulated system failures
- End-to-end workflow integration

## 3. Multilingual Translation Tests

Five target languages were tested using the English instruction:

"Please check in at the front desk and wait for further instructions."

| Test ID | Language | Result | Status |
|---|---|---|---|
| G-LANG-01 | Chinese | Translation generated; inaccurate rendering of "check in" observed | PASS with quality limitation |
| G-LANG-02 | Spanish | Translation generated; inaccurate check-in wording observed | PASS with quality limitation |
| G-LANG-03 | French | Translation generated; inaccurate check-in wording observed | PASS with quality limitation |
| G-LANG-04 | Russian | Translation generated; inaccurate check-in wording observed | PASS with quality limitation |
| G-LANG-05 | Arabic | Translation generated; check-in wording requires validation | PASS with quality limitation |

**Interpretation:** The five-language generation capability was demonstrated. These results do not establish translation accuracy or suitability for unsupervised visitor communication.

## 4. Error Handling Tests

| Test ID | Test Scenario | Expected Result | Observed Result | Status |
|---|---|---|---|---|
| G-ERROR-01 | Invalid language selection | Cancel translation | Invalid selection rejected | PASS |
| G-ERROR-02 | Silent audio input | Stop when no speech is recognized | No speech detected in tested sample; translation cancelled | PASS |
| G-ERROR-03 | Guard rejects translation and provides no correction | Cancel workflow | Translation cancelled | PASS |
| G-ERROR-04 | Invalid approval input | Reject invalid response | Translation cancelled | PASS |
| G-ERROR-05 | Missing audio file | Report missing file | File-not-found error displayed | PASS |
| G-ERROR-06 | Simulated translation failure | Stop before visitor display | Exception handled; translation cancelled | PASS |

**Limitation:** The silent-audio test used a specific test recording. Whisper may still generate inaccurate text or hallucinate speech under other silent or noisy conditions.

## 5. Visitor Display Regression Tests

| Test ID | Language | Observed Result | Status |
|---|---|---|---|
| G-UI-ZH-01 | Chinese | Chinese characters displayed correctly and centered | PASS |
| G-UI-ES-01 | Spanish | Accented characters and line wrapping displayed correctly | PASS |
| G-UI-FR-01 | French | Accented characters and line wrapping displayed correctly | PASS |
| G-UI-RU-01 | Russian | Cyrillic text displayed correctly across multiple lines | PASS |
| G-UI-AR-01 | Arabic | RTL short- and long-sentence presentation passed after correction | PASS for tested cases |

These tests evaluated the display component directly using approved sample text. They do not independently demonstrate translation accuracy.

## 6. Arabic RTL Defect and Resolution

### Initial defect

The initial Tkinter interface supported Arabic character rendering but did not consistently position punctuation correctly.

After introducing `arabic-reshaper` and `python-bidi`, the short-sentence punctuation test improved. However, long sentences initially wrapped in the wrong vertical reading order.

### Corrective action

The display logic was updated to:

1. Detect the Arabic language code (`ar`).
2. Split the original Arabic text into lines based on measured display width.
3. Apply Arabic reshaping and bidirectional visual ordering separately to each line.
4. Display the resulting lines with right alignment.
5. Preserve the original display configuration for other languages.

### Retest outcome

The tested Arabic short and long sentences displayed with connected characters, appropriate punctuation placement, and correct top-to-bottom line order.

**Remaining limitation:** Additional tests are required for mixed Arabic-English content, numbers, longer paragraphs, and different screen sizes.

## 7. End-to-End Integration Test

**Test ID:** G-E2E-01  
**Test Name:** Guard-to-Visitor End-to-End Workflow  
**Status:** PASS

### Input

English audio:

"Please check in at the front desk and wait for further instructions."

### Expected result

The system should recognize the English instruction, generate a translation, require guard review, and display only the guard-approved message.

### Actual result

1. Whisper processed the English audio.
2. M2M100 generated a Chinese translation.
3. The generated translation contained an incorrect interpretation of "check in."
4. The guard rejected the generated translation.
5. The guard manually entered:

   請在前台登記，並等待進一步指示。

6. The guard approved the corrected message.
7. The Visitor Display opened and showed the corrected Chinese text.

### Evidence

`G-E2E-01_Approved_Corrected_Chinese.png`

### Interpretation

The tested end-to-end workflow successfully enforced the guard approval step before displaying the corrected message.

This supports the feasibility of the human-in-the-loop control for the tested scenario, but does not prove the effectiveness of guard review in every operational situation.

## 8. Key Findings

1. The system generated translations in all five configured target languages.
2. The Visitor Display rendered the tested multilingual messages successfully.
3. Arabic RTL punctuation and multiline display defects were identified and corrected for the tested examples.
4. The system handled six tested error conditions without intentionally displaying unapproved messages.
5. The guard approval and correction process successfully prevented one known inaccurate translation from being shown to the visitor.
6. Translation quality remains a significant operational limitation.

## 9. Remaining Risks and Limitations

- M2M100 may mistranslate context-dependent guard-station instructions.
- Whisper may misrecognize speech in noisy environments or produce text from some silent recordings.
- Arabic RTL behavior has not been exhaustively tested across mixed scripts and display sizes.
- Translation accuracy has not been independently validated by qualified speakers of all target languages.
- The current tests do not establish production readiness, accessibility compliance, or performance under realistic guard-station operating conditions.

## 10. Recommended Next Steps

1. Expand the translation test set using common guard-station instructions.
2. Obtain human evaluation of translation quality across all five languages.
3. Test speech recognition with noise, different accents, and varying recording quality.
4. Test Arabic mixed-script content, numbers, and longer paragraphs.
5. Verify that the approval requirement remains effective across all supported languages.
6. Document privacy, retention, reliability, and accessibility requirements before any real-world deployment.

## 11. Evidence Inventory

| Evidence Item | Description | Availability |
|---|---|---|
| G-E2E-01_Approved_Corrected_Chinese.png | Corrected Chinese displayed after guard approval | Saved by tester |
| Chinese UI regression screenshot | Chinese display verification | Screenshot observed; local filename unconfirmed |
| Spanish UI regression screenshot | Spanish display verification | Screenshot observed; local filename unconfirmed |
| French UI regression screenshot | French display verification | Screenshot observed; local filename unconfirmed |
| Russian UI regression screenshot | Russian display verification | Screenshot observed; local filename unconfirmed |
| Arabic RTL screenshots | Initial defect, short-sentence correction, and multiline correction | Screenshots observed; local filenames unconfirmed |
| Error handling screenshots | Six error-condition tests | Previously tested; local filenames unconfirmed |

## 12. Overall Assessment

Week 6 testing demonstrated functional progress in multilingual message generation, guard approval controls, visitor-facing display, Arabic RTL presentation, and error handling.

The Guard-to-Visitor workflow passed the documented end-to-end test using a manually corrected Chinese translation.

The prototype remains suitable for continued controlled testing and development. Additional translation-quality, speech-recognition, accessibility, privacy, and operational validation is required before real-world deployment.
