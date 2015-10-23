# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created: Sun Nov 23 22:10:20 2014
#      by: PyQt4 UI code generator 4.10.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

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
        self.messageLabel = QtGui.QLabel(cipherImageViewForm)
        self.messageLabel.setGeometry(QtCore.QRect(40, 343, 61, 16))
        self.messageLabel.setObjectName(_fromUtf8("messageLabel"))
        self.messageEdit = QtGui.QLineEdit(cipherImageViewForm)
        self.messageEdit.setGeometry(QtCore.QRect(100, 340, 561, 25))
        self.messageEdit.setObjectName(_fromUtf8("messageEdit"))
        self.encryptButton = QtGui.QPushButton(cipherImageViewForm)
        self.encryptButton.setGeometry(QtCore.QRect(20, 70, 131, 28))
        self.encryptButton.setObjectName(_fromUtf8("encryptButton"))
        self.saveImageButton = QtGui.QPushButton(cipherImageViewForm)
        self.saveImageButton.setGeometry(QtCore.QRect(20, 120, 131, 28))
        self.saveImageButton.setObjectName(_fromUtf8("saveImageButton"))
        self.decryptButton = QtGui.QPushButton(cipherImageViewForm)
        self.decryptButton.setGeometry(QtCore.QRect(130, 400, 121, 26))
        self.decryptButton.setObjectName(_fromUtf8("decryptButton"))

        self.rawImage = QtGui.QImage()
        self.cipherImage = QtGui.QImage()
        self.number_char = 255

        self.retranslateUi(cipherImageViewForm)
        QtCore.QObject.connect(self.openImageButton, QtCore.SIGNAL(_fromUtf8("clicked()")), self.abrir_imagen)
        QtCore.QObject.connect(self.saveImageButton, QtCore.SIGNAL(_fromUtf8("clicked()")), self.guardar_imagen)
        QtCore.QObject.connect(self.encryptButton, QtCore.SIGNAL(_fromUtf8("clicked()")), self.encriptar)
        QtCore.QObject.connect(self.decryptButton, QtCore.SIGNAL(_fromUtf8("clicked()")), self.desencriptar)


    def retranslateUi(self, CipherImageForm):
        CipherImageForm.setWindowTitle(_translate("CipherImageForm", "Identificación de Características para la Detección de Rostros Humanos", None))
        self.openImageButton.setText(_translate("CipherImageForm", "Abrir Imagen", None))
        self.messageLabel.setText(_translate("CipherImageForm", "Mensaje:", None))
        self.encryptButton.setText(_translate("CipherImageForm", "Cifrar Imagen", None))
        self.saveImageButton.setText(_translate("CipherImageForm", "Guardar Imagen Cifrada", None))
        self.decryptButton.setText(_translate("CipherImageForm", "Descifrar Mensaje", None))

    def abrir_imagen(self):

        # Limpiamos el mensaje y las vistas de imagenes
        self.messageEdit.clear()
        if self.rawImageView.scene() != None:
            self.rawImageView.scene().clear()

        # Abrimos un cuadro de diálogo para escoger la imagen
        imageName = QtGui.QFileDialog.getOpenFileName()
        print unicode(imageName)

        # Abrimos la imagen
        image = QtGui.QImage(imageName)
        # Generamos una escena, que cargara la imagen y se mostrará en la vista
        scene = QtGui.QGraphicsScene()
        item = QtGui.QGraphicsPixmapItem(QtGui.QPixmap.fromImage(image))
        self.rawImageView.setScene(scene)
        # Adaptamos el tamaño de la imagen
        self.rawImageView.fitInView(item)
        
        scene.addItem(item)

        # Asignamos la imagen temporal a la imagen de trabajo
        self.rawImage = image
        self.cipherImage = image

    def guardar_imagen(self):
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
        imagefile.write(self.cipherImage)

    def encriptar(self):
        print "Encriptando"
        # Obtenemos el texto a esconder y lo convertimos a array de bits
        text = unicode(self.messageEdit.text())
        bits = self.str_to_bits(text)

        # QImage * newImage = new QImage(origin->width(), origin->height(), QImage::Format_ARGB32);
        # print bits
        # Dimensiones de la imagen
        width = self.rawImage.width()
        height = self.rawImage.height()

        # Definimos la cantidad de saltos entre pixeles
        paso = (width * height) / self.number_char# len(bits)

        # Definimos cipherImage con las dimensiones de la original
        self.cipherImage = QtGui.QImage(width, height, QtGui.QImage.Format_ARGB32)

        # Count nos permite saber cuantos bits se han escrito en la imagen
        count = 0

        for x in range(width):
            for y in range(height):
                # Obtenemos el pixel de la imagen en la posicion x,y
                old_color = QtGui.QColor(self.rawImage.pixel(x, y))

                # Obtenemos solo canal azul
                blue = old_color.blue()

                # Preguntamos si el punto es múltiplo de paso
                is_paso = ((x * height) + y) % paso == 0

                # Si es multiplo de paso, y ademas no hemos escrito todos los bits, escondemos el siguiente
                if (paso and count < len(bits)):
                    # El canal azul tendrá 128 si el bit está encendido, 64 si está apagado
                    blue = 128 if (bits[count] == 1) else 64
                    # print blue, count
                    count += 1 # Escribimos un bit, aumentamos count

                # Creamos un nuevo color con el canal azul modificado y lo asignamos al pixel en x,y
                new_color = QtGui.QColor(old_color.red(), old_color.green(), blue)
                self.cipherImage.setPixel(x, y, new_color.rgb())

        # En el canal azul del último pixel guardamos el número de caracteres escondidos
        old_color = QtGui.QColor(self.rawImage.pixel(width - 1, height - 1))
        new_color = QtGui.QColor(old_color.red(), old_color.green(), len(text))
        self.cipherImage.setPixel(width - 1, height - 1, new_color.rgb())

        # Sobre escribimos la imagen
        scene = QtGui.QGraphicsScene()
        item = QtGui.QGraphicsPixmapItem(QtGui.QPixmap.fromImage(self.cipherImage))
        self.rawImageView.setScene(scene)
        self.rawImageView.fitInView(item)
        
        scene.addItem(item)
        print "Encriptado finalizado"
        self.messageEdit.clear()


        #self.rawImage = self.cipherImage

    def desencriptar(self):
        #self.rawImage = self.cipherImage

        # Dimensiones de la imagen cifrada
        width = self.cipherImage.width()
        height = self.cipherImage.height()

        # Calculamos numero de saltos entre pixeles
        paso = (width * height) / self.number_char

        # Obtenemos numero de caracteres a decodificar, en el canal azul del ultimo pixel
        color = QtGui.QColor(self.cipherImage.pixel(width - 1, height - 1))
        total = color.blue() * 8
        # print total

        # Contador de bits y array de bits
        count = 0
        bits = []

        for x in range(width):
            for y in range(height):
                # Obtenemos el pixel y nos quedamos con el canal azul
                color = QtGui.QColor(self.cipherImage.pixel(x, y))
                blue = color.blue()

                # Si es un multiplo de paso y no hemos excedido el total de pixeles a recuperar, lo recuperamos
                is_paso = ((x * height) + y) % paso == 0
                if (paso and count < total):
                    # Si el numero es 128 encendemos el bit, si no, lo apagamos
                    bit = 1 if (blue == 128) else 0
                    # Lo agregamos a la lista de bits y aumentamos el contador
                    bits.append(bit)
                    count += 1

        # Convertimos los bits a texto. bits[::-1] nos permite invertir la lista de bits para facilitar su conversion
        text = self.bits_to_str(bits[::-1])
        # Imprimimos el texto recuperado
        self.messageEdit.setText(text)


    def str_to_bits(self, text):
        '''Recibe un string y lo convierte a una lista de bits'''
        bits = []

        for char in text:
            # Para cada caracter del string, obtenemos su valor entero y lo vamos comparando con cada bit
            # encendido, por ejemplo a la "a" le corresponde 97, que en binario es "[0, 1, 1, 0, 0, 0, 0, 1]"
            # hacemos un AND a nivel de bits con 64 = "[0, 1, 0, 0, 0, 0, 0, 0]", lo que nos da como resultado
            # "[0, 1, 0, 0, 0, 0, 0, 0]", ahora sabemos que ese caracter tiene ese bit encendido. Repetimos el 
            # paso para los 8 bits hasta obtener una representacion binaria de la cadena
            i = 7
            num = ord(char)
            while i >= 0:
                bit_pos = 2 ** i
                bits.append( (num&bit_pos) / bit_pos)
                i -= 1

        return bits

    def bits_to_str(self, bits):
        '''Proceso inverso, recibe una lista de bits y regresa un string'''
        text = []
        # Obtenemos el total de caracteres. 1 por cada 8 bits
        total = len(bits) / 8

        for i in range(total):
            # Nos desplazamos de 8 en 8 para obtener la representación binaria del numero individual
            num_bits = bits[i * 8 : (i + 1) * 8]
            # print num_bits
            # Realizamos la sumatoria de los bits encendidos. Por ejemplo: a -> "[0, 1, 1, 0, 0, 0, 0, 1]"
            # 64 + 32 + 1 = 97
            suma = 0
            for j in range(8):
                suma += num_bits[j] * (2 ** j)
            # Convertimos el numero en char y lo agregamos a la lista
            text.append(chr(suma))

        # Invertimos la lista y la retornamos en forma de cadena
        text = text[::-1]
        return "".join(text)

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    cipherImageViewForm = QtGui.QWidget()
    ui = Ui_CipherImageForm()
    ui.setupUi(cipherImageViewForm)
    cipherImageViewForm.show()
    sys.exit(app.exec_())
