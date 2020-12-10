import sys
from PyQt5.QtWidgets import (
    QApplication,
    QFileDialog,
    QGridLayout,
    QPushButton,
    QLineEdit,
    QWidget
)


class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QGridLayout()

        self.iTargetFolder = QLineEdit()
        self.iTargetFolder.setReadOnly(False)

        self.iMusescoreUrl = QLineEdit()
        self.iMusescoreUrl.setPlaceholderText("Paste Musescore URL")

        self.bDownload = QPushButton("Download")

        self.bSelectTargetFolder = QPushButton("Select")
        self.row = 0
        self.buildUi()
        self.assignFunctions()

    def inCurrentRow(self):
        return self.row

    def inNextRow(self):
        self.row += 1
        return self.row

    def buildUi(self):
        self.iTargetFolder.setPlaceholderText("Please select a folder.")

        self.layout.addWidget(self.iTargetFolder, self.inCurrentRow(), 0, 1, 2)
        self.layout.addWidget(self.bSelectTargetFolder, self.inCurrentRow(), 2)
        self.layout.addWidget(self.iMusescoreUrl, self.inNextRow(), 0, 1, 3)

        self.layout.addWidget(self.bDownload, self.inNextRow(), 1)

        self.setLayout(self.layout)


    def assignFunctions(self):
        self.bSelectTargetFolder.clicked.connect(self.selectFolder)

    def selectFolder(self):
        folder = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        print(folder)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
