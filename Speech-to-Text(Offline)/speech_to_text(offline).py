
import pyaudio
import wave
import soundfile as sf
from transformers import WhisperProcessor, WhisperForConditionalGeneration
import threading

# Initialize the Whisper model and processor
processor = WhisperProcessor.from_pretrained("openai/whisper-large-v3")
model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-large-v3")
model.config.forced_decoder_ids = None

# Audio recording parameters
RATE = 16000
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1

# Initialize PyAudio
p = pyaudio.PyAudio()

class Recorder:
    def __init__(self):
        self.frames = []
        self.stream = None
        self.recording = False

    def start_recording(self):
        self.stream = p.open(format=FORMAT,
                             channels=CHANNELS,
                             rate=RATE,
                             input=True,
                             frames_per_buffer=CHUNK)
        self.recording = True
        print("Recording... Press Enter to stop.")

        while self.recording:
            data = self.stream.read(CHUNK)
            self.frames.append(data)

    def stop_recording(self):
        self.recording = False
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()

    def save_recording(self, filename="output.wav"):
        wf = wave.open(filename, "wb")
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(self.frames))
        wf.close()

def record_audio():
    recorder = Recorder()
    recording_thread = threading.Thread(target=recorder.start_recording)
    recording_thread.start()
    
    input()  # Wait for the user to press Enter to stop recording
    recorder.stop_recording()
    
    recording_thread.join()  # Ensure the recording thread has finished
    recorder.save_recording()

def transcribe_audio():
    # Load the saved audio file
    audio_input, sample_rate = sf.read("output.wav")

    # Process the audio input with the specified language (change 'en' to another language code if needed)
    input_features = processor(audio_input, sampling_rate=sample_rate, return_tensors="pt", language='hi').input_features

    # Generate token IDs
    predicted_ids = model.generate(input_features)

    # Decode token IDs to text
    transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)
    print("Transcription:", transcription[0])



if __name__ == "__main__":
    input("Press Enter to start recording...")
    record_audio()
    
    transcribe_audio()

    p.terminate()
