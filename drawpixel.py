# This Python file uses the following encoding: utf-8
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenuBar, qApp, \
    QAction, QFileDialog, QAction
from PyQt5.QtGui import QImage, QIcon, QPainter, QPen, QBrush, QPixmap
from PyQt5.QtCore import Qt, QPoint
from PyQt5 import QtCore, QtGui, QtWidgets

class DrawPixel(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Window
        self.setObjectName("Draw Pixel")
        self.resize(800,600)

        # canvas
        self.canvas = QImage(800, 600, QImage.Format_RGB32)
        self.canvas.fill(Qt.white)

        # Default Properties
        self.drawing = False
        self.brushSize = 2
        self.brushColor = Qt.black
        self.lastPoint = QPoint()

        # self.toolbar = QtWidgets.QToolBar("Size Bar", self)
        # self.toolbar.addAction("PlaceHolder")

        # self.sizeSlider = QtWidgets.QSlider(self)
        # self.toolbar.addWidget(self.sizeSlider)

        self.initActions()
        self.initSizeActions()
        self.initColorActions()
        self.initMenu()

    # Make & Init Menu bar
    def initMenu(self):
        self.menubar = self.menuBar()

        self.fileMenu = self.menubar.addMenu("File")
        self.fileMenu.addAction(self.saveAct)

        self.editMenu = self.menubar.addMenu("Edit")
        self.editMenu.addAction(self.clearAct)
        self.editMenu.addAction(self.debugAct)

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
        self.clearAct = QtWidgets.QAction("Clear", self,
                                             triggered=self.clearScreen)
        # Debug Action
        self.debugAct = QtWidgets.QAction("Debug Message", self,
                                     shortcut="Ctrl+D", triggered=lambda: self.printMessage(self.centralWidget()))

    # Add & Change Sizes
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
        self.brushSize = size

    # TODO: Add Color Wheel
    def initColorActions(self):
        self.blackAction = QAction("Black", self, triggered=lambda: self.changeColor(Qt.black))
        self.whiteAction = QAction("White", self, triggered=lambda: self.changeColor(Qt.white))
        self.redAction = QAction("Red", self, triggered=lambda:self.changeColor(Qt.red))
        self.greenAction = QAction("Green", self, triggered=lambda:self.changeColor(Qt.green))
        self.yellowAction = QAction("Yellow", self, triggered=lambda:self.changeColor(Qt.yellow))
    def changeColor(self, color):
        self.brushColor = color

    def mousePressEvent(self, event):
        # If left mouse button pressed, set drawing mode & last pt
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.lastPoint = event.pos()

    def mouseMoveEvent(self, event):

        # if drawing mode
        if Qt.LeftButton & self.drawing:
            # Create QPainter & begin painting immediately on self.canvas
            painter = QPainter(self.canvas)

            # Set Pen Options
            painter.setPen(QPen(self.brushColor, self.brushSize,
                                Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            # Draw Line from last pt to this pt
            # Last Pt set during mouse pressed
            painter.drawLine(self.lastPoint, event.pos())

            # DEBUG
            print("Last: {0} \t Curr: {1}".format(self.lastPoint, event.pos()))


            #update last pt
            self.lastPoint = event.pos()

            # Redraw widget, in this case QMainWindow. Signals paintEvent
            self.update()

    def mouseReleaseEvent(self, event):
        # Set drawing mode off
        if event.button() == Qt.LeftButton:
            self.drawing = False

    def paintEvent(self, event):
        # Paint immediately onto self (e.g. QMainWindow)
        canvasPainter = QPainter(self)

        '''
        Draws the rectangular portion (source) of the given (image) into the
        (target) rectangle in the paint device : drawImage(target, image, 
        source)
        Draws canvas.rect of canvas onto QMainWindow.rect Only works cause 
        QMainWindow and Canvas are same size
        
        Note: The image is scaled to fit the rectangle, if image 
        and rectangle size disagree.
        '''

        canvasPainter.drawImage(self.rect(), self.canvas, self.canvas.rect())

        # DEBUG
        print("QMainWindow: {0} \t Canvas: {1}".format(self.rect(),
                                                       self.canvas.rect()))

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

    def clearScreen(self):
        self.canvas.fill(Qt.white)
        self.update()

if __name__ == "__main__":
    # Init Main App
    app = QApplication(sys.argv)

    # Main Window
    gui = DrawPixel()

    # Show & Only exit w/ user
    gui.show()
    sys.exit(app.exec_())