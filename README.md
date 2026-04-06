# Girl Friday

![Girl Friday in action](./Screenshot%202026-04-06%20at%2009.56.07.png)

A voice-powered AI assistant using Whisper for speech recognition and Ollama for chat, with pyttsx3 for spoken responses. All processing happens locally — no cloud dependencies.

> **What's in a name?** "Girl Friday" is a nod to the classic "girl Friday" — a trusted personal assistant. This is your AI assistant that listens, thinks, and talks back.

## Features

- **Voice interaction** — speak to the assistant, hear its responses
- **Text fallback** — type directly if microphone isn't available
- **Configurable** — switch models, adjust recording duration via CLI or env vars
- **Self-contained** — all models run locally via Ollama
- **Privacy-first** — no data leaves your machine

## Requirements

- Python 3.11+
- [Ollama](https://ollama.ai/) running locally (for the chat model)
- [Homebrew](https://brew.sh/) (for ffmpeg on macOS)
- Microphone (for voice mode)
- ffmpeg (for audio processing)

## Setup

### 1. Install system dependencies

```bash
brew install ffmpeg
```

### 2. Set up Python environment with pyenv

```bash
cd ~/projects/girl-friday

# The project uses pyenv-virtualenv — the .python-version file auto-activates it
# When you cd into the project, run:
eval "$(pyenv init -)"

# Or create the environment manually if needed:
pyenv virtualenv 3.11.10 girl-friday
pyenv local girl-friday
```

### 3. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up Ollama

Make sure Ollama is running with a model available:

```bash
# Start Ollama (if not already running)
ollama serve

# Pull a model (first time only)
ollama pull neural-chat

# Or try another model:
ollama pull llama3.2
ollama pull mistral
```

## Usage

### Voice mode (default)

```bash
cd ~/projects/girl-friday
eval "$(pyenv init -)"
python -m girl_friday.cli
```

Say "stop" to exit. The assistant will listen, respond via voice, and loop.

### Text mode

```bash
python -m girl_friday.cli --text "Hello, how are you?"
```

Useful for testing without a microphone or for quick queries.

### Check dependencies

```bash
python -m girl_friday.cli --check
```

Verifies Python version, all packages installed, and Ollama service is reachable.

### List available Ollama models

```bash
python -m girl_friday.cli --models
```

## Configuration

### Environment variables

| Variable | Default | Description |
|----------|---------|-------------|
| `GIRL_FRIDAY_WHISPER_MODEL` | `base` | Whisper model size |
| `GIRL_FRIDAY_OLLAMA_MODEL` | `neural-chat` | Ollama model name |
| `GIRL_FRIDAY_RECORD_DURATION` | `5` | Recording length in seconds |
| `GIRL_FRIDAY_SAMPLE_RATE` | `16000` | Audio sample rate in Hz |

### CLI arguments

CLI arguments override environment variables:

```bash
girl-friday --whisper-model tiny --ollama-model llama2 --duration 10
```

### Whisper model sizes

| Model | Size | Speed | Accuracy |
|-------|------|-------|----------|
| `tiny` | ~39 MB | Fastest | Baseline |
| `base` | ~139 MB | Fast | Good |
| `small` | ~488 MB | Medium | Better |
| `medium` | ~1.5 GB | Slow | High |
| `large` | ~2.9 GB | Slowest | Highest |

The `base` model offers a good balance of speed and accuracy for most use cases.

### Ollama model recommendations

For voice assistants, models that excel at quick, concise responses work best:

- **neural-chat** — optimized for conversation (default)
- **llama3.2** — general purpose, good at following instructions
- **mistral** — fast, excellent at reasoning
- **phi3** — lightweight, surprisingly capable

Pull a model first if you haven't:
```bash
ollama pull neural-chat
```

## Troubleshooting

### "ffmpeg not found"

Install ffmpeg:
```bash
brew install ffmpeg
```

### Microphone not working / permission denied

**macOS:** Grant microphone access in System Settings → Privacy & Security → Microphone.

### Ollama service not responding

Make sure Ollama is running:
```bash
ollama serve
```

If using a different model, ensure it's downloaded:
```bash
ollama pull <model-name>
```

### Whisper model fails to load

The base model (~139 MB) downloads on first use. If it fails, manually download:
```bash
python -c "import whisper; whisper.load_model('base')"
```

### Audio recording quality issues

- Reduce `GIRL_FRIDAY_RECORD_DURATION` for shorter clips (default: 5 seconds)
- Increase sample rate if quality is poor
- Ensure you're in a relatively quiet environment

## Use cases

- **Hands-free queries** — ask questions while doing other things
- **Voice-controlled automation** — extend to control smart home devices
- **Language practice** — have conversational practice with AI
- **Accessibility** — voice control for those who prefer speaking over typing
- **Prototyping** — rapid voice interface development

## Architecture

```
girl_friday/
├── __init__.py       # Package marker
├── cli.py            # Entry point, argument parsing
├── audio.py          # Recording, STT (Whisper), TTS (pyttsx3)
├── ollama_client.py  # Ollama chat interface
└── config.py         # Configuration from env/CLI
```

**Data flow:**
1. Microphone records audio
2. Whisper transcribes speech → text
3. Ollama generates a response
4. pyttsx3 speaks the response aloud

## Limitations

- **Latency** — There's a delay between speaking and hearing the response (recording + transcription + LLM + TTS). Faster models reduce this.
- **Microphone quality** — Better mic = better transcription accuracy
- **Background noise** — Whisper may pick up ambient sounds incorrectly
- **Speaker-dependent** — Whisper works best with consistent voice patterns
- **Single-turn per exchange** — Currently records → responds → records again (not continuous listening)

## Project origin

Refactored from a single-script French voice assistant (`mon_assistant_vocal.py`).
Original code by Kigen.

## License

MIT
