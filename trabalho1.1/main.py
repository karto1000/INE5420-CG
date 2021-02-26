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
from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QFrame, QSplitter, QApplication, QLabel)
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
        # self.function_map = {
        #     0: self.draw_point,
        #     1: self.draw_line,
        #     2: self.draw_polygon,
        # }

        self.last_point = None
        self.pen_color = QtGui.QColor('#000000')
        self.scale = 1

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

        ### List of functions ###
        self.listDrawElements = QtWidgets.QListWidget()

        itemPonto = QtWidgets.QListWidgetItem("Ponto")
        self.listDrawElements.addItem(itemPonto)
        itemReta = QtWidgets.QListWidgetItem("Reta")
        self.listDrawElements.addItem(itemReta)
        itemPoligono = QtWidgets.QListWidgetItem("Polígono")
        self.listDrawElements.addItem(itemPoligono)
        itemRotate = QtWidgets.QListWidgetItem("Rotate")
        self.listDrawElements.addItem(itemRotate)
        itemScale = QtWidgets.QListWidgetItem("Scale")
        self.listDrawElements.addItem(itemScale)
        self.listDrawElements.clicked.connect(self.listview_clicked)
        ### List of functions ###

        ### Objects ###
        
        self.listObjects = QtWidgets.QListWidget()
        self.labelObjects = QLabel("Objects")
        ### Objects ###
        
        ### Left Box ###
        vBoxMenuFuncoes = QtWidgets.QVBoxLayout()

        vBoxMenuFuncoes.addWidget(self.listDrawElements)
        vBoxMenuFuncoes.addWidget(self.labelObjects)
        vBoxMenuFuncoes.addWidget(self.listObjects)
        groupBoxWindow = QtWidgets.QGroupBox("Window")
        vBoxMenuFuncoes.addWidget(groupBoxWindow)
        self.label = QtWidgets.QLabel()
        vBoxMenuFuncoes.addWidget(self.label)
        groupBoxMenuFuncoes.setLayout(vBoxMenuFuncoes)
        ### Left Box ###

        

        ### Transformations ###
        vBoxWindow = QtWidgets.QHBoxLayout()

        plus = QtWidgets.QPushButton("+")
        minus = QtWidgets.QPushButton("-")
        vBoxWindow.addWidget(plus)
        vBoxWindow.addWidget(minus)
        groupBoxWindow.setLayout(vBoxWindow)
        ### Transformations ###

        ### Interactions ###
        debugTextBrowser = QtWidgets.QTextBrowser()
        self.canvas = Canvas()
        w = QtWidgets.QWidget()
        l = QtWidgets.QHBoxLayout()
        w.setLayout(l)
        # # dá zoom in na tela
        # zoomInButton.clicked.connect(self.canvas.on_zoom_in)
        # # dá zoom out na tela
        # zoomOutButton.clicked.connect(self.canvas.on_zoom_out)
        
        palette = QtWidgets.QHBoxLayout()
        self.add_palette_buttons(palette)

        ### Interactions ###

        ### Left Part ###
        vertical = QtWidgets.QVBoxLayout()
        
        vertical.addWidget(self.canvas)
        vertical.addWidget(debugTextBrowser)
        vertical.addLayout(palette)
        ### Left Part ###

        l.addWidget(groupBoxMenuFuncoes)
        l.addLayout(vertical)
        w.setFixedSize(800,600)

        self.setCentralWidget(w)
        self.show()

    def listview_clicked(self):
        item = self.listDrawElements.currentRow()

        self.canvas.set_funciont(item)
        print(item)
        self.label.setText(str(item))

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
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
