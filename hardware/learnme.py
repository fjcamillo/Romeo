import cv2
import json, requests

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

cap = cv2.VideoCapture(0)

transfered = 0

while True:

    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x,y,w,h) in faces:
        cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0) ,2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]

        eyes = eye_cascade.detectMultiScale(roi_gray)

        payload = {'body': 'Rommel'}
        payload = json.dumps(payload)
        # transfered = 1
        r = requests.post("https://04e27ba9.ngrok.io/chat/hardware/", data=payload)
        for (ex,ey,ew,eh) in eyes:
            cv2.rectangle(roi_color, (ex,ey), (ex+ew,ey+eh), (0,255,0), 2)


    cv2.imshow('img', img)
    k=cv2.waitKey(30) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
cap.release()
