from PyQt5.QtWidgets import *
import sys, pickle
from PyQt5 import uic, QtWidgets ,QtCore, QtGui
from data_visualise import data_
from table_display import DataFrameModel
from add_steps import add_steps
import linear_rg, logistic_reg, KNN
import pre_trained


class UI(QMainWindow):
  def __init__(self):
    super(UI, self).__init__()
    uic.loadUi('mainwindow.ui', self)

    global data, steps
    data = data_()
    steps = add_steps()

    self.Browse = self.findChild(QPushButton, "Browse")
    self.columns = self.findChild(QListWidget, "column_list")
    self.table = self.findChild(QTableView, "tableView")
    self.data_shape = self.findChild(QLabel, "shape")
    self.label_2 = self.findChild(QLabel, "label_2")
    self.submit_btn = self.findChild(QPushButton, "Submit")
    self.target_col = self.findChild(QLabel, "target_col")
    self.cat_column = self.findChild(QComboBox, "cat_column")
    self.convert_btn = self.findChild(QPushButton, "convert_btn")
    self.drop_column = self.findChild(QComboBox, "drop_column")
    self.drop_btn = self.findChild(QPushButton, "drop")
    self.empty_column = self.findChild(QComboBox, "empty_column")
    self.fillmean_btn = self.findChild(QPushButton, "fillmean")
    self.fillna_btn = self.findChild(QPushButton, "fillna")
    # self.scaler = self.findChild(QComboBox, "scaler")
    self.scale_btn = self.findChild(QPushButton, "scale_btn")
    
    self.scatter_X = self.findChild(QComboBox, "scatter_X")
    self.scatter_Y = self.findChild(QComboBox, "scatter_Y")
    self.scatter_c = self.findChild(QComboBox, "scatter_c")
    self.scatter_mark = self.findChild(QComboBox, "scatter_mark")
    self.scatterplot_btn = self.findChild(QPushButton, "scatter_show")

    self.plot_X = self.findChild(QComboBox, "plot_X")
    self.plot_Y = self.findChild(QComboBox, "plot_Y")
    self.plot_c = self.findChild(QComboBox, "plot_c")
    self.plot_mark = self.findChild(QComboBox, "plot_mark")
    self.lineplot_btn = self.findChild(QPushButton, "line_show")
    
    self.train_btn = self.findChild(QPushButton, "train")

    # pre-trained 자료 가져오기
    self.pre_trained_btn = self.findChild(QPushButton, "pre_trained")
    self.go_pre_trained_btn = self.findChild(QPushButton, "go_pre_trained")

    self.Browse.clicked.connect(self.getCSV) # 버튼을 누르면 getCSV 이라는 함수를 호출
    self.columns.clicked.connect(self.target)
    self.submit_btn.clicked.connect(self.set_target) 
    self.convert_btn.clicked.connect(self.con_cat) 
    self.drop_btn.clicked.connect(self.dropc)
    self.fillmean_btn.clicked.connect(self.fill_mean) 
    self.fillna_btn.clicked.connect(self.fill_na)
    self.scale_btn.clicked.connect(self.scale_value) 
    self.scatterplot_btn.clicked.connect(self.scatter_plot)
    self.lineplot_btn.clicked.connect(self.line_plot)

    self.train_btn.clicked.connect(self.train_func)

    self.pre_trained_btn.clicked.connect(self.upload_model)
    self.go_pre_trained_btn.clicked.connect(self.test_pretrained)


  def upload_model(self):
    self.filePath_pre, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', './models/',"pkl(*.pkl)")
    with open(self.filePath_pre, 'rb') as file:
      self.pickle_model = pickle.load(file)
        
  def test_pretrained(self):
    self.testing=pre_trained.UI(self.df,self.target_value,self.pickle_model,self.filePath_pre)

  def train_func(self):
    myDict = {"Linear Regression" : linear_rg, "Logistic Regression" : logistic_reg, "kNN" : KNN}

    if self.target_value != "":
      self.win=myDict[self.model_select.currentText()].UI(self.df, self.target_value, steps)

  def line_plot(self):
    x=self.plot_X.currentText()
    y=self.plot_Y.currentText()
    c=self.plot_c.currentText()
    marker=self.plot_mark.currentText()
    data.line_plot(df=self.df, x=x, y=y, c=c, marker=marker)


  def scatter_plot(self):
    x=self.scatter_X.currentText()
    y=self.scatter_Y.currentText()
    c=self.scatter_c.currentText()
    marker=self.scatter_mark.currentText()
    data.scatter_plot(df=self.df, x=x, y=y, c=c, marker=marker)

  def scale_value(self):
    if self.scaler.currentText() == 'StandardScale':
      self.df, func_name = data.StandardScale(self.df, self.target_value)
    elif self.scaler.currentText() == 'MinMaxScale':
      self.df, func_name = data.MinMaxScale(self.df, self.target_value)
    else:
      self.df, func_name = data.PowerScale(self.df, self.target_value)

    steps.add_text(self.scaler.currentText()+" applied to data")
    steps.add_pipeline(self.scaler.currentText(),func_name)
    self.filldetails()

  def fill_mean(self):
    selected = self.df[self.empty_column.currentText()]
    type = self.df[self.empty_column.currentText()].dtype
    if type != 'object':
      self.df[self.empty_column.currentText()] = data.fillmean(self.df, self.empty_column.currentText())
      self.filldetails()
    else:
      print("datatype is object")

  def fill_na(self):
    self.df[self.empty_column.currentText()] = data.fillna(self.df, self.empty_column.currentText())
    self.filldetails()
    print("유후")



  def filldetails(self, flag = 1): # 처리 다 끝난것을 채워넣는 함수
    if flag == 0:
      self.df = data.read_file(str(self.filePath)) # data_visualise 에서 read_file함수 받아서 데이터프레임으로 받게 됨

    self.columns.clear()
    self.column_list = data.get_column_list(self.df)
    print(self.column_list)

    for i , j in enumerate(self.column_list):
      # print(i,j)
      stri = f'{j} ------ {str(self.df[j].dtype)}'
      # stri = f'{j}'
      # print(stri)
      self.columns.insertItem(i, stri)

    x, y = data.get_shape(self.df)
    self.data_shape.setText(f'{((x), (y))}')
    self.fill_combo_box()

  def fill_combo_box(self):
    self.cat_column.clear()
    self.cat_column.addItems(self.column_list)
    self.drop_column.clear()
    self.drop_column.addItems(self.column_list)
    self.empty_column.clear()
    self.empty_column.addItems(self.column_list)

    self.scatter_X.clear()
    self.scatter_X.addItems(self.column_list)
    self.scatter_Y.clear()
    self.scatter_Y.addItems(self.column_list)

    self.plot_X.clear()
    self.plot_X.addItems(self.column_list)
    self.plot_Y.clear()
    self.plot_Y.addItems(self.column_list)

    x = DataFrameModel(self.df)
    self.table.setModel(x)


  def getCSV(self):
    self.filePath, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open file", "", "csv(*.csv)")
    self.columns.clear()
    print(self.filePath)
    if self.filePath != "":
      self.filldetails(0)

  def target(self):
    self.item = self.columns.currentItem()

  def set_target(self):
    self.target_value = str(self.item.text()).split()[0]
    print(self.target_value)
    steps.add_code(f"target=data[{self.target_value}]")
    self.target_col.setText(self.target_value)

  def con_cat(self):
    selected = self.cat_column.currentText()
    # print(selected)
    self.df[selected], func_name = data.convert_category(self.df, selected)
    steps.add_text("Column "+ selected + " converted using LabelEncoder")
    steps.add_pipeline("LabelEncoder",func_name)
    self.filldetails()

  def dropc(self):
    selected = self.drop_column.currentText()
    self.df = data.drop_columns(self.df, selected)
    steps.add_code("data=data.drop('"+self.drop_column.currentText()+"',axis=1)")
    steps.add_text("Column "+ self.drop_column.currentText()+ " dropped")
    self.filldetails()

if __name__ == "__main__":
  app = QtWidgets.QApplication(sys.argv)
  window = UI()
  window.show()

  sys.exit(app.exec_())