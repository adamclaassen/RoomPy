#@author Adam Claassen
#All functions are as defined by http://www.irobot.com/images/consumer/hacker/Roomba_SCI_Spec_Manual.pdf
#Retrived in December 2013

import serial as pyserial
class Roomba:

    baud_dict = {300:"0", 600:"1", 1200:"2", 2400:"3", 4800:"4", 9600:"5", 144000:"6", 19200:"7", 28800:"8", 38400:"9", 57600:"10", 115200:"11"}
    motor_dict = {"main":2, "vacuum":1, "side":0}
    def __init__(self):
        """
        generate a new instance of the class
        """
        pass

    def open_serial_port(self, port, baudrate = 19200, timeout = 0.1):
        """
        open a serial port with the default settings from the SCI manual
        or specify baudrate and/or timeout with keyword args
        """
        self.serial = pyserial.Serial(port, baudrate, timeout)
    

    def set_off_mode(self):
        """
        turns the Roomba to off mode
        """
        pass

    def set_safe_mode(self):
        """
        set Roomba to safe mode
        """
        self.serial.write("131")

    def set_full_mode(self):
        """
        set Roomba to full mode
        """
        self.serial.write("132")

    def set_passive_mode(self):
        """
        set Roomba to passive mode
        """
        pass

    def start(self):
        """
        start SCI listening on Roomba
        """
        self.serial.write("128")

    def set_baud(self, baud):
        """
        change baudrate of Roomba
        """
        self.serial.write("129")
        self.serial.write(self.baud_dict[baud])

    def sleep(self):
        """
        put Roomba to sleep
        """
        self.serial.write("133")

    def wake(self):
        """
        hold device detect low for 500ms wake roomba up
        not sure how to do this right now
        """
        pass

    def spot_clean(self):
        """
        start spot cleaning
        """
        self.serial.write("134")

    def clean(self):
        """
        start normal cleaning
        """
        self.serial.write("135")

    def max_clean(self):
        """
        start max cleaning
        """
        self.serial.write("136")

    def drive(self, speed, turn):
        """
        drive Roomba
        speed is in mm/s
        turn is radius in mm
        """
        drive_bytes = []
        drive_bytes += self.get_drive_output(speed)
        drive_bytes += self.get_drive_output(turn)
        self.serial.write("137")
        self.serial.write(str(drive_bytes[0]))
        self.serial.write(str(drive_bytes[1]))
        self.serial.write(str(drive_bytes[2]))
        self.serial.write(str(drive_bytes[3]))

    def drive_straight(self, speed):
        """
        drive straight forewards at speed
        """
        drive_bytes = []
        drive_bytes += self.get_drive_output(speed)
        self.serial.write("137")
        self.serial.write(str(drive_bytes[0]))
        self.serial.write(str(drive_bytes[1]))
        self.serial.write("128")
        self.serial.write("000")

    def turn_clockwise(self, speed):
        """
        turn clockwise (at speed?)
        does this work if you write "-1" directly
        or if you hash -1 through get_drive_output
        """
        pass

    def turn_counterclockwise(self, speed):
        """
        turn counterclockwise (at speed?)
        see above
        """
        pass

    def cleaning(self, motor):
        """
        start cleaning motors
        Options are:
          "main" for the main brushes below
          "vacuum" for the sucking power
          "side" for the baseboard brush thingy on the side
        """
        self.serial.write("138")
        self.serial.write(self.motor_dict[motor])

    def leds(self, p_color, p_intensity, status = 0, spot = 0, clean = 0, clean_max = 0):
        """
        do things with leds
        p_color: 0-255 Green-Red
        p_intensity: 0-255 off-on
        status: 10 red 01 green 11 amber 00 off
        spot, clean, max_clean: 1 on 0 off
        """
        self.serial.write("139")
        bits = str(status) + str(spot) + str(clean) + str(clean_max)
        bits = int(bits, 2)
        self.serial.write(str(bits))
        self.serial.write(str(

    def sensor(self, sensor):
        """
        read from sensors on the Roomba
        """
        self.serial.write("142")
        self.serial.write(self.sensors[sensor])

    def get_drive_output(self, value):
        """
        private function for turning mm/s drive speed or mm turn radius into properly formatted bytes for the roomba
        """
        if value >= 0:
            value = hex(value)
            value = value[2:].zfill(4)
            byte1 = value[:1]
            byte2 = value[2:]
            byte1 = int(byte1, 16)
            byte2 = int(byte2, 16)
            return [byte1, byte2]

        if value < 0:
            value = bin(value)
            value = value[2:].zfill(16)
            twos = ''
            for bit in value:
                if bit == '0': 
                    twos += '1'
                if bit == '1':
                    twos += '0'

            twos = '0b' + twos
            twos = int(twos, 2)
            hexed = hex(twos)
            byte1 = hexed[2:3]
            byte2 = hexed[4:5]
            byte1 = int(byte1, 16)
            byte2 = int(byte2, 16)
            return [byte1, byte2]
        
        
