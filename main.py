import sys
import os
from docx2pdf import convert
from PyPDF2 import PdfFileReader
from PyQt5 import QtCore, QtWidgets
from form import Ui_Main


class PrintCounterMainWindow(QtWidgets.QMainWindow, Ui_Main):
    price = {
        'blackSingle': 0.3,
        'blackDouble': 0.5,
        'colorSingle': 0.5,
        'colorDouble': 0.7
    }
    spinBoxs = ['blackSingle', 'blackDouble', 'colorSingle', 'colorDouble']

    def __init__(self):
        super(PrintCounterMainWindow, self).__init__()
        self.setupUi(self)
        self.discount.setValue(10)
        self.total.setDigitCount(4)
        for box in self.spinBoxs:
            getattr(self, box).valueChanged['int'].connect(self.change)
        self.discount.valueChanged['int'].connect(self.change)

        self.reset.clicked.connect(self.do_reset)

    def change(self):
        total = 0.0
        for box in self.spinBoxs:
            total += int(getattr(self, box).text()) * self.price[box]
        discount = int(self.discount.text()) * 0.1
        total *= discount
        print('total', total)
        self.total.display(total)

    def do_reset(self):
        for box in self.spinBoxs:
            getattr(self, box).setValue(0)

        self.discount.setValue(10)
        self.total.display(0)

    def is_print_one_side(self, fileName=''):
        return \
            QtWidgets.QMessageBox \
                .question(self, '提示', fileName + '是否为单面打印',
                          QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                          QtWidgets.QMessageBox.Yes) == QtWidgets.QMessageBox.Yes

    def dragEnterEvent(self, event):
        t = event.mimeData().text()
        if t.endswith('.docx') or t.endswith('.doc') or t.endswith('.pdf'):
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        try:
            filePath = event.mimeData().text().replace('file://', '')
            outputPath = './tmp.pdf'
            print(os.path.basename(event.mimeData().text()))
            if filePath.endswith('.pdf'):
                reader = PdfFileReader(filePath)
            else:
                print(filePath)
                convert(filePath, outputPath)
                reader = PdfFileReader(outputPath)
            page = reader.getNumPages()
            if os.path.exists(outputPath):
                os.remove(outputPath)
            print('add page', page)
            if self.is_print_one_side(os.path.basename(event.mimeData().text())):
                self.blackSingle.setValue(int(self.blackSingle.text()) + page)
            else:
                self.blackDouble.setValue(int(self.blackDouble.text()) + (int(page / 2)))
                self.blackSingle.setValue(int(self.blackSingle.text()) + (int(page) % 2))

        except Exception as e:
            print(e)


if __name__ == '__main__':
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QtWidgets.QApplication(sys.argv)
    window = PrintCounterMainWindow()
    window.show()

    sys.exit(app.exec_())
