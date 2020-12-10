import sys
from PyQt5.QtWidgets import (
    QApplication,
    QCheckBox,
    QFileDialog,
    QGridLayout,
    QPushButton,
    QLineEdit,
    QWidget
)
from optionhandler import OptionHandler

class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.optionHandler = OptionHandler()

        self.layout = QGridLayout()

        self.iTargetFolder = QLineEdit()
        self.iTargetFolder.setReadOnly(False)
        if self.optionHandler.has("targetDir"):
            self.iTargetFolder.setText(self.optionHandler.get("targetDir"))

        self.iMusescoreUrl = QLineEdit()
        self.iMusescoreUrl.setPlaceholderText("Paste Musescore URL")

        self.cbSaveImg = QCheckBox("Save Images")
        self.cbSavePdf = QCheckBox("Save PDF")

        self.bDownload = QPushButton("Download")
        self.bDownload.setEnabled(False)

        self.bSelectTargetFolder = QPushButton("Select")
        self.row = 0
        self.buildUi()
        self.assignFunctions()

    def inCurrentRow(self):
        return self.row

    def inNextRow(self):
        self.row += 1
        return self.row

    def checkUrl(self):
        self.bDownload.setEnabled(self.iMusescoreUrl.text() != "")

    def buildUi(self):
        self.iTargetFolder.setPlaceholderText("Please select a folder.")

        self.layout.addWidget(self.iTargetFolder, self.inCurrentRow(), 0, 1, 2)
        self.layout.addWidget(self.bSelectTargetFolder, self.inCurrentRow(), 2)
        self.layout.addWidget(self.iMusescoreUrl, self.inNextRow(), 0, 1, 3)

        self.layout.addWidget(self.cbSaveImg, self.inNextRow(), 0)
        self.layout.addWidget(self.cbSavePdf, self.inCurrentRow(), 1)
        self.layout.addWidget(self.bDownload, self.inCurrentRow(), 2)

        self.setLayout(self.layout)

    def assignFunctions(self):
        self.bSelectTargetFolder.clicked.connect(self.selectFolder)
        self.iMusescoreUrl.textChanged.connect(self.checkUrl)

    def selectFolder(self):
        folder = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        if folder:
            self.optionHandler.set("targetDir", folder)
        self.iTargetFolder.setText(folder)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
