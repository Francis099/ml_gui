
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QTextEdit ,QListWidget ,QTableView ,QComboBox,QLabel,QLineEdit,QTextBrowser
import sys,pickle

from PyQt5 import uic, QtWidgets ,QtCore, QtGui
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import metrics
import matplotlib.pyplot as plt
import numpy as np
import data_visualise
import table_display
import pandas as pd
import common


class UI(QMainWindow):
  def __init__(self, df, target, user_actions):
    super(UI, self).__init__()
    uic.loadUi('./UI_files/LinearRegression.ui', self)

    self.user_act = user_actions

    global data
    data=data_visualise.data_()
    steps=common.common_steps(df,target)
    self.X,self.n_classes,self.target_value,self.df,self.column_list=steps.return_data()
    self.target = self.findChild(QLabel,"target")
    self.columns= self.findChild(QListWidget,"columns")
    self.test_size= self.findChild(QLabel,"test_size") 
    self.test_data= self.findChild(QLineEdit,"test_data")
    self.test_size_btn=self.findChild(QPushButton,"test_size_btn")
    self.train_btn= self.findChild(QPushButton, "train")
    self.intercept=self.findChild(QLabel,"intercept")
    self.weights=self.findChild(QTextBrowser,"weights")
    # MAE, MSE, RMSE 받아오기
    self.mae=self.findChild(QLabel,"mae")
    self.mse=self.findChild(QLabel,"mse")
    self.rmse=self.findChild(QLabel,"rmse")

    self.setvalue()

    self.test_size_btn.clicked.connect(self.test_split) 
    self.train_btn.clicked.connect(self.training) 

    self.show()
  
  def training(self):
    self.reg=LinearRegression().fit(self.x_train,self.y_train)
    str1=""

    coef=' '.join(map(str, self.reg.coef_))
    print(coef)
    
    self.intercept.setText(str(self.reg.intercept_))
    self.weights.setText(coef)

    pre=self.reg.predict(self.x_test)
    self.mae.setText(str(metrics.mean_absolute_error(self.y_test,pre)))
    self.mse.setText(str(metrics.mean_squared_error(self.y_test,pre)))
    self.rmse.setText(str(np.sqrt(metrics.mean_squared_error(self.y_test,pre))))

  def test_split(self):
    self.x_train,self.x_test,self.y_train,self.y_test = train_test_split(self.df,self.X[self.target_value],test_size=float(self.test_data.text()),random_state=0)
    print(self.y_train.shape)
    print(self.y_test.shape)
    self.train_size.setText(str(self.x_train.shape))
    self.test_size.setText(str(self.x_test.shape))

  def setvalue(self):        
    self.target.setText(self.target_value)
    self.columns.clear()
    self.columns.addItems(self.column_list)
