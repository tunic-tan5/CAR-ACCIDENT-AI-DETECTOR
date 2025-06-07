# Car Accident AI Detector

This project monitors driver's drowsiness , distress and accidents using camera and voice input. It alerts the driver and sends emergency messages to emergency contacts in driver's automatically.

## Features
- Drowsiness detection using OpenCV
- Voice distress detection with speech recognition
- Text-to-speech alerts
- Emergency message sending via Twilio (optional)
- Simple GUI interface

## Twilio Setup and Testing

This project uses **Twilio** TO SEND EMERGENCY SMS MESSAGES when the driver is unresponsive or in distress.

### How to get started with Twilio:

1. Sign up for a free Twilio account at [https://www.twilio.com/try-twilio](https://www.twilio.com/try-twilio).
2. After signup, get a **Twilio phone number** from the Twilio Console. This is the number messages will be sent from.
3. Copy your **Account SID** and **Auth Token** from the Twilio Console dashboard.
4. Update the following variables in the project’s main script with your Twilio details:

```python
TWILIO_SID = "your_account_sid"
TWILIO_AUTH_TOKEN = "your_auth_token"
TWILIO_PHONE_NUMBER = "+1XXXXXXXXXX"  # Your Twilio phone number
EMERGENCY_CONTACTS = ['+91xxxxxxxxxx']  # Numbers to receive SMS alerts

## How to Run
1. Install Python 3.7 or above.
2. Install dependencies: `pip install -r requirements.txt`
3. Run the main script: `python app.py`

## Author
Gara Tanmai
