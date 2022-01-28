import os

SUDOPASSWORD = '2207'
SHUTDOWNCOMMAND = 'shutdown now'
RASPIVIDCOMMAND = 'raspivid -t 0 -w 1280 -h 720'

IC2_BRIDGE_ADDRESS = 0x05

I2C_INTERFACE = "/dev/input/js0"
EVENT_FORMAT = "3Bh2b"

PS4_CONTROLLER_STICK_THRESH = 0.2

MOTOR_MAX_SPEED = 200
STICK_NORMALIZE = 255

RADIO_DATA_COUNT = 8

# DATA LAYOUT
# 0 = direction M1
# 1 = direction M2
# 2 = speed M1  (left stick values)
# 3 = speed M2  (left stick values)
# 4 = buttons (values) 1 = cross, 2 = square, 3 = triangle, 4 = circle
# 5 = right stick x_values
# 6 = right stick y_values
# 7 = PS button


START_MARKER = '<'
END_MARKER = '>'
SEPERATOR = ':'

DATA_IDENT_MC = 1   # Motor-Control
DATA_IDENT_SS = 2   # Sonar-Sensor
