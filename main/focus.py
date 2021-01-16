from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from random import randint
from PyQt5.QtCore import QTimer,QDateTime
import sqlite3
import sys
from performance import performance


con=sqlite3.connect('focus.db')
cur=con.cursor()

count=0
stri=''
min=0
class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Focus layout')
        self.setGeometry(350,150,524,391)
        self.start=True
        self.UI()
        self.show()


    def UI(self):
        self.designlayout()
        self.layouts()


    def designlayout(self):
        self.bot1list=QListWidget()
        self.bot1list.itemClicked.connect(self.singleclick)
        self.bot2lbl=QLabel('Task')
        self.bot2lined=QLineEdit('')
        self.bot2btn=QPushButton('Timer')




        self.lbl1=QLabel('Task')
        self.lbl2=QLabel('Time')
        self.lined1=QLineEdit()
        self.lined2=QLineEdit()
        self.btn1=QPushButton('Insert task')
        self.btn2=QPushButton('Performance')
        self.btn3=QPushButton('Yearly')

        self.btn1.clicked.connect(self.inserttask)
        self.btn2.clicked.connect(self.performance)


        self.readdataset()

    def layouts(self):
        self.mainlayouts=QVBoxLayout()
        self.toplayout=QHBoxLayout()
        self.botlayout=QVBoxLayout()

        self.topright3layout=QVBoxLayout()
        self.toprightlayout=QFormLayout()
        self.topright2layout=QHBoxLayout()
        self.topleftlayout=QVBoxLayout()
        self.top1layout=QHBoxLayout()
        self.top2layout=QHBoxLayout()
        self.top3layout=QHBoxLayout()

        self.bot1layout=QHBoxLayout()
        self.bot2layout=QFormLayout()


        self.bot1rlayout=QVBoxLayout()
        self.bot1llayout=QVBoxLayout()



        self.topright3layout.addLayout(self.toprightlayout)
        self.topright3layout.addLayout(self.topright2layout)
        self.toplayout.addLayout(self.topright3layout,5)

        self.toplayout.addLayout(self.topleftlayout,5)
        self.toplayout.setContentsMargins(10,10,10,10)


        self.bot1layout.addLayout(self.bot1rlayout)
        self.bot1layout.setContentsMargins(10,10,10,50)





        self.botlayout.addLayout(self.bot1layout)
        self.botlayout.addLayout(self.bot2layout)


        self.mainlayouts.addLayout(self.toplayout)
        self.mainlayouts.addLayout(self.botlayout)



        #add QtWidgets
        self.toprightlayout.addRow(self.lbl1,self.lined1)
        self.toprightlayout.addRow(self.lbl2,self.lined2)
        self.topright2layout.addWidget(self.btn1)
        self.topright2layout.addWidget(self.btn2)
        self.topright2layout.addWidget(self.btn3)

        self.bot1rlayout.addWidget(self.bot1list)





        self.setLayout(self.mainlayouts)
    def readdataset(self):
        query1="SELECT * FROM daily"
        daily=cur.execute(query1).fetchall()
        for t in daily:
            self.bot1list.addItem(str(t[0])+": "+t[1]+"  "+str(t[2])+" time section")
            self.bot1list.setFont(QFont('Times',12))




    def inserttask(self):
        task=self.lined1.text()
        time=self.lined2.text()

        if (task and time):
            query="Insert INTO daily (task,time) Values(?,?) "
            cur.execute(query,(task,time))
            con.commit()

        query1="SELECT * FROM daily ORDER BY ROWid DESC LIMIT 1"
        dal=cur.execute(query1).fetchone()
        print(dal)
        self.bot1list.addItem(str(dal[0])+": "+dal[1]+"  "+str(dal[2])+" time section")
        self.bot1list.setFont(QFont('Times',12))



    def singleclick(self):
        a=self.bot1list.currentItem().text()


        self.tasktimer=tasktimer(text=a)
        self.close()


    def performance(self):
        self.performance=performance()









