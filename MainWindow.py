# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.
import sys
import os
from PyQt5.QtGui import QPixmap
from PyQt5 import QtCore, QtGui, QtWidgets
from pydicom import dcmread
import cv2
import numpy as np


class Ui_MainWindow(object):
    n_files = 0

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1301, 815)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(20, 170, 256, 611))
        self.listWidget.setObjectName("listWidget")
        self.lbl_selected_file = QtWidgets.QLabel(self.centralwidget)
        self.lbl_selected_file.setGeometry(QtCore.QRect(30, 110, 241, 41))
        self.lbl_selected_file.setObjectName("lbl_selected_file")
        self.lbl_image = QtWidgets.QLabel(self.centralwidget)
        self.lbl_image.setGeometry(QtCore.QRect(360, 20, 681, 751))
        self.lbl_image.setObjectName("lbl_image")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1301, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.lbl_selected_file.setText(_translate("MainWindow", "lbl_selected_file"))
        self.lbl_image.setText(_translate("MainWindow", "lbl_image"))

        #self.listWidget.addItem("Item 1")
        #self.listWidget.addItem("Item 2")

        self.lbl_image.setPixmap(QPixmap('D:/heart.png'))
        self.get_files()

        self.listWidget.itemClicked.connect(self.Clicked)  # connect itemClicked to Clicked method

    def Clicked(self, item):
        self.lbl_selected_file.setText(item.text())
        file_name = item.text()
        path = 'D:/2022_Dicom_Sorted/nelson01082021/20210108/#-#_data_s168314_3tbcardiac_3tb7831/mid_sax_cine/'
        fpath = path + file_name
        ds = dcmread(fpath)

        # Normal mode:
        print()
        print(f"File path........: {fpath}")
        print(f"SOP Class........: {ds.SOPClassUID} ({ds.SOPClassUID.name})")
        print()
        pat_name = ds.PatientName
        display_name = pat_name.family_name + ", " + pat_name.given_name
        print(f"Patient's Name...: {display_name}")
        print(f"Patient ID.......: {ds.PatientID}")
        print(f"Modality.........: {ds.Modality}")
        print(f"Study Date.......: {ds.StudyDate}")
        print(f"Image size.......: {ds.Rows} x {ds.Columns}")
        print(f"Pixel Spacing....: {ds.PixelSpacing}")
        print(f"Image Position Patient..: {ds.ImagePositionPatient}")
        print(f"Slice location...: {ds.get('SliceLocation', '(missing)')}")

        # Load dimensions based on the number of rows, columns, and slices (along the Z axis)
        ConstPixelDims = (int(ds.Rows), int(ds.Columns), self.n_files)

        # Load spacing values (in mm)
        ConstPixelSpacing = (float(ds.PixelSpacing[0]), float(ds.PixelSpacing[1]), float(ds.SliceThickness))

        x = np.arange(0.0, (ConstPixelDims[0] + 1) * ConstPixelSpacing[0], ConstPixelSpacing[0])
        y = np.arange(0.0, (ConstPixelDims[1] + 1) * ConstPixelSpacing[1], ConstPixelSpacing[1])
        z = np.arange(0.0, (ConstPixelDims[2] + 1) * ConstPixelSpacing[2], ConstPixelSpacing[2])



        # get the pixel information into a numpy array
        data = ds.pixel_array
        print('The image has {} x {} voxels'.format(data.shape[0], data.shape[1]))
        #zoomed = cv2.resize(data, (data.shape[0] * 4, data.shape[1] * 4), interpolation=cv2.INTER_CUBIC)
        # create QImage from numpy array
        #image = image_to_grayscale(data)
        image = QtGui.QImage(data, data.shape[1], data.shape[0], data.shape[1] * 3, QtGui.QImage.Format_BGR888)
        pix = QtGui.QPixmap(image)
        self.lbl_image.setPixmap(QtGui.QPixmap(pix))
        #pixmap = QtGui.QPixmap(image)

        #self.lbl_image.setPixmap(pixmap)
        #plt.imshow(zoomed, cmap=plt.cm.gray)
        #read_dicom_image(self, file_name)
        #QMessageBox.information(self, "ListWidget", "You clicked: " + item.text())

    def get_files(self):
        path = 'D:/2022_Dicom_Sorted/nelson01082021/20210108/#-#_data_s168314_3tbcardiac_3tb7831/mid_sax_cine/'
        dir_list = os.listdir(path)
        for fn in dir_list:
            self.listWidget.addItem(fn)
        self.n_files = len(dir_list)
        fpath = path + dir_list[1]
        ds = dcmread(fpath)

        # Normal mode:
        print()
        print(f"File path........: {fpath}")
        print(f"SOP Class........: {ds.SOPClassUID} ({ds.SOPClassUID.name})")
        print()
        pat_name = ds.PatientName
        display_name = pat_name.family_name + ", " + pat_name.given_name
        print(f"Patient's Name...: {display_name}")
        print(f"Patient ID.......: {ds.PatientID}")
        print(f"Modality.........: {ds.Modality}")
        print(f"Study Date.......: {ds.StudyDate}")
        print(f"Image size.......: {ds.Rows} x {ds.Columns}")
        print(f"Pixel Spacing....: {ds.PixelSpacing}")
        print(f"Image Position Patient..: {ds.ImagePositionPatient}")
        print(f"Slice location...: {ds.get('SliceLocation', '(missing)')}")

        # Load dimensions based on the number of rows, columns, and slices (along the Z axis)
        ConstPixelDims = (int(ds.Rows), int(ds.Columns), self.n_files)

        # Load spacing values (in mm)
        ConstPixelSpacing = (float(ds.PixelSpacing[0]), float(ds.PixelSpacing[1]), float(ds.SliceThickness))

        x = np.arange(0.0, (ConstPixelDims[0] + 1) * ConstPixelSpacing[0], ConstPixelSpacing[0])
        y = np.arange(0.0, (ConstPixelDims[1] + 1) * ConstPixelSpacing[1], ConstPixelSpacing[1])
        z = np.arange(0.0, (ConstPixelDims[2] + 1) * ConstPixelSpacing[2], ConstPixelSpacing[2])

        # The array is sized based on 'ConstPixelDims'
        ArrayDicom = np.zeros(ConstPixelDims, dtype=ds.pixel_array.dtype)

        # loop through all the DICOM files  skip file[0] it's weird?
        for filenameDCM in range(1, len(dir_list)):
            fpath = path + dir_list[filenameDCM]
            ds = dcmread(fpath)                         # read the file
            ArrayDicom[:, :, filenameDCM-1] = ds.pixel_array   # store the raw image data
        print("yeah!, all read")

    def image_to_grayscale(self, img):
        # Convert pixel_array (img) to -> gray image (img_2d_scaled)
        ## Step 1. Convert to float to avoid overflow or underflow losses.
        img_2d = img.astype(float)

        ## Step 2. Rescaling grey scale between 0-255
        img_2d_scaled = (np.maximum(img_2d, 0) / img_2d.max()) * 255.0

        ## Step 3. Convert to uint
        img_2d_scaled = np.uint8(img_2d_scaled)
        return img_2d_scaled

    def read_dicom_image(self, file_name):
        path = 'D:/2022_Dicom_Sorted/nelson01082021/20210108/#-#_data_s168314_3tbcardiac_3tb7831/mid_sax_cine/'
        fpath = path + file_name
        ds = dcmread(fpath)

        # Normal mode:
        print()
        print(f"File path........: {fpath}")
        print(f"SOP Class........: {ds.SOPClassUID} ({ds.SOPClassUID.name})")
        print()

        pat_name = ds.PatientName
        display_name = pat_name.family_name + ", " + pat_name.given_name
        print(f"Patient's Name...: {display_name}")
        print(f"Patient ID.......: {ds.PatientID}")
        print(f"Modality.........: {ds.Modality}")
        print(f"Study Date.......: {ds.StudyDate}")
        print(f"Image size.......: {ds.Rows} x {ds.Columns}")
        print(f"Pixel Spacing....: {ds.PixelSpacing}")
        print(f"Image Position Patient..: {ds.ImagePositionPatient}")
        print(f"Slice location...: {ds.get('SliceLocation', '(missing)')}")
        # get the pixel information into a numpy array
        data = ds.pixel_array
        print('The image has {} x {} voxels'.format(data.shape[0], data.shape[1]))

        #zoomed = cv2.resize(data, (data.shape[0] * 4, data.shape[1] * 4), interpolation=cv2.INTER_CUBIC)
        #plt.imshow(zoomed, cmap=plt.cm.gray)
        #self.lbl_image.setPixmap(QPixmap(zoomed))



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
