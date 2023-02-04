import cv2

cv_0 = cv2.VideoCapture(2)
cv_1 = cv2.VideoCapture(9)
cv_2 = cv2.VideoCapture(5)
cv_3 = cv2.VideoCapture(7)
cv_4 = cv2.VideoCapture(11)

while True:
    
    ret0, frame0 = cv_0.read()
    ret1, frame1 = cv_1.read()
    ret2, frame2 = cv_2.read()
    ret3, frame3 = cv_3.read()
    ret4, frame4 = cv_4.read()

    if (ret0):
        cv2.imshow('Cam 0', frame0)

    if (ret1):
        cv2.imshow('Cam 1', frame1)

    if (ret2):
        cv2.imshow('Cam 2', frame2)
    
    if (ret3):
        cv2.imshow('Cam 3', frame3)    
    
    if (ret4):
        cv2.imshow('Cam 4', frame4)   

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
cv_0.release()
cv_1.release()
cv_2.release()
cv_3.release()
cv_4.release()
cv2.destroyAllWindows()
