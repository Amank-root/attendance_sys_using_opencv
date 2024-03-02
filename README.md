# Overview

``Developing this from scratch in a week with no knowledge of pandas, tkinter, and face-recognition modules was challenging, yet exciting at the same time. ``

The project aims to streamline the attendance-taking process by accurately identifying students and marking their attendance on specific dates. Leveraging computer vision techniques, particularly face recognition, along with libraries such as OpenCV and pandas in Python, the system seeks to enhance efficiency, reduce errors, and provide a more effective means of managing attendance records.

# Mechanism

1. **Data Collection:** Gather images of students' faces for training the face recognition model.
2. **Training:** Utilize OpenCV and the face-recognition module to train the model on the collected images to recognize specific individuals.
3. **Recognition:** Capture images or video frames during attendance sessions and apply the trained model to recognize faces.
4. **Attendance Marking:** Compare recognized faces with the database of students and mark them as present for the particular date using the Pandas library to manage attendance records.

# Flowchart
![Flowchart](https://raw.githubusercontent.com/Amank-root/attendance_sys_using_opencv/main/projectFlowchart.png)

# Prerequisites

- CMake
- Dlib
- Setuptools

# Getting Started

```bash
git clone https://github.com/Amank-root/attendance_sys_using_opencv.git
cd attendance_sys_using_opencv
pip install virtualenv # Use only if venv is not installed
```

#### Creating and activating Python environment (Windows)

```bash
python -m venv env_name
env_name/Scripts/activate
```

#### Creating and activating Python environment (Linux)

```bash
virtualenv virtualenv_name
source virtualenv_name/bin/activate
```

```bash
# Command after setting up the environment
pip install -r requirement.txt
```

#### Running the script

```bash
python main.py
```

# Training

Create an empty folder and add the images of the person you want to train. In the GUI interface, provide the path of the folder.

# Testing
![Ratan Tata Output](https://raw.githubusercontent.com/Amank-root/attendance_sys_using_opencv/main/test_data/sample_output/Nov-20.jpg)

# References

1. [Github (Face-recognition)](https://github.com/ageitgey/face_recognition/)
2. Geek for Geeks
3. [YouTube (Tkinter Crash Course)](https://www.youtube.com/watch?v=mop6g-c5HEY)
