import sys
from PyQt4 import QtGui, QtCore
from functools import partial
import main as entry

class Window(QtGui.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.setGeometry(50, 50, 341, 509)
        self.setWindowTitle("Encryption utility")

        self.home()
    
    def home(self):
        self.labelFichier = QtGui.QLabel("Fichier:", self)
        self.labelFichier.move(5, 143)

        self.searchBar = QtGui.QLineEdit(self)
        self.searchBar.resize(241, 21)
        self.searchBar.move(50, 147)

        self.fileButton = QtGui.QToolButton(self)
        self.fileButton.clicked.connect(self.openFile)
        self.fileButton.setText("...")
        self.fileButton.resize(31, 24)
        self.fileButton.move(300, 145)

        self.labelRecent = QtGui.QLabel("Récent:", self)
        self.labelRecent.move(5, 180)

        self.recentFile = QtGui.QListWidget(self)
        self.recentFile.resize(321, 211)
        self.recentFile.move(10, 210)
        self.readRecent()

        self.fileName = str()

        self.encryptButton = QtGui.QPushButton("Chiffrer", self)
        self.encryptButton.clicked.connect(self.encrypt)
        self.encryptButton.move(20, 450)

        self.decryptButton = QtGui.QPushButton("Déchiffrer", self)
        self.decryptButton.clicked.connect(self.decrypt)
        self.decryptButton.move(221, 450)

        self.show()

    def openFile(self):
        name = QtGui.QFileDialog.getOpenFileName(self,"Open File")
        self.searchBar.setText(name)
        self.fileName = self.searchBar.text()
    
    def encrypt(self):
        key = self.enterKey().encode()
        entry.encrypt(self.fileName, key)
        self.fileName = self.fileName + ".enc"
        self.addRecent()
        self.readRecent()
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
        password, ok = QtGui.QInputDialog.getText(self, "chiffrement", "Veuillez entrer un mot de passe:")
        
        if ok:
            return password

    def addRecent(self):
        with open("recent", "a+") as recent:
            recent.write(self.fileName+"\n")
            

    def readRecent(self):
        with open("recent", "r") as recent:
            content = recent.read()
            uniq = content.split("\n")
            uniq = set(uniq)
            uniq = list(uniq)
            print(uniq)
            itemList =  [self.recentFile.item(i).text() for i in range(self.recentFile.count())]
            print(itemList)
            for item in itemList:
                for uItem in uniq:
                    if item != uItem:
                        self.recentFile.addItems(item)       
    
def main():
    app = QtGui.QApplication(sys.argv)
    GUI = Window()
    sys.exit(app.exec_())

main()
