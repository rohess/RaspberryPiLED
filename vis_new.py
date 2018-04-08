#
# main file for LED strip gain display
#
import numpy as np
import config
from qt_gui import UserInterface
from audio import Microphone
if config.USE_GUI:
    import pyqtgraph as pg
    from pyqtgraph.Qt import QtCore, QtGui
if config.USE_LED:
    import RPi.GPIO as GPIO
    import Adafruit_WS2801
    import Adafruit_GPIO.SPI as SPI


def microphone_update(audio_samples):
    # Normalize samples between 0 and 1 (16 bit value gets divided by 2^15)
    y_data = audio_samples / 2.0 ** 15
    # Find the maximum of the absolute values of our samples - this is our volume value
    vol = np.max(np.abs(y_data))
    if config.DEBUG:
        print(str(vol))
    if config.USE_LED:
        update_led-strip(vol)
    if config.USE_GUI:
        ui.graph_update(vol)
        ui.process_events()


def update_led_strip(vol):
    # This routine sends output to the LED Strip
    # input is the mic level between 0 and 1
    # We set the colors, judging by the sounds' "position" on the strip.
    # If vol is not loud enough it will not be displayed for stability reasons.
    if ((vol * 310) // 10) > 4:
        for k in np.arange((vol * 310) // 10, dtype=np.int16):
            if k < 20:
                color1 = (0, 255, 0)
            elif k < 28:
                color1 = (0, 255, 255)
            else:
                color1 = (0, 0, 255)
            if config.DEBUG:
                print('color: ', color1, k, vol)
            pixels.set_pixel(k, Adafruit_WS2801.RGB_to_color(color1[0], color1[1], color1[2]))

    for z in np.arange((vol * 310) // 10, 32, dtype=np.int16):
        color1 = (0, 0, 0)
        if config.DEBUG:
            print('color: ', color1, z, vol)
        pixels.set_pixel(z, Adafruit_WS2801.RGB_to_color(color1[0], color1[1], color1[2]))
    pixels.show()

if __name__ == '__main__':
    # Creates GUI window if the user chooses to do so
    if config.USE_GUI:
        ui = UserInterface()
    if config.USE_LED:
        # Initialize LEDs and set to red
        SPI_PORT = 0
        SPI_DEVICE = 0
        PIXEL_COUNT = 32
        pixels = Adafruit_WS2801.WS2801Pixels(PIXEL_COUNT, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE), gpio=GPIO)
        pixels.clear()
        color = (0, 0, 255)
        for i in range(32):
            pixels.set_pixel(i, Adafruit_WS2801.RGB_to_color(color[0], color[1], color[2]))
        pixels.show()

    # Start listening to live audio stream
    mic = Microphone()
    try:
        mic.start_stream(microphone_update)
    except KeyboardInterrupt:
        pass