from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QImage, QPainter, QPen, QColor
from PyQt5.QtCore import Qt, QPoint, QSize

class Canvas(QWidget):

    def __init__(self):
        super().__init__()
        self.myPenWidth = 3
        self.myPenColor = QColor()
        self.myPenColor = Qt.black

        self.drawing = False
        self.modified = False
        self.lastPoint = QPoint()

        self.image = QImage(self.size(), QImage.Format_RGB32)
        self.image.fill(Qt.white)

        self.maybeSave = True

    # Drawing Options
    def setPenColor(self, color):
        self.myPenColor = color
    def penColor(self):
        return self.myPenColor

    def setPenWidth(self, width):
        self.myPenWidth = width

    def clearScreen(self):
        self.image.fill(Qt.white)
        self.modified = True
        self.update()

    # Painting Functions
    def mousePressEvent(self, mouseEvent):
        # If left mouse button pressed, set drawing mode & last pt
        if mouseEvent.button() == Qt.LeftButton:
            self.drawing = True
            self.lastPoint = mouseEvent.pos()

    def mouseMoveEvent(self, mouseEvent):
        # if drawing mode
        if Qt.LeftButton & self.drawing:
            self.drawLineTo(mouseEvent.pos())

    def mouseReleaseEvent(self, mouseEvent):
        # Set drawing mode off
        if (mouseEvent.button() == Qt.LeftButton and self.drawing):
            self.drawLineTo(mouseEvent.pos())
            self.drawing = False

    def paintEvent(self, paintEvent):
        # Paint immediately onto self (e.g. QWidget)
        painter = QPainter(self)
        dirtyRect = paintEvent.rect()
        painter.drawImage(dirtyRect, self.image, dirtyRect)

    def drawLineTo(self, endPoint):
        painter = QPainter(self.image)
        painter.setPen(QPen(self.myPenColor, self.myPenWidth,
                            Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        painter.drawLine(self.lastPoint, endPoint)

        self.modified = True
        self.update()
        self.lastPoint = endPoint


    # IO Functions
    def saveImage(self, fileName):
        visibleImage = self.image
        if visibleImage.save(fileName):
            self.modified = False
            return True
        else:
            return False

    def openImage(self, fileName):
        loadedImage = QImage(fileName)

        # Will run if image is corrupted
        if loadedImage is None:
            return False

        newSize = loadedImage.size()
        newSize.expandedTo(self.size()) # Finds max W/H

        self.resizeImage(newSize)
        self.image = loadedImage

        self.modified = False
        self.update()
        return True



    # View Functions
    def resizeEvent(self, resizeEvent):
        if self.width() > self.image.width() or self.height() > \
                self.image.height():
            newWidth = max(self.width() + 128, self.image.width())
            newHeight = max(self.height() + 128, self.image.height())
            self.resizeImage(QSize(newWidth, newHeight))
            self.update()

    def resizeImage(self, newSize):
        if self.image.size() == newSize:
            return

        newImage = QImage(newSize, QImage.Format_RGB32)
        newImage.fill(Qt.white)
        painter = QPainter(newImage)
        painter.drawImage(QPoint(0,0), newImage, newImage.rect())
        self.image = newImage