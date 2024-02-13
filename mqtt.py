import cv2
import time
import paho.mqtt.publish as publish

# MQTT configuration
mqtt_broker = "broker.hivemq.com"  # Update with your MQTT broker address
mqtt_topic = "/image"    # Update with the MQTT topic your NodeMCU is subscribed to

# OpenCV setup
cap = cv2.VideoCapture(0)
fullbody_cascade = cv2.CascadeClassifier('haarcascade_fullbody.xml')
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

last_detection_time = time.time()
timer_interval = 10  # seconds
count = 0

while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    fullbodies = fullbody_cascade.detectMultiScale(gray, scaleFactor=1.9, minNeighbors=1)
    for (x, y, w, h) in fullbodies:
        last_detection_time = time.time()
        if count == 0:
            print("Detected")
            publish.single(mqtt_topic, payload="1", hostname=mqtt_broker)
            count = 1

    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
    for (x, y, w, h) in faces:
        last_detection_time = time.time()
        if count == 0:
            print("Detected")
            publish.single(mqtt_topic, payload="1", hostname=mqtt_broker)
            count = 1

    elapsed_time = time.time() - last_detection_time
    if elapsed_time >= timer_interval and count == 1:
        print("Not Detected")
        publish.single(mqtt_topic, payload="0", hostname=mqtt_broker)
        count = 0

    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
