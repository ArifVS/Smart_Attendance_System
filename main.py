# Import the required libraries
import face_recognition
import cv2
import numpy as np
import csv
import os
from datetime import datetime

teacher_number = input("Enter Teacher WhatsApp Number (with country code): ")

# Initialize the video capture object for the default camera
video_capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# ============================
# LOAD ALL STUDENT FACES
# ============================
known_face_encodings = []
known_face_names = []

faces_folder = "faces"

for filename in os.listdir(faces_folder):
    if filename.lower().endswith((".jpg", ".jpeg", ".png")):
        path = os.path.join(faces_folder, filename)

        # Load the image
        image = face_recognition.load_image_file(path)
        encodings = face_recognition.face_encodings(image)

        if len(encodings) > 0:
            encoding = encodings[0]

            # student name = filename without extension
            name = os.path.splitext(filename)[0]

            known_face_encodings.append(encoding)
            known_face_names.append(name)

            print(f"Loaded: {name}")

        else:
            print(f"Face not detected in {filename}, skipping...")

# Copy known_face_names for attendance
students = known_face_names.copy()

# ============================
# ATTENDANCE CSV SETUP
# ============================
now = datetime.now()
current_date = now.strftime("%d-%m-%Y")

f = open(f"{current_date}.csv", "w+", newline="")
lnwriter = csv.writer(f)
lnwriter.writerow(["Name", "Date", "Day", "Time"])
# ============================
# START VIDEO LOOP
# ============================
while True:
    _, frame = video_capture.read()

    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):

        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        face_distance = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distance)

        name = "Unknown"

        if matches[best_match_index]:
            name = known_face_names[best_match_index]

        # Scale face location back to full-size frame
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4
        # Draw rectangle around each face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

        # Write name on the frame
        cv2.putText(frame, name, (left, top - 10),
            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Mark attendance for each recognized face
        if name in students:
            students.remove(name)

            now = datetime.now()
            date = now.strftime("%d-%m-%Y")
            day = now.strftime("%A")
            time = now.strftime("%H:%M:%S")

            lnwriter.writerow([name, date, day, time])
            print(f"Marked present: {name} | {date} | {day} | {time}")


    cv2.imshow("HMC Attendance", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

video_capture.release()
cv2.destroyAllWindows()
f.close()

import pandas as pd

csv_file = f"{current_date}.csv"
excel_file = f"{current_date}.xlsx"

df = pd.read_csv(csv_file)
df.to_excel(excel_file, index=False)





from send_to_whatsapp import send_whatsapp_document
csv_file = f"{current_date}.csv"
try:
    send_whatsapp_document(teacher_number, csv_file)
    print("Attendance sent successfully!")
except Exception as e:
    print("Failed to send attendance:", e)



