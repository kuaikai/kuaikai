import time

import numpy as np


class Frame:
    def __init__(self):
        self.array = np.zeros((120, 160, 3), dtype=np.uint8)

class PiCamera:
    def __init__(self):
        self.resolution = None
        self.framerate = None

    def capture_continuous(self, capture, format, use_video_port):
        while True:
            yield Frame()

    def close(self):
        pass
