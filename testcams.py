from threading import Thread
import cv2, time
 
class VideoStreamWidget(object):
    def __init__(self, src=0):
        self.capture = cv2.VideoCapture(src)
        # Start the thread to read frames from the video stream
        self.thread = Thread(target=self.update, args=())
        self.thread.daemon = True
        self.thread.start()

    def update(self):
        # Read the next frame from the stream in a different thread
        if self.capture.isOpened():
            while True:
                (self.status, self.frame) = self.capture.read()
                time.sleep(.01)
    
    def show_frame(self):
        # Display frames in main program
        cv2.imshow('frame', self.frame)
        key = cv2.waitKey(1)
        if key == ord('q'):
            self.capture.release()
            cv2.destroyAllWindows()
            exit(1)

if __name__ == '__main__':
    video_stream_widget1 = VideoStreamWidget(src=9)
    video_stream_widget2 = VideoStreamWidget(src=2)
    video_stream_widget3 = VideoStreamWidget(src=5)
    video_stream_widget4 = VideoStreamWidget(src=7)
    video_stream_widget5 = VideoStreamWidget(src=11)
    while True:
        try:
            video_stream_widget1.show_frame()
            video_stream_widget2.show_frame()
            video_stream_widget3.show_frame()
            video_stream_widget4.show_frame()
            video_stream_widget5.show_frame()
        except AttributeError:
            pass