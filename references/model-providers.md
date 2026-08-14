# Model provider configuration

External model use is optional. Prefer the active agent unless the user explicitly asks for another model or a repeatable provider call is part of the workflow.

## OpenAI-compatible endpoint

```bash
export TEST_WRITER_BASE_URL="https://provider.example/v1"
export TEST_WRITER_API_KEY="..."
export TEST_WRITER_MODEL="model-name"
python scripts/invoke_model.py --provider openai-compatible --prompt-file request.txt
```

`TEST_WRITER_BASE_URL` may point to a hosted API or a local server implementing `/chat/completions`. The key is optional for local servers that do not authenticate.

## Ollama

```bash
export TEST_WRITER_OLLAMA_URL="http://127.0.0.1:11434"
export TEST_WRITER_MODEL="qwen2.5-coder"
python scripts/invoke_model.py --provider ollama --prompt-file request.txt
```

## Prompt-only mode

Use this for another agent, an unsupported CLI, or manual transfer:

```bash
python scripts/invoke_model.py --provider prompt --prompt-file request.txt
```

Never pass secrets as command-line arguments because process listings and shell history may expose them.
