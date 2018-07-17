from Matrix import Matrix
from BresenhamsLineAlgorithm import BresenhamsLineAlgorithm as Bla
from Player import Player
from Ball import Ball
import cv2
import RPi.GPIO as GPIO
from picamera import PiCamera, array
import numpy as np
from time import sleep

# globals
matrix = Matrix()
bresenham = Bla(matrix)
player1 = Player(1)
player2 = Player(2)
ball = Ball(bresenham)
wins = False

start_button = 38
exit_button = 40
camera = PiCamera()


# ---------------------------------------------------------------------------------------------------------------- #
def setup_gpio():
    """
    Does the setup for all GPIO Pins, except for the two buttons, as they have to be set globally
    :return: when setup is completed
    """
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
    GPIO.setup(exit_button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    return


# ---------------------------------------------------------------------------------------------------------------- #
def standby():
    """
    Shows the standby mode of the matrix, as long as the start button is not pressed.
    When the start button is pressed it waits for both players to be ready.
    :return: when 'start' was pressed and both players are registered
    """
    start_input = GPIO.input(start_button)
    # just light the edges of the matrix
    # until start button is pushed
    while not start_input:
        print("standby\n")
        print("please press start to start the game!")
        matrix.draw_standby()
        start_input = GPIO.input(start_button)

    # then register players
    while True:
        # try to register again
        if register_players():
            break

    return


# ---------------------------------------------------------------------------------------------------------------- #
def loop():
    """
    keep playing until somebody wins
    1. checks if either 'stop' or 'exit' button were pressed
    2. searches for players hand positions
    3. moves ball for two steps and also displays the field
    :return: when 'start'/ 'stop' button was pressed again
    """
    while not globals()['wins']:
        start_input = GPIO.input(start_button)
        exit_input = GPIO.input(exit_button)
        # keep playing until exit button or stop button are pressed
        if exit_input:
            print("The Game is being turned off because you hit the exit button!\n")
            exit()
        else:
            if start_input:
                print("returning to standby mode because the stop button was pressed!\n")
                return

        # where are the hands of the players?
        take_and_process_picture()

        for i in range(2):
            # let ball roll
            move_ball()

            display_board()

    return


# ---------------------------------------------------------------------------------------------------------------- #
def take_and_process_picture():
    """
    1. a local stream for picture saving is initialised
    2. camera resolution is set and picture captured into stream
    3. the captured image is read from the stream and split into the two sides
    4. the (now) two pictures are resized to the size of the field
    5. the mask for the hands is created
    6. the pictures are reduced to the hand positions
    7. the background/ foreground noise is reduced
    8. the pictures are converted in gray tones
    9. the contours of the hands are searched and saved
    10. the middle of the contours is determined
    11. the new player positions are set
    :return: True when both players hands were found - important for standby() when registering players
    """
    player1_reg = False
    player2_reg = False
    # code oriented at:
    # https://raspberrypi.stackexchange.com/questions/24232/picamera-taking-pictures-fast-and-processing-them

    # capture picture into stream
    stream = array.PiBGRArray(camera)
    camera.resolution = (640, 320)      # (x,y)
    camera.start_preview()
    sleep(0.5)
    camera.capture(stream, format="bgr", use_video_port=True)
    camera.stop_preview()

    # turn data into cv2 image
    # print(stream.array[0].size / 3, stream.array.size / stream.array[0].size)
    img = np.frombuffer(stream.getvalue(), dtype=np.uint8).reshape(320, 640, 3)

    # split in picture into two sides
    x = img[0].size / 3
    x = x if x % 2 == 0 else x-1
    x = int(0.5*x)
    max_y = img.size / img[0].size
    left = img[0:max_y, 0:x]
    right = img[0:max_y, x:img[0].size/3]

    # Resizing the images and convert them to HSV values for better recognition
    left = cv2.resize(left, (32, 32))
    right = cv2.resize(right, (32, 32))

    # Defining the skin color range and calculating if these values lie in that
    skin_lower = np.array([0.5*255, 0.6*255, 0.7*255], np.uint8)
    skin_upper = np.array([0.6*255, 0.7*255, 0.8*255], np.uint8)
    # get the mask
    left_mask = cv2.inRange(left, skin_lower, skin_upper)
    right_mask = cv2.inRange(right, skin_lower, skin_upper)
    # apply mask
    left_hand = cv2.bitwise_and(left, left, mask=left_mask)
    right_hand = cv2.bitwise_and(right, right, mask=right_mask)

    # cleans the skin colour space, extracting noise making it smaller
    # https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_imgproc/py_morphological_ops/py_morphological_ops.html
    kernel = np.ones((3, 3), "uint8")
    # outside noise cancelling
    left_hand = cv2.morphologyEx(left_hand, cv2.MORPH_OPEN, kernel)
    right_hand = cv2.morphologyEx(right_hand, cv2.MORPH_OPEN, kernel)
    # inside noise cancelling
    left_hand = cv2.morphologyEx(left_hand, cv2.MORPH_CLOSE, kernel)
    right_hand = cv2.morphologyEx(right_hand, cv2.MORPH_CLOSE, kernel)
    # making it smaller
    left_hand = cv2.erode(left_hand, kernel)
    right_hand = cv2.erode(right_hand, kernel)

    left_hand = cv2.cvtColor(left_hand, cv2.COLOR_BGR2GRAY)
    right_hand = cv2.cvtColor(right_hand, cv2.COLOR_BGR2GRAY)

    left_contours = cv2.findContours(left_hand, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[1]
    right_contours = cv2.findContours(right_hand, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[1]

    # change center of player1 and player2
    # https://www.pyimagesearch.com/2016/02/01/opencv-center-of-contour/
    if not left_contours == []:
        print("player 1 detected!")
        middle = cv2.moments(left_contours[0])
        x = int(middle["m10"] / middle["m00"])
        y = int(middle["m01"] / middle["m00"])
        player1.set_position(x, y)
        player1_reg = True
    else:
        print("player 1 not detected.")

    if not right_contours == []:
        print("player 2 detected!")
        middle = cv2.moments(right_contours[0])
        x = int(middle["m10"] / middle["m00"])
        y = int(middle["m01"] / middle["m00"])
        player1.set_position(x, y)
        player2_reg = True
    else:
        print("player 2 not detected.")

    cv2.destroyAllWindows()

    return player1_reg & player2_reg


# ---------------------------------------------------------------------------------------------------------------- #
def register_players():
    """
    method that displays on the matrix, that the players should put their hands on the table
    so the camera can capture them
    :return: True if it was possible to determine positions for both players
    """
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
    return take_and_process_picture()


# ---------------------------------------------------------------------------------------------------------------- #
def goal(identity):
    """
    1. adds a point to the score of the player who scored
    2. checks if a player reached ten points and therefore wins
    :param identity: id of the player who scored
    :return: void
    """
    # add point to score of the player who scored
    if identity == 1:
        player1.score += 1
        print("Player 1 scored a goal!\n")
        ball.set_ball(0)
    else:
        player2.score += 1
        print("Player 2 scored a goal!\n")
        ball.set_ball(1)

    # display Score on each side of the field
    print(player1.score + " : " + player2.score)

    # if score of one player is 10 he wins
    if player1.score == 10:
        winner(1)
    else:
        if player2.score == 10:
            winner(2)

    return


# ---------------------------------------------------------------------------------------------------------------- #
def winner(identity):
    """
    1. display Text "WINNER" on the field side of the winner and Text "LOOSER" on the looser's side
    2. set global variable "wins" to true, so the loop can be exited
    :param identity: id of the player who reached 10 points
    :return: void
    """

    print("Player " + "1" if identity == 0 else "0" + "looses!\n")
    print("Player " + identity + " wins!\n")

    globals()['wins'] = True
    return


# ---------------------------------------------------------------------------------------------------------------- #
def display_board():
    """
    displays the field/ board (outer lines, middle, goals, ball & players)
    :return: void
    """
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

    matrix.draw_pixel(ball.x, ball.y)              # blue      ball

    for x, y in (player1.x, player1.y):            # orange    player 1
        matrix.draw_pixel(x, y)                    #

    for x, y in (player2.x, player2.y):            # purple    player 2
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
    """
    1. ball is moved
    2. check if it is a gaol
    3. check if a player hit the ball - if yes calculate a new path of the goal
    :return:
    """
    ball.move()
    # goal?
    scored = matrix.is_goal(ball.x, ball.y)
    if scored != -1:
        goal(scored)

    # hit?
    a = player1.x[0] == ball.x & player1.y[0] == ball.y
    b = player1.x[1] == ball.x & player1.y[1] == ball.y
    c = player1.x[2] == ball.x & player1.y[2] == ball.y
    d = player1.x[3] == ball.x & player1.y[3] == ball.y
    if a | b | c | d:
        ball.calculate_path()
        print("player 1 hit the ball\n")

    a = player2.x[0] == ball.x & player2.y[0] == ball.y
    b = player2.x[1] == ball.x & player2.y[1] == ball.y
    c = player2.x[2] == ball.x & player2.y[2] == ball.y
    d = player2.x[3] == ball.x & player2.y[3] == ball.y
    if a | b | c | d:
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
"""
let's go!
The actual game starts here!
1. Game remains in standby mode until the start button is hit.
2. Game is played (loop) while nobody won or the stop button is hit
3. If the exit button is hit the table turns off
"""
setup_gpio()
usage()

print("let the game begin!")
exit_input = GPIO.input(exit_button)
while not exit_input:
    standby()
    print("entering game mode now!")
    loop()
    exit_input = GPIO.input(exit_button)

print("game was ended!")
GPIO.cleanup()
