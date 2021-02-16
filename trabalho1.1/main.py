"""
RafaelOliveira PyQt5 

Essa é uma aplciação que permite desenhar pontos, retas e polígonos;
Essa aplicação também permite movimentar e dar zoom na viewport 

Autor: Rafael Oliveira e Teo Haeser
Curso: INE5420 - Computacao Grafica
"""

import sys
#from Drawings  TODO
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QFrame, QSplitter, QApplication)
from PyQt5.QtGui import QIcon

COLORS = [
# 17 undertones https://lospec.com/palette-list/17undertones
'#000000', '#141923', '#414168', '#3a7fa7', '#35e3e3', '#8fd970', '#5ebb49',
'#458352', '#dcd37b', '#fffee5', '#ffd035', '#cc9245', '#a15c3e', '#a42f3b',
'#f45b7a', '#c24998', '#81588d', '#bcb0c2', '#ffffff',
]

class Canvas(QtWidgets.QLabel):

    def __init__(self):
        super().__init__()
        pixmap = QtGui.QPixmap(700, 500)
        pixmap.fill(Qt.white)
        self.setPixmap(pixmap)
        self.function = 0
        self.function_map = {
            0: self.draw_point,
            1: self.draw_line,
            2: self.draw_polygon,
        }

        self.last_point = None
        self.pen_color = QtGui.QColor('#000000')

    def set_pen_color(self, c):
        self.pen_color = QtGui.QColor(c)
    
    def set_funciont(self, f):
        self.function = f
        self.last_point = None

    def create_object(self, posi, name):
        self.parentWidget().add_object(posi, name)

    def draw_point(self, posi):
        painter = QtGui.QPainter(self.pixmap())
        p = painter.pen()
        p.setWidth(4)
        p.setColor(self.pen_color)
        painter.setPen(p)
        painter.drawPoint(posi)
        painter.end()
        self.update()
        #self.create_object(posi, "point") TODO#

    def draw_line(self, posi):
        if not self.last_point:
            self.last_point = posi
        else:
            painter = QtGui.QPainter(self.pixmap())
            p = painter.pen()
            p.setWidth(4)
            p.setColor(self.pen_color)
            painter.setPen(p)
            painter.drawLine(self.last_point, posi)
            painter.end()
            self.update()
            self.last_point = None
        
    def draw_polygon(self, posi):
        if not self.last_point:
            self.last_point = posi
            self.first_point = posi
        else:
            self.draw_line(posi)
            self.last_point = posi

        # verify if the mouse was pressed
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = True
            a = self.function_map.get(self.function, lambda: 'Invalid')
            a(event.pos())
            #self.draw_point(event.pos())
            #self.lastPoint = event.pos()

            # print the pressed point
            print(self.last_point)
        else: 
            if self.function == 2:          # to close the polygon
                self.draw_polygon(self.first_point)
    
    # define the save function, to save the draw
    def save(self):
        filePath, _ = QtWidgets.QFileDialog.getSaveFileName(self, 'Save Image', '', 'PNG(*.png);;JPEG(*.jpg *.jpeg);; All Files(*.*)')
        if filePath == '':
            return
        self.pixmap.save(filePath)
    
    def clear(self):
        pixmap = QtGui.QPixmap(700, 500)
        pixmap.fill(Qt.white)
        self.setPixmap(pixmap)


