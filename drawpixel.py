# This Python file uses the following encoding: utf-8
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenuBar, qApp, \
    QAction, QFileDialog, QAction, QLabel, QMessageBox, QInputDialog, \
    QColorDialog, QToolBar, QSlider
from PyQt5.QtCore import Qt
from Canvas import *

class DrawPixel(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.canvas = Canvas()
        self.setCentralWidget(self.canvas)

        self.initActions()
        self.initMenu()

        self.setWindowTitle("Draw Pixel")
        self.resize(800, 600)

        self.toolbar = QToolBar("Size Bar", self)
        self.toolbar.addAction("PlaceHolder")

        self.sizeSlider = QSlider(self)
        self.toolbar.addWidget(self.sizeSlider)


    def initMenu(self):
        self.menubar = self.menuBar()

        self.fileMenu = self.menubar.addMenu("File")
        self.fileMenu.addAction(self.saveAct)
        self.fileMenu.addAction(self.openAct)

        self.editMenu = self.menubar.addMenu("Edit")
        self.editMenu.addAction(self.undoAct)
        self.editMenu.addAction(self.redoAct)
        self.editMenu.addSeparator()
        self.editMenu.addAction(self.clearAct)
        self.editMenu.addAction(self.debugAct)

        self.viewMenu = self.menubar.addMenu("View")
        self.viewMenu.addAction(self.zoomInAct)
        self.viewMenu.addAction(self.zoomOutAct)

        self.brushOptionsMenu = self.menubar.addMenu("Brush Options")
        self.brushOptionsMenu.addAction(self.brushWidthAct)
        self.brushOptionsMenu.addAction(self.brushColorAct)

    def initActions(self):
        # Open Action
        self.openAct = QAction("Open", self)
        self.openAct.setShortcut("Ctrl+O")
        self.openAct.triggered.connect(self.openFile)

        # Save Action
        self.saveAct = QAction("Save", self)
        self.saveAct.setShortcut("Ctrl+S")
        self.saveAct.triggered.connect(self.saveFile)

        # Clear Action
        self.clearAct = QAction("Clear", self)
        self.clearAct.triggered.connect(self.canvas.clearScreen)

        # Debug Action
        self.debugAct = QAction("Debug Message", self)
        self.debugAct.setShortcut("Ctrl+D")
        self.debugAct.triggered.connect(lambda: self.printMessage("DEBUG"))

        # Brush Width
        self.brushWidthAct = QAction("Brush Width", self)
        self.brushWidthAct.triggered.connect(self.setBrushWidth)

        self.brushColorAct = QAction("Brush Color", self)
        self.brushColorAct.triggered.connect(self.setBrushColor)

        # Undo
        self.undoAct = QAction("Undo", self)
        self.undoAct.setShortcut("Ctrl+Z")
        self.undoAct.triggered.connect(lambda: self.printMessage("Undo"))
        # Redo
        self.redoAct = QAction("Redo", self)
        self.redoAct.setShortcut("Ctrl+Shift+Z")
        self.redoAct.triggered.connect(lambda:
                                         self.printMessage("Redo"))
        # Zoom In
        self.zoomInAct = QAction("Zoom In", self)
        self.zoomInAct.setShortcut("Ctrl+Plus")
        self.zoomInAct.triggered.connect(lambda: self.printMessage("ZoomIn"))

        # Zoom Out
        self.zoomOutAct = QAction("Zoom Out", self)
        self.zoomOutAct.setShortcut("Ctrl+Minus")
        self.zoomOutAct.triggered.connect(lambda: self.printMessage(
            "ZoomOut"))

    def setBrushWidth(self):
        # returns tuple
        newWidth, ok = QInputDialog().getInt(self, "Scribble", "Select Pen "
                                                               "Width",  1,
                                             1, 50)
        if ok:
            self.canvas.setPenWidth(newWidth)

    def setBrushColor(self):
        newColor = QColorDialog().getColor(self.canvas.penColor(), self)
        if newColor.isValid():
            self.canvas.setPenColor(newColor)

    def openFile(self):
        filePath, fileFormat = QFileDialog.getOpenFileName(self, "Open File",
                                                         ".", "Images (*.png *.jpg)")
        if filePath == "":
            return False
        return self.canvas.openImage(filePath)

    # TODO: Add more File Types
    # TODO: Add compression option
    def saveFile(self):
        filePath, fileFormat = QFileDialog.getSaveFileName(self,
                                                          "Save Image", "",
                                                  "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) ")
        if filePath == "":
            return False
        return self.canvas.saveImage(filePath)

    def maybeSave(self):
        if self.canvas.modified:
            ret = QMessageBox().warning(self, "Scribble", "Image has been "
                                                     "modified \n Do you "
                                                          "want to save your changes?",
                                   QMessageBox.Save | QMessageBox.Discard |
                                   QMessageBox.Cancel)
            if ret == QMessageBox.Save:
                return self.saveFile()
            elif ret == QMessageBox.Cancel:
                return False
        return True

    def closeEvent(self, QCloseEvent):
        if self.maybeSave():
            QCloseEvent.accept()
        else:
            QCloseEvent.ignore()

def pa(strings):
    for message in strings:
        print(message, "\n")
def p(message):
    print(message)

if __name__ == "__main__":
    # Init Main App
    app = QApplication(sys.argv)

    # Main Window
    gui = DrawPixel()

    # Show & Only exit w/ user
    gui.show()

    sys.exit(app.exec_())