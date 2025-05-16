import cv2
import mediapipe as mp
import socket

# Initialize MediaPipe Hands.
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_drawing = mp.solutions.drawing_utils

# Set up socket connection
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('192.168.129.231', 12345)  # Replace with your ESP8266 IP and port

def detect_hand_gesture(image):
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Extract coordinates for index and pinky fingertips
            index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            pinky_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]

            # Calculate the distance between fingertips to determine if the fist is closed
            distance = ((index_finger_tip.x - pinky_tip.x) ** 2 + (index_finger_tip.y - pinky_tip.y) ** 2) ** 0.5

            if distance < 0.1:
                return "CLOSED"
            else:
                return "OPEN"
    return "NONE"

cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    gesture = detect_hand_gesture(frame)
    if gesture == "CLOSED":
        sock.sendto(b'CLOSED', server_address)
        cv2.putText(frame, 'Fist: CLOSED', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
    elif gesture == "OPEN":
        sock.sendto(b'OPEN', server_address)
        cv2.putText(frame, 'Fist: OPEN', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

    cv2.imshow('Hand Gesture', frame)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

