# Skillova Category 6 - AI Chatbots and Prompt Engineering

## Objective

Use a generative AI API to produce short, professional workplace emails and updates that never exceed three sentences.

## Files

- `prompt_email_assistant.py` - Groq API script, system prompt, tests and validation
- `FINAL_REPORT.pdf` - concise explanation of the approach
- `RESEARCH_log.docx` - completed timestamped research log
- `TEST_RESULTS.md` and `test_results.json` - created automatically after running the script

## Run the project

1. Create a Groq API key in Groq Console.
2. Install the Python package:

```bash
pip install groq
```

3. Run:

```bash
python prompt_email_assistant.py
```

The script asks for the API key privately if `GROQ_API_KEY` is not already set. The key is not saved in the code or output files.

## What the script proves

The script tests four different workplace requests. For each response it checks:

- one to three sentences
- no more than 70 words
- no bullet or numbered-list formatting

If a response fails, the script sends one correction request and checks it again. It then saves the real API responses and pass/fail evidence in `TEST_RESULTS.md` and `test_results.json`.

## Submission step

Run the script once, confirm all four tests show `PASS`, and include the two generated result files in the repository before submission.

## References

- Groq text generation: https://console.groq.com/docs/text-chat
- Groq supported models: https://console.groq.com/docs/models
- Groq API-key security: https://console.groq.com/docs/production-readiness/security-onboarding
