import face_recognition as fr
import os
import numpy as np
import pickle

path = "./train/"
known_names = []
known_name_encodings = []
images = os.listdir(path)

for i in images:
    name_input = input(f"Enter the name of the person in the image {i[0:6]}: ")
    image = fr.load_image_file(path + i)
    image_path = path + i
    encoding = fr.face_encodings(image)[0]
    known_name_encodings.append(encoding)
    known_names.append([os.path.splitext(os.path.basename(image_path))[0].capitalize(), name_input.capitalize()])

known_name_encodings_with_names = []
known_name_encodings_with_names.append(known_names)
known_name_encodings_with_names.append(known_name_encodings)

with open("known_name_encodings.npy", "wb") as file:
    pickle.dump(known_name_encodings_with_names, file)




















# # with open("known_name_encodings.npy", "rb") as file:
# #     known_name_encodings_with_names = pickle.load(file)
# #     known_names= known_name_encodings_with_names[0]
# #     known_name_encodings = known_name_encodings_with_names[1]
# #     print("Known names and encodings loaded successfully!")
# #     print("known_file_name: ", known_names[0])
# #     print("known_person_name: ", known_names[1])
# with open("unknown.txt", "w") as file:
#     file.write(str(known_name_encodings_with_names))
#     print("Data saved successfully!")