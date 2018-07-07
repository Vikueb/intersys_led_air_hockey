from Matrix import Matrix
from BresenhamsLineAlgorithm import BresenhamsLineAlgorithm as Bla
from Player import Player
from Ball import Ball
import cv2
import RPi.GPIO as GPIO
from picamera import PiCamera
import numpy as np
import io

# globals
matrix = Matrix()
bresenham = Bla(matrix)
player1 = Player(1)
player2 = Player(2)
ball = Ball(bresenham)
wins = False


# ---------------------------------------------------------------------------------------------------------------- #
def setup_gpio():
    # pin setup for matrix
    # http://www.netzmafia.de/skripten/hardware/RasPi/RasPi_GPIO_C.html
    print("setting up GPIO")
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    pins = [7, 11, 13, 15, 19, 21, 23, 12, 16, 18, 22, 24, 26]
    for p in pins:
        GPIO.setup(p, GPIO.OUT)

    # pin setup for buttons
    GPIO.setup(start_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(exit_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    return


# ---------------------------------------------------------------------------------------------------------------- #
def standby():
    # just light the edges of the matrix
    # until start button is pushed
    while not GPIO.input(start_button) == 1:
        print("standby\n")
        print("please press start to start the game!")
        matrix.draw_standby()

    # then register players
    while True:
        # try to register again
        if register_players():
            break

    return


# ---------------------------------------------------------------------------------------------------------------- #
def loop():
    # keep playing until somebody wins
    while not wins:
        # keep playing until exit button or stop button are pressed
        if GPIO.input(exit_button) == 1:
            print("The Game is being turned off because you hit the exit button!\n")
            exit()
        else:
            if GPIO.input(start_button) == 1:
                print("returning to standby mode because the stop button was pressed!\n")
                return

        for i in range(3):
            # let ball roll
            move_ball()

            display_board()

        # where are the hands of the players?
        take_and_process_picture()

        for i in range(3):
            # let ball roll
            move_ball()

            display_board()

    return


# ---------------------------------------------------------------------------------------------------------------- #
def take_and_process_picture():
    player1_reg = False
    player2_reg = False
    # code oriented at:
    # https://raspberrypi.stackexchange.com/questions/24232/picamera-taking-pictures-fast-and-processing-them

    # capture picture into stream
    camera.capture(stream, format='jpeg', use_video_port=True)
    # convert image into numpy array
    data = np.fromstring(stream.getvalue(), dtype=np.uint8)

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

    # Defining the skin color range and calculating if these values lie in that
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
        player1.set_position(x, y)
        player1_reg = True
    else:
        print("player 1 not detected.")

    if not right_contours == []:
        print("player 2 detected!")
        middle = cv2.moments(right_contours)
        x = int(middle["m10"] / middle["m00"])
        y = int(middle["m01"] / middle["m00"])
        player1.set_position(x, y)
        player2_reg = True
    else:
        print("player 2 not detected.")

    return player1_reg & player2_reg


# ---------------------------------------------------------------------------------------------------------------- #
def register_players():
    print("Put your hands on the table!")
    # display Text:
    #                  Put your hand
    #                      here.
    #
    #                   _
    #                _ | | _
    #             _ | || || |
    #            | || || || |  _
    #            | || || || | / /
    #            |          |/ /
    #            \            /
    #             \          /
    #              \________/

    # then let the camera catch them
    take_and_process_picture()
    return


# ---------------------------------------------------------------------------------------------------------------- #
def goal(identity):
    # add point to score of the player who scored
    if identity == 1:
        player1.score += 1
        print("Player 1 scored a goal!\n")
    else:
        player2.score += 1
        print("Player 2 scored a goal!\n")

    # display Score on each side of the field
    print(player1.score + " : " + player2.score)

    # if score of one player is 10 he wins
    if player1.score == 10:
        winner(1)
        wins = True
    else:
        if player2.score == 10:
            winner(2)
            wins = True

    return


# ---------------------------------------------------------------------------------------------------------------- #
def winner(identity):
    # display Text "WINNER" on the field side of the winner
    # and display Text "LOOSER" on the looser's side

    print("Player " + "1" if identity == 0 else "0" + "looses!\n")
    print("Player " + identity + " wins!\n")

    wins = True
    return


# ---------------------------------------------------------------------------------------------------------------- #
def display_board():
    matrix.draw_goals()                            # red

    matrix.draw_line_horizontal(0, 63, 0)          # green     outer line
    matrix.draw_line_horizontal(0, 63, 31)         # green
    matrix.draw_line_vertical(0, 0, 11)            # green
    matrix.draw_line_vertical(0, 20, 31)           # green
    matrix.draw_line_vertical(63, 0, 11)           # green
    matrix.draw_line_vertical(63, 20, 31)          # green

    matrix.draw_line_vertical(31, 0, 11)           # green     middle line
    matrix.draw_line_vertical(31, 20, 31)          # green

    matrix.draw_circle(31, 16)                     # green
    matrix.draw_pixel(31, 16)                      # green

    matrix.draw_pixel(ball.x, ball.y)    # blue      ball

    for x, y in (player1.x, player1.y):       # orange    player 1
        matrix.draw_pixel(x, y)                    #

    for x, y in (player2.x, player2.y):       # purple    player 2
        matrix.draw_pixel(x, y)                    #

    print("-------------------------------------------------------------------------\n")
    print("displaying board with ball at: (" + ball.x + ", " + ball.y + ")\n")
    print("heading: " + ball.direction + ".\n")
    print("Player 1 is on position: ")
    print("(" + x + ", " + y + ")\n" for i, x, y in (range(4), player1.x, player1.y))
    print("Player 2 is on position: ")
    print("(" + x + ", " + y + ")\n" for i, x, y in (range(4), player2.x, player2.y))
    print("-------------------------------------------------------------------------\n")

    return


# ---------------------------------------------------------------------------------------------------------------- #
def move_ball():
    ball.move()
    # goal?
    scored = matrix.is_goal(ball.x, ball.y)
    if scored != -1:
        goal(scored)

    # hit?
    if player1.x == ball.x & player1.y == ball.y:
        ball.calculate_path()
        print("player 1 hit the ball\n")
    if player2.x == ball.x & player2.y == ball.y:
        ball.calculate_path()
        print("player 2 hit the ball\n")

    return


# ---------------------------------------------------------------------------------------------------------------- #
def usage():
    print("\n")
    print("PROGRAMMING EXERCISE FOR INTERACTIVE SYSTEMS  \n")
    print("**********************************************\n")
    print("    Copyright 2018 by Vincent Kuebler,        \n")
    print("    Kora Regitz, Betim Sulejmani and          \n")
    print("    Mehmood UI Hassan.                        \n")
    print("    Students of Computer Science              \n")
    print("    Saarland University, Saarbruecken, Germany\n")
    print("    All rights reserved. Unauthorised usage,  \n")
    print("    copying, hiring, and selling prohibited.  \n")
    print("**********************************************\n\n")

    return


# ---------------------------------------------------------------------------------------------------------------- #
# let's go!
usage()

start_button = 38
exit_button = 40
setup_gpio()
camera = PiCamera()
# saving the picture to an in-program stream rather than a file
stream = io.StringIO()

print("let the game begin!")
while GPIO.input(exit_button) == 0:
    standby()
    print("entering game mode now!")
    loop()

print("game was ended!")
GPIO.cleanup()
