This is a very simple project to experiment with controlling Adafruit_WS2801 LED strips from a Raspberry Pi.
For convenience, there is also a mode you can run on a (Windows) PC without the WS2801 and RasPi libraries.

We use three classes to abstract the led strip, the handling of the microphone and the QT gui
If required, the main function will create objects for all three classes, the use of the U and the Led strip can be disabled via config.
The LED Strip will only run on a Raspberry Pi

Todo
- mock the RASPI and Adafruit_WS2801 specific functions to be able to test these parts on PC too.
- build tests for the audio and UI parts
- make the system more robust for different parameters, i.e. different i/o config due to other sound devices

Files
config.py - config data
raspberry_py_led.py -