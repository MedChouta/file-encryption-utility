import sys
import os
from PyQt4 import QtGui, QtCore
from functools import partial
import main as entry

class Window(QtGui.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.setGeometry(50, 50, 341, 509)
        self.setFixedSize(341, 509)
        self.setWindowTitle("Encryption utility")

        self.home()
    
    def home(self):
        #image
        logoSize = 120
        self.logo = QtGui.QLabel(self)
        self.logo.setGeometry(341/2 - logoSize/2, 10, logoSize, logoSize)
        self.logo.setPixmap(QtGui.QPixmap(os.getcwd() + "/logo.png"))

        #File search bar
        self.labelFichier = QtGui.QLabel("File:", self)
        self.labelFichier.move(10, 143)

        self.searchBar = QtGui.QLineEdit(self)
        self.searchBar.resize(241, 21)
        self.searchBar.move(50, 147)

        #Search file button
        self.fileButton = QtGui.QToolButton(self)
        self.fileButton.clicked.connect(self.openFile)
        self.fileButton.setText("...")
        self.fileButton.resize(31, 24)
        self.fileButton.move(300, 145)


        #Recent files
        self.labelRecent = QtGui.QLabel("Recent files:", self)
        self.labelRecent.move(5, 180)

        self.recentFile = QtGui.QListWidget(self)
        self.recentFile.itemDoubleClicked.connect(self.autoSearch)
        self.recentFile.resize(321, 211)
        self.recentFile.move(10, 210)
        self.readRecent()

        self.fileName = str()

        #Encrypt/Decrypt Buttons
        self.encryptButton = QtGui.QPushButton("Encrypt", self)
        self.encryptButton.clicked.connect(self.encrypt)
        self.encryptButton.move(20, 450)

        self.decryptButton = QtGui.QPushButton("Decrypt", self)
        self.decryptButton.clicked.connect(self.decrypt)
        self.decryptButton.move(221, 450)

        self.show()

    def openFile(self):
        name = QtGui.QFileDialog.getOpenFileName(self,"Open File")
        self.searchBar.setText(name)
        self.fileName = self.searchBar.text()
    
    def encrypt(self):
        key = self.enterKey().encode()
        try:
            entry.encrypt(self.fileName, key)
            self.fileName = self.fileName + ".enc"
            self.addRecent()
            self.readRecent()
        except(FileNotFoundError):
            QtGui.QMessageBox.critical(self, "Error", "The specified file was not found")

        self.searchBar.setText("")
        self.fileName = ""
    
    def decrypt(self):
        key = self.enterKey().encode()
        entry.decrypt(self.fileName, key)
        self.fileName = self.fileName[:-4]
        self.addRecent()
        self.readRecent()
        self.searchBar.setText("")
        self.fileName = ""

    def enterKey(self):
        password, ok = QtGui.QInputDialog.getText(self, "Password", "Please enter a password:")
        
        if ok:
            return password

    def addRecent(self):
        with open("recent", "a+") as recent:
            recent.write(self.fileName+"\n")
            

    def readRecent(self):
        self.recentFile.clear()
        with open("recent", "r") as recent:
            paths = recent.read().split("\n")
            #paths = paths.split("\n")
            paths = filter(None, set(paths))
            #paths = filter(None, paths)
            paths = list(paths)
            paths = self.fileExists(paths)
            self.recentFile.addItems(paths)

    def autoSearch(self, item):
         self.searchBar.setText(item.text())
         self.fileName = self.searchBar.text()
    
    def fileExists(self, fileList):
        """ Checks if a file exists to filter the Recent files list
            or to stop Encryption/Decryption if the file does not exist
         """
        
        for file in fileList:
            try:
                with open(file, "r"):
                    pass
            except(FileNotFoundError):
                fileList.remove(file)

        return fileList

    
def main():
    app = QtGui.QApplication(sys.argv)
    GUI = Window()
    sys.exit(app.exec_())

main()
