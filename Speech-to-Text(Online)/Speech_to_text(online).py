import speech_recognition as sr

def take_user_input():
    """Takes user input, recognizes it using Speech Recognition module and returns the transcribed text"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening...')
        r.pause_threshold = 1
        r.energy_threshold = 4000
        r.dynamic_energy_threshold = True
        audio = r.listen(source, timeout=5, phrase_time_limit=7)

    try:
        print('Recognizing...')
        query = r.recognize_google(audio, language='en-in')
        print(f"Transcription: {query}")
    except Exception as e:
        print("Error:", e)
        print("Sorry, I did not understand that.")
        query = 'None'
    return query

if __name__ == '__main__':
    while True:
        transcription = take_user_input()
        if transcription.lower() in ['exit', 'stop']:
            print("Exiting transcription...")
            break
