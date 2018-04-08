#
# raspberry_pi_led.py
# main file for LED strip microphone gain level display
#
import numpy as np
import config as cnf
from qt_gui import UserInterface
from audio import Microphone
from led_strip import LEDStrip


def microphone_update(audio_samples):
    """ function calculates volume values between 0 and 1 to use for display
    calls UI and LED update according to config"""
    # Normalize samples between 0 and 1 (16 bit value gets divided by 2^15)
    y_data = audio_samples / 2.0 ** 15
    # Find the maximum of the absolute values of our samples - this is our volume value
    vol = np.max(np.abs(y_data))
    if cnf.DEBUG:
        print(str(vol))
    if cnf.USE_LED:
        led.update_led_strip(vol)
    if cnf.USE_GUI:
        ui.graph_update(vol)


if __name__ == '__main__':
    # Creates GUI window if the user chooses to do so
    if cnf.USE_GUI:
        ui = UserInterface()
    # creates LED object if so configured - this will also initialise the strip
    if cnf.USE_LED:
        led = LEDStrip()
    # creates pyaudio object and starts capturing samples from a live audio stream
    mic = Microphone()
    try:
        mic.start_stream(microphone_update)
    except KeyboardInterrupt:
        pass
