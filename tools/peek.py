#!/usr/bin/env python
"""Grab images from onboard cameras

For case of picamera, the code follows the example at
https://picamera.readthedocs.io/en/release-1.13/recipes1.html#capturing-to-a-file


SCL <scott@rerobots.net>
2018
"""
import time

from picamera import PiCamera


camera = PiCamera()
camera.resolution = (160, 120)
camera.start_preview()
time.sleep(2)
camera.capture('peek.jpg')
