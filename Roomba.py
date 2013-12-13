class Roomba:

    baud_dict = {300:"0", 600:"1", 1200:"2", 2400:"3", 4800:"4", 9600:"5", 144000:"6", 19200:"7", 28800:"8", 38400:"9", 57600:"10", 115200:"11"}
    motor_dict = {"main":2, "vacuum":1, "side":0}
    def __init__(self):
        pass

    def open_serial_port(self, port):
        self.serial = open(port, "rw")

    def set_off_mode(self):
        pass

    def set_safe_mode(self):
        self.serial.write("131")

    def set_full_mode(self):
        self.serial.write("132")

    def set_passive_mode(self):
        pass

    def start(self):
        self.serial.write("128")

    def set_baud(self, baud):
        self.serial.write("129")
        self.serial.write(self.baud_dict[baud])

    def sleep(self):
        self.serial.write("133")

    def wake(self):
        """
        hold device detect low for 500ms wake roomba up
        not sure how to do this right now
        """
        pass

    def spot_clean(self):
        self.serial.write("134")

    def clean(self):
        self.serial.write("135")

    def max_clean(self):
        self.serial.write("136")

    def drive(self, speed, turn):
        """
        speed is in mm/s
        turn is radius in mm
        """
        pass

    def cleaning(self, motor):
        """
        Options are:
          "main" for the main brushes below
          "vacuum" for the sucking power
          "side" for the baseboard brush thingy on the side
        """
        self.serial.write("138")
        self.serial.write(self.motor_dict[motor])

    #def leds(self, led, color, intensity):
        #self.serial.write("139")

    def sensor(self, sensor):
        self.serial.write("142")
        self.serial.write(self.sensors[sensor])
        
