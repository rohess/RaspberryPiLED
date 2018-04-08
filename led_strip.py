import config as cnf
if cnf.USE_LED:
    import RPi.GPIO as gpio
    import Adafruit_WS2801 as ws
    import Adafruit_GPIO.SPI as spi
import numpy as np


class LEDStrip:
    def __init__(self):
        # Initialize LEDs and set to red
        self.pixels = ws.WS2801Pixels(cnf.N_PIXELS, spi_obj=spi.SpiDev(cnf.SPI_PORT, cnf.SPI_DEV), gpio_obj=spi)
        self.pixels.clear()
        color = (0, 0, 255)
        for i in range(32):
            self.pixels.set_pixel(i, ws.RGB_to_color(color[0], color[1], color[2]))
        self.pixels.show()

    def update_led_strip(self, vol):
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
                if cnf.DEBUG:
                    print('color: ', color1, k, vol)
                    self.pixels.set_pixel(k, ws.RGB_to_color(color1[0], color1[1], color1[2]))
        for z in np.arange((vol * 310) // 10, 32, dtype=np.int16):
            color1 = (0, 0, 0)
            if cnf.DEBUG:
                print('color: ', color1, z, vol)
                self.pixels.set_pixel(z, ws.RGB_to_color(color1[0], color1[1], color1[2]))
                self.pixels.show()
