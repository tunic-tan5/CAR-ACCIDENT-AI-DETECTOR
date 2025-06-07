import threading
import time
import speech_recognition as sr
import pyttsx3
from camera_module import monitor_driver_drowsiness
from voice_module import monitor_driver_distress
# from twilio.rest import Client  # Uncomment if using Twilio

import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import queue

# Twilio config (use your creds if you want real SMS)
TWILIO_SID = "your_sid"
TWILIO_AUTH_TOKEN = "your_token"
TWILIO_PHONE_NUMBER = "+1XXXXXXXXXX"
EMERGENCY_CONTACTS = ['+91xxxxxxxxxx']

# Initialize TTS and recognizer globally
engine = pyttsx3.init()
recognizer = sr.Recognizer()
microphone = sr.Microphone()
speech_lock = threading.Lock()

# --- GUI App ---
class CarAccidentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Car Accident Detection System")
        self.log_queue = queue.Queue()

        self.log_text = ScrolledText(root, state='disabled', height=20, width=70)
        self.log_text.pack(padx=10, pady=10)

        self.root.after(100, self.process_log_queue)

    def log(self, message):
        self.log_queue.put(message)

    def process_log_queue(self):
        try:
            while True:
                msg = self.log_queue.get_nowait()
                self.log_text.config(state='normal')
                self.log_text.insert(tk.END, msg + "\n")
                self.log_text.see(tk.END)
                self.log_text.config(state='disabled')
        except queue.Empty:
            pass
        self.root.after(100, self.process_log_queue)

# --- Speak ---
def speak(message):
    with speech_lock:
        engine.say(message)
        engine.runAndWait()

# --- Listen ---
def listen(timeout=5, phrase_time_limit=5):
    with speech_lock:
        with microphone as source:
            recognizer.adjust_for_ambient_noise(source)
            try:
                audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
                response = recognizer.recognize_google(audio).lower()
                return response
            except sr.WaitTimeoutError:
                return None
            except sr.UnknownValueError:
                return ""
            except sr.RequestError:
                return ""

# --- Send Emergency Message ---
def send_emergency_message(reason, logger):
    logger(f"🚨 [SIMULATION] Emergency message: {reason}")
    # Uncomment below to enable Twilio
    """
    from twilio.rest import Client
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
    for contact in EMERGENCY_CONTACTS:
        try:
            message = client.messages.create(
                body=f"Emergency! {reason}. Please check on the driver.",
                from_=TWILIO_PHONE_NUMBER,
                to=contact
            )
            logger(f"✅ Message sent to {contact}")
        except Exception as e:
            logger(f"❌ Failed to send message to {contact}: {str(e)}")
    """

# --- Handle Drowsiness ---
def handle_drowsiness_event(logger):
    logger("😴 Handling drowsiness event...")
    speak("Your eyes are closed for a long time. Are you okay?")
    response = listen()
    if response is None:
        logger("⏱️ No response (timeout). Sending emergency message.")
        send_emergency_message("Driver unresponsive due to drowsiness", logger)
    elif "yes" in response or "okay" in response:
        logger("👍 Driver said they are okay.")
    else:
        logger("⚠️ Driver not okay or no clear response. Sending emergency message.")
        send_emergency_message("Driver appears drowsy or unwell", logger)

# --- Handle Distress ---
def handle_distress_event(unresponsive=False, logger=None):
    if unresponsive:
        logger("⏱️ Driver unresponsive during distress detection. Sending emergency message.")
        send_emergency_message("Driver unresponsive during distress detection", logger)
        return

    logger("🚨 Handling distress event...")
    speak("I heard you may need help. Are you okay?")
    response = listen()
    if response is None:
        logger("⏱️ No response after distress keyword. Sending emergency message.")
        send_emergency_message("Driver not responding after distress keyword", logger)
    elif "yes" in response or "okay" in response:
        logger("👍 Driver said they are okay.")
    else:
        logger("⚠️ Driver confirmed distress. Sending emergency message.")
        send_emergency_message("Driver confirmed distress", logger)

# --- Threads ---
def drowsiness_monitor_thread(logger):
    def on_drowsiness_detected():
        handle_drowsiness_event(logger)
    monitor_driver_drowsiness(on_drowsiness_detected=on_drowsiness_detected)

def distress_monitor_thread(logger):
    def on_distress_detected(unresponsive=False):
        handle_distress_event(unresponsive, logger)
    monitor_driver_distress(on_distress_detected=on_distress_detected)

# --- Main ---
def main():
    root = tk.Tk()
    app = CarAccidentApp(root)

    threading.Thread(target=drowsiness_monitor_thread, args=(app.log,), daemon=True).start()
    threading.Thread(target=distress_monitor_thread, args=(app.log,), daemon=True).start()

    root.mainloop()

if __name__ == "__main__":
    main()
