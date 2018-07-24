# intersys_led_air_hockey
This is a Raspberry Pi 3B python project for the Lecture "Interactive Systems" at the University of Saarland.
In a group of three to four people we first had to think about four possible projects with either Arduino 
Uno or Raspberry Pi.

We decided to do an LED Air Hockey Table with the idea to digitize and making playing easier and more interesting.
There were a lot of difficulties to overcome.

The recommended software [RPI RGB LED Matrix](https://github.com/hzeller/rpi-rgb-led-matrix) doesn't work 
on our Raspberry Pi because of inexplicable reasons. That's why we had to make the modification to give 
the matrix a random output so it does something. With 32x64 = 2048 and just 16 outputs it's difficult to 
find out - without any documentation - how to control the LED's.

You can find the test video [here](https://www.dropbox.com/s/t4hwyunx3ss2w0f/VID_20180724_143618.3gp?dl=0).

After that another bug was fixed and of course we hope to be able to solve the mystery of the matrix
control.

We hope you can enjoy the project, if you have any questions contact [Vincent Kübler](mailto:artemis0597@yahoo.de).

