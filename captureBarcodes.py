import cv2
from pyzbar.pyzbar import decode


def captureBarcodes(idmap):
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)
    camera = True
    res = set()
    while camera:
        success, frame = cap.read()
        for code in decode(frame):
            ID = code.data.decode('utf-8')
            if ID[0] != '2': ID = '2'+ID
            if ID not in res and ID in idmap: 
                print(ID, "has been marked present")
            res.add(ID)
        cv2.imshow('barcode-scanning', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('g'):
            cv2.destroyAllWindows()
            break
    print("Following students are marked present\n")
    for student in res: print(student)
    cap.release()
    return res