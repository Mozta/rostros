# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created: Sun Sep 23 22:10:20 2015
#      by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

# Import para la detección
import copy
import numpy as np
import cv2

# Variables globales
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')

img = ""
crop_img = []
cont_i = 0

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

class Ui_CipherImageForm(object):
    def setupUi(self, CipherImageForm):
        CipherImageForm.setObjectName(_fromUtf8("CipherImageForm"))
        CipherImageForm.resize(1194, 787)
        self.rawImageView = QtGui.QGraphicsView(CipherImageForm)
        self.rawImageView.setGeometry(QtCore.QRect(180, 20, 1000, 750))
        self.rawImageView.setObjectName(_fromUtf8("rawImage"))
        self.openImageButton = QtGui.QPushButton(cipherImageViewForm)
        self.openImageButton.setGeometry(QtCore.QRect(20, 20, 131, 28))
        self.openImageButton.setObjectName(_fromUtf8("openImageButton"))
        self.encryptButton = QtGui.QPushButton(cipherImageViewForm)
        self.encryptButton.setGeometry(QtCore.QRect(20, 70, 131, 28))
        self.encryptButton.setObjectName(_fromUtf8("encryptButton"))
        self.saveImageButton = QtGui.QPushButton(cipherImageViewForm)
        self.saveImageButton.setGeometry(QtCore.QRect(20, 120, 131, 28))
        self.saveImageButton.setObjectName(_fromUtf8("saveImageButton"))

        self.rawImage = QtGui.QImage()
        self.cipherImage = QtGui.QImage()
        self.number_char = 255

        self.retranslateUi(cipherImageViewForm)
        QtCore.QObject.connect(self.openImageButton, QtCore.SIGNAL(_fromUtf8("clicked()")), self.abrir_imagen)
        QtCore.QObject.connect(self.saveImageButton, QtCore.SIGNAL(_fromUtf8("clicked()")), self.guardar_imagen)
        QtCore.QObject.connect(self.encryptButton, QtCore.SIGNAL(_fromUtf8("clicked()")), self.buscaRostros)


    def retranslateUi(self, CipherImageForm):
        CipherImageForm.setWindowTitle(_translate("CipherImageForm", "Identificación de Características para la Detección de Rostros Humanos", None))
        self.openImageButton.setText(_translate("CipherImageForm", "Abrir Imagen", None))
        self.encryptButton.setText(_translate("CipherImageForm", "Buscar Rostros", None))
        self.saveImageButton.setText(_translate("CipherImageForm", "Guardar Imagen", None))

    def abrir_imagen(self):
        # Limpiamos las vistas de imagenes
        if self.rawImageView.scene() != None:
            self.rawImageView.scene().clear()

        # Abrimos un cuadro de diálogo para escoger la imagen
        filters = "All files (*.*);;Images (*.png *.bmp *.jpg)"
        selected_filter = "Images (*.png *.bmp *.jpg)"
        imageName = QtGui.QFileDialog.getOpenFileName(None, "Abrir imagen", "", filters, selected_filter)
        #print unicode(imageName)
        route = unicode(self.parseo(imageName))
        print route

        # Abrimos la imagen para mostrar
        image = QtGui.QImage(imageName)
        # Cargamos la plantilla
        
        # Abrimos la imagen con opencv
        global img
        img = cv2.imread(route)

        # Generamos una escena, que cargara la imagen y se mostrará en la vista
        scene = QtGui.QGraphicsScene()
        item = QtGui.QGraphicsPixmapItem(QtGui.QPixmap.fromImage(self.cvImgToQtImg(img)))
        self.rawImageView.setScene(scene)
        # Adaptamos el tamaño de la imagen
        self.rawImageView.fitInView(item)
        
        scene.addItem(item)

        # Asignamos la imagen temporal a la imagen de trabajo
        self.rawImage = image
        self.cipherImage = image

    def guardar_imagen(self):
        global img
        global cont_i
        global crop_img

        # Abrimos un cuadro de dialogo para guardar la imagen en formato png
        imageName = QtGui.QFileDialog.getSaveFileName(None , "Save Image", "", "png (*.png)")
        print unicode(imageName)
        if not imageName.endsWith(".png"):
            imageName += ".png"

        # Con ImageWriter podemos configurar los parámetros de guardado de la imagen
        imagefile = QtGui.QImageWriter()
        imagefile.setFileName(imageName)
        imagefile.setFormat("png")
        # Guardamos la imagen
        imagefile.write(self.cvImgToQtImg(img))

        #Guardamos las mini imagenes
        for x in crop_img:
            cv2.imwrite(self.parseo(unicode(imageName)).rstrip(".png")+'_'+str(cont_i)+'.png',self.redimensionar_imagen(crop_img[cont_i]))
            cont_i += 1

    def redimensionar_imagen(self, image):
        resized_image = cv2.resize(image, (300, 300)) 
        return resized_image



    def encapsular(self):
        # Sobre escribimos la imagen
        scene = QtGui.QGraphicsScene()
        item = QtGui.QGraphicsPixmapItem(QtGui.QPixmap.fromImage(self.cipherImage))
        self.rawImageView.setScene(scene)
        self.rawImageView.fitInView(item)
        
        scene.addItem(item)
        print "Encapsulado finalizado"


    def parseo(self,ruta):
        return ruta.replace("/","\\")

    def buscaRostros(self):
        global face_cascade
        global img
        global cont_i
        global crop_img


        #convertimos la imagen a blanco y negro
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 

        #buscamos las coordenadas de los rostros  y
        #guardamos su posicion
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        print faces
        #Dibujamos un rectangulo en las coordenadas de cada rostro
        for (x,y,w,h) in faces:
            cv2.rectangle(img,(x,y),(x+w,y+h),(125,255,0),2)
            #crop_img = img[x:y,x+w:y+h]
            crop_img.append(img[y:y+h,x:x+w])

        #Abrimos el archivo contador
        archi=open('C:\Users\Rafael\Documents\Servicio Social\Tracking\contador.txt','r')
        c=int(archi.readline())
        archi.close()
        archi=open('C:\Users\Rafael\Documents\Servicio Social\Tracking\contador.txt','w')
        c+=1
        archi.write(str(c))
        archi.close()

        #Guardamos la imagen por default
        cv2.imwrite('C:\Users\Rafael\Documents\Servicio Social\Tracking\FotosProcesadas\img'+str(c)+'.jpg',img)
        cv2.destroyAllWindows()

        # Sobre escribimos la imagen
        scene = QtGui.QGraphicsScene()
        item = QtGui.QGraphicsPixmapItem(QtGui.QPixmap.fromImage(self.cvImgToQtImg(img)))
        self.rawImageView.setScene(scene)
        self.rawImageView.fitInView(item)
        
        scene.addItem(item)
        print "Deteccion finalizada"

    def cvImgToQtImg(self, image):
        #Convierte la imagen de openCV a una imagen qT
        '''
        (cvImage) -> qtImage
        '''
        cvImage = copy.deepcopy(image)
        height, width, byteValue = cvImage.shape
        byteValue = byteValue * width

        cv2.cvtColor(cvImage, cv2.COLOR_BGR2RGB, cvImage)

        return QtGui.QImage(cvImage, width, height, byteValue, QtGui.QImage.Format_RGB888)


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    cipherImageViewForm = QtGui.QWidget()
    ui = Ui_CipherImageForm()
    ui.setupUi(cipherImageViewForm)
    cipherImageViewForm.show()
    sys.exit(app.exec_())
