import cv2
import face_recognition as fr
import numpy as np
import pickle
import cvzone as cvzone
import os
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

path = "./test_data/sample_data/"
images = os.listdir(path)

for i in images:
    img = cv2.imread(path + i)
    face_locations = fr.face_locations(img)
    face_encodings = fr.face_encodings(img, face_locations)
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = fr.compare_faces(known_name_encodings, face_encoding)
        name = "unknown"
        face_distances = fr.face_distance(known_name_encodings, face_encoding)
        best_match = np.argmin(face_distances)
        if matches[best_match]:
            name = known_names[best_match][1]
            writer.writerows([[name, "Present"]])

        cvzone.cornerRect(img, bbox=[left, top, right-left, bottom-top], rt=0)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(img, name, (left + 6, bottom + 25), font, 1.0, (255, 255, 255), 1)

    cv2.imshow("Result", img)
    cv2.imwrite(f"./test_data/sample_output/{i[0:6]}.jpg", img)

    cv2.waitKey(0)
    cv2.destroyAllWindows()






















# test_image = "./test/sample_data/000001.jpg"
# image = cv2.imread(test_image)
# with open("known_name_encodings.npy", "rb") as file:
#     known_name_encodings_with_names = pickle.load(file)
#     known_names= known_name_encodings_with_names[0]
#     known_name_encodings = known_name_encodings_with_names[1]

# face_locations = fr.face_locations(image)
# face_encodings = fr.face_encodings(image, face_locations)

# for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
#    matches = fr.compare_faces(known_name_encodings, face_encoding)
#    name = ""
#    face_distances = fr.face_distance(known_name_encodings, face_encoding)
#    best_match = np.argmin(face_distances)
#    if matches[best_match]:
#        name = known_names[best_match][1]
#        print(name)
#    cvzone.cornerRect(image, bbox=[left, top, right-left-3, bottom-top-3], rt=0)
#    font = cv2.FONT_HERSHEY_DUPLEX
#    cv2.putText(image, name, (left + 6, bottom + 25), font, 1.0, (255, 255, 255), 1)

# cv2.imshow("Result", image)
# cv2.imwrite("./output.jpg", image)

# cv2.waitKey(0)
# cv2.destroyAllWindows()

