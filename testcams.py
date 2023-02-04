import cv2

for i in range(5):
    cv2.namedWindow('cam'+str(i))
    cv2.moveWindow('cam'+str(i), 50*(i+1), 50*(i+1))

# capture from cameras
cap = [cv2.VideoCapture(2), cv2.VideoCapture(5), cv2.VideoCapture(7), cv2.VideoCapture(9), cv2.VideoCapture(11)]

while True:
    for i in range(5):
        ret, frame = cap[i].read()
        cv2.imshow('cam'+str(i), frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

for i in range(5):
    cap[i].release()
cv2.destroyAllWindows()