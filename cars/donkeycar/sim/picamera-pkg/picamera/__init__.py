import time


class Frame:
    def __init__(self):
        self.array = list()

class PiCamera:
    def __init__(self):
        self.resolution = None
        self.framerate = None

    def capture_continuous(self, capture, format, use_video_port):
        while True:
            time.sleep(1)
            yield Frame()

    def close(self):
        pass
