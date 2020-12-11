import os
import platform
import shutil
import sys
import tempfile

from PyPDF2 import PdfFileReader
from PyQt5 import QtCore, QtWidgets
from docx2pdf import convert
from pdf2image import convert_from_path

from doc2pdf import doc2pdf
from form import Ui_Main
from image import is_color_image


class PrintCounterMainWindow(QtWidgets.QMainWindow, Ui_Main):
    price = {
        'blackSingle': 0.3,
        'blackDouble': 0.5,
        'colorSingle': 0.5,
        'colorDouble': 0.7
    }
    spinBoxs = ['blackSingle', 'blackDouble', 'colorSingle', 'colorDouble']

    fileName = ''

    def __init__(self):
        super(PrintCounterMainWindow, self).__init__()
        self.setupUi(self)
        self.notice.setText(None)
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
        print('[Counter] total', total)
        self.total.display(total)

    def do_reset(self):
        for box in self.spinBoxs:
            getattr(self, box).setValue(0)

        self.discount.setValue(10)
        self.total.display(0)
        self.notice.setText(None)

    def is_print_one_side(self):
        return \
            QtWidgets.QMessageBox \
                .question(self, '提示', self.fileName + ' 是否为单面打印',
                          QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                          QtWidgets.QMessageBox.Yes) == QtWidgets.QMessageBox.Yes

    def is_color_print(self):
        return \
            QtWidgets.QMessageBox \
                .question(self, '提示', self.fileName + ' 是否为彩色打印',
                          QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                          QtWidgets.QMessageBox.Yes) == QtWidgets.QMessageBox.Yes

    def dragEnterEvent(self, event):
        t = event.mimeData().text()
        if t.endswith('.docx') or t.endswith('.doc') or t.endswith('.pdf'):
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        self.notice.setText('正在计算，请稍等')
        QtWidgets.qApp.processEvents()
        try:
            if platform.system() == 'Windows':
                filePath = event.mimeData().text().replace('file:///', '')
            else:
                filePath = event.mimeData().text().replace('file://', '')

            print('[Counter] filepath, event data', filePath, event.mimeData().text())
            outputPath = os.path.join(os.getcwd(), 'tmp.pdf')
            if filePath.endswith('.pdf'):
                shutil.copyfile(filePath, outputPath)
            elif filePath.endswith('.doc') and platform.system() == 'Windows':
                doc2pdf(filePath, outputPath)
            else:
                convert(filePath, outputPath)

            reader = PdfFileReader(outputPath)

            page = reader.getNumPages()

            self.fileName = os.path.basename(event.mimeData().text())
            print('[Counter] file name', self.fileName)

            blackSingle = 0
            blackDouble = 0
            colorSingle = 0
            colorDouble = 0

            with tempfile.TemporaryDirectory() as path:
                if platform.system() == 'Windows':
                    images_from_path = convert_from_path(outputPath, output_folder=path,
                                                         poppler_path=r"C:\Users\Jacky\Desktop\Release-20.12.1\poppler-20.12.1\bin")
                else:
                    images_from_path = convert_from_path(outputPath, output_folder=path)
                # 单面打印
                if self.is_print_one_side():
                    # 彩印
                    if self.is_color_print():
                        # 识别每一张图是否为彩色
                        for image in images_from_path:
                            if is_color_image(image):
                                colorSingle += 1
                            else:
                                blackSingle += 1
                        # 更新值
                        self.blackSingle.setValue(int(self.blackSingle.text()) + blackSingle)
                        self.colorSingle.setValue(int(self.colorSingle.text()) + colorSingle)
                    # 黑白打印
                    else:
                        # 直接更新值
                        self.blackSingle.setValue(int(self.blackSingle.text()) + page)
                        blackSingle = page
                # 双面打印
                else:
                    # 彩印
                    if self.is_color_print():
                        for i in range(0, page, 2):
                            # 单数是彩色
                            if is_color_image(images_from_path[i]):
                                # 下一面没了
                                if i + 1 >= page:
                                    colorSingle += 1
                                # 下一面还有，不管是啥都算彩色
                                else:
                                    colorDouble += 1
                            # 单数是黑白
                            else:
                                # 下一面没了
                                if i + 1 >= page:
                                    blackSingle += 1
                                # 下一面还有而且是彩色
                                elif is_color_image(images_from_path[i + 1]):
                                    colorDouble += 1
                                # 下一面还有而且是黑白
                                else:
                                    blackDouble += 1
                        self.blackSingle.setValue(int(self.blackSingle.text()) + blackSingle)
                        self.blackDouble.setValue(int(self.blackDouble.text()) + blackDouble)
                        self.colorSingle.setValue(int(self.colorSingle.text()) + colorSingle)
                        self.colorDouble.setValue(int(self.colorDouble.text()) + colorDouble)
                    # 黑白
                    else:
                        blackSingle = int(page) % 2
                        blackDouble = int(page / 2)
                        self.blackSingle.setValue(int(self.blackSingle.text()) + blackSingle)
                        self.blackDouble.setValue(int(self.blackDouble.text()) + blackDouble)

            if os.path.exists(outputPath):
                os.remove(outputPath)

            print('[Counter] add pages %s, blackSingle %s, blackDouble %s, colorSingle %s, colorDouble %s' % (page,
                                                                                                              blackSingle,
                                                                                                              blackDouble,
                                                                                                              colorSingle,
                                                                                                              colorDouble))
            self.notice.setText(None)
        except Exception as e:
            print('[Counter] Error', e)
            if os.path.exists(os.path.join(os.getcwd(), 'debug')):
                self.notice.setText('计算错误 %s' % e)


if __name__ == '__main__':
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QtWidgets.QApplication(sys.argv)
    window = PrintCounterMainWindow()
    window.show()

    sys.exit(app.exec_())
