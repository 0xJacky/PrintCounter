import sys
import form

from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow

if __name__ == '__main__':
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()

    ui = form.Ui_Main()
    ui.setupUi(MainWindow)

    def change():
        bS = 0.3
        bD = 0.5
        cS = 0.5
        cD = 0.7
        blackSingle = int(ui.blackSingle.text())
        blackDouble = int(ui.blackDouble.text())
        colorSingle = int(ui.colorSingle.text())
        colorDouble = int(ui.colorDouble.text())
        discount = int(ui.discount.text()) * 0.1
        total = (bS * blackSingle + bD * blackDouble + cS * colorSingle + cD * colorDouble) * discount
        print(total)
        ui.total.display(total)

    def reset():
        ui.blackSingle.setValue(0)
        ui.blackDouble.setValue(0)
        ui.colorSingle.setValue(0)
        ui.colorDouble.setValue(0)
        ui.discount.setValue(10)
        ui.total.display(0)

    ui.discount.setValue(10)
    ui.total.setDigitCount(4)
    ui.blackSingle.valueChanged['int'].connect(lambda: change())
    ui.blackDouble.valueChanged['int'].connect(lambda: change())
    ui.colorSingle.valueChanged['int'].connect(lambda: change())
    ui.colorDouble.valueChanged['int'].connect(lambda: change())
    ui.discount.valueChanged['int'].connect(lambda: change())
    ui.reset.clicked.connect(lambda: reset())

    MainWindow.show()

    sys.exit(app.exec_())
