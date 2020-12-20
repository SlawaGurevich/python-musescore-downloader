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
from scraper import Scraper
from downloader import Downloader

class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Musescore PDF Downloader")
        self.setFixedSize(350, 140)

        self.optionHandler = OptionHandler()
        self.scraper = Scraper()
        self.downloader = Downloader()

        self.layout = QGridLayout()

        self.iTargetFolder = QLineEdit()
        self.iTargetFolder.setReadOnly(False)
        if self.optionHandler.has("targetDir"):
            self.iTargetFolder.setText(self.optionHandler.get("targetDir"))

        self.iMusescoreUrl = QLineEdit()
        self.iMusescoreUrl.setPlaceholderText("Paste Musescore URL")

        self.cbSaveImg = QCheckBox("Save Images")

        if self.optionHandler.has("saveImages"):
            self.cbSaveImg.setChecked(self.optionHandler.get("saveImages") == "yes")

        self.cbSavePdf = QCheckBox("Save PDF")

        if self.optionHandler.has("savePdf"):
            self.cbSavePdf.setChecked(self.optionHandler.get("savePdf") == "yes")

        self.bDownload = QPushButton("Download")

        self.bSelectTargetFolder = QPushButton("Select")
        self.row = 0
        self.buildUi()
        self.checkUrl()
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
        self.bDownload.clicked.connect(self.startDownload)
        self.cbSaveImg.clicked.connect(self.setSaveImages)
        self.cbSavePdf.clicked.connect(self.setSavePdf)

    def startDownload(self):
        files = self.scraper.scrape(self.iMusescoreUrl.text().strip().split(","))
        self.downloader.download(files, self.iTargetFolder.text(), saveImages=self.cbSaveImg.isChecked(), savePdf=self.cbSavePdf.isChecked())

    def selectFolder(self):
        folder = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        if folder:
            self.optionHandler.set("targetDir", folder)
        self.iTargetFolder.setText(folder)

    def setSaveImages(self):
        if self.cbSaveImg.isChecked():
            value="yes"
        else:
            value="no"
        self.optionHandler.set("saveImages", value)

    def setSavePdf(self):
        if self.cbSavePdf.isChecked():
            value="yes"
        else:
            value="no"
        self.optionHandler.set("savePdf", value)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
