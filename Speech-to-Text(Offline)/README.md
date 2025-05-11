# Whisper Transcription with Live Audio Recording

This project uses OpenAI's Whisper model to transcribe audio recorded via microphone in real-time using PyAudio. It supports multiple languages, including Hindi.

---

## 🛠️ Features

- Record audio using microphone input
- Save as a `.wav` file
- Transcribe audio using `openai/whisper-large-v3` from Hugging Face
- Supports multilingual transcription (default: Hindi)

---

## 📦 Requirements

- Python 3.7+
- PyTorch
- Hugging Face Transformers
- SoundFile
- PyAudio

Install all dependencies using:

```bash
pip install -r requirements.txt
