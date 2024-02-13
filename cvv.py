import cv2
import time

cap = cv2.VideoCapture(0)  # Use the default camera (0) on your laptop

# Load the full body and face Haar Cascade classifiers
fullbody_cascade = cv2.CascadeClassifier('haarcascade_fullbody.xml')
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Initialize variables for timer and count
last_detection_time = time.time()
timer_interval = 10  # seconds
count = 0

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect full bodies
    fullbodies = fullbody_cascade.detectMultiScale(gray, scaleFactor=1.9, minNeighbors=1)
    for (x, y, w, h) in fullbodies:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        last_detection_time = time.time()  # Update last detection time
        if count == 0:
            print("Detected")
            count = 1

    # Detect faces
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        last_detection_time = time.time()  # Update last detection time
        if count == 0:
            print("Detected")
            count = 1

    # Check if 10 seconds have passed since the last detection
    elapsed_time = time.time() - last_detection_time
    if elapsed_time >= timer_interval and count == 1:
        print("Not Detected")
        count = 0

    # Display the resulting frame
    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
cap.release()
cv2.destroyAllWindows()