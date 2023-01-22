from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
import hashlib

version = "0.1.0"


class Ui_MainWindow(QtCore.QObject):
    data_for_thread = QtCore.pyqtSignal(str, int)

    def __init__(self):
        super().__init__()
        self.i = 0
        self.worker = Worker()
        self.worker_thread = QtCore.QThread()

        self.data_for_thread.connect(self.worker.hash_file)
        self.worker.progress.connect(self.pbar_update)
        self.worker.result.connect(self.result)

        self.worker.moveToThread(self.worker_thread)
        self.worker_thread.start()

    def setupUi(self, MainWindow):
        MainWindow.setWindowIcon(QtGui.QIcon("assets/logo.png"))
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(750, 400)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(225, 225, 225))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(225, 225, 225))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(240, 240, 240))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        self.centralwidget.setPalette(palette)
        self.centralwidget.setStyleSheet("")
        self.centralwidget.setObjectName("centralwidget")

        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setSpacing(20)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.input_layout = QtWidgets.QGridLayout()
        self.input_layout.setHorizontalSpacing(50)
        self.input_layout.setVerticalSpacing(15)
        self.input_layout.setObjectName("input_layout")

        self.hash_label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(10)
        self.hash_label.setFont(font)
        self.hash_label.setObjectName("hash_label")
        self.input_layout.addWidget(self.hash_label, 2, 0, 1, 1)

        self.hash_input_box = QtWidgets.QLineEdit(self.centralwidget)
        self.hash_input_box.setObjectName("hash_input_box")
        self.input_layout.addWidget(self.hash_input_box, 3, 0, 1, 1)

        self.File_path_box = QtWidgets.QLineEdit(self.centralwidget)
        self.File_path_box.setObjectName("File_path_box")
        self.input_layout.addWidget(self.File_path_box, 1, 0, 1, 1)

        self.browse_btn = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.browse_btn.setFont(font)
        self.browse_btn.setObjectName("browse_btn")
        self.input_layout.addWidget(self.browse_btn, 1, 1, 1, 1)
        self.browse_btn.clicked.connect(self.file_browse)

        self.file_label = QtWidgets.QLabel(self.centralwidget)
        self.file_label.setEnabled(True)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(10)
        self.file_label.setFont(font)
        self.file_label.setObjectName("file_label")
        self.input_layout.addWidget(self.file_label, 0, 0, 1, 1)
        self.gridLayout_2.addLayout(self.input_layout, 0, 0, 1, 1)

        self.result_btn = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.result_btn.sizePolicy().hasHeightForWidth())
        self.result_btn.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        self.result_btn.setFont(font)
        self.result_btn.setObjectName("result_btn")
        self.gridLayout_2.addWidget(self.result_btn, 4, 0, 2, 1)
        self.result_btn.hide()

        # Progress Bar
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setEnabled(True)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setMaximum(10)
        self.progressBar.setTextVisible(True)
        self.progressBar.setObjectName("progressBar")
        self.gridLayout_2.addWidget(self.progressBar, 6, 0, 1, 1)
        self.progressBar.hide()

        self.output_layout = QtWidgets.QGridLayout()
        self.output_layout.setHorizontalSpacing(50)
        self.output_layout.setVerticalSpacing(20)
        self.output_layout.setObjectName("output_layout")

        self.hash_label2 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.hash_label2.setFont(font)
        self.hash_label2.setObjectName("hash_label2")
        self.output_layout.addWidget(self.hash_label2, 3, 0, 1, 1)

        self.cpy_hash_btn = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.cpy_hash_btn.setFont(font)
        self.cpy_hash_btn.setObjectName("cpy_hash_btn")
        self.output_layout.addWidget(self.cpy_hash_btn, 4, 2, 1, 1)


        self.check_btn = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.check_btn.sizePolicy().hasHeightForWidth())
        self.check_btn.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        self.check_btn.setFont(font)
        self.check_btn.setObjectName("check_btn")
        self.output_layout.addWidget(self.check_btn, 2, 0, 1, 1)
        self.check_btn.clicked.connect(self.check_hash)

        self.hash_output_box = QtWidgets.QLineEdit(self.centralwidget)
        self.hash_output_box.setObjectName("hash_output_box")
        self.output_layout.addWidget(self.hash_output_box, 4, 0, 1, 1)
        self.cpy_hash_btn.clicked.connect(self.copy_hash)

        self.algriothm_box = QtWidgets.QComboBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.algriothm_box.sizePolicy().hasHeightForWidth())
        self.algriothm_box.setSizePolicy(sizePolicy)
        self.algriothm_box.setObjectName("algriothm_box")
        self.output_layout.addWidget(self.algriothm_box, 2, 2, 1, 1)
        self.gridLayout_2.addLayout(self.output_layout, 2, 0, 2, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.algriothm_box.addItems(["MD5", "SHA1", "SHA224", "SHA256", "SHA384", "SHA512 "])

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 750, 21))

        self.menubar.setObjectName("menubar")

        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setTearOffEnabled(False)
        self.menuFile.setObjectName("menuFile")

        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setTearOffEnabled(False)
        self.menuHelp.setObjectName("menuHelp")

        MainWindow.setMenuBar(self.menubar)
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionHelp = QtWidgets.QAction(MainWindow)
        self.actionHelp.setObjectName("actionHelp")
        self.actionAbout_2 = QtWidgets.QAction(MainWindow)
        self.actionAbout_2.setObjectName("actionAbout_2")
        self.menuFile.addAction(self.actionExit)
        self.menuHelp.addAction(self.actionHelp)
        self.menuHelp.addAction(self.actionAbout_2)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.actionExit.triggered.connect(lambda: sys.exit())
        self.actionAbout_2.triggered.connect(lambda: pop_up(1))

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "PyHash Checker"))
        self.hash_label.setText(_translate("MainWindow", "Enter Hash:"))
        self.browse_btn.setText(_translate("MainWindow", "Browse"))
        self.file_label.setText(_translate("MainWindow", "Choose File:"))
        self.result_btn.setText(_translate("MainWindow", "RESULT"))
        self.hash_label2.setText(_translate("MainWindow", "Generated Hash:"))
        self.cpy_hash_btn.setText(_translate("MainWindow", "Copy"))
        self.check_btn.setText(_translate("MainWindow", "CHECK"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionHelp.setText(_translate("MainWindow", "How to Use"))
        self.actionAbout_2.setText(_translate("MainWindow", "About"))

    def copy_hash(self):
        clipboard = QtGui.QGuiApplication.clipboard()
        clipboard.setText(self.hash_output_box.text(), clipboard.Clipboard)

    def file_browse(self):
        self.file_path = QtWidgets.QFileDialog.getOpenFileName(caption="Select File")
        self.File_path_box.setText(self.file_path[0])

    def check_hash(self):

        self.file_path = self.File_path_box.text()
        if self.file_path == "":
            pop_up(0)

        self.method = self.algriothm_box.currentIndex()
        self.hash_inputted = self.hash_input_box.text()

        print(self.file_path)
        file_size = QtCore.QFileInfo(self.file_path).size()
        print("File size : ", file_size)
        self.progressBar.setMaximum(int(file_size/65536))
        if file_size < 10000:
            self.progressBar.hide()
        else:
            self.progressBar.show()

        print(int(file_size/65536))

        self.data_for_thread.emit(self.file_path, self.method)

    def result(self, hash_out):
        self.result_btn.show()
        self.hash_output_box.setText(hash_out)

        if self.hash_inputted == hash_out:
            self.result_btn.setText("HASH MATCHES")
            self.result_btn.setStyleSheet("QPushButton{ color: rgb(52, 182, 50); border: 3px solid rgb(35, 208, 75);"
                                          " background-color: rgb(232, 232, 232); font-size:18px; }")
        else:
            self.result_btn.setText("HASH DOES NOT MATCH")
            self.result_btn.setStyleSheet("QPushButton{ color: rgb(197, 61, 63); border: 3px solid rgb(220, 48, 51);"
                                          " background-color: rgb(232, 232, 232); font-size:18px; }")

    def pbar_update(self, val):
        self.progressBar.setValue(val)


def pop_up(mode):

    if mode == 0:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("Select File ")
        msg.setWindowTitle("Error")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        msg.exec_()
    if mode == 1:
        about = QMessageBox()

        about.setIcon(QMessageBox.Information)
        about.setWindowTitle(f"PyHash Checker {version}")
        about.setText(f"PyHash Checker is an utility app to check the cryptographic checksum of a file."
                      f"\nMade using Python and PyQt5\n\nVersion: {version}\nAuthor: RBN")
        about.setInformativeText(f'<a href="https://github.com/PixelRBN/PyHash-Checker">Github</a>')

        about.exec_()


class Worker(QtCore.QObject):

    progress = QtCore.pyqtSignal(int)
    result = QtCore.pyqtSignal(str)

    @QtCore.pyqtSlot(str, int)
    def hash_file(self, fpath, method):
        size = 65536
        result_hash = ""

        md5 = hashlib.md5()
        sha1 = hashlib.sha1()
        sha224 = hashlib.sha224()
        sha256 = hashlib.sha256()
        sha384 = hashlib.sha384()
        sha512 = hashlib.sha512()

        try:
            with open(fpath, 'rb') as f:
                i = 0
                while True:
                    i += 1
                    self.progress.emit(i)

                    print(i)
                    data = f.read(size)
                    if not data:
                        break
                    if method == 0:
                        md5.update(data)
                    elif method == 1:
                        sha1.update(data)
                    elif method == 2:
                        sha224.update(data)
                    elif method == 3:
                        sha256.update(data)
                    elif method == 4:
                        sha384.update(data)
                    elif method == 5:
                        sha512.update(data)

                if method == 0:
                    result_hash = md5.hexdigest()
                    print(result_hash)
                if method == 1:
                    result_hash = sha1.hexdigest()
                if method == 2:
                    result_hash = sha224.hexdigest()
                if method == 3:
                    result_hash = sha256.hexdigest()
                if method == 4:
                    result_hash = sha384.hexdigest()
                if method == 5:
                    result_hash = sha512.hexdigest()

            self.result.emit(result_hash)
        except:
            pass


# TODO Kill the thread on closing or cancel


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
