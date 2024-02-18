import face_recognition as fr
import os
import numpy as np
import pickle
import pandas as pd
import uuid

# Trained data appended
known_names = []
known_name_encodings = []
known_name_encodings_with_names = []
known_name_encodings_with_namess = []

# Train 
def train(path="./train/", sID=False):
    # path = "./train/"
    images = os.listdir(path)
    if sID:
        files = os.listdir(path)
        for i in range(0, len(files)):
            os.rename(path + files[i], path + str(uuid.uuid4()) + ".jpg")
        images = os.listdir(path)

    for i in images:
        name_input = input(f"Enter the name of the person in the image {i[0:6]}: ")
        image = fr.load_image_file(path + i)
        image_path = path + i
        encoding = fr.face_encodings(image)[0]
        known_name_encodings.append(encoding)
        known_names.append([os.path.splitext(os.path.basename(image_path))[0].capitalize(), name_input.capitalize()])
    known_name_encodings_with_names.append(known_names)
    known_name_encodings_with_names.append(known_name_encodings)

# train a fresh data
def genesis_train(make, path="./train/", sID=False, file="known_name_encodings.npy"):
    if make:
        # print("Making new data file")
        train(path, sID)
        write_csv_name()
        # with open(file, "wb") as data:
        #     pickle.dump(known_name_encodings_with_names, data)
        #     print("Data saved successfully!")
    with open(file, "wb") as data:
        pickle.dump(known_name_encodings_with_names, data)
            # Testing code
    # with open(file, "w") as data:
    #     print("Appending to existing data")
    #     # pickle.dump(known_name_encodings_with_names, data)
    #     data.write(str(known_name_encodings_with_names))

# Add data to existing data
def add_data(path="./train/", sID=False, file="known_name_encodings.npy"):
    train(path, sID)
    with open(file, "rb") as data:
        global known_name_encodings_with_namess
        known_name_encodings_with_namess = pickle.load(data)
        known_name_encodings_with_names[0].extend(known_name_encodings_with_namess[0])
        known_name_encodings_with_names[1].extend(known_name_encodings_with_namess[1])
    genesis_train(file=file, make=False)
    write_csv_name(add=True)

# Write to csv
def write_csv_name(add=False):
    if add:
        new_data = known_names[0:len(known_names)-len(known_name_encodings_with_namess[0])]
        df = pd.read_csv("attendance.csv")
        new_row = pd.DataFrame({"name": [i[1] for i in new_data], "roll no.": [i[0] for i in new_data]})
        con_df = pd.concat([df, new_row]).drop_duplicates()
        con_df.fillna("Absent", inplace=True)
        # print(con_df)
        con_df.to_csv("attendance.csv", mode='w',index=False)
    else:
        new_data = known_names
        new_row = pd.DataFrame({"name": [i[1] for i in new_data], "roll no.": [i[0] for i in new_data]})
        new_row.to_csv("attendance.csv", index=False)
    
    known_names.clear()
    known_name_encodings.clear()
    known_name_encodings_with_names.clear()
    known_name_encodings_with_namess.clear()


# genesis_train(make=True, path="./dash/")
# add_data(path="./dash/", sID=False)
# write_csv_name()