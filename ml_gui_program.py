from PyQt5.QtWidgets import *
import sys, pickle
from PyQt5 import uic, QtWidgets ,QtCore, QtGui
from data_visualise import data_
from table_display import DataFrameModel

class UI(QMainWindow):
  def __init__(self):
    super(UI, self).__init__()
    uic.loadUi('mainwindow.ui', self)

    global data, steps
    data = data_()

    self.Browse = self.findChild(QPushButton, "Browse")
    self.columns = self.findChild(QListWidget, "column_list")
    self.table = self.findChild(QTableView, "tableView")

    self.Browse.clicked.connect(self.getCSV) # 버튼을 누르면 getCSV 이라는 함수를 호출

  def filldetails(self, flag = 1):
    if flag == 0:
      self.df = data.read_file(str(self.filePath)) # data_visualise 에서 read_file함수 받아서 데이터프레임으로 받게 됨

    self.columns.clear()
    self.column_list = data.get_column_list(self.df)
    print(self.column_list)

    for i , j in enumerate(self.column_list):
      # print(i,j)
      stri = f'{j}------{str(self.df[j].dtype)}'
      # print(stri)
      self.columns.insertItem(i, stri)
    
    self.fill_combo_box()

  def fill_combo_box(self):
    x = DataFrameModel(self.df)
    self.table.setModel(x)

  def getCSV(self):
    self.filePath, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open file", "", "csv(*.csv)")
    self.columns.clear()
    print(self.filePath)
    if self.filePath != "":
      self.filldetails(0)

if __name__ == "__main__":
  app = QtWidgets.QApplication(sys.argv)
  window = UI()
  window.show()

  sys.exit(app.exec_())