from ps4_control import PS4Controller
from i2c_com import I2CCom
from radio_control import RadioControl

from static import I2C_INTERFACE
from static import EVENT_FORMAT
from static import SUDOPASSWORD
from static import SHUTDOWNCOMMAND
from static import RASPIVIDCOMMAND

from subprocess import call
import threading
import subprocess
import os
from raspivid import RaspiVidController
import time
import sys

def main():

    # create raspivid controller
    #vidcontrol = RaspiVidController("/home/pi/test.h264", 10000, False, ["-fps", "25"])
    vidcontrol = RaspiVidController("/home/pi/test", 10000, 1280, 720, True)

    try:
        print("Starting raspivid controller")
        # start up raspivid controller
        vidcontrol.start()
        # wait for it to finish
        while (vidcontrol.isAlive()):
            time.sleep(0.5)

    # Ctrl C
    except KeyboardInterrupt:
        print("Cancelled")

    # Error
    except:
        print("Unexpected error:", sys.exc_info()[0])

        raise

    # if it finishes or Ctrl C, shut it down
    finally:
        print("Stopping raspivid controller")
        # stop the controller
        vidcontrol.stopController()
        # wait for the tread to finish if it hasn't already
        vidcontrol.join()

    print("Done")

######################################################################################################
######################################################################################################


def main2():

    i2c_timeout = 0.1

    ps4_controller = PS4Controller(interface=I2C_INTERFACE, connecting_using_ds4drv=False,
                                   event_format=EVENT_FORMAT)

    ps4_controller.start()

    i2c_com = I2CCom()

    radio_controller = RadioControl()

    vidcontrol = RaspiVidController("/home/pi/test2", 10000, 1280, 720, True)


    while True:

        _, radio_send_string = radio_controller.convert_radio_raw_data_to_send_string(ps4_controller.button_id,
                                                                                      ps4_controller.l3_x,
                                                                                      ps4_controller.l3_y,
                                                                                      ps4_controller.r3_x,
                                                                                      ps4_controller.r3_y,
                                                                                      ps4_controller.ps_button_pushed)
        i2c_com.send_data_to_slave(radio_send_string, i2c_timeout)

        i2c_com.log_data("[Radio-data] ", radio_send_string)

        #tmp_array = i2c_com.read_data_from_i2c()

        #i2c_com.log_data("[MasterControl receiving] ", tmp_array)

        if ps4_controller.button_id == 1:
            vidcontrol = RaspiVidController("/home/pi/capture", 300000, 1280, 720, True)
            vidcontrol.start()
            ps4_controller.reset_button_id()
        elif ps4_controller.button_id == 4:
            vidcontrol = RaspiVidController("/home/pi/capture", 0, 1280, 720, True)
            vidcontrol.start()
            #call(["pkill raspivid"], shell=True)
            ps4_controller.reset_button_id()

        # if ps4_controller.get_ps_button() == True:
        #     os.system('echo %s|sudo -S %s' % (SUDOPASSWORD, SHUTDOWNCOMMAND))
        # else:
        #     continue



if __name__ == '__main__':
    main2()
