class PiCamera:
    def __init__(self):
        self.resolution = None
        self.framerate = None

    def capture_continuous(self, capture, format, use_video_port):
        while True:
            yield list()

    def close(self):
        pass
