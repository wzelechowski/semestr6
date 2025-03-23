import os
import pickle

from PIL.ImageOps import expand
from PyQt5.QtCore import Qt

import Signal
import inspect
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGridLayout, \
    QComboBox, QLineEdit, QFileDialog, QStackedWidget
from PyQt5.QtWidgets import QPushButton


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CPS")
        self.showFullScreen()
        self.variants = {
            'Szum o rozkładzie jednostajnym': Signal.UniformlyDistributedNoise,
            'Szum gaussowski': Signal.GaussianNoise,
            'Sygnał sinusoidalny': Signal.SinuosidalSignal,
            'Sygnał sinusoidalny wyprostowany jednopołówkowo': Signal.SinusoidalOneHalfSignal,
            'Sygnał sinusoidalny wyprostowany dwupołówkowo': Signal.SinusoidalTwoHalfSignal,
            'Sygnał prostokątny': Signal.SquareSignal,
            'Sygnał prostokątny symetryczny': Signal.SquareSimetricalSignal,
            'Sygnał trójkątny': Signal.TriangleSignal,
            'Skok jednostkowy': Signal.UnitJump,
            'Impuls jednostkowy': Signal.UnitImpulse,
            'Szum impulsowy': Signal.ImpulseNoise,
        }

        self.signal1 = None
        self.signal2 = None
        self.signal1_class = self.variants['Szum o rozkładzie jednostajnym']
        self.signal2_class = self.variants['Szum o rozkładzie jednostajnym']
        self.show1 = False
        self.show2 = False

        def set_params1():
            signature = inspect.signature(self.signal1_class.__init__)
            params = signature.parameters
            params = [param for param in params if param != 'self']
            self.param1 = params

        def set_params2():
            signature = inspect.signature(self.signal2_class.__init__)
            params = signature.parameters
            params = [param for param in params if param != 'self']
            self.param2 = params

        set_params1()
        set_params2()


        # creating window
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        grid_layout = QGridLayout()

        # creating widgets
        signal1_label = QLabel("Sygnał 1")
        signal1_label.setAlignment(Qt.AlignHCenter)
        signal1_label.setStyleSheet(f"font-size: 24px; margin-top: {int(self.height() * 0.05)}")

        self.save1 = QPushButton('Zapisz')
        self.save1.setStyleSheet(f"font-size: 20px; padding:5px; margin-left: {int(self.width() * 0.03)};")

        self.read1 = QPushButton('Wczytaj')
        self.read1.setStyleSheet(f"font-size: 20px; padding:5px; margin-left: {int(self.width() * 0.02)};")

        self.confirm1 = QPushButton('Potwierdź')
        self.confirm1.setStyleSheet(f"font-size: 20px; padding:5px; margin-left: {int(self.width() * 0.01)};")

        self.combo_box1 = QComboBox()
        for variant in self.variants:
            self.combo_box1.addItem(variant)

        self.combo_box1.setStyleSheet(f"font-size: 20px;")

        params1_layout = QGridLayout()
        params1_layout.setContentsMargins(int(self.width() * 0.05), 0, int(self.width() * 0.04), 0)
        params1_values = []

        for i, param in enumerate(self.param1):
            row, col = i // 3, i % 3
            label = QLabel(param)
            label.setStyleSheet(f"font-size: 20px; margin-left: {int(self.width() * 0.02)}")
            qline = QLineEdit()
            qline.setFixedHeight(30)
            qline.setStyleSheet(f"font-size: 20px;")
            params1_layout.addWidget(label, row, col * 2)
            params1_layout.addWidget(qline, row, col * 2 + 1)
            params1_values.append(qline)

        params1_widget = QWidget()
        params1_widget.setLayout(params1_layout)

        signal2_label = QLabel("Sygnał 2")
        signal2_label.setAlignment(Qt.AlignHCenter)
        signal2_label.setStyleSheet(f"font-size: 24px; margin-top: {int(self.height() * 0.05)}")

        self.save2 = QPushButton('Zapisz')
        self.save2.setStyleSheet(f"font-size: 20px; padding:5px; margin-left: {int(self.width() * 0.03)};")

        self.read2 = QPushButton('Wczytaj')
        self.read2.setStyleSheet(f"font-size: 20px; padding:5px; margin-left: {int(self.width() * 0.02)};")

        self.confirm2 = QPushButton('Potwierdź')
        self.confirm2.setStyleSheet(f"font-size: 20px; padding:5px; margin-left: {int(self.width() * 0.01)};")

        self.combo_box2 = QComboBox()
        for variant in self.variants:
            self.combo_box2.addItem(variant)

        self.combo_box2.setStyleSheet("font-size: 20px;")

        params2_layout = QGridLayout()
        params2_layout.setContentsMargins(int(self.width() * 0.04), 0, int(self.width() * 0.05), 0)
        params2_values = []

        for i, param in enumerate(self.param2):
            row, col = i // 3, i % 3
            label = QLabel(param)
            label.setStyleSheet(f"font-size: 20px; margin-left: {int(self.width() * 0.02)}")
            qline = QLineEdit()
            qline.setFixedHeight(30)
            qline.setStyleSheet(f"font-size: 20px;")
            params2_layout.addWidget(label, row, col * 2)
            params2_layout.addWidget(qline, row, col * 2 + 1)
            params2_values.append(qline)

        params2_widget = QWidget()
        params2_widget.setLayout(params2_layout)

        stacked_widget1 = QStackedWidget()

        bottom_signal1_label = QLabel("Parametry")
        bottom_signal1_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        stacked_widget1.addWidget(bottom_signal1_label)

        bottom_signal2_label = QLabel("Bottom Sygnał 2")
        bottom_signal2_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        bottom_signal2_label.setStyleSheet("background-color: lightyellow; font-size: 24px;")

        #creating functions
        def confirm1_click():
            try:
                values = [float(qline.text()) for qline in params1_values]
                self.signal1 = self.signal1_class(*values)
                self.signal1.generate_t()
                self.signal1.generate_signal()
            except Exception as e:
                print(e)


        def confirm2_click():
            try:
                values = [float(qline.text()) for qline in params2_values]
                self.signal2 = self.signal2_class(*values)
                self.signal2.generate_t()
                self.signal2.generate_signal()
            except Exception as e:
                print(e)

        def show_attr_1():
            while params1_layout.count():
                child = params1_layout.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()

            set_params1()
            params1_values.clear()
            for i, param in enumerate(self.param1):
                row, col = i // 3, i % 3
                label = QLabel(param)
                label.setStyleSheet(f"font-size: 20px; margin-left: {int(self.width() * 0.02)}")
                qline = QLineEdit()
                qline.setFixedHeight(30)
                qline.setStyleSheet(f"font-size: 20px;")
                params1_layout.addWidget(label, row, col * 2)
                params1_layout.addWidget(qline, row, col * 2 + 1)
                params1_values.append(qline)

            params1_widget.setLayout(params1_layout)

        def update_signal1():
            selected_variant = self.combo_box1.currentText()
            self.signal1_class = self.variants[selected_variant]
            show_attr_1()

        def save1_click():
            file_path, _ = QFileDialog.getSaveFileName(None, "Zapisz plik", f'{os.getcwd()}/files/{self.signal1}',
                                                       "Pliki binarne (*.pkl);;Wszystkie pliki (*)")
            try:
                if file_path:
                    with open(file_path, 'wb') as file:
                        pickle.dump(self.signal1, file)
            except Exception as e:
                print(e)

        def read1_click():
            file_path, _ = QFileDialog.getOpenFileName(None, 'Wczytaj plik', f'{os.getcwd()}/files',
                                                       'Pliki binarne (*.pkl);;Wszystkie pliki (*)')
            try:
                if file_path:
                    with open(file_path, 'rb') as file:
                        self.signal1 = pickle.load(file)

                        for key, value in self.variants.items():
                            if isinstance(self.signal1, value):
                                self.combo_box1.setCurrentText(key)
                        update_signal1()

                        for i, key in enumerate(self.param1):
                            if key in vars(self.signal1) and i < len(params1_values):
                                params1_values[i].setText(str(vars(self.signal1)[key]))

            except Exception as e:
                print(e)

        def show_attr_2():
            try:
                while params2_layout.count():
                    child = params2_layout.takeAt(0)
                    if child.widget():
                        child.widget().deleteLater()

                set_params2()
                params2_values.clear()
                for i, param in enumerate(self.param2):
                    row, col = i // 3, i % 3
                    label = QLabel(param)
                    label.setStyleSheet(f"font-size: 20px; margin-left: {int(self.width() * 0.02)}")
                    qline = QLineEdit()
                    qline.setFixedHeight(30)
                    qline.setStyleSheet(f"font-size: 20px;")
                    params2_layout.addWidget(label, row, col * 2)
                    params2_layout.addWidget(qline, row, col * 2 + 1)
                    params2_values.append(qline)

                params2_widget.setLayout(params2_layout)
            except Exception as e:
                print(e)



        def update_signal2():
            selected_variant = self.combo_box2.currentText()
            self.signal2_class = self.variants[selected_variant]
            show_attr_2()



        def save2_click():
            file_path, _ = QFileDialog.getSaveFileName(None, "Zapisz plik", f'{os.getcwd()}/files/{self.signal2}',
                                                       "Pliki binarne (*.pkl);;Wszystkie pliki (*)")
            try:
                if file_path:
                    with open(file_path, 'wb') as file:
                        pickle.dump(self.signal2, file)
            except Exception as e:
                print(e)

        def read2_click():
            file_name, _ = QFileDialog.getOpenFileName(None, 'Wczytaj plik', f'{os.getcwd()}/files',
                                                      'Pliki binarne (*.pkl);;Wszystkie pliki (*)')
            try:
                if file_name:
                    with open(file_name, 'rb') as file:
                        self.signal2 = pickle.load(file)

                        for key, value in self.variants.items():
                            if isinstance(self.signal2, value):
                                self.combo_box2.setCurrentText(key)
                        update_signal2()

                        for i, key in enumerate(self.param1):
                            if key in vars(self.signal2) and i < len(params2_values):
                                params2_values[i].setText(str(vars(self.signal2)[key]))
            except Exception as e:
                print(e)


        #events
        self.confirm1.clicked.connect(confirm1_click)
        self.confirm2.clicked.connect(confirm2_click)
        self.combo_box1.activated.connect(update_signal1)
        self.combo_box2.activated.connect(update_signal2)
        self.save1.clicked.connect(save1_click)
        self.save2.clicked.connect(save2_click)
        self.read1.clicked.connect(read1_click)
        self.read2.clicked.connect(read2_click)

        # adding widgets
        signal1_check_box_layout = QHBoxLayout()
        signal1_check_box_layout.addWidget(self.combo_box1, alignment=Qt.AlignCenter)

        signal1_widget = QWidget()
        signal1_widget.setLayout(signal1_check_box_layout)

        signal1_operations_layout = QHBoxLayout()
        signal1_operations_layout.addWidget(self.save1, alignment=Qt.AlignCenter)
        signal1_operations_layout.addWidget(self.confirm1, alignment=Qt.AlignCenter)
        signal1_operations_layout.addWidget(self.read1, alignment=Qt.AlignCenter)

        signal1_operations_widget = QWidget()
        signal1_operations_widget.setLayout(signal1_operations_layout)

        signal2_check_box_layout = QHBoxLayout()
        signal2_check_box_layout.addWidget(self.combo_box2, alignment=Qt.AlignCenter)

        signal2_widget = QWidget()
        signal2_widget.setLayout(signal2_check_box_layout)

        signal2_operations_layout = QHBoxLayout()
        signal2_operations_layout.addWidget(self.save2, alignment=Qt.AlignCenter)
        signal2_operations_layout.addWidget(self.confirm2, alignment=Qt.AlignCenter)
        signal2_operations_layout.addWidget(self.read2, alignment=Qt.AlignCenter)

        signal2_operations_widget = QWidget()
        signal2_operations_widget.setLayout(signal2_operations_layout)

        grid_layout.addWidget(signal1_label, 0, 0)
        grid_layout.addWidget(signal1_widget, 1, 0)
        grid_layout.addWidget(params1_widget, 2, 0)
        grid_layout.addWidget(signal1_operations_widget, 3, 0)
        grid_layout.addWidget(signal2_label, 0, 1)
        grid_layout.addWidget(signal2_widget, 1, 1)
        grid_layout.addWidget(params2_widget, 2, 1)
        grid_layout.addWidget(signal2_operations_widget, 3, 1)
        grid_layout.addWidget(bottom_signal1_label, 4, 0, 5, 1)
        grid_layout.addWidget(bottom_signal2_label, 4, 1, 5, 1)
        central_widget.setLayout(grid_layout)