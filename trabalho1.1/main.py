"""
RafaelOliveira PyQt5 

Essa é uma aplciação que permite desenhar pontos, retas e polígonos;
Essa aplicação também permite movimentar e dar zoom na viewport 

Autor: Rafael Oliveira e Teo Haeser
Curso: INE5420 - Computacao Grafica
"""

import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QFrame, QSplitter, QApplication)
from PyQt5.QtGui import QIcon

class Example(QWidget):
    # construtor para a classe Exemplo
    def __init__(self):

        # super() chama o objeto da classe pai e seu construtor __init__()
        super().__init__()

        # cria a GUI
        self.initUI()
    
    def initUI(self):

        hbox = QHBoxLayout(self)

        # define o frame da direita onde ficará os botoes de comandos
        left = QFrame(self)
        left.setFrameShape(QFrame.StyledPanel)
        # define a cor de fundo do QFrame da direita VERDE
        left.setStyleSheet('QFrame{background: #8FB178}')

        # define o frame do topo da direita onde será a viewport
        topright = QFrame(self)
        topright.setFrameShape(QFrame.StyledPanel)
        # define a cor de fundo do QFrame que vai ficar no topo direita AZUL 
        topright.setStyleSheet('QFrame{background: #A4DDEE}')

        # define o frame de baixo da direita onde será a caixa de mensagens do sistema
        bottomright = QFrame(self)
        bottomright.setFrameShape(QFrame.StyledPanel)
        # define a cor de fundo do QFrame de baixo AMARELO
        bottomright.setStyleSheet('QFrame{background: #fce94f}')

        # define o primeiro Splitter a ser feito na vertical entre
        splitter1 = QSplitter(Qt.Vertical)
        splitter1.addWidget(topright)
        splitter1.addWidget(bottomright)


        splitter2 = QSplitter(Qt.Horizontal)
        splitter2.addWidget(left)
        splitter2.addWidget(splitter1)

        hbox.addWidget(splitter2)
        self.setLayout(hbox)

        # define o tamanho da janela e a posição (x=300, y=300, largura=450, altura=400 )
        self.setGeometry(300, 300, 450, 400)
        
        # define o titulo da janela
        self.setWindowTitle('Trabalho 1.1')
        
        # aplica o icone na janela
        self.setWindowIcon(QIcon('web.png')) 

        # mostra todos os widgets criados
        self.show()

def main():
    # cria a aplicacao PyQt
    app = QApplication(sys.argv)
    
    # cria uma instancia da classe Example
    ex = Example()

    # inicia a aplicacao app
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()