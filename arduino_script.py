import serial
import time
ser = serial.Serial('/dev/cu.usbmodem14201', 9600)
time.sleep(1)
def readarduino(ser):
    did=True
    while ser.inWaiting(): # Check number of characters left in buffer
        if did and ser.inWaiting() < 490: # Select last 500 characters in buffer
            for i in range(6):
                print(ser.readline()) # Print 6 lines in buffer
            did = False
        ser.readline()  # Clear buffer line by line until ser.inWaiting goes to 0
readarduino(ser)
data =[]                       # empty list to store the data
for i in range(50):
    b = ser.readline()         # read a byte string
    string_n = b.decode()  # decode byte string into Unicode  
    string = string_n.rstrip() # remove \n and \r
    # flt = float(string)        # convert string to float
    print(string)
    data.append(string)           # add to the end of data list
    time.sleep(0.1)            # wait (sleep) 0.1 seconds
readarduino(ser)
ser.close()


for line in data:
    print(line)