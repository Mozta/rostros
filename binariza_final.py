# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'binariza.ui'
#
# Created: Thu Sep  3 16:00:14 2015
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

# Mis import
import copy
import numpy as np
import cv2

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(664, 451)
        self.gridLayout = QtGui.QGridLayout(Form)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.graphicsView = QtGui.QGraphicsView(Form)
        self.graphicsView.setObjectName(_fromUtf8("graphicsView"))
        self.horizontalLayout.addWidget(self.graphicsView)
        self.abrir_btn = QtGui.QPushButton(Form)
        self.abrir_btn.setObjectName(_fromUtf8("abrir_btn"))
        self.horizontalLayout.addWidget(self.abrir_btn)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.horizontalSlider = QtGui.QSlider(Form)
        self.horizontalSlider.setMaximum(255)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName(_fromUtf8("horizontalSlider"))
        self.horizontalLayout_2.addWidget(self.horizontalSlider)
        self.guardar_btn = QtGui.QPushButton(Form)
        self.guardar_btn.setObjectName(_fromUtf8("guardar_btn"))
        self.horizontalLayout_2.addWidget(self.guardar_btn)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.label = QtGui.QLabel(Form)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QObject.connect(self.horizontalSlider, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.label.setNum)
        QtCore.QObject.connect(self.abrir_btn, QtCore.SIGNAL(_fromUtf8("clicked()")), self.abrir_imagen)
        QtCore.QObject.connect(self.guardar_btn, QtCore.SIGNAL(_fromUtf8("clicked()")), self.guardar_imagen)
        QtCore.QObject.connect(self.horizontalSlider, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.cambio_barra)
        QtCore.QMetaObject.connectSlotsByName(Form)
        Form.setTabOrder(self.abrir_btn, self.guardar_btn)
        Form.setTabOrder(self.guardar_btn, self.horizontalSlider)
        Form.setTabOrder(self.horizontalSlider, self.graphicsView)

        # Mias!!!
        self.qtImage = QtGui.QImage()
        self.cvImage = np.zeros((0,0,3), np.uint8) # cvImage vacia
        self.img_cargada = False

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "By JordyCuan", None))
        self.abrir_btn.setText(_translate("Form", "Abrir Imagen", None))
        self.guardar_btn.setText(_translate("Form", "Guardar Imagen", None))
        self.label.setText(_translate("Form", "0", None))

    def abrir_imagen(self):
        print "abrir_imagen"

        # Abrimos un cuadro de diálogo para escoger la imagen
        imageName = QtGui.QFileDialog.getOpenFileName()
        print unicode(imageName)

        if imageName == "":
            print "No selected image :("
            return

        if self.graphicsView.scene() != None:
            self.graphicsView.scene().clear()

        #qtImageName = [str(x) for x in imageName]
        qtImageName = str(imageName)
        self.cvImage = cv2.imread(qtImageName)
        # cv2.imshow("ImPrueba", self.cvImage)

        # Abrimos la imagen
        cvImage = copy.deepcopy(self.cvImage)
        height, width, byteValue = cvImage.shape
        byteValue = byteValue * width

        cv2.cvtColor(cvImage, cv2.COLOR_BGR2RGB, cvImage)

        image = QtGui.QImage(cvImage, width, height, byteValue, QtGui.QImage.Format_RGB888)
        # image = QtGui.QImage(imageName)
        # Generamos una escena, que cargara la imagen y se mostrará en la vista
        # scene = QtGui.QGraphicsScene()
        # item = QtGui.QGraphicsPixmapItem(QtGui.QPixmap.fromImage(image))
        # self.graphicsView.setScene(scene)
        # Adaptamos el tamaño de la imagen
        # self.graphicsView.fitInView(item)

        # scene.addItem(item)
        # cv2.imshow("ImPrueba", self.cvImage)
        self.mostrarImgUI(image)
        self.img_cargada = True 


    def guardar_imagen(self):
        if not self.img_cargada:
            return

        # Abrimos un cuadro de dialogo para guardar la imagen en formato JPG
        imageName = QtGui.QFileDialog.getSaveFileName(None , "Save Image", "", "JPG (*.JPG)")
        print unicode(imageName)
        if not imageName.endsWith(".JPG"):
            imageName += ".JPG"

        # Guardamos la imagen
        cv2.imwrite(str(imageName), self.cvImage)

        # imagefile = QtGui.QImageWriter()
        # imagefile.setFileName(imageName)
        # imagefile.setFormat("png")
        # Guardamos la imagen
        # imagefile.write(self.qtImage)


    def cambio_barra(self, valor):
        # print "cambio_barra", valor
        img = copy.deepcopy(self.cvImage)
        h, w, c = img.shape

        for y in xrange(h):
            for x in xrange(w):
                l = ( img.item(y,x,0) , img.item(y,x,1) , img.item(y,x,2) )
                prom = np.mean( l ) # promedio
                if prom > valor:
                    img.itemset((y,x,0), 255) # blanco
                    img.itemset((y,x,1), 255)
                    img.itemset((y,x,2), 255)
                else:
                    img.itemset((y,x,0), 0) # negro
                    img.itemset((y,x,1), 0) 
                    img.itemset((y,x,2), 0) 

        self.mostrarImgUI( self.cvImgToQtImg(img) )



    def cvImgToQtImg(self, image):
        '''
        (cvImage) -> qtImage
        '''
        cvImage = copy.deepcopy(image)
        height, width, byteValue = cvImage.shape
        byteValue = byteValue * width

        cv2.cvtColor(cvImage, cv2.COLOR_BGR2RGB, cvImage)

        return QtGui.QImage(cvImage, width, height, byteValue, QtGui.QImage.Format_RGB888)

    def mostrarImgUI(self, image):
        scene = QtGui.QGraphicsScene()
        item = QtGui.QGraphicsPixmapItem(QtGui.QPixmap.fromImage(image))
        self.graphicsView.setScene(scene)
        # Adaptamos el tamaño de la imagen
        self.graphicsView.fitInView(item)

        scene.addItem(item)



if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Form = QtGui.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

