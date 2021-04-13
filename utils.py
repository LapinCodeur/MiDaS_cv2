import numpy as np
import datetime
from time import time, sleep
from threading import Thread

def save_name():
    sname = str(datetime.datetime.now())
    sname = sname.split()[1]
    sname = sname.replace('.', '_')
    return sname

class PerfTools:
    # Class to measure performance
    def __init__(self):
        self.timedep = time()
        self.time_list = []

    def start(self):
        self.timedep = time()

    def end_hz(self):
        return 1/self.end()

    def end(self):
        elapsed = time() - self.timedep
        self.time_list.append(elapsed)
        return elapsed

    def get_average(self):
        return np.mean(self.time_list)

    def get_average_hz(self):
        return 1/self.get_average()

    def get_last(self):
        return self.time_list[-1]


class RPI_Video:
    """Class to access the raspberry pi camera"""
    def __init__(self, resolution=(320, 240), framerate=24):
        from picamera.array import PiRGBArray
        from picamera import PiCamera

        self.camera = PiCamera()
        self.camera.resolution = resolution
        self.camera.framerate = framerate
        self.rawCapture = PiRGBArray(self.camera, size=resolution)
        self.stream = self.camera.capture_continuous(self.rawCapture, format="bgr", use_video_port=True)
        sleep(1)

        self.frame = None
        self.stopped = False
        self.frameVerif = False
        self.start()

    def start(self):
        Thread(target=self.update, args=()).start()
        sleep(1)
        while not self.new_frame():
            sleep(0.001)
        return self

    def update(self):
        for f in self.stream:
            if self.stopped:
                self.stream.close()
                self.rawCapture.close()
                self.camera.close()
                return
            self.frame = f.array
            self.rawCapture.truncate(0)
            self.frameVerif = True

    def read(self, wait = False):
        if wait:
            while not self.new_frame():
                sleep(0.001)
        status = self.frameVerif
        self.frameVerif = False
        return status, self.frame

    def new_frame(self):
        return self.frameVerif

    def release(self):
        self.stopped = True
