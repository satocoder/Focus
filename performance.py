from PyQt5.QtWidgets import *
from PyQt5.QtChart import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from random import randint
from PyQt5.QtCore import QTimer,QDateTime
import sqlite3
import sys


con=sqlite3.connect('focus.db')
cur=con.cursor()

class performance(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Marginal Timer')
        self.setGeometry(350,150,524,391)
        self.don_chart()
        self.show()
    def don_chart(self):
        series=QPieSeries()
        series.setHoleSize(0.35)
        series.append("First task",4.28)
        slice=QPieSlice()
        slice=series.append('Present task',15.6)
        slice.setExploded()
        slice.setLabelVisible()

        series.append('Other tasks',23.8)
        series.append('Way to go',56.4)

        chart=QChart()
        chart.addSeries(series)
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.setTitle('DonoutChart')

        chartview= QChartView(chart)
        chartview.setRenderHint(QPainter.Antialiasing)

        self.setCentralWidget(chartview)
