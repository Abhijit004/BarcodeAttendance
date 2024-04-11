import cv2
from pyzbar.pyzbar import decode

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)
camera = True

def captureBarcodes(idmap):
    res = set()
    while camera:
        success, frame = cap.read()
        for code in decode(frame):
            ID = '2'+code.data.decode('utf-8')
            if ID not in res and ID in idmap: 
                print(ID, "has been marked present")
            res.add(ID)
        cv2.imshow('testing-code-scan', frame)
        if cv2.waitKey(1) & 0xFF == ord('g'):
            cv2.destroyAllWindows()
            break
    print("Following students are marked present\n")
    for student in res: print(student)
    return res