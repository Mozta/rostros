import sys
import os.path

#Script para generar el archivo CSV que contiene la base de datos

if __name__ == "__main__":

    if len(sys.argv) != 2:
        print "Se usa asi: create_csv.py tu_carpeta > faces.csv"
        sys.exit(1)

    BASE_PATH=sys.argv[1]
    SEPARATOR=";"

    label = 0
    for dirname, dirnames, filenames in os.walk(BASE_PATH):
        for subdirname in dirnames:
            subject_path = os.path.join(dirname, subdirname)
            for filename in os.listdir(subject_path):
                abs_path = "%s/%s" % (subject_path, filename)
                print "%s%s%d" % (abs_path, SEPARATOR, label)
            label = label + 1
