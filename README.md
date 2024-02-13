

# CV Eonshift

## Energy consumption using CV


## Installation

1. **Install Dependencies:**

    - To establish MQTT server connection:
       
        pip install paho-mqtt
    
    - For OpenCV (for computer vision project):
      
        pip install opencv-python
      
2. **Upload `connection.ino` to NodeMCU:**

    - Upload the `connection.ino` file to your NodeMCU board using the Arduino IDE or any other suitable method.

## Usage

1. **Running the MQTT Client:**

    - Run the MQTT client script (`mqtt.py`) to establish a connection with the MQTT server.

2. **Interacting with NodeMCU:**

    - After the MQTT client is running, it will send messages to the NodeMCU based on the detected input (1 or 0). Ensure the NodeMCU is connected to the MQTT server and properly configured to receive messages.

## File Descriptions

- **mqtt.py:** Python script to establish connection with MQTT server and send messages to NodeMCU.
- **connection.ino:** Arduino sketch to run on NodeMCU, receives messages from MQTT server and controls LED based on the received messages.

