__author__ = 'jacopobacchi'
import RPi.GPIO as GPIO
import time
import shlex
import subprocess

# Define Buttons
PREV = 4
NEXT = 17
PLAY = 27
REPEAT = 22
GPIO.setmode(GPIO.BCM)
GPIO.setup(PREV, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(NEXT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(PLAY, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(REPEAT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
prev_input = 0
next_input = 0
play_input = 0
repeat_input = 0
play = 1
while True:
  #take a reading
  input1 = GPIO.input(PREV)
  #if the last reading was low and this one high, print
  if ((not prev_input) and input):
    print("Button PREV pressed")
    cmd = "mpc prev"
    args = shlex.split(cmd)
    output = subprocess.Popen(args)
  #update previous input
  prev_input = input1
  time.sleep(0.05)
  #take a reading
  input2 = GPIO.input(NEXT)
  #if the last reading was low and this one high, print
  if ((not next_input) and input):
    print("Button NEXT pressed")
    cmd = "mpc next"
    args = shlex.split(cmd)
    output = subprocess.Popen(args)
  #update previous input
  next_input = input2
  time.sleep(0.05)
  #take a reading
  input3 = GPIO.input(PLAY)
  #if the last reading was low and this one high, print
  if ((not play_input) and input):
    print("Button PLAY pressed")
    print(play)
    if (play == 1 ):
        cmd = "mpc play"
        args = shlex.split(cmd)
        output = subprocess.Popen(args)
        play = 0
    else:
        cmd = "mpc pause"
        args = shlex.split(cmd)
        output = subprocess.Popen(args)
        play = 1
  #update previous input
  play_input = input3
  time.sleep(0.05)
  #take a reading
  input4 = GPIO.input(REPEAT)
  if ((not repeat_input) and input):
    print("Button REPEAT pressed")
    cmd = "mpc repeat"
    args = shlex.split(cmd)
    output = subprocess.Popen(args)
  #update previous input
  repeat_input = input4
  #slight pause to debounce
  time.sleep(0.05)