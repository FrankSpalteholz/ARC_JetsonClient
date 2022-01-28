import numpy as np
from static import PS4_CONTROLLER_STICK_THRESH
from static import MOTOR_MAX_SPEED
from static import STICK_NORMALIZE
from static import START_MARKER
from static import END_MARKER
from static import SEPERATOR
from static import DATA_IDENT_MC
from static import RADIO_DATA_COUNT

class RadioControl:

    def __init__(self, **kwargs):
        self.ps4_controller_thresh = PS4_CONTROLLER_STICK_THRESH
        self.max_motor_speed = MOTOR_MAX_SPEED
        self.stick_normalize = STICK_NORMALIZE
        self.startmarker = START_MARKER
        self.endmarker = END_MARKER
        self.seperator = SEPERATOR
        self.data_ident_mc = DATA_IDENT_MC

    def convert_array_to_send_string(self, send_data):

        send_string = self.startmarker + self.seperator
        send_string += str(self.data_ident_mc) + self.seperator

        for i in range(send_data.size):
            send_string += str(int(send_data[i]))
            if i < send_data.size - 1:
                send_string += self.seperator
        send_string += self.endmarker

        return send_string

    def convert_radio_raw_data_to_send_string(self, button_id,
                                              raw_left_stick_x,
                                              raw_left_stick_y,
                                              raw_right_stick_x,
                                              raw_right_stick_y,
                                              ps_button_pushed):

        tmp_array = np.zeros((RADIO_DATA_COUNT,1))
        tmp_string = ""

        if raw_left_stick_x < 0 and raw_left_stick_x < -self.ps4_controller_thresh:
            tmp_array[0] = 1
            tmp_array[1] = -1
            for i in range(2):
                tmp_array[i + 2] = int(self.max_motor_speed * abs(raw_left_stick_x))

        if raw_left_stick_x > 0 and raw_left_stick_x > self.ps4_controller_thresh:
            tmp_array[0] = -1
            tmp_array[1] = 1
            for i in range(2):
                tmp_array[i + 2] = int(self.max_motor_speed * abs(raw_left_stick_x))

        if raw_left_stick_y < 0 and raw_left_stick_y < -self.ps4_controller_thresh:
            tmp_array[0] = -1
            tmp_array[1] = -1
            for i in range(2):
                tmp_array[i + 2] = int(self.max_motor_speed * abs(raw_left_stick_y))

        if raw_left_stick_y > 0 and raw_left_stick_y > self.ps4_controller_thresh:
            tmp_array[0] = 1
            tmp_array[1] = 1
            for i in range(2):
                tmp_array[i + 2] = int(self.max_motor_speed * abs(raw_left_stick_y))

        tmp_array[4] = button_id

        tmp_array[5] = int(self.stick_normalize * raw_right_stick_x)
        tmp_array[6] = int(self.stick_normalize * raw_right_stick_y)
        tmp_array[7] = ps_button_pushed


        #print(str(tmp_array))
        tmp_string = self.convert_array_to_send_string(tmp_array)

        return tmp_array, tmp_string