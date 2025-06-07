import cv2
import time

def monitor_driver_drowsiness(on_drowsiness_detected):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye.xml")

    cap = cv2.VideoCapture(0)
    eyes_closed_time = 0
    EYES_CLOSED_THRESHOLD = 5  # seconds

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        eyes_detected = False

        for (x, y, w, h) in faces:
            roi_gray = gray[y:y+h, x:x+w]
            eyes = eye_cascade.detectMultiScale(roi_gray)
            if len(eyes) > 0:
                eyes_detected = True

        if not eyes_detected:
            if eyes_closed_time == 0:
                eyes_closed_time = time.time()
            elif time.time() - eyes_closed_time > EYES_CLOSED_THRESHOLD:
                on_drowsiness_detected()
                eyes_closed_time = 0
        else:
            eyes_closed_time = 0

        cv2.imshow("Driver Monitoring", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
