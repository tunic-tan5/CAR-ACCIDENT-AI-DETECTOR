import speech_recognition as sr

def monitor_driver_distress(on_distress_detected):
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    while True:
        with microphone as source:
            print("🎧 Listening for distress keywords...")
            recognizer.adjust_for_ambient_noise(source)
            try:
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                query = recognizer.recognize_google(audio).lower()
                print(f"Driver said: {query}")
            except sr.WaitTimeoutError:
                print("No speech detected (timeout). Assuming unresponsive.")
                on_distress_detected(unresponsive=True)
                continue
            except sr.UnknownValueError:
                print("Could not understand audio.")
                continue
            except sr.RequestError:
                print("Speech recognition service failed.")
                continue

            distress_keywords = ['help', 'emergency', 'distress', 'help me', 'save me']
            if any(keyword in query for keyword in distress_keywords):
                on_distress_detected(unresponsive=False)
