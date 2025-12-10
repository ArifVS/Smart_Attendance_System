
# AI-Based Face Recognition Attendance System with WhatsApp Integration

Requirements:
1. Python Version: Use Python 3.7–3.10(compatible with dlib & face_recognition).

2. Required Libraries: face_recognition, opencv-python, numpy, pandas, openpyxl, requests.

3. Install Libraries:
    pip install face_recognition opencv-python numpy pandas openpyxl requests

4. faces Folder: Add student images inside faces/ (filename = student name).

5. Run Application:
    python main.py
6. Teacher Input: Enter teacher’s WhatsApp number in CLI (format: +9198XXXXXXXX).

7. Face Recognition: System detects faces via webcam, matches embeddings, and logs attendance.

8. Attendance Output: Generates DD-MM-YYYY.csv and auto-converts to DD-MM-YYYY.xlsx.

9. WhatsApp Sending: Uses WhatsApp Cloud API to upload & send the XLSX file to the teacher.

10. Prerequisites: WhatsApp Business API setup, verified phone number, payment method, and permanent access token.
