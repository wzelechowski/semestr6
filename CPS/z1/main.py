from PyQt5.QtWidgets import QApplication
import sys
import MainWindow

def main():
    app = QApplication(sys.argv)
    window = MainWindow.MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()