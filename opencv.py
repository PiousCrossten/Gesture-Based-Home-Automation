import cv2
import mediapipe as mp
import serial
import time

# Set up serial communication with Arduino
arduino = serial.Serial('COM6', 9600, timeout=1)
time.sleep(2)  # Wait for the connection to establish

# Initialize MediaPipe Hand detection
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

# Initialize the camera (use 0 for the default camera)
cap = cv2.VideoCapture(0)

def count_fingers(hand_landmarks):
    """
    Count the number of fingers raised based on landmarks.
    """
    finger_tips = [8, 12, 16, 20]  # Index, Middle, Ring, Pinky finger tips
    count = 0

    # Thumb detection (special case)
    if hand_landmarks.landmark[4].x < hand_landmarks.landmark[3].x:
        count += 1  # Thumb is considered raised
    
    # Count raised fingers for index, middle, ring, and pinky
    for tip in finger_tips:
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y:
            count += 1
    
    return count

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Flip the frame for a more intuitive camera display
    frame = cv2.flip(frame, 1)

    # Convert the BGR image to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Draw hand landmarks on the frame
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            # Count the number of raised fingers
            finger_count = count_fingers(hand_landmarks)
            
            # Send corresponding command to Arduino based on finger count
            if finger_count == 1:
                arduino.write(b'1')  # Turn on Relay 1
            elif finger_count == 2:
                arduino.write(b'2')  # Turn on Relay 2
            elif finger_count == 3:
                arduino.write(b'4')  # Turn on Relay 3
            elif finger_count == 4:
                arduino.write(b'6')  # Turn on Relay 4
            else:
                # If no fingers are raised, turn off all relays
                arduino.write(b'0')  # Turn off Relay 1
                arduino.write(b'3')  # Turn off Relay 2
                arduino.write(b'5')  # Turn off Relay 3
                arduino.write(b'7')  # Turn off Relay 4

    # Display the frame
    cv2.imshow("Finger Detection", frame)

    # Exit if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
arduino.close()

