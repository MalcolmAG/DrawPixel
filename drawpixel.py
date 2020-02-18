# This Python file uses the following encoding: utf-8
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenuBar, qApp, \
    QAction, QFileDialog, QAction, QLabel
from PyQt5.QtGui import QImage, QIcon, QPainter, QPen, QBrush, QPixmap
from PyQt5.QtCore import Qt, QPoint
from PyQt5 import QtCore, QtGui, QtWidgets
from Canvas import *

class DrawPixel(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.canvas = Canvas()
        self.setCentralWidget(self.canvas)

        self.initActions()
        self.initSizeActions()
        self.initColorActions()
        self.initMenu()

        self.setWindowTitle("Draw Pixel")
        self.resize(800, 600)

        # self.toolbar = QtWidgets.QToolBar("Size Bar", self)
        # self.toolbar.addAction("PlaceHolder")

        # self.sizeSlider = QtWidgets.QSlider(self)
        # self.toolbar.addWidget(self.sizeSlider)


    def initMenu(self):
        self.menubar = self.menuBar()

        self.fileMenu = self.menubar.addMenu("File")
        self.fileMenu.addAction(self.saveAct)

        self.editMenu = self.menubar.addMenu("Edit")
        self.editMenu.addAction(self.undoAct)
        self.editMenu.addAction(self.redoAct)
        self.editMenu.addSeparator()
        self.editMenu.addAction(self.clearAct)
        self.editMenu.addAction(self.debugAct)

        self.viewMenu = self.menubar.addMenu("View")
        self.viewMenu.addAction(self.zoomInAct)
        self.viewMenu.addAction(self.zoomOutAct)

        self.brushSizeMenu = self.menubar.addMenu("Brush Size")
        self.brushSizeMenu.addAction(self.threepxAction)
        self.brushSizeMenu.addAction(self.fivepxAction)
        self.brushSizeMenu.addAction(self.sevenpxAction)
        self.brushSizeMenu.addAction(self.ninepxAction)

        self.brushColorMenu = self.menubar.addMenu("Brush Color")
        self.brushColorMenu.addAction(self.yellowAction)
        self.brushColorMenu.addAction(self.blackAction)
        self.brushColorMenu.addAction(self.whiteAction)
        self.brushColorMenu.addAction(self.redAction)
        self.brushColorMenu.addAction(self.greenAction)

    def initActions(self):
        # Save Action
        self.saveAct = QAction("Save", self, shortcut = "Ctrl+S",
                          triggered=self.save)
        # Clear Action
        self.clearAct = QAction("Clear", self,
                                             triggered=self.canvas.clearScreen)
        # Debug Action
        self.debugAct = QAction("Debug Message", self,
                                     shortcut="Ctrl+D", triggered=lambda: self.printMessage(self.centralWidget()))
        # Undo
        self.undoAct = QAction("Undo", self, shortcut="Ctrl+Z",
                                         triggered=lambda:
                                         self.printMessage("Undo"))
        # Redo
        self.redoAct = QAction("Redo", self, shortcut="Ctrl+Shift+Z",
                                         triggered=lambda:
                                         self.printMessage("Redo"))
        self.zoomInAct = QAction("Zoom In", self,
                                          shortcut="Ctrl+Plus",
                                         triggered=lambda:
                                         self.printMessage("Zoom In"))
        self.zoomOutAct = QAction("Zoom Out", self,
                                          shortcut="Ctrl+Minus",
                                         triggered=lambda:
                                         self.printMessage("Zoom Out"))

    # TODO: Add size slider
    def initSizeActions(self):
        self.threepxAction = QAction(QIcon("icons/threepx.png"), "3px", self,
                                triggered=lambda: self.changeSize(3))
        self.fivepxAction = QAction(QIcon("icons/fivepx.png"), "5px", self,
                                    triggered=lambda: self.changeSize(5))
        self.sevenpxAction = QAction(QIcon("icons/sevenpx.png"), "7px", self,
                                    triggered=lambda: self.changeSize(7))
        self.ninepxAction = QAction(QIcon("icons/ninepx.png"), "9px", self,
                                    triggered=lambda: self.changeSize(9))
    def changeSize(self, size):
        self.canvas.setPenWidth(size)

    # TODO: Add Color Wheel
    def initColorActions(self):
        self.blackAction = QAction("Black", self, triggered=lambda: self.changeColor(Qt.black))
        self.whiteAction = QAction("White", self, triggered=lambda: self.changeColor(Qt.white))
        self.redAction = QAction("Red", self, triggered=lambda:self.changeColor(Qt.red))
        self.greenAction = QAction("Green", self, triggered=lambda:self.changeColor(Qt.green))
        self.yellowAction = QAction("Yellow", self, triggered=lambda:self.changeColor(Qt.yellow))
    def changeColor(self, color):
        self.canvas.setPenColor(color)

    def printMessage(self, message):
        print(message)

    # TODO: Add more File Types
    # TODO: Add compression option
    def save(self):
        filePath = QFileDialog.getSaveFileName(self, "Save Image", "",
                                                  "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) ")
        if filePath == "":
            return
        self.canvas.save(filePath)

if __name__ == "__main__":
    # Init Main App
    app = QApplication(sys.argv)

    # Main Window
    gui = DrawPixel()

    # Show & Only exit w/ user
    gui.show()
    sys.exit(app.exec_())
