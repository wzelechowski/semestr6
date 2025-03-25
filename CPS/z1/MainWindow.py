import os
import pickle
from copy import deepcopy


import Signal
import inspect
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGridLayout, \
    QComboBox, QLineEdit, QFileDialog, QStackedWidget, QTabWidget, QListWidget, QSlider
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QStackedWidget, QLabel
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

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
        self.combined_signal = None
        self.signal1_class = self.variants['Szum o rozkładzie jednostajnym']
        self.signal2_class = self.variants['Szum o rozkładzie jednostajnym']
        self.bins = 50

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
        self.save1.setStyleSheet(f"font-size: 20px; padding:10px; margin-left: {int(self.width() * 0.03)}; background-color: white;border: 2px solid black; border-radius: 10px;")

        self.read1 = QPushButton('Wczytaj')
        self.read1.setStyleSheet(f"font-size: 20px; padding:10px; margin-left: {int(self.width() * 0.03)}; background-color: white;border: 2px solid black; border-radius: 10px;")

        self.confirm1 = QPushButton('Potwierdź')
        self.confirm1.setStyleSheet(f"font-size: 20px; padding:10px; margin-left: {int(self.width() * 0.03)}; background-color: white;border: 2px solid black; border-radius: 10px;")

        self.combo_box1 = QComboBox()
        for variant in self.variants:
            self.combo_box1.addItem(variant)

        self.combo_box1.setStyleSheet("""
            QComboBox {
                font-size: 20px;
                border-radius: 10px;
                border: 2px solid black;
                padding: 5px;
                background-color: white;  /* Tło w ciemnym kolorze */
            }
            QComboBox::down-arrow {
                width: 10px;
                height: 10px;
                border: none;
                image: url('path/to/arrow.png');  /* Możesz dodać własny obrazek dla strzałki */
            }
            QComboBox::drop-down {
                border: none;
            }
        """)

        params1_layout = QGridLayout()
        params1_layout.setContentsMargins(int(self.width() * 0.05), 0, int(self.width() * 0.04), 0)
        params1_values = []

        for i, param in enumerate(self.param1):
            row, col = i // 3, i % 3
            label = QLabel(param)
            label.setStyleSheet(f"font-size: 20px; margin-left: {int(self.width() * 0.02)}")
            qline = QLineEdit()
            qline.setFixedHeight(30)
            qline.setStyleSheet(f"font-size: 20px; background-color: white;border: 2px solid black;")
            params1_layout.addWidget(label, row, col * 2)
            params1_layout.addWidget(qline, row, col * 2 + 1)
            params1_values.append(qline)

        params1_widget = QWidget()
        params1_widget.setLayout(params1_layout)
        params1_widget.setStyleSheet('border-radius: 10px;')

        signal2_label = QLabel("Sygnał 2")
        signal2_label.setAlignment(Qt.AlignHCenter)
        signal2_label.setStyleSheet(f"font-size: 24px; margin-top: {int(self.height() * 0.05)}")

        self.save2 = QPushButton('Zapisz')
        self.save2.setStyleSheet(f"font-size: 20px; padding:10px; margin-left: {int(self.width() * 0.03)}; background-color: white;border: 2px solid black; border-radius: 10px;")

        self.read2 = QPushButton('Wczytaj')
        self.read2.setStyleSheet(f"font-size: 20px; padding:10px; margin-left: {int(self.width() * 0.03)}; background-color: white;border: 2px solid black; border-radius: 10px;")

        self.confirm2 = QPushButton('Potwierdź')
        self.confirm2.setStyleSheet(f"font-size: 20px; padding:10px; margin-left: {int(self.width() * 0.03)}; background-color: white;border: 2px solid black; border-radius: 10px;")

        self.combo_box2 = QComboBox()
        for variant in self.variants:
            self.combo_box2.addItem(variant)

        self.combo_box2.setStyleSheet("""
            QComboBox {
                font-size: 20px;
                border-radius: 10px;
                border: 2px solid black;
                padding: 5px;
                background-color: white;
            }
            QComboBox::down-arrow {
                border: none;
            }
            QComboBox::drop-down {
                border: none;
            }
        """)

        params2_layout = QGridLayout()
        params2_layout.setContentsMargins(int(self.width() * 0.04), 0, int(self.width() * 0.05), 0)
        params2_values = []

        for i, param in enumerate(self.param2):
            row, col = i // 3, i % 3
            label = QLabel(param)
            label.setStyleSheet(f"font-size: 20px; margin-left: {int(self.width() * 0.02)}")
            qline = QLineEdit()
            qline.setFixedHeight(30)
            qline.setStyleSheet(f"font-size: 20px; background-color: white;border: 2px solid black;")
            params2_layout.addWidget(label, row, col * 2)
            params2_layout.addWidget(qline, row, col * 2 + 1)
            params2_values.append(qline)

        params2_widget = QWidget()
        params2_widget.setLayout(params2_layout)
        params2_widget.setStyleSheet('border-radius: 10px;')

        tab_widget1 = QTabWidget()

        plot1_widget = QStackedWidget()
        plot1_layout = QVBoxLayout()
        plot1_label = QLabel("Wykres")
        plot1_layout.addWidget(plot1_label)
        plot1_widget.setLayout(plot1_layout)

        histogram1_widget = QStackedWidget()
        histogram1_layout = QVBoxLayout()
        histogram1_label = QLabel("Histogram")
        histogram1_layout.addWidget(histogram1_label)
        histogram1_widget.setLayout(histogram1_layout)

        params1_bottom_widget = QListWidget()
        params1_bottom_layout = QVBoxLayout()
        params1_bottom_widget.setLayout(params1_bottom_layout)

        tab_widget2 = QTabWidget()

        plot2_widget = QStackedWidget()
        plot2_layout = QVBoxLayout()
        plot2_label = QLabel("Wykres")
        plot2_layout.addWidget(plot2_label)
        plot2_widget.setLayout(plot2_layout)

        histogram2_widget = QStackedWidget()
        histogram2_layout = QVBoxLayout()
        histogram2_label = QLabel("Histogram")
        histogram2_layout.addWidget(histogram2_label)
        histogram2_widget.setLayout(histogram2_layout)

        params2_bottom_widget = QListWidget()
        params2_bottom_layout = QVBoxLayout()
        params2_bottom_widget.setLayout(params2_bottom_layout)

        arithmetic_widget = QWidget()
        self.plus = QPushButton('+')
        self.plus.setStyleSheet(f"font-size: 20px; padding:10px;; background-color: white;border: 2px solid black; border-radius: 10px;")

        self.minus = QPushButton('-')
        self.minus.setStyleSheet(f"font-size: 20px; padding:10px; background-color: white;border: 2px solid black; border-radius: 10px;")

        self.multiply =QPushButton('*')
        self.multiply.setStyleSheet(f"font-size: 20px; padding:10px; background-color: white;border: 2px solid black; border-radius: 10px;")

        self.divide = QPushButton(':')
        self.divide.setStyleSheet(f"font-size: 20px; padding:10px; background-color: white;border: 2px solid black; border-radius: 10px;")

        arithmetic_layout = QVBoxLayout()
        arithmetic_layout.addWidget(self.plus)
        arithmetic_layout.addWidget(self.minus)
        arithmetic_layout.addWidget(self.multiply)
        arithmetic_layout.addWidget(self.divide)

        arithmetic_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        arithmetic_widget.setLayout(arithmetic_layout)

        def create_plot_canvas(stacked_widget, signal=None):
            if signal is not None:
                canvas = signal.plot_signal()
            else:
                fig = Figure(figsize=(5, 3))
                canvas = FigureCanvas(fig)
                ax = fig.add_subplot()
                ax.plot()
                ax.set_xlabel('Czas[t]')
                ax.set_ylabel('Amplituda[A]')
                ax.set_title(signal)
                ax.grid(True)

            stacked_widget.addWidget(canvas)
            stacked_widget.setCurrentWidget(canvas)

        def create_hist_canvas(stacked_widget, signal=None):
            if signal is not None:
                canvas = signal.histogram_signal(self.bins)
            else:
                fig = Figure(figsize=(5, 3))
                canvas = FigureCanvas(fig)
                ax = fig.add_subplot()
                ax.hist([])
                ax.set_ylabel('Liczba próbek')
                ax.set_xlabel('Amplituda[A]')
                ax.set_title(signal)
                ax.grid(True)

            stacked_widget.addWidget(canvas)
            stacked_widget.setCurrentWidget(canvas)

        def create_params(list_widget, signal=None):
            list_widget.clear()

            if signal is None:
                return

            list = signal.signal_params()
            for param in list:
                name, value = param
                list_widget.addItem(f'{name} {value}')

        def update_bins():
            self.bins = self.slider.value()
            self.slider_label.setText(f'Bins: {self.bins}')
            self.slider_label.setStyleSheet('font-size: 20px; padding:10px;')

            if self.signal1 is not None:
                create_hist_canvas(histogram1_widget, self.signal1)

            if self.signal2 is not None:
                create_hist_canvas(histogram2_widget, self.signal2)

            if self.combined_signal is not None:
                create_hist_canvas(combined_histogram_widget, self.combined_signal)


        create_plot_canvas(plot1_widget)
        create_hist_canvas(histogram1_widget)
        create_params(params1_bottom_widget)
        tab_widget1.addTab(plot1_widget, 'Wykres')
        tab_widget1.addTab(histogram1_widget, 'Histogram')
        tab_widget1.addTab(params1_bottom_widget, 'Parametry')

        create_plot_canvas(plot2_widget)
        create_hist_canvas(histogram2_widget)
        create_params(params2_bottom_widget)
        tab_widget2.addTab(plot2_widget, 'Wykres')
        tab_widget2.addTab(histogram2_widget, 'Histogram')
        tab_widget2.addTab(params2_bottom_widget, 'Parametry')

        combined_signal_widget = QTabWidget()

        combined_plot_widget = QStackedWidget()
        combined_plot_layout = QVBoxLayout()
        combined_plot_label = QLabel('Wykres')
        combined_plot_layout.addWidget(combined_plot_label)
        combined_plot_widget.setLayout(combined_plot_layout)

        combined_histogram_widget = QStackedWidget()
        combined_histogram_layout = QVBoxLayout()
        combined_histogram_label = QLabel('Histogram')
        combined_histogram_layout.addWidget(combined_histogram_label)
        combined_histogram_widget.setLayout(combined_histogram_layout)

        combined_params_widget = QListWidget()
        combined_params_layout = QVBoxLayout()
        combined_params_widget.setLayout(combined_params_layout)

        create_plot_canvas(combined_plot_widget)
        create_hist_canvas(combined_histogram_widget)
        create_params(combined_params_widget)
        combined_signal_widget.addTab(combined_plot_widget, 'Wykres')
        combined_signal_widget.addTab(combined_histogram_widget, 'Histogram')
        combined_signal_widget.addTab(combined_params_widget, 'Parametry')\

        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setMinimum(10)
        self.slider.setMaximum(100)
        self.slider.setValue(self.bins)
        self.slider_label = QLabel(f'Bins: {self.bins}')
        self.slider_label.setStyleSheet('font-size: 20px; padding:10px;')


        self.left = QPushButton("""
        ^__
        """)
        self.left.setStyleSheet(f"font-size: 20px; padding:10px; margin-left: {int(self.width() * 0.03)}; background-color: white;border: 2px solid black; border-radius: 10px;")

        self.right = QPushButton("""
        __^
        """)
        self.right.setStyleSheet(f"font-size: 20px; padding:10px; margin-left: {int(self.width() * 0.03)}; background-color: white;border: 2px solid black; border-radius: 10px;")


        self.save3 = QPushButton('Zapisz')
        self.save3.setStyleSheet(f"font-size: 20px; padding:10px; margin-left: {int(self.width() * 0.03)}; background-color: white;border: 2px solid black; border-radius: 10px;")

        self.read3 = QPushButton('Wczytaj')
        self.read3.setStyleSheet(f"font-size: 20px; padding:10px; margin-left: {int(self.width() * 0.03)}; background-color: white;border: 2px solid black; border-radius: 10px;")

        self.reset = QPushButton('Reset')
        self.reset.setStyleSheet(f"font-size: 20px; padding:10px; margin-left: {int(self.width() * 0.03)}; background-color: white;border: 2px solid black; border-radius: 10px;")

        #creating functions
        def confirm1_click():
            try:
                values = [float(qline.text()) for qline in params1_values]
                self.signal1 = self.signal1_class(*values)
                self.signal1.generate_t()
                self.signal1.generate_signal()
                create_plot_canvas(plot1_widget, self.signal1)
                create_hist_canvas(histogram1_widget, self.signal1)
                create_params(params1_bottom_widget, self.signal1)
            except Exception as e:
                print(e)


        def confirm2_click():
            try:
                values = [float(qline.text()) for qline in params2_values]
                self.signal2 = self.signal2_class(*values)
                self.signal2.generate_t()
                self.signal2.generate_signal()
                create_plot_canvas(plot2_widget, self.signal2)
                create_hist_canvas(histogram2_widget, self.signal2)
                create_params(params2_bottom_widget, self.signal2)
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
                qline.setStyleSheet(f"font-size: 20px; background-color: white;border: 2px solid black;")
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
                        create_plot_canvas(plot1_widget, self.signal1)
                        create_hist_canvas(histogram1_widget, self.signal1)
                        create_params(params1_bottom_widget, self.signal1)

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
                    qline.setStyleSheet(f"font-size: 20px; background-color: white;border: 2px solid black;")
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
                        create_plot_canvas(plot2_widget, self.signal2)
                        create_hist_canvas(histogram2_widget, self.signal2)
                        create_params(params2_bottom_widget, self.signal2)

                        for key, value in self.variants.items():
                            if isinstance(self.signal2, value):
                                self.combo_box2.setCurrentText(key)
                        update_signal2()

                        for i, key in enumerate(self.param1):
                            if key in vars(self.signal2) and i < len(params2_values):
                                params2_values[i].setText(str(vars(self.signal2)[key]))
            except Exception as e:
                print(e)

        def add():
            try:
                if self.combined_signal is None:
                    self.combined_signal = deepcopy(self.signal1)
                self.combined_signal +  self.signal2
                create_plot_canvas(combined_plot_widget, self.combined_signal)
                create_hist_canvas(combined_histogram_widget, self.combined_signal)
                create_params(combined_params_widget, self.combined_signal)
            except Exception as e:
                print(e)

        def sub():
            try:
                if self.combined_signal is None:
                    self.combined_signal = deepcopy(self.signal1)
                self.combined_signal -  self.signal2
                create_plot_canvas(combined_plot_widget, self.combined_signal)
                create_hist_canvas(combined_histogram_widget, self.combined_signal)
                create_params(combined_params_widget, self.combined_signal)
            except Exception as e:
                print(e)

        def mul():
            try:
                if self.combined_signal is None:
                    self.combined_signal = deepcopy(self.signal1)
                self.combined_signal *  self.signal2
                create_plot_canvas(combined_plot_widget, self.combined_signal)
                create_hist_canvas(combined_histogram_widget, self.combined_signal)
                create_params(combined_params_widget, self.combined_signal)
            except Exception as e:
                print(e)

        def div():
            try:
                if self.combined_signal is None:
                    self.combined_signal /= self.signal2
                self.combined_signal = deepcopy(self.signal1)
                self.combined_signal /  self.signal2
                create_plot_canvas(combined_plot_widget, self.combined_signal)
                create_hist_canvas(combined_histogram_widget, self.combined_signal)
                create_params(combined_params_widget, self.combined_signal)
            except Exception as e:
                print(e)

        def reset():
            create_plot_canvas(combined_plot_widget, None)
            create_hist_canvas(combined_histogram_widget, None)
            create_params(combined_params_widget, None)
            self.combined_signal = None

        def save3_click():
            file_path, _ = QFileDialog.getSaveFileName(None, "Zapisz plik", f'{os.getcwd()}/files/{self.combined_signal}',
                                                       "Pliki binarne (*.pkl);;Wszystkie pliki (*)")
            try:
                if file_path:
                    with open(file_path, 'wb') as file:
                        pickle.dump(self.combined_signal, file)
            except Exception as e:
                print(e)

        def left_click():
            if self.combined_signal is not None:
                self.signal1 = deepcopy(self.combined_signal)
                create_plot_canvas(plot1_widget, self.signal1)
                create_hist_canvas(histogram1_widget, self.signal1)
                create_params(params1_bottom_widget, self.signal1)

        def right_click():
            if self.combined_signal is not None:
                self.signal2 = deepcopy(self.combined_signal)
                create_plot_canvas(plot2_widget, self.signal2)
                create_hist_canvas(histogram2_widget, self.signal2)
                create_params(params2_bottom_widget, self.signal2)


        #events
        self.confirm1.clicked.connect(confirm1_click)
        self.confirm2.clicked.connect(confirm2_click)
        self.combo_box1.activated.connect(update_signal1)
        self.combo_box2.activated.connect(update_signal2)
        self.save1.clicked.connect(save1_click)
        self.save2.clicked.connect(save2_click)
        self.read1.clicked.connect(read1_click)
        self.read2.clicked.connect(read2_click)
        self.plus.clicked.connect(add)
        self.minus.clicked.connect(sub)
        self.multiply.clicked.connect(mul)
        self.divide.clicked.connect(div)
        self.reset.clicked.connect(reset)
        self.save3.clicked.connect(save3_click)
        self.left.clicked.connect(left_click)
        self.right.clicked.connect(right_click)
        self.slider.valueChanged.connect(update_bins)

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

        combined_signal_operations_layout = QHBoxLayout()
        combined_signal_operations_layout.addWidget(self.save3, alignment=Qt.AlignCenter)
        combined_signal_operations_layout.addWidget(self.slider, alignment=Qt.AlignCenter)
        combined_signal_operations_layout.addWidget(self.slider_label, alignment=Qt.AlignCenter)
        combined_signal_operations_layout.addWidget(self.reset, alignment=Qt.AlignCenter)

        combined_signal_operation_widget = QWidget()
        combined_signal_operation_widget.setLayout(combined_signal_operations_layout)


        grid_layout.addWidget(signal1_label, 0, 0, 1, 4)
        grid_layout.addWidget(signal1_widget, 1, 0, 1, 4)
        grid_layout.addWidget(params1_widget, 2, 0, 1, 4)
        grid_layout.addWidget(signal1_operations_widget, 3, 0, 1, 4)
        grid_layout.addWidget(signal2_label, 0, 5, 1, 4)
        grid_layout.addWidget(signal2_widget, 1, 5, 1, 4)
        grid_layout.addWidget(params2_widget, 2, 5, 1, 4)
        grid_layout.addWidget(signal2_operations_widget, 3, 5, 1, 4)
        grid_layout.addWidget(tab_widget1, 4, 0, 4, 4)
        grid_layout.addWidget(arithmetic_widget, 4, 4, 5, 1)
        grid_layout.addWidget(tab_widget2, 4, 5, 4, 4)
        grid_layout.addWidget(combined_signal_widget, 9, 2, 5, 5)
        grid_layout.addWidget(self.left, 9, 1, 1, 1)
        grid_layout.addWidget(self.right, 9, 7, 1, 1)
        grid_layout.addWidget(combined_signal_operation_widget, 15, 3, 1, 3)

        central_widget.setLayout(grid_layout)