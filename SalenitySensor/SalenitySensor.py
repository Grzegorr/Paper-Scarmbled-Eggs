import serial
import numpy as np
import time



class SolenitySensor:

    def __init__(self, no_read):
        self.no_readings = no_read
        self.ser = serial.Serial(port='COM5', baudrate=9600, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=10)
        print("I am connected.")
        self.current_measurements = np.full(self.no_readings, np.inf)

    def readDataLine(self):

        self.ser.flushOutput()
        self.ser.flushInput()
        time.sleep(1)

        #Synchronize
        while True:
            bit = self.ser.read(1)
            #print(bit)
            if bit == b'\n':
                print("Synchronized")
                break

        line = self.ser.read(18)
        string = ""
        for i in line:
            j = chr(int(i))
            string = string + j
        print(string)
        splits = string.split()
        splits = splits[1].split(':')
        splits = splits[1].split('/')
        number_str = splits[0][0:-2]
        #print(number_str)
        reading = float(number_str)
        #print(reading)
        return reading

    def getNextReading(self):
        next_index = (self.current_measurements == np.inf).argmax(axis=0)
        print("Next Index: " + str(next_index))
        dataLine = self.readDataLine()
        self.current_measurements[next_index] = dataLine
        print(self.current_measurements)

    def resetData(self):
        self.current_measurements = np.full(self.no_readings, np.inf)

    def returnData(self):
        return self.current_measurements

if __name__ == '__main__':
    SALT = SolenitySensor(20)
    while True:
        SALT.getNextReading()
        time.sleep(3)



