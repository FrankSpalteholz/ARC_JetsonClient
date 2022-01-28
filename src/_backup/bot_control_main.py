from ps4_control import PS4Controller
from i2c_com import I2CCom

from radio_control import RadioControl

from static import I2C_INTERFACE
from static import EVENT_FORMAT
from static import SUDOPASSWORD
from static import SHUTDOWNCOMMAND

import os, os.path
import threading
import pygame
import time

def music_player_thread(path):
    pygame.mixer.music.load(path)
    pygame.mixer.Sound(path).set_volume(1.0)
    pygame.mixer.music.play()
   # print("played song:" + path)

def music_welcome_player_thread(path):
    pygame.mixer.music.load(path)
    pygame.mixer.Sound(path).set_volume(1.0)
    pygame.mixer.music.play()
   # print("played song:" + path)


def main():

    i2c_timeout = 0.1

    ps4_controller = PS4Controller(interface=I2C_INTERFACE, connecting_using_ds4drv=False,
                                   event_format=EVENT_FORMAT)
    ps4_controller.start()

    i2c_com = I2CCom()

    radio_controller = RadioControl()

    ###############################################################################################

    pygame.mixer.init()


    # WIN
    #welcome_path = r'D:\dev\SpeedTurtleBot\src\music_samples\welcome.wav'
    #song_folder_path = r'D:\dev\SpeedTurtleBot\src\music_samples\song_folder\\'

    # LINUX
    welcome_path = "/home/pi/_dev/SpeedTurtleBot/src/music_samples/welcome.wav"
    song_folder_path = "/home/pi/_dev/SpeedTurtleBot/src/music_samples/song_folder/"

    song_counter = 1
    path, dirs, files = next(os.walk(song_folder_path))
    song_num = len(files)

    is_music = False;

    music_thread = threading.Thread(target=music_welcome_player_thread, args=(welcome_path, ))
    music_thread.start()
    time.sleep(7)


    #################################################################################################

    while True:

        _, radio_send_string = radio_controller.convert_radio_raw_data_to_send_string(ps4_controller.button_id,
                                                                                      ps4_controller.l3_x,
                                                                                      ps4_controller.l3_y,
                                                                                      ps4_controller.r3_x,
                                                                                      ps4_controller.r3_y,
                                                                                      ps4_controller.get_ps_button())
        i2c_com.send_data_to_slave(radio_send_string, i2c_timeout)

        i2c_com.log_data("[Radio-data] ", radio_send_string)

        if ps4_controller.music_button_id == 3:
            pygame.mixer.music.stop()
            if is_music == True:
                is_music = False
            else:
                is_music = True
            ps4_controller.reset_music_button_id()

        if is_music == True:
            if ps4_controller.button_id == 2:
                pygame.mixer.music.stop()
                ps4_controller.reset_music_button_id()

            if pygame.mixer.music.get_busy():
                if ps4_controller.music_button_id == 2:
                    #print("stopping song")
                    pygame.mixer.music.stop()
                    if song_counter < song_num:
                        song_counter += 1
                    else:
                        song_counter = 1
                    ps4_controller.reset_music_button_id()
            else:
               #print("song finished")
                song_path = song_folder_path + str(song_counter) + ".wav"
                song_thread = threading.Thread(target=music_player_thread, args=(song_path,))
                song_thread.start()
                song_thread.join()
                if song_counter < song_num:
                    song_counter += 1
                else:
                    song_counter = 1


        # if ps4_controller.get_ps_button() == True:
        #     p = os.system('echo %s|sudo -S %s' % (SUDOPASSWORD, SHUTDOWNCOMMAND))
        # else:
        #     continue


if __name__ == '__main__':
    main()
