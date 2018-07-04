from Matrix import Matrix
from BresenhamsLineAlgorithm import BresenhamsLineAlgorithm as Bla
from Player import Player
import cv2
from RPi.GPIO import GPIO
from picamera import PiCamera
import numpy as np
import io


class Game:

    def __init__(self):
        self.matrix = Matrix()
        self.bresenham = Bla(self.matrix)
        self.player1 = Player(1)
        self.player2 = Player(2)

        self.setup_gpio()
        self.camera = PiCamera()
        # saving the picture to an in-program stream rather than a file
        self.stream = io.BytesIO()
        self.standby()

    @staticmethod
    def setup_gpio():
        # pin setup
        # http://www.netzmafia.de/skripten/hardware/RasPi/RasPi_GPIO_C.html
        GPIO.cleanup()
        GPIO.setmode(GPIO.BOARD)
        pins = [7, 11, 13, 15, 19, 21, 23, 12, 16, 18, 22, 24, 26]
        for p in pins:
            GPIO.setup(p, GPIO.OUT)

        pass

    def take_and_process_picture(self):
        # code oriented at:
        # https://raspberrypi.stackexchange.com/questions/24232/picamera-taking-pictures-fast-and-processing-them

        # capture picture into stream
        self.camera.capture(self.stream, format='jpeg', use_video_port=True)
        # convert image into numpy array
        data = np.fromstring(self.stream.getvalue(), dtype=np.uint8)

        # split in picture into two sides
        data_left = data[0:int:(0.5*len(data[0])), 0:len(data)]
        data_right = data[int:(0.5*len(data[0])):len(data[0]), 0:len(data)]

        # turn the arrays into cv2 images
        left = cv2.imdecode(data_left, 1)
        right = cv2.imdecode(data_right, 1)

        # Resizing the images and convert them to HSV values for better recognition
        left = cv2.resize(left, (64, 32))
        right = cv2.resize(right, (64, 32))

        left = cv2.cvtColor(left, cv2.COLOR_BGR2HSV)
        right = cv2.cvtColor(right, cv2.COLOR_BGR2HSV)

        # Defining the red color range and calculating if these values lie in the range
        red_lower = np.array([0.5*255, 0.6*255, 0.7*255], np.uint8)
        red_upper = np.array([0.6*255, 0.7*255, 0.8*255], np.uint8)
        # binarize
        left_binary = cv2.inRange(left, red_lower, red_upper)
        right_binary = cv2.inRange(right, red_lower, red_upper)
        # threshold
        left_thresh = cv2.threshold(left_binary, 60, 255, cv2.THRESH_BINARY)[1]
        right_thresh = cv2.threshold(right_binary, 60, 255, cv2.THRESH_BINARY)[1]

        # cleans the skin colour space, extracting noise making it smaller
        # https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_imgproc/py_morphological_ops/py_morphological_ops.html
        kernel = np.ones((3, 3), "uint8")
        # outside noise cancelling
        left_thresh = cv2.morphologyEx(left_thresh, cv2.MORPH_OPEN, kernel)
        right_thresh = cv2.morphologyEx(right_thresh, cv2.MORPH_OPEN, kernel)
        # inside noise cancelling
        left_thresh = cv2.morphologyEx(left_thresh, cv2.MORPH_CLOSE, kernel)
        right_thresh = cv2.morphologyEx(right_thresh, cv2.MORPH_CLOSE, kernel)
        # making it smaller
        left_thresh = cv2.erode(left_thresh, kernel)
        right_thresh = cv2.erode(right_thresh, kernel)

        left_contours, _ = cv2.findContours(left_thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        right_contours, _ = cv2.findContours(right_thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        # change center of player1 and player2
        # https://www.pyimagesearch.com/2016/02/01/opencv-center-of-contour/
        if not left_contours == []:
            print("player 1 detected!")
            middle = cv2.moments(left_contours)
            x = int(middle["m10"] / middle["m00"])
            y = int(middle["m01"] / middle["m00"])
            self.player1.set_position(x, y)
        else:
            print("player 1 not detected.")

        if not right_contours == []:
            print("player 2 detected!")
            middle = cv2.moments(right_contours)
            x = int(middle["m10"] / middle["m00"])
            y = int(middle["m01"] / middle["m00"])
            self.player1.set_position(x, y)
        else:
            print("player 2 not detected.")

        pass

    @staticmethod
    def standby():
        # just light the edges of the matrix
        # until start button is pushed
        # then register players
        pass

    @staticmethod
    def register_players(self):
        # display Text:
        #                     Please
        #                  put your hands
        #                      here.
        #
        #                        _
        #                     _  /\ _
        #                  _ / \| |/ \
        #                 / \| || || |  _
        #                 | || || || | / /
        #                 |          |/ /
        #                 \            /
        #                  \          /
        #                   \________/

        pass

    def loop(self):
        # loop

        pass
