"""
Girl Friday — Voice Assistant

A voice-powered AI assistant using Whisper for speech-to-text,
Ollama for chat, and pyttsx3 for text-to-speech.

Usage:
    girl-friday                    # Start interactive voice assistant
    girl-friday --text "Hello"      # Text input mode
    girl-friday --models           # List available models
    girl-friday --check            # Verify all dependencies
"""
import argparse
import os
import sys
import tempfile

from girl_friday.audio import record_audio, speech_to_text, text_to_speech, get_whisper_model
from girl_friday.ollama_client import chat_with_ollama
from girl_friday.config import Config


def check_dependencies():
    """Verify all required dependencies are installed and accessible."""
    checks = []
    errors = []

    # Python version
    py_version = f"{sys.version_info.major}.{sys.version_info.minor}"
    if sys.version_info < (3, 11):
        errors.append(f"Python 3.11+ required, found {py_version}")
    else:
        checks.append(f"Python {py_version} ✓")

    # Check Ollama
    try:
        import ollama
        model = Config.OLLAMA_MODEL
        checks.append(f"ollama installed ✓")
    except ImportError:
        errors.append("ollama not installed")

    # Check Whisper
    try:
        import whisper
        model = Config.WHISPER_MODEL
        checks.append(f"whisper installed ✓")
    except ImportError:
        errors.append("whisper not installed")

    # Check TTS
    try:
        import pyttsx3
        checks.append("pyttsx3 installed ✓")
    except ImportError:
        errors.append("pyttsx3 not installed")

    # Check sounddevice
    try:
        import sounddevice
        checks.append("sounddevice installed ✓")
    except ImportError:
        errors.append("sounddevice not installed")

    # Check Ollama service
    try:
        import ollama as o
        o.chat(model=Config.OLLAMA_MODEL, messages=[{"role": "user", "content": "hi"}], options={"num_predict": 5})
        checks.append("Ollama service responding ✓")
    except Exception as e:
        errors.append(f"Ollama service not reachable: {e}")

    print("=== Girl Friday Dependency Check ===\n")
    for c in checks:
        print(c)
    if errors:
        print()
        for e in errors:
            print(f"ERROR: {e}")
        print("\nRun: poetry install")
        return False
    return True


def interactive_mode(config: Config):
    """Run the voice assistant in interactive mode."""
    print("🎙  Girl Friday voice assistant started")
    print("   Say 'stop' to exit\n")

    # Warm up Whisper model
    print("Loading Whisper model...")
    get_whisper_model(config.WHISPER_MODEL)

    print("Ready. Speak into your microphone.\n")

    while True:
        temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix=".wav").name

        try:
            # Record
            record_audio(temp_audio, duration=config.RECORD_DURATION,
                        samplerate=config.SAMPLE_RATE)
            user_input = speech_to_text(temp_audio)

            if not user_input.strip():
                print("... (nothing detected, try again)")
                continue

            if "stop" in user_input.lower():
                print("👋 Goodbye!")
                break

            print(f"🗣 You: {user_input}")

            # Get AI response
            response = chat_with_ollama(user_input)
            print(f"🤖 Friday: {response}")

            # Speak response
            text_to_speech(response)

        except KeyboardInterrupt:
            print("\n👋 Interrupted.")
            break
        finally:
            if os.path.exists(temp_audio):
                os.unlink(temp_audio)


def text_mode(text: str, config: Config):
    """Process a single text input and print response."""
    print(f"🗣 You: {text}")
    response = chat_with_ollama(text)
    print(f"🤖 Friday: {response}")


def main():
    parser = argparse.ArgumentParser(
        description="Girl Friday — Voice Assistant",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument("--text", "-t", metavar="INPUT",
                       help="Run in text mode instead of voice")
    parser.add_argument("--check", action="store_true",
                       help="Check dependencies and exit")
    parser.add_argument("--models", action="store_true",
                       help="List available Ollama models")
    parser.add_argument("--duration", type=int, default=5,
                       help="Recording duration in seconds (default: 5)")
    parser.add_argument("--whisper-model", default=None,
                       help="Whisper model to use (default: base)")
    parser.add_argument("--ollama-model", default=None,
                       help="Ollama model to use (default: neural-chat)")

    args = parser.parse_args()

    # Override config from CLI args
    config = Config()
    if args.duration:
        config.RECORD_DURATION = args.duration
    if args.whisper_model:
        config.WHISPER_MODEL = args.whisper_model
    if args.ollama_model:
        config.OLLAMA_MODEL = args.ollama_model

    if args.check:
        sys.exit(0 if check_dependencies() else 1)

    if args.models:
        try:
            import ollama
            models = ollama.list()
            print("Available Ollama models:")
            for m in models.get("models", []):
                print(f"  - {m['name']}")
        except Exception as e:
            print(f"Error listing models: {e}")
        sys.exit(0)

    if args.text:
        text_mode(args.text, config)
    else:
        interactive_mode(config)


if __name__ == "__main__":
    main()