class tasktimer(QWidget):
    def __init__(self,text):
        super().__init__()
        self.setWindowTitle('Marginal Timer')
        self.setGeometry(350,150,524,391)
        self.start=False
        self.sec=0
        self.min=0
        self.text=text
        self.UI()
        self.show()
    def UI(self):
        self.designlayout()
        self.layouts()

    def designlayout(self):
        ##Timer
        self.label=QLabel('00:00')
        self.label.setAlignment(Qt.AlignCenter)

        self.label.setFont(QFont('Times',120))
        self.label1=QLabel(self.text[3:-16])
        self.label2=QLabel(self.text[-14])
        self.startBtn=QPushButton('Start')
        self.endBtn=QPushButton('Stop')



        self.timer=QTimer()
        self.timer.timeout.connect(self.showTime)


        self.startBtn.clicked.connect(self.startTimer)
        self.endBtn.clicked.connect(self.endTimer)


        self.progressBar=QProgressBar()


    def layouts(self):
        self.mainlayout=QVBoxLayout()
        self.hboxlayout=QHBoxLayout()
        self.mainlayout.addWidget(self.label)
        self.mainlayout.addLayout(self.hboxlayout)
        self.hboxlayout.addWidget(self.label1)
        self.hboxlayout.addWidget(self.label2)
        self.mainlayout.addWidget(self.startBtn)
        self.mainlayout.addWidget(self.endBtn)
        self.mainlayout.addWidget(self.progressBar)
        self.setLayout(self.mainlayout)



    def showTime(self):
        if self.start:





            self.sec+=1

            if self.sec>=60:
                self.sec=0

                self.min+=1
            if self.min==25:
                self.close()
            time=f"{self.min:02}"+":"+f"{self.sec:02}"
            self.label.setText(time)
            self.progressBar.setValue(int(self.min*4+(self.sec)/60*4))
        else:
            pass

    def startTimer(self):
        self.start=True
        self.timer.start(1000)



    def endTimer(self):

        self.timer.stop()

    def closeEvent(self,even):
        tx=self.text.split(":")
        id=tx[0]

        time=QDateTime.currentDateTime()
        timeDisplay=time.toString('yyyy-MM-dd')
        dal=timeDisplay.split('-')[2]
        mal=timeDisplay.split('-')[1]
        yal=timeDisplay.split('-')[0]



        query="SELECT * from daily WHERE id=?"
        a=cur.execute(query,(id,)).fetchone()




        dtime=a[3]
        mtime=a[4]
        ytime=a[5]
        dts=a[6]
        mts=a[7]
        yts=a[8]


        if dtime==None:
            dtime='0: '
        if mtime==None:
            mtime='0: '
        if ytime==None:
            ytime='0: '
        if dts==None:
            dts=''
        if mts==None:
            mts=''
        if yts==None:
            yts=''

        dtime=float(dtime.split(":")[0])
        mtime=float(mtime.split(":")[0])
        ytime=float(ytime.split(":")[0])


        dtime+=self.min+self.sec/60
        mtime+=self.min+self.sec/60
        ytime+=self.min+self.sec/60

        if  a[3]==None:
            dtime=str(round(self.min+self.sec/60,2))+":"+dal


        elif a[3].split(":")[1]!=dal:
            dtime=str(round(self.min+self.sec/60,2))+":"+dal
            dts+=dal+":"+str(dtime)+","


        else:
            dtime=str(round(dtime,2))+":"+dal


        if a[4]==None:
            mtime=str(round(self.min+self.sec/60,2))+":"+mal


        elif a[4].split(":")[1]!=mal:
            mtime=str(round(self.min+self.sec/60,2))+":"+mal
            mts+=mal+":"+str(mtime)+','


        else:
            mtime=str(round(mtime,2))+":"+mal

        if a[5]==None:
            ytime=str(round(self.min+self.sec/60,2))+":"+yal


        elif a[5].split(":")[1]!=yal:
            ytime=str(round(self.min+self.sec/60,2))+":"+yal
            yts+=mal+":"+str(ytime)+","


        else:
            ytime=str(round(ytime,2))+":"+yal



        self.sec=0
        self.min=0




        query1="UPDATE daily set dtime =? , mtime =? , ytime =?, dts=? , mts=? , yts=?   WHERE id=?"
        cur.execute(query1,(dtime, mtime, ytime,dts, mts, yts, id))
        con.commit()

        self.start=False

        self.main=Window()


def main():
    App=QApplication(sys.argv)
    window=Window()
    sys.exit(App.exec_())

if __name__=='__main__':
    main()
