from PyQt5.QtWidgets import QApplication, QMainWindow, QMenuBar, qApp, \
    QAction, QFileDialog, QAction, QWidget
from PyQt5.QtGui import QImage, QIcon, QPainter, QPen, QBrush, QPixmap, QColor
from PyQt5.QtCore import Qt, QPoint
from PyQt5 import QtCore, QtGui, QtWidgets


class Canvas(QWidget):

    def __init__(self):
        super().__init__()
        self.myPenWidth = 1
        self.myPenColor = QColor()
        self.myPenColor = Qt.black

        self.drawing = False
        self.modified = False
        self.lastPoint = QPoint()

        self.image = QImage(self.size(), QImage.Format_RGB32)
        self.image.fill(Qt.white)

    def setPenColor(self, color):
        self.myPenColor = color

    def setPenWidth(self, width):
        self.myPenWidth = width

    def clearScreen(self):
        self.image.fill(Qt.white)
        self.modified = True
        self.update()

    def mousePressEvent(self, event):
        # If left mouse button pressed, set drawing mode & last pt
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.lastPoint = event.pos()

    def mouseMoveEvent(self, event):

        # if drawing mode
        if Qt.LeftButton & self.drawing:
            self.drawLineTo(event.pos())

    def mouseReleaseEvent(self, event):
        # Set drawing mode off
        if (event.button() == Qt.LeftButton and self.drawing):
            self.drawLineTo(event.pos())
            self.drawing = False

    def paintEvent(self, event):
        # Paint immediately onto self (e.g. QMainWindow)
        painter = QPainter(self)
        dirtyRect = event.rect()
        painter.drawImage(dirtyRect, self.image, dirtyRect)

    def drawLineTo(self, endPoint):
        painter = QPainter(self.image)
        painter.setPen(QPen(self.myPenColor, self.myPenWidth,
                            Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        painter.drawLine(self.lastPoint, endPoint)

        self.modified = True
        self.update()
        self.lastPoint = endPoint
