#
# main file for LED strip gain display
#
import pyaudio
import numpy as np
import config
import microphone
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
    if config.USE_GUI:
        update_bar_graph(vol)
    if config.USE_GUI:
        graph_update(vol)
        app.processEvents()


def graph_update(vol):
    global bg1
    bar_plot.clear()
    bg1 = pg.BarGraphItem(x=[0], height=vol, width=0.3, brush='g')
    bar_plot.addItem(bg1)


def update_bar_graph(vol):
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


def init_gui():
    app1 = QtGui.QApplication([])
    view1 = pg.GraphicsView()
    layout1 = pg.GraphicsLayout(border=(100, 100, 100))
    view1.setCentralItem(layout1)
    view1.show()
    view1.setWindowTitle('Visualization Demo')
    view1.resize(800, 600)
    # create bar plot
    bar_plot1 = layout1.addPlot(title='Microphone Level', colspan=3)
    bg = pg.BarGraphItem(x=[0], height=[0], width=0.3, brush='g')
    bar_plot1.addItem(bg)
    return app1, bg, bar_plot1


if __name__ == '__main__':
    # Creates GUI window if the user chooses to do so
    bg1 = None
    app = None
    bar_plot = None
    print(config.USE_GUI)
    if config.USE_GUI:
        app = QtGui.QApplication([])
        view = pg.GraphicsView()
        layout = pg.GraphicsLayout(border=(100, 100, 100))
        view.setCentralItem(layout)
        view.show()
        view.setWindowTitle('Visualization Demo')
        view.resize(800, 600)
        # create bar plot
        bar_plot = layout.addPlot(title='Microphone Level', colspan=3)
        bg1 = pg.BarGraphItem(x=[0], height=[0], width=0.3, brush='g')
        bar_plot.addItem(bg1)
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
    p = pyaudio.PyAudio()
    info = p.get_host_api_info_by_index(0)
    num_devices = info.get('deviceCount')
    for i in range(0, num_devices):
        if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
            print("Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name'))

    # Start listening to live audio stream
    microphone.start_stream(microphone_update)
