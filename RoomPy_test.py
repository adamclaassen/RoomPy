#@author Adam Claassen

import RoomPy
import time
rp = RoomPy(test = true)

rp.open_serial_port("/dev/ttyUSB0")
rp.start()
rp.set_safe_mode()
rp.leds(status = 10)
rp.spot_clean()
rp.drive_straight()
time.sleep(1)
rp.drive(0, 0)
rp.turn_clockwise()
time.sleep(2)
rp.drive(0,0)
rp.leds(status = 1)
