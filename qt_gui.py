import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui

class UserInterface:
    def __init__(self):
        self.app = QtGui.QApplication([])
        self.view = pg.GraphicsView()
        self.layout = pg.GraphicsLayout(border=(100, 100, 100))
        self.view.setCentralItem(self.layout)
        self.view.show()
        self.view.setWindowTitle('Visualization Demo')
        self.view.resize(800, 600)
        # create bar plot
        self.bar_plot = self.layout.addPlot(title='Microphone Level', colspan=3)
        self.bg = pg.BarGraphItem(x=[0], height=[0], width=0.3, brush='g')
        self.bar_plot.addItem(self.bg)

    def graph_update(self, vol):
        self.bar_plot.clear()
        bg = pg.BarGraphItem(x=[0], height=vol, width=0.3, brush='g')
        self.bar_plot.addItem(bg)
        self.app.processEvents()
