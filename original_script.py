import ollama
import whisper
import pyttsx3
import sounddevice as sd
import numpy as np
import tempfile
import wave

# Initialisation de Whisper (STT) et du moteur vocal (TTS)
whisper_model = whisper.load_model("base")
engine = pyttsx3.init()

def record_audio(filename, duration=5, samplerate=44100):
    """Enregistre l'audio du micro et le sauvegarde temporairement"""
    print("🎤 Parlez maintenant...")
    audio = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=1, dtype=np.int16)
    sd.wait()

    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(samplerate)
        wf.writeframes(audio.tobytes())

def speech_to_text(filename):
    """Convertit l'audio en texte avec Whisper"""
    result = whisper_model.transcribe(filename)
    return result["text"]

def text_to_speech(text):
    """Convertit le texte en voix avec pyttsx3"""
    engine.say(text)
    engine.runAndWait()

def chat_with_ollama(user_input):
    """Génère une réponse avec NeuralChat d'Ollama"""
    response = ollama.chat(model="neural-chat", messages=[{"role": "user", "content": user_input}])
    return response["message"]["content"]

# Boucle principale
while True:
    temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix=".wav").name
    record_audio(temp_audio)
    user_input = speech_to_text(temp_audio)

    if "stop" in user_input.lower():
        print("🛑 Assistant vocal arrêté.")
        break

    print("🗣 Vous avez dit :", user_input)
    
    response = chat_with_ollama(user_input)
    print("🤖 Réponse AI :", response)

    text_to_speech(response)
