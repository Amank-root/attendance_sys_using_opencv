import cv2
import face_recognition as fr
import numpy as np
import pickle
import cvzone as cvzone
import csv
import datetime

time = datetime.datetime.now().date().strftime("%Y-%m-%d")
attend = open("attendance.csv", "a")
writer = csv.writer(attend)
writer.writerow(["name", time])
with open("known_name_encodings.npy", "rb") as file:
    known_name_encodings_with_names = pickle.load(file)
    known_names= known_name_encodings_with_names[0]
    known_name_encodings = known_name_encodings_with_names[1]


cap = cv2.VideoCapture(1)
cap.set(3, 1200)
cap.set(4, 720)

def recognize():
    cv2.useOptimized()
    while cap.isOpened():
        ret, frame = cap.read()
        # rgb_frame = frame[:, :, ::-1]
        _img = cv2.resize(frame, (0,0), None, 0.25, 0.25)
        rgb_frame = cv2.cvtColor(_img, cv2.COLOR_BGR2RGB)
        face_locations = fr.face_locations(rgb_frame)
        face_encodings = fr.face_encodings(rgb_frame, face_locations)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = fr.compare_faces(known_name_encodings, face_encoding)
            name = "Unknown"
            face_distances = fr.face_distance(known_name_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_names[best_match_index][1]
                writer.writerows([[name, "Present"]])

            top, right, bottom, left = top*4, right*4, bottom*4, left*4
            # cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cvzone.cornerRect(frame, bbox=[left, top, right-left, bottom-top], rt=0)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (0, 0, 255), 1)

        cv2.imshow('Video', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()
    cap.release()


if __name__ == "__main__":
    recognize()
