__author__ = 'Anti'
import Tkinter
import ScrolledText
import ControllableWindow


class ExtractionWindow(ControllableWindow.ControllableWindow):
    def __init__(self, title):
        ControllableWindow.ControllableWindow.__init__(self, title, 525, 200)
        self.canvas = ScrolledText.ScrolledText(self)
        self.canvas.pack()
        self.freq_points = None
        self.freq_indexes = None
        self.recorded_signals = None
        self.connection = None
        self.headset_freq = 128

    def resetCanvas(self):
        self.canvas.insert(Tkinter.END, "Starting\n")

    def setup(self, options, sensor_names, window_function, filter_coefficients, freq_points=None, recorded_signal=None, connection=None):
        self.freq_points = freq_points
        self.freq_indexes = []
        self.recorded_signals = recorded_signal
        self.connection = connection
        ControllableWindow.ControllableWindow.setup(self, options, sensor_names, window_function, filter_coefficients)