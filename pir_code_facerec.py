import RPi.GPIO as GPIO
import time
import tkinter as tk
import os

# Setup board pin numbering
GPIO.setmode(GPIO.BCM)

# Setup PIR pin output
GPIO.setup(22, GPIO.IN)  # PIR sensor connected to pin 22

# --- functions ---

# Function to start recognition script
def startface():
     os.system('python rec_ser_img.py')


# Start PIR sensor detection
def pirsensor():
    try:
        print('Setting alarm')
        time.sleep(2)  # Stabilze sensor
        print('Alarm active')
        while True:
            if GPIO.input(22):
                print ('Start code input')
                time.sleep(1)
                root.mainloop()
    except:
        GPIO.cleanup()

def code(value):

    # inform function to use external/global variable
    global pin

    if value == '*':
        # remove last number from `pin`
        pin = pin[:-1]
        # remove all from `entry` and put new `pin`
        e.delete('0', 'end')
        e.insert('end', pin)

    elif value == '#':
        # check pin

        if pin == "1234":
            startface()
        else:
            print("PIN ERROR!", pin)
            # clear `pin`
            pin = ''
            # clear `entry`
            e.delete('0', 'end')

    else:
        # add number to pin
        pin += value
        # add number to `entry`
        e.insert('end', value)

    print("Current:", pin)

# --- main ---

# PIR detection
pirsensor()

keys = [
    ['1', '2', '3'],
    ['4', '5', '6'],
    ['7', '8', '9'],
    ['*', '0', '#'],
]

# create global variable for pin
pin = '' # empty string

root = tk.Tk()
root.wm_attributes('-fullscreen','true')

panel = tk.PanedWindow(root)
panel.pack(fill='both', expand=1)

# place to display pin
e = tk.Entry(panel)
e.grid(row=0, column=0, columnspan=3, ipady=5)

# create buttons using `keys`
for y, row in enumerate(keys, 1):
    for x, key in enumerate(row):
        # `lambda` inside `for` has to use `val=key:code(val)`
        # instead of direct `code(key)`
        b = tk.Button(panel, text=key, command=lambda val=key:code(val))
        b.grid(row=y, column=x, ipadx=10, ipady=10)

# Exit full screen
root.bind("<Escape>", lambda event:root.destory())

root.mainloop()