class QPaletteButton(QtWidgets.QPushButton):

    def __init__(self, color):
        super().__init__()
        self.setFixedSize(QtCore.QSize(24,24))
        self.color = color
        self.setStyleSheet("background-color: %s;" % color)

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.objects = []       # list of tuples

        self.InitUI()

    def InitUI(self):    
        groupBoxMenuFuncoes = QtWidgets.QGroupBox("Menu Funções ")
        groupBoxMenuFuncoes.setFont(QtGui.QFont("Sanserif", 10))

        self.listDrawElements = QtWidgets.QListWidget()
        #sself.listDrawElements.setGeometry(10, 30, 171, 50)
        
        #self.listDrawElements.setGeometry(QtCore.QRect(10, 30, 171, 50))
        itemPonto = QtWidgets.QListWidgetItem("Ponto")
        self.listDrawElements.addItem(itemPonto)
        itemReta = QtWidgets.QListWidgetItem("Reta")
        self.listDrawElements.addItem(itemReta)
        itemPoligono = QtWidgets.QListWidgetItem("Polígono")
        self.listDrawElements.addItem(itemPoligono)

        self.label = QtWidgets.QLabel()

        vBoxMenuFuncoes = QtWidgets.QVBoxLayout()
        groupBoxWindow = QtWidgets.QGroupBox("Window")
        #groupBoxWindow.setGeometry(QtCore.QRect(10, 130, 171, 391))
        vBoxMenuFuncoes.addWidget(self.listDrawElements)
        vBoxMenuFuncoes.addWidget(groupBoxWindow)

        self.listDrawElements.clicked.connect(self.listview_clicked)
        vBoxMenuFuncoes.addWidget(self.label)

        groupBoxMenuFuncoes.setLayout(vBoxMenuFuncoes)

        vBoxWindow = QtWidgets.QHBoxLayout()
        plusButton = QtWidgets.QPushButton("+")
        minusButton = QtWidgets.QPushButton("-")
        vBoxWindow.addWidget(plusButton)
        vBoxWindow.addWidget(minusButton)

        groupBoxWindow.setLayout(vBoxWindow)

        debugTextBrowser = QtWidgets.QTextBrowser()
        self.canvas = Canvas()

        listObjects = QtWidgets.QListWidget()

        w = QtWidgets.QWidget()
        l = QtWidgets.QHBoxLayout()
        w.setLayout(l)

        palette = QtWidgets.QHBoxLayout()
        self.add_palette_buttons(palette)

        vertical = QtWidgets.QVBoxLayout()
        vertical.addWidget(self.canvas)
        vertical.addWidget(debugTextBrowser)
        vertical.addLayout(palette)

        l.addWidget(groupBoxMenuFuncoes)
        l.addLayout(vertical)
        l.addWidget(listObjects)
        
        #palette.addWidget(l)
        #l.addLayout(palette)

        # ============== MENU BAR ==================== #
        # instantiate the menu bar
        mainMenu = self.menuBar()
        # define a menu called 'File'
        fileMenu = mainMenu.addMenu('File')
        # define a menu called 'Brush Size'
        brushMenu = mainMenu.addMenu('Brush Size')
        # define a menu called 'Brush Color'
        brushColor = mainMenu.addMenu('Brush Color')

        # create a action called 'Save' and set an icon to it
        saveAction = QtWidgets.QAction(QtGui.QIcon('icons/save.png'), 'Save', self)
        # define a shortcut to the action 'Save'
        saveAction.setShortcut('Ctrl+s')
        # set the action created as submenu to the menu called 'filemenu'
        fileMenu.addAction(saveAction)
        saveAction.triggered.connect(self.canvas.save)

        clearAction = QtWidgets.QAction(QtGui.QIcon('icons/clear.png'), 'Clear', self)
        clearAction.setShortcut('Ctrl+c')
        fileMenu.addAction(clearAction)
        clearAction.triggered.connect(self.canvas.clear)

        threepxAction = QtWidgets.QAction(QtGui.QIcon('icons/threepx.png'), '3px', self)
        threepxAction.setShortcut('Ctrl+3')
        brushMenu.addAction(threepxAction)

        fivepxAction = QtWidgets.QAction(QtGui.QIcon('icons/fivepx.png'), '5px', self)
        fivepxAction.setShortcut('Ctrl+5')
        brushMenu.addAction(fivepxAction)

        sevenpxAction = QtWidgets.QAction(QtGui.QIcon('icons/sevenpx.png'), '7px', self)
        sevenpxAction.setShortcut('Ctrl+7')
        brushMenu.addAction(sevenpxAction)

        ninepxAction = QtWidgets.QAction(QtGui.QIcon('icons/ninepx.png'), '9px', self)
        ninepxAction.setShortcut('Ctrl+9')
        brushMenu.addAction(ninepxAction)

        redAction = QtWidgets.QAction(QtGui.QIcon('icons/red.png'), 'Red', self)
        redAction.setShortcut('Ctrl+r')
        brushColor.addAction(redAction)

        greenAction = QtWidgets.QAction(QtGui.QIcon('icons/green.png'), 'Green', self)
        greenAction.setShortcut('Ctrl+g')
        brushColor.addAction(greenAction)

        blackAction = QtWidgets.QAction(QtGui.QIcon('icons/black.png'), 'Black', self)
        blackAction.setShortcut('Ctrl+b')
        brushColor.addAction(blackAction)

        yellowAction = QtWidgets.QAction(QtGui.QIcon('icons/yellow.png'), 'Yellow', self)
        yellowAction.setShortcut('Ctrl+y')
        brushColor.addAction(yellowAction)

        self.setCentralWidget(w)
        self.show()

    def listview_clicked(self):
        item = self.listDrawElements.currentRow()
        self.canvas.set_funciont(item)
        print(item)
        self.label.setText(str(item))

    '''
    # define the save function, to save the draw
    def save(self):
        filePath, _ = QtWidgets.QFileDialog.getSaveFileName(self, 'Save Image', '', 'PNG(*.png);;JPEG(*.jpg *.jpeg);; All Files(*.*)')
        if filePath == '':
            return
        self.canvas.save(filePath)
    '''

    def add_palette_buttons(self, layout):
        for c in COLORS:
            b = QPaletteButton(c)
            b.pressed.connect(lambda c=c: self.canvas.set_pen_color(c))
            layout.addWidget(b)

    def add_object(self, obj, name):
        name = name + str(self.listObjects.count())
        self.objects.append([name, [posi]])
        itemPoligono = QtWidgets.QListWidgetItem(name)
        self.listObjects.addItem(itemPoligono)
        self.update()
        

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    # window.show()
    #app.exec_()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
