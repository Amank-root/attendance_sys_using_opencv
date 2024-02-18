import cv2
import face_recognition as fr
import numpy as np
import pickle
import cvzone as cvzone
import csv
import datetime
import threading

# Initialize variables
time = datetime.datetime.now().date().strftime("%Y-%m-%d")
attend = open("attendance.csv", "a")
writer = csv.writer(attend)
writer.writerow(["name", time])
with open("known_name_encodings.npy", "rb") as file:
    known_name_encodings_with_names = pickle.load(file)
    known_names = known_name_encodings_with_names[0]
    known_name_encodings = known_name_encodings_with_names[1]

# Video capture setup with resolution
cap = cv2.VideoCapture(1)
cap.set(3, 1200)
cap.set(4, 720)

# Define frame processing function
def process_frame(frame, pervious_time=None):
    current_time = cv2.getTickCount()  # Get current timestamp
    delta_time = (current_time - pervious_time) / cv2.getTickFrequency() if pervious_time else 0
    # Frame pre-processing for efficiency
    _img = cv2.resize(frame, (0, 0), None, 0.25, 0.25)
    rgb_frame = cv2.cvtColor(_img, cv2.COLOR_BGR2RGB)

    # Face detection and encoding
    face_locations = fr.face_locations(rgb_frame)
    face_encodings = fr.face_encodings(rgb_frame, face_locations)

    # Loop through detected faces
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # Match against known encodings
        matches = fr.compare_faces(known_name_encodings, face_encoding)
        name = "Unknown"
        face_distances = fr.face_distance(known_name_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)

        if matches[best_match_index]:
            # Find closest match
            name = known_names[best_match_index][1]
            print(name)
            # Mark attendance
            writer.writerows([[name, "Present"]])

        # Draw bounding box and name
        top, right, bottom, left = top * 4, right * 4, bottom * 4, left * 4
        # cvzone.cornerRect(frame, bbox=[left, top, right - left, bottom - top], rt=0)
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (0, 0, 255), 1)
    return current_time

# Define recognition thread
def recognize():
    global cap
    previous_time = None 
    while True:
        # Capture frame in separate thread
        ret, frame = cap.read()
        previous_time = process_frame(frame, previous_time)

        # Process frame in separate thread
        # threading.Thread(target=process_frame, args=(frame,previous_time)).start()

        # Display and handle exit key
        cv2.imshow('Video', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release resources
    cap.release()
    cv2.destroyAllWindows()

# Main thread - start recognition
if __name__ == "__main__":
    # Use threading for smoother video display
    recognition_thread = threading.Thread(target=recognize)
    recognition_thread.start()

    # Wait for recognition thread to finish
    recognition_thread.join()
    attend.close()