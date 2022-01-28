import threading
import time
from pyPS4Controller.controller import Controller


class MyController(Controller):
    def __init__(self, **kwargs):
        Controller.__init__(self, **kwargs)
        self.scale = 32767
        self.l3_x = 0.0
        self.l3_y = 0.0
        self.r3_x = 0.0
        self.r3_y = 0.0
        self.button_id = 0

    def start(self):
        self.start_thread = threading.Thread(target=self.run, args=())
        self.start_thread.daemon = True  # Daemonize thread
        self.start_thread.start()

    # Auto setup connection and start thread and stuff

    def run(self):
        while True:
            self.listen()
            self.stop_motion()
            print('listen exit, should not happen')
            time.sleep(1)

    def stop_motion(self):
        self.l3_x = 0.0
        self.l3_y = 0.0
        self.r3_x = 0.0
        self.r3_y = 0.0

    def on_connect_callback(self):
        super()
        print('Hoi on_connect_callback event')

    def on_disconnect_callback(self):
        print('Hoi on disconnect event')

    def on_L3_up(self, value):
        self.l3_y = value / -self.scale

    def on_L3_down(self, value):
        self.l3_y = value / -self.scale

    def on_L3_left(self, value):
        self.l3_x = value / self.scale

    def on_L3_right(self, value):
        self.l3_x = value / self.scale

    def on_R3_up(self, value):
        self.r3_y = value / -self.scale

    def on_R3_down(self, value):
        self.r3_y = value / -self.scale

    def on_R3_left(self, value):
        self.r3_x = value / self.scale

    def on_R3_right(self, value):
        self.r3_x = value / self.scale

    # bug in the modul  square = x,
    #                   triangle = square
    #                   circle = triangle
    #                   x = square

    def on_x_press(self):
        self.button_id = 4

    def on_x_release(self):
        self.button_id = 0

    def on_triangle_press(self):
        self.button_id = 2

    def on_triangle_release(self):
        self.button_id = 0

    def on_circle_press(self):
        self.button_id = 3

    def on_circle_release(self):
        self.button_id = 0

    def on_square_press(self):
        self.button_id = 1

    def on_square_release(self):
        self.button_id = 0


# controller = MyController(interface="/dev/input/js0", connecting_using_ds4drv=False, event_format="3Bh2b")
# controller.start()
#
# while True:
#     print(f'l3_x: {controller.l3_x:.2f} l3_y: {controller.l3_y:.2f} r3_x: {controller.r3_x:.2f} r3_y: {controller.r3_y:.2f}')
#
#     time.sleep(0.5)
