from PyQt5.QtWidgets import (
   QApplication, QWidget,
   QFileDialog, # Диалог открытия файлов (и папок)
   QLabel, QPushButton, QListWidget,
   QHBoxLayout, QVBoxLayout,
)
import os 
from PyQt5.QtGui import QPixmap
from PIL import Image
from PyQt5.QtCore import Qt
from PIL.ImageFilter import (
   BLUR, CONTOUR, DETAIL, EDGE_ENHANCE, EDGE_ENHANCE_MORE,
   EMBOSS, FIND_EDGES, SMOOTH, SMOOTH_MORE, SHARPEN,
   GaussianBlur, UnsharpMask
)
app = QApplication([])
main_win = QWidget()
main_win.resize(700 , 500)
main_win.setWindowTitle('Мини-мини-мини фотошопер, блогиат')

papka = QPushButton('Папка')
spisok = QListWidget()
kartinka = QLabel('Картинка')

levo = QPushButton('Лево')
pravo = QPushButton('Право')
zerkalo = QPushButton('Зеркало')
rezkost = QPushButton('Резкость')
ch_b = QPushButton('Ч/б')

layout_main1 = QHBoxLayout()

layout_vert1 = QVBoxLayout()
layout_vert2 = QVBoxLayout()
layout_H2 = QHBoxLayout()

layout_H2.addWidget(levo)
layout_H2.addWidget(pravo)
layout_H2.addWidget(zerkalo)
layout_H2.addWidget(rezkost)
layout_H2.addWidget(ch_b)

layout_vert1.addWidget(papka)
layout_vert1.addWidget(spisok)

layout_vert2.addWidget(kartinka)
layout_vert2.addLayout(layout_H2)

layout_main1.addLayout(layout_vert1)
layout_main1.addLayout(layout_vert2)


main_win.setLayout(layout_main1)
main_win.show()

workdir = ''
def chooseWorkdir():
   global workdir
   workdir = QFileDialog.getExistingDirectory()

def filter(files, extensions):
   result = list()
   for file_name in files:
      for ext in extensions:
         if file_name.endswith(ext):
            result.append(file_name)
   return (result)

def show_File_name_List():
   extensions = ['.jpg','.jpeg', '.png', '.gif', '.bmp']
   chooseWorkdir()
   file_names = filter(os.listdir(workdir) , extensions)
   spisok.clear()
   for file_name in file_names:
      spisok.addItem(file_name)

papka.clicked.connect(show_File_name_List)

class Image_processor():
   def __init__ (self):
      self.image  = None
      self.dir = None
      self.file_name = None
      self.save_dir = 'modifigh'

   def loadImage(self, dir, file_name):
      self.dir = dir
      self.file_name = file_name

      image_path = os.path.join(dir, file_name)
      self.image = Image.open(image_path)

   def showImage(self, path):
      kartinka.hide()
      pixmapimage = QPixmap(path)

      w , h = kartinka.width(), kartinka.height()
      pixmapimage = pixmapimage.scaled(w, h, Qt.KeepAspectRatio)

      kartinka.setPixmap(pixmapimage)
      kartinka.show()

   def do_ch_b(self):
      self.image = self.image.convert('L')
      self.save_Image()
      image_path = os.path.join(self.dir, self.save_dir, self.file_name)
      self.showImage(image_path)

   def do_zerkalo(self):
      self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
      self.save_Image()
      image_path = os.path.join(self.dir, self.save_dir, self.file_name)
      self.showImage(image_path)

   def do_pravo(self):
      self.image = self.image.transpose(Image.ROTATE_270)
      self.save_Image()
      image_path = os.path.join(self.dir, self.save_dir, self.file_name)
      self.showImage(image_path)

   def do_levo(self):
      self.image = self.image.transpose(Image.ROTATE_90)
      self.save_Image()
      image_path = os.path.join(self.dir, self.save_dir, self.file_name)
      self.showImage(image_path)

   def do_reskost(self):
      self.image = self.image.filter(SHARPEN)
      self.save_Image()
      image_path = os.path.join(self.dir, self.save_dir, self.file_name)
      self.showImage(image_path)

   def save_Image(self):
      path = os.path.join(self.dir, self.save_dir)
      if not(os.path.exists(path) or os.path.isdir(path)):
         os.mkdir(path)
      image_path = os.path.join(path, self.file_name)
      self.image.save(image_path)

workimage = Image_processor()

def show_Chosen_Image():
   if spisok.currentRow() >= 0:
      file_name = spisok.currentItem().text()
      workimage.loadImage(workdir, file_name)
      image_path = os.path.join(workimage.dir, workimage.file_name)
      workimage.showImage(image_path)

spisok.currentRowChanged.connect(show_Chosen_Image)
ch_b.clicked.connect(workimage.do_ch_b)
zerkalo.clicked.connect(workimage.do_zerkalo)
pravo.clicked.connect(workimage.do_pravo)
levo.clicked.connect(workimage.do_levo)
rezkost.clicked.connect(workimage.do_reskost)

app.exec_()


















