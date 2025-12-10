import cv2
import os

# Create folder if not exists
if not os.path.exists("faces"):
    os.makedirs("faces")

# Take user input
name = input("Enter Student Name: ").strip()
regno = input("Enter Register Number: ").strip()

filename = f"{name}_{regno}.jpg"
filepath = os.path.join("faces", filename)

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

print("Press SPACE to capture image")
print("Press Q to quit")

while True:
    ret, frame = cap.read()
    cv2.imshow("Capture Student Face", frame)

    key = cv2.waitKey(1)

    if key == 32:   # SPACE key
        cv2.imwrite(filepath, frame)
        print(f"Saved face as {filepath}")
        break

    elif key == ord('q'):
        print("Cancelled")
        break

cap.release()
cv2.destroyAllWindows()
