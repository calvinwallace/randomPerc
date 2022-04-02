from PyQt6.QtWidgets import *
from qtrangeslider import QRangeSlider
from PyQt6.QtCore import Qt
import sys
from perc_generator import Generator

rate = 44100
samples_dir = 'Samples'


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle('Perc-Generator')
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.create_layout()

    def create_layout(self):
        # Texteingabe
        self.text_label = QLabel('Text')
        self.layout.addWidget(self.text_label)

        self.text_widget = QTextEdit()
        self.layout.addWidget(self.text_widget)

        # Einstellungen
        self.settings_label = QLabel('Einstellungen')
        self.layout.addWidget(self.settings_label)

        self.settings_frame = QFrame()
        self.settings_frame.setFrameStyle(6)
        self.settings_layout = QHBoxLayout()
        self.settings_frame.setLayout(self.settings_layout)
        self.layout.addWidget(self.settings_frame)

        # Linke Seite mit Labels
        self.left_widget = QWidget()
        self.settings_layout.addWidget(self.left_widget)
        self.left_layout = QVBoxLayout()
        self.left_widget.setLayout(self.left_layout)

        self.left_layout.addWidget(QLabel('BPM'))
        self.left_layout.addWidget(QLabel('Zählzeit'))
        self.left_layout.addWidget(QLabel('Dynamik'))

        # Mitte mit Labels
        self.mid_widget = QWidget()
        self.settings_layout.addWidget(self.mid_widget)
        self.mid_layout = QVBoxLayout()
        self.mid_widget.setLayout(self.mid_layout)

        self.bpm = QSlider(Qt.Horizontal)
        self.mid_layout.addWidget(self.bpm)
        self.res = QSlider(Qt.Horizontal)
        self.mid_layout.addWidget(self.res)
        self.dyn = QRangeSlider(Qt.Horizontal)
        self.mid_layout.addWidget(self.dyn)

        # Rechte Seite mit aktuellen Werten
        self.right_widget = QWidget()
        self.settings_layout.addWidget(self.right_widget)
        self.right_layout = QVBoxLayout()
        self.right_widget.setLayout(self.right_layout)

        self.bpm_val = QLabel()
        self.right_layout.addWidget(self.bpm_val)
        self.res_val = QLabel()
        self.right_layout.addWidget(self.res_val)
        self.dyn_val = QLabel()
        self.right_layout.addWidget(self.dyn_val)

        # Button
        self.create_btn = QPushButton('Start')
        self.layout.addWidget(self.create_btn)


class Controller:
    def __init__(self):
        self.win = MainWindow()
        self.text = 'ABC'
        self.bpm = 90
        self.res = 1 / 32
        self.dyn_min = 1
        self.dyn_max = 1
        self.date = True

        self.set_ranges()
        self.init_signals()
        self.handle_bpm_changed()
        self.handle_res_changed()
        self.handle_dyn_changed()

    def set_ranges(self):
        self.win.bpm.setRange(30, 300)
        self.win.res.setRange(0, 4)

    def init_signals(self):
        self.win.create_btn.clicked.connect(self.handle_start_click)
        self.win.bpm.valueChanged.connect(self.handle_bpm_changed)
        self.win.res.valueChanged.connect(self.handle_res_changed)
        self.win.dyn.valueChanged.connect(self.handle_dyn_changed)

    def handle_bpm_changed(self):
        self.bpm = int(self.win.bpm.value())
        self.win.bpm_val.setText(str(self.bpm))

    def handle_res_changed(self):
        res = self.win.res.value()
        if res == 0:
            self.res = 1 / 32
            self.win.res_val.setText('1/32')
        elif res == 1:
            self.res = 1 / 16
            self.win.res_val.setText('1/16')
        elif res == 2:
            self.res = 1 / 8
            self.win.res_val.setText('1/8')
        elif res == 3:
            self.res = 1 / 4
            self.win.res_val.setText('1/4')
        elif res == 4:
            self.res = 1 / 2
            self.win.res_val.setText('1/2')

    def handle_dyn_changed(self):
        self.dyn_min = self.win.dyn.value()[0] / 100
        self.dyn_max = self.win.dyn.value()[1] / 100
        self.win.dyn_val.setText(f'{self.dyn_min} - {self.dyn_max}')

    def handle_start_click(self):
        self.text = self.win.text_widget.toPlainText()

        g = Generator(self.text, self.bpm, self.res, self.dyn_min, self.dyn_max, date=self.date)
        g.export()

    def run(self):
        self.win.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    c = Controller()
    c.run()
    sys.exit(app.exec())
