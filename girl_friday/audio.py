"""Audio handling: recording, STT, and TTS."""
import wave
import numpy as np
import sounddevice as sd
import whisper
import pyttsx3

# Lazy-loaded Whisper model (loaded once at first use)
_whisper_model = None
_engine = None


def get_whisper_model(model_name: str = "base"):
    """Get or create the Whisper model (singleton)."""
    global _whisper_model
    if _whisper_model is None:
        _whisper_model = whisper.load_model(model_name)
    return _whisper_model


def get_tts_engine():
    """Get or create the TTS engine (singleton)."""
    global _engine
    if _engine is None:
        _engine = pyttsx3.init()
    return _engine


def record_audio(filename: str, duration: int = 5, samplerate: int = 16000):
    """
    Record audio from the microphone and save to a WAV file.

    Args:
        filename: Path to save the recorded audio
        duration: Recording duration in seconds
        samplerate: Audio sample rate in Hz
    """
    print("🎤 Recording... (speak now)")
    audio = sd.rec(int(samplerate * duration), samplerate=samplerate,
                   channels=1, dtype=np.int16)
    sd.wait()
    print("✓ Recording complete")

    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)  # 16-bit
        wf.setframerate(samplerate)
        wf.writeframes(audio.tobytes())


def speech_to_text(filename: str, model_name: str = "base") -> str:
    """
    Transcribe audio file to text using Whisper.

    Args:
        filename: Path to the audio file
        model_name: Whisper model to use

    Returns:
        The transcribed text
    """
    model = get_whisper_model(model_name)
    result = model.transcribe(filename, fp16=False)
    return result["text"]


def text_to_speech(text: str):
    """
    Convert text to speech and play it.

    Args:
        text: The text to speak
    """
    engine = get_tts_engine()
    engine.say(text)
    engine.runAndWait()
