#@author Adam Claassen
#All functions are as defined by http://www.irobot.com/images/consumer/hacker/Roomba_SCI_Spec_Manual.pdf
#Retrived in December 2013

import serial as pyserial
class Roomba:

    baud_dict = {300:"0", 600:"1", 1200:"2", 2400:"3", 4800:"4", 9600:"5", 144000:"6", 19200:"7", 28800:"8", 38400:"9", 57600:"10", 115200:"11"}
    motor_dict = {"main":2, "vacuum":1, "side":0}
    def __init__(self, test = false):
        """
        generate a new instance of the class
        """
        self.test = test
        self.led = [0,255,1,0,0,0]

    def open_serial_port(self, port, baudrate = 19200, timeout = 0.1):
        """
        open a serial port with the default settings from the SCI manual
        or specify baudrate and/or timeout with keyword args
        """
        if not self.test:
          self.serial = pyserial.Serial(port, baudrate, timeout)
        else:
          self.serial = open("testlog.log", 'w')
    

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

    def drive(self, speed = 0, turn = 0, case = 0):
        """
        Drive Roomba
        speed is in mm/s
        turn is radius in mm, - left + right
        if you don't set case, then speed and turn work normally
        if you set case to "straight", "ccw", or "cw" use kwargs for speed
        """
        if case == 0:
            drive_bytes = []
            drive_bytes += self.get_drive_output(speed)
            drive_bytes += self.get_drive_output(turn)
            self.serial.write("137")
            self.serial.write((drive_bytes[0]))
            self.serial.write((drive_bytes[1]))
            self.serial.write((drive_bytes[2]))
            self.serial.write((drive_bytes[3]))

        if case == "straight":
            self.serial.write("137")
            self.serial.write((self.get_drive_output(speed)[0]))
            self.serial.write((self.get_drive_output(speed)[1]))

        if case == "ccw":
            self.serial.write("137")
            self.serial.write((self.get_drive_output(speed)[0]))
            self.serial.write((self.get_drive_output(speed)[1]))
            self.serial.write((self.get_drive_output(1)[0]))
            self.serial.write((self.get_drive_output(1)[1]))

        if case == "cw":
            self.serial.write("137")
            self.serial.write(self.get_drive_output(speed)[0])
            self.serial.write(self.get_drive_output(speed)[1])
            self.serial.write(self.get_drive_output(-1)[0])
            self.serial.write(self.get_drive_output(-1)[1])

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

    def leds(self, p_color = self.led[0], p_intensity = self.led[1], status = self.led[2], spot = self.led[3], clean = self.led[4], clean_max = self.led[5]):
        """
        do things with leds
        use this with kwargs, it will store your previous values
        p_color: 0-255 Green-Red (default 0)
        p_intensity: 0-255 off-on (default 255)
        status: 10 red 01 green 11 amber 00 off (default 1)
        spot, clean, max_clean: 1 on 0 off (default 0)
        set defaults in self.led in __init__
        """
        self.led[0] = p_color
        self.led[1] = p_intensity
        self.led[2] = status
        self.led[3] = spot
        self.led[4] = clean
        self.led[5] = clean_max
        self.serial.write("139")
        bits = str(status) + str(spot) + str(clean) + str(clean_max)
        bits = int(bits, 2)
        self.serial.write(str(bits))
        self.serial.write(str(p_color))
        self.serial.write(str(p_intensity))

    def sensor(self, sensor):
        """
        read from sensors on the Roomba
        """
        self.serial.write("142")
        self.serial.write(self.sensors[sensor])

  
    def get_drive_output(self, value):
        byte0_out = ''
        value = input("Value: ")
        value = int(value)

        byte0 = bin(value)
        byte0 = byte0[2:]
        byte0 = byte0.zfill(16)
        byte1 = byte0[:8]
        byte2 = byte0[8:]

        if value >= 0:
            return [str(int(byte1, 2)), str(int(byte2, 2))]

        else:
            for i in range(len(byte0)):
                if byte0[i] == "1":
                    byte0_out += "0"
                else:
                    byte0_out += "1"

            byte0 = "0b" + byte0_out
            byte0 = bin(int(byte0, 2) + 1)
            byte1 = byte0[2:10]
            byte2 = byte0[10:]
            return [str(int(byte1, 2)), str(int(byte2, 2))]


        
