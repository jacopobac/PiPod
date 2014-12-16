__author__ = 'jacopobacchi'
import RPi.GPIO as GPIO
import time
import subprocess
import shlex

# Define GPIO to LCD mapping
LCD_RS = 7
LCD_E  = 8
LCD_D4 = 25
LCD_D5 = 24
LCD_D6 = 23
LCD_D7 = 18

# Define some device constants
LCD_WIDTH = 16    # Maximum characters per line
LCD_CHR = True
LCD_CMD = False

LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line

# Timing constants
E_PULSE = 0.00005
E_DELAY = 0.00005


# Define Buttons
PREV = 4
NEXT = 17
PLAY = 21
REPEAT = 22

def main():
  # Main program block
  GPIO.setmode(GPIO.BCM)       # Use BCM GPIO numbers
  GPIO.setup(LCD_E, GPIO.OUT)  # E
  GPIO.setup(LCD_RS, GPIO.OUT) # RS
  GPIO.setup(LCD_D4, GPIO.OUT) # DB4
  GPIO.setup(LCD_D5, GPIO.OUT) # DB5
  GPIO.setup(LCD_D6, GPIO.OUT) # DB6
  GPIO.setup(LCD_D7, GPIO.OUT) # DB7
  GPIO.setup(PREV, GPIO.IN, pull_up_down=GPIO.PUD_UP)
  GPIO.setup(NEXT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
  GPIO.setup(PLAY, GPIO.IN, pull_up_down=GPIO.PUD_UP)
  GPIO.setup(REPEAT, GPIO.IN, pull_up_down=GPIO.PUD_UP)

  # Initialise display
  lcd_init()
  # Initialize the MPC database
  init()
  #buttoncontrol()
  cmd = 'mpc status'
  a=0
  foo = 0
  time.sleep(1)
  while True:
      args = shlex.split(cmd)
      output = subprocess.Popen(args,stdout = subprocess.PIPE, shell = True)
      if a==0: #16 chars
        i=1
        while i<3:
            nextline = output.stdout.readline()
            if nextline == '' and output.poll() != None:
                break
            else:
                if i==1:
                    if nextline.__len__() < 33: #more than 1 row
                        foo = 3
                    elif nextline.__len__() < 49: #more than 2 rows
                        foo = 2
                    elif nextline.__len__() < 65: #more than 3 rows
                        foo = 1
                    else:
                        lcd_byte(LCD_LINE_1, LCD_CMD)
                        lcd_string(nextline[:15])
                        print(nextline[:15])

                    lcd_byte(LCD_LINE_1, LCD_CMD)
                    lcd_string(nextline)
                else:
                    nextline = nextline[17:26]
                    lcd_byte(LCD_LINE_2, LCD_CMD)
                    lcd_string(nextline)
            i=i+1
        output.communicate()
        foo = 1
      if a==1: #32 chars
        args = shlex.split(cmd)
        output = subprocess.Popen(args,stdout = subprocess.PIPE, shell = True)
        i=1
        while i<3:
            nextline = output.stdout.readline()
            if nextline == '' and output.poll() != None:
                break
            else:
                if i==1:
                    lcd_byte(LCD_LINE_1, LCD_CMD)
                    lcd_string(nextline[17:])
                else:
                    nextline = nextline[17:26]
                    lcd_byte(LCD_LINE_2, LCD_CMD)
                    lcd_string(nextline)
                i=i+1
        foo = 2
        output.communicate()

      if a==2: #48 chars
        args = shlex.split(cmd)
        output = subprocess.Popen(args,stdout = subprocess.PIPE, shell = True)
        i=1
        while i<3:
            nextline = output.stdout.readline()
            if nextline == '' and output.poll() != None:
                break
            else:
                if i==1:
                    lcd_byte(LCD_LINE_1, LCD_CMD)
                    lcd_string(nextline[33:])
                else:
                    nextline = nextline[17:26]
                    lcd_byte(LCD_LINE_2, LCD_CMD)
                    lcd_string(nextline)
                i=i+1
        foo = 3
        output.communicate()
      if a==3: #64 chars
        args = shlex.split(cmd)
        output = subprocess.Popen(args,stdout = subprocess.PIPE, shell = True)
        i=1
        while i<3:
            nextline = output.stdout.readline()
            if nextline == '' and output.poll() != None:
                break
            else:
                if i==1:
                    lcd_byte(LCD_LINE_1, LCD_CMD)
                    lcd_string(nextline[49:])
                else:
                    nextline = nextline[17:26]
                    lcd_byte(LCD_LINE_2, LCD_CMD)
                    lcd_string(nextline)
                i=i+1
        foo = 0
        output.communicate()
      if foo >= 1:
         a = foo
      else:
         a = 0
      buttoncontrol()
      time.sleep(1)


def lcd_init():
  # Initialise display
  lcd_byte(0x33,LCD_CMD)
  lcd_byte(0x32,LCD_CMD)
  lcd_byte(0x28,LCD_CMD)
  lcd_byte(0x0C,LCD_CMD)
  lcd_byte(0x06,LCD_CMD)
  lcd_byte(0x01,LCD_CMD)

def lcd_string(message):
  # Send string to display

  message = message.ljust(LCD_WIDTH," ")

  for i in range(LCD_WIDTH):
    lcd_byte(ord(message[i]),LCD_CHR)

def lcd_byte(bits, mode):
  # Send byte to data pins
  # bits = data
  # mode = True  for character
  #        False for command

  GPIO.output(LCD_RS, mode) # RS

  # High bits
  GPIO.output(LCD_D4, False)
  GPIO.output(LCD_D5, False)
  GPIO.output(LCD_D6, False)
  GPIO.output(LCD_D7, False)
  if bits&0x10==0x10:
    GPIO.output(LCD_D4, True)
  if bits&0x20==0x20:
    GPIO.output(LCD_D5, True)
  if bits&0x40==0x40:
    GPIO.output(LCD_D6, True)
  if bits&0x80==0x80:
    GPIO.output(LCD_D7, True)

  # Toggle 'Enable' pin
  time.sleep(E_DELAY)
  GPIO.output(LCD_E, True)
  time.sleep(E_PULSE)
  GPIO.output(LCD_E, False)
  time.sleep(E_DELAY)

  # Low bits
  GPIO.output(LCD_D4, False)
  GPIO.output(LCD_D5, False)
  GPIO.output(LCD_D6, False)
  GPIO.output(LCD_D7, False)
  if bits&0x01==0x01:
    GPIO.output(LCD_D4, True)
  if bits&0x02==0x02:
    GPIO.output(LCD_D5, True)
  if bits&0x04==0x04:
    GPIO.output(LCD_D6, True)
  if bits&0x08==0x08:
    GPIO.output(LCD_D7, True)

  # Toggle 'Enable' pin
  time.sleep(E_DELAY)
  GPIO.output(LCD_E, True)
  time.sleep(E_PULSE)
  GPIO.output(LCD_E, False)
  time.sleep(E_DELAY)

def init(): #update and addAll does't work
    sec = 5
    update = 'mpc update'
    argsUpdate = shlex.split(update)
    addAll = 'mpc ls | mpc add'
    argsAddAll = shlex.split(addAll)
    while sec>0:
        #subprocess.call(argsUpdate)
        lcd_byte(LCD_LINE_1, LCD_CMD)
        lcd_string("Starting up...")
        lcd_byte(LCD_LINE_2, LCD_CMD)
        lcd_string("%s Seconds left" % sec)
        time.sleep(1)
        sec=sec-1
    lcd_byte(LCD_LINE_2, LCD_CMD)
    lcd_string("Almost done...")
    #subprocess.call(argsAddAll)
    time.sleep(5)
    lcd_byte(LCD_LINE_1, LCD_CMD)
    lcd_string("PiPod says")
    lcd_byte(LCD_LINE_2, LCD_CMD)
    lcd_string("Hello!")
    time.sleep(1)
def buttoncontrol():
  prev_input = 0
  next_input = 0
  play_input = 0
  repeat_input = 0
  play = 1
  input1 = GPIO.input(PREV)
  if (not prev_input) and input:
    print("Button PREV pressed")
    cmd = "mpc prev"
    args = shlex.split(cmd)
    subprocess.Popen(args, shell = True)
  prev_input = input1
  time.sleep(0.05)
  input2 = GPIO.input(NEXT)
  if (not next_input) and input:
    print("Button NEXT pressed")
    cmd = "mpc next"
    args = shlex.split(cmd)
    subprocess.Popen(args, shell = True)
  next_input = input2
  time.sleep(0.05)
  input3 = GPIO.input(PLAY)
  if (not play_input) and input:
    print("Button PLAY pressed")
    if (play == 1 ):
        cmd = "mpc pause"
        args = shlex.split(cmd)
        subprocess.Popen(args, shell = True)
    else:
        cmd = "mpc play"
        args = shlex.split(cmd)
        subprocess.Popen(args, shell = True)
  play_input = input3
  time.sleep(0.05)
  input4 = GPIO.input(REPEAT)
  if ((not repeat_input) and input):
    print("Button REPEAT pressed")
    cmd = "mpc repeat"
    args = shlex.split(cmd)
    subprocess.Popen(args, shell = True)
  repeat_input = input4
  time.sleep(0.05)
  print("HEY I'M A BUTTON")
#
if __name__ == '__main__':
  main()